from __future__ import annotations
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

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
        """Send a key to the Freebox HTTP remote API."""
        base = f"http://{self._host}/pub/remote_control"
        params = {"code": self._code, "key": key}
        if long:
            params["long"] = "true"
        try:
            async with self._session.get(base, params=params, timeout=5) as resp:
                if resp.status != 200:
                    _LOGGER.warning(
                        "Failed to send key '%s' to %s: HTTP %s",
                        key, self._host, resp.status
                    )
                    return False
                return True
        except Exception as e:
            _LOGGER.error("Error sending key '%s' to %s: %s", key, self._host, e)
            return False

    async def async_ping(self) -> bool:
        """Lightweight check by sending the 'home' key which is non-destructive."""
        return await self.async_send_key("home")
