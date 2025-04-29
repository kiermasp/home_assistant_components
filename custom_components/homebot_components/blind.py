"""Blind entity for HomeBot Components."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.cover import (
    ATTR_POSITION,
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEVICE_TYPE_BLIND

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the blind entity."""
    _LOGGER.debug("Setting up blind entity for entry: %s", entry.entry_id)
    
    # Create the blind entity
    blind = HomeBotBlind(
        hass,
        entry,
        entry.data["up_switch"],
        entry.data["down_switch"],
        entry.data["up_trigger"],
        entry.data["down_trigger"],
        entry.data.get("open_time", 30),
        entry.data.get("close_time", 30),
    )
    
    async_add_entities([blind])
    _LOGGER.debug("Blind entity added: %s", blind.name)


class HomeBotBlind(CoverEntity):
    """Representation of a HomeBot blind."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        up_switch: str,
        down_switch: str,
        up_trigger: str,
        down_trigger: str,
        open_time: int,
        close_time: int,
    ) -> None:
        """Initialize the blind."""
        self.hass = hass
        self._entry = entry
        self._up_switch = up_switch
        self._down_switch = down_switch
        self._up_trigger = up_trigger
        self._down_trigger = down_trigger
        self._open_time = open_time
        self._close_time = close_time
        self._position = 100
        self._is_opening = False
        self._is_closing = False

        # Set up the entity
        self._attr_name = f"HomeBot Blind {entry.entry_id}"
        self._attr_unique_id = f"{DOMAIN}_{DEVICE_TYPE_BLIND}_{entry.entry_id}"
        self._attr_device_class = CoverDeviceClass.BLIND
        self._attr_supported_features = (
            CoverEntityFeature.OPEN
            | CoverEntityFeature.CLOSE
            | CoverEntityFeature.SET_POSITION
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self.name,
            manufacturer="HomeBot",
            model="External Blind",
            via_device=(DOMAIN, self._entry.entry_id),
        )

    @property
    def current_cover_position(self) -> int:
        """Return the current position of the blind."""
        return self._position

    @property
    def is_closed(self) -> bool:
        """Return if the blind is closed."""
        return self._position == 0

    @property
    def is_opening(self) -> bool:
        """Return if the blind is opening."""
        return self._is_opening
    
    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"{self._attr_unique_id}"

    @property
    def is_closing(self) -> bool:
        """Return if the blind is closing."""
        return self._is_closing

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the blind."""
        _LOGGER.debug("Opening blind")
        self._is_opening = True
        self._is_closing = False
        self.async_write_ha_state()

        # Turn on the up switch
        await self.hass.services.async_call(
            "switch",
            "turn_on",
            {"entity_id": self._up_switch},
        )

        # Turn off the down switch
        await self.hass.services.async_call(
            "switch",
            "turn_off",
            {"entity_id": self._down_switch},
        )

        # Turn off the switch after the specified duration
        await self.hass.async_add_executor_job(
            lambda: self.hass.loop.call_later(
                self._open_time,
                lambda: self.hass.services.async_call(
                    "switch",
                    "turn_off",
                    {"entity_id": self._up_switch},
                ),
            )
        )

        # Update position
        self._position = 100
        self._is_opening = False
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the blind."""
        _LOGGER.debug("Closing blind")
        self._is_closing = True
        self._is_opening = False
        self.async_write_ha_state()

        # Turn on the down switch
        await self.hass.services.async_call(
            "switch",
            "turn_on",
            {"entity_id": self._down_switch},
        )

        # Turn off the up switch
        await self.hass.services.async_call(
            "switch",
            "turn_off",
            {"entity_id": self._up_switch},
        )

        # Turn off the switch after the specified duration
        await self.hass.async_add_executor_job(
            lambda: self.hass.loop.call_later(
                self._close_time,
                lambda: self.hass.services.async_call(
                    "switch",
                    "turn_off",
                    {"entity_id": self._down_switch},
                ),
            )
        )

        # Update position
        self._position = 0
        self._is_closing = False
        self.async_write_ha_state()

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        """Set the position of the blind."""
        position = kwargs.get(ATTR_POSITION, 0)
        _LOGGER.debug("Setting blind position to %s", position)
        
        if position > self._position:
            # Need to open
            await self.async_open_cover()
        elif position < self._position:
            # Need to close
            await self.async_close_cover() 