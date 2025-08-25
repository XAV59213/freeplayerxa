from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, DEFAULT_NAME, CONF_CODE, CONF_HOST, CONF_CHANNELS, CONF_KEY_DELAY
from .client import FreeboxRemoteClient  # ⬅️ plus d’import depuis __init__.py

DATA_SCHEMA = vol.Schema({
    vol.Required("name", default=DEFAULT_NAME): str,
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_CODE): vol.Any(str, int),
})

async def _validate(hass: HomeAssistant, host: str, code: str) -> bool:
    client = FreeboxRemoteClient(hass, host, str(code))
    return await client.async_ping()

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            name = user_input["name"].strip()
            host = user_input[CONF_HOST].strip()
            code = str(user_input[CONF_CODE]).strip()

            await self.async_set_unique_id(f"{host}-{code}")
            self._abort_if_unique_id_configured()

            valid = await _validate(self.hass, host, code)
            if not valid:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=name,
                    data={"name": name, CONF_HOST: host, CONF_CODE: code},
                    options={CONF_KEY_DELAY: 80}
                )
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

    async def async_step_import(self, user_input):
        return await self.async_step_user(user_input)

    @staticmethod
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, entry):
        self._entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Options", data=user_input)

        current_channels = self._entry.options.get(CONF_CHANNELS, "")
        current_delay = self._entry.options.get(CONF_KEY_DELAY, 80)
        schema = vol.Schema({
            vol.Optional(CONF_CHANNELS, default=current_channels): str,
            vol.Optional(CONF_KEY_DELAY, default=current_delay): vol.All(vol.Coerce(int), vol.Range(min=0, max=1000)),
        })
        return self.async_show_form(step_id="init", data_schema=schema)
