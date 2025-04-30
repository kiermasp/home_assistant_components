"""The External Blinds integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .config_flow import HomeBotComponentsConfigFlow
from .blind import async_setup_entry as async_setup_blind

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up External Blinds from a config entry."""
    
    _LOGGER.debug("Setting up HomeBot Components with config: %s", entry.data)
    _LOGGER.info("Setting up HomeBot Components")

    hass.data.setdefault(DOMAIN, {})

    # Store the configuration
    hass.data[DOMAIN][entry.entry_id] = entry.data
    _LOGGER.debug("Stored configuration for entry_id: %s", entry.entry_id)

    # Set up the blind entity
    await async_setup_blind(hass, entry, hass.data[DOMAIN][entry.entry_id])
    _LOGGER.debug("Blind entity setup completed")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    _LOGGER.debug("Unloading HomeBot Components for entry_id: %s", entry.entry_id)
    _LOGGER.info("Unloading HomeBot Components")
    
    hass.data[DOMAIN].pop(entry.entry_id)
    _LOGGER.debug("Removed configuration for entry_id: %s", entry.entry_id)
    return True