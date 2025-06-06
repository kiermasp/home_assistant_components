"""Config flow for HomeBot Components integration."""

from __future__ import annotations
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import (
    DEFAULT_CLOSE_TIME,
    DEFAULT_OPEN_TIME,
    DEVICE_TYPE_BLIND,
    DEVICE_TYPE_BUTTON,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

class HomeBotComponentsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HomeBot Components."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        _LOGGER.debug("Starting user configuration step")
        if user_input is None:
            _LOGGER.debug("Showing initial configuration form")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("device_type"): SelectSelector(
                            SelectSelectorConfig(
                                options=[
                                    {"value": DEVICE_TYPE_BLIND, "label": "External Blind"},
                                    {"value": DEVICE_TYPE_BUTTON, "label": "Button Control"},
                                ],
                                mode=SelectSelectorMode.DROPDOWN,
                            )
                        ),
                    }
                ),
            )

        _LOGGER.debug("User selected device type: %s", user_input["device_type"])
        if user_input["device_type"] == DEVICE_TYPE_BLIND:
            return await self.async_step_blind()
        
        if user_input["device_type"] == DEVICE_TYPE_BUTTON:
            _LOGGER.warning("Button control not yet implemented")
            return self.async_abort(reason="not_implemented")

    async def async_step_blind(self, user_input=None):
        """Handle the blind configuration step."""
        _LOGGER.debug("Starting blind configuration step")
        errors = {}

        if user_input is not None:
            _LOGGER.debug("Validating blind configuration: %s", user_input)
            try:
                # Validate the configuration
                await self._validate_blind_config(user_input)
                _LOGGER.debug("Blind configuration validated successfully")
                return self.async_create_entry(
                    title="External Blind",
                    data={
                        "device_type": DEVICE_TYPE_BLIND,
                        **user_input,
                    },
                )
            except Exception as err:
                _LOGGER.error("Error validating blind configuration: %s", str(err))
                errors["base"] = str(err)

        _LOGGER.debug("Showing blind configuration form")
        return self.async_show_form(
            step_id="blind",
            data_schema=vol.Schema(
                {
                    vol.Required("up_switch"): EntitySelector(
                        EntitySelectorConfig(domain="switch", multiple=False)
                    ),
                    vol.Required("down_switch"): EntitySelector(
                        EntitySelectorConfig(domain="switch", multiple=False)
                    ),
                    vol.Required("up_trigger"): EntitySelector(
                        EntitySelectorConfig(domain="binary_sensor", multiple=False)
                    ),
                    vol.Required("down_trigger"): EntitySelector(
                        EntitySelectorConfig(domain="binary_sensor", multiple=False)
                    ),
                    vol.Optional(
                        "close_time",
                        default=DEFAULT_CLOSE_TIME,
                    ): NumberSelector(
                        NumberSelectorConfig(
                            min=1,
                            max=300,
                            mode=NumberSelectorMode.BOX,
                            unit_of_measurement="s",
                        )
                    ),
                    vol.Optional(
                        "open_time",
                        default=DEFAULT_OPEN_TIME,
                    ): NumberSelector(
                        NumberSelectorConfig(
                            min=1,
                            max=300,
                            mode=NumberSelectorMode.BOX,
                            unit_of_measurement="s",
                        )
                    ),
                }
            ),
            errors=errors,
        )

    async def _validate_blind_config(self, user_input):
        """Validate the blind configuration."""
        _LOGGER.debug("Validating blind configuration: %s", user_input)
        if user_input["up_switch"] == user_input["down_switch"]:
            _LOGGER.error("Up and down switches are the same: %s", user_input["up_switch"])
            raise ValueError("Up and down switches must be different")
        if user_input["up_trigger"] == user_input["down_trigger"]:
            _LOGGER.error("Up and down triggers are the same: %s", user_input["up_trigger"])
            raise ValueError("Up and down triggers must be different") 