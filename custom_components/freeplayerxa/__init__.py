from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, PLATFORMS

class FreeboxRemoteClient:
    def __init__(self, hass: HomeAssistant, host: str, code: str):
        self._hass = hass
        self._host = host.strip()
        self._code = str(code).strip()
        self._session = async_get_clientsession(hass)

    @property
    def host(self) -> str:
        return self._host

    @property
    def code(self) -> str:
        return self._code

    async def async_send_key(self, key: str, long: bool = False) -> bool:
        """Send a key to the Freebox HTTP remote API.
        Returns True if the request succeeded (HTTP 200), else False.
        """
        base = f"http://{self._host}/pub/remote_control"
        params = {"code": self._code, "key": key}
        if long:
            params["long"] = "true"
        try:
            async with self._session.get(base, params=params, timeout=5) as resp:
                return resp.status == 200
        except Exception:
            return False

    async def async_ping(self) -> bool:
        """Lightweight check by sending the 'home' key which is non-destructive."""
        return await self.async_send_key("home")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = entry.data
    client = FreeboxRemoteClient(hass, data["host"], data["code"])
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"client": client}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
