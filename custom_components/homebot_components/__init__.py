"""The External Blinds integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .blind_controller import setup_blind_control

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up External Blinds from a config entry."""
    
    _LOGGER.info("Setting up HomeBot Components")

    hass.data.setdefault(DOMAIN, {})

    # Store the configuration
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Set up the blind control
    await setup_blind_control(hass, entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    _LOGGER.info("Setting async_unload_entry")
    
    hass.data[DOMAIN].pop(entry.entry_id)
    return True