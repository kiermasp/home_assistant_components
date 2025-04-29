"""Blind controller for HomeBot Components."""

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
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)

async def setup_blind_control(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Set up the blind control logic."""
    config = entry.data

    @callback
    async def _handle_trigger_event(event):
        """Handle trigger events."""
        new_state = event.data.get("new_state")
        if new_state is None:
            return

        entity_id = event.data.get("entity_id")
        if entity_id == config["up_trigger"] and new_state.state == STATE_ON:
            await control_blind(hass, config["up_switch"], config["open_time"])
        elif entity_id == config["down_trigger"] and new_state.state == STATE_ON:
            await control_blind(hass, config["down_switch"], config["close_time"])

    # Listen for state changes on the trigger entities
    async_track_state_change_event(
        hass,
        [config["up_trigger"], config["down_trigger"]],
        _handle_trigger_event,
    )

async def control_blind(
    hass: HomeAssistant, switch_entity: str, duration: int
) -> None:
    """Control the blind by turning the switch on for a specified duration."""
    # Turn on the switch
    await hass.services.async_call(
        "switch",
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: switch_entity},
    )

    # Turn off the switch after the specified duration
    await hass.async_add_executor_job(
        lambda: hass.loop.call_later(
            duration,
            lambda: hass.services.async_call(
                "switch",
                SERVICE_TURN_OFF,
                {ATTR_ENTITY_ID: switch_entity},
            ),
        )
    ) 