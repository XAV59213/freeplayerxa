from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature
from homeassistant.components.media_player.const import MediaPlayerState
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, CONF_CHANNELS, KEY_MAP

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    client = data["client"]
    name = entry.data.get("name")
    entity = FreePlayerXAEntity(hass, entry, client, name)
    async_add_entities([entity], True)

class FreePlayerXAEntity(MediaPlayerEntity):
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client, name: str) -> None:
        self._hass = hass
        self._entry = entry
        self._client = client
        self._attr_name = name
        self._attr_unique_id = f"{client.host}-{client.code}"
        self._state = MediaPlayerState.OFF
        self._muted = False

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=self.name,
            manufacturer="Free",
            model="Freebox Player",
        )

    @property
    def state(self) -> MediaPlayerState | None:
        return self._state

    @property
    def supported_features(self) -> int:
        return (
            MediaPlayerEntityFeature.TURN_ON
            | MediaPlayerEntityFeature.TURN_OFF
            | MediaPlayerEntityFeature.VOLUME_STEP
            | MediaPlayerEntityFeature.VOLUME_MUTE
            | MediaPlayerEntityFeature.PREVIOUS_TRACK
            | MediaPlayerEntityFeature.NEXT_TRACK
            | MediaPlayerEntityFeature.SELECT_SOURCE
        )

    @property
    def source_list(self):
        channels_raw = self._entry.options.get(CONF_CHANNELS, "").strip()
        if not channels_raw:
            return None
        names = []
        for line in channels_raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                num, label = line.split(":", 1)
            elif "=" in line:
                label, num = line.split("=", 1)
            else:
                num, label = line, f"Ch {line}"
            names.append(label.strip())
        return names or None

    def _channel_map(self) -> dict[str, str]:
        channels_raw = self._entry.options.get(CONF_CHANNELS, "").strip()
        mapping: dict[str, str] = {}
        for line in channels_raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                num, label = line.split(":", 1)
                mapping[label.strip()] = num.strip()
            elif "=" in line:
                label, num = line.split("=", 1)
                mapping[label.strip()] = num.strip()
            else:
                mapping[f"Ch {line}"] = line.strip()
        return mapping

    async def async_turn_on(self) -> None:
        ok = await self._client.async_send_key(KEY_MAP["power"])  # toggle power
        if ok:
            self._state = MediaPlayerState.ON
            self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        ok = await self._client.async_send_key(KEY_MAP["power"])  # toggle power
        if ok:
            self._state = MediaPlayerState.OFF
            self.async_write_ha_state()

    async def async_volume_up(self) -> None:
        await self._client.async_send_key(KEY_MAP["vol_up"]) 

    async def async_volume_down(self) -> None:
        await self._client.async_send_key(KEY_MAP["vol_down"]) 

    async def async_mute_volume(self, mute: bool) -> None:
        ok = await self._client.async_send_key(KEY_MAP["mute"]) 
        if ok:
            self._muted = not self._muted
            self.async_write_ha_state()

    async def async_media_next_track(self) -> None:
        await self._client.async_send_key(KEY_MAP["chan_up"]) 

    async def async_media_previous_track(self) -> None:
        await self._client.async_send_key(KEY_MAP["chan_down"]) 

    async def async_select_source(self, source: str) -> None:
        mapping = self._channel_map()
        number = mapping.get(source)
        if not number:
            return
        for d in str(number):
            await self._client.async_send_key(d)
            await asyncio.sleep(0.08)
        await self._client.async_send_key(KEY_MAP["ok"]) 

    async def async_update(self) -> None:
        reachable = await self._client.async_ping()
        if reachable:
            self._state = MediaPlayerState.ON
        self._attr_available = reachable
