"""The External Blinds integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_ON,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN
from .blind_controller import setup_blind_control

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up External Blinds from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Store the configuration
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Set up the blind control
    await setup_blind_control(hass, entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True