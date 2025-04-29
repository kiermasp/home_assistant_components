"""Config flow for External Blinds integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import (
    DOMAIN,
    DEFAULT_CLOSE_TIME,
    DEFAULT_OPEN_TIME,
)


class ExternalBlindsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for External Blinds."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate the configuration
                await self._validate_config(user_input)
                return self.async_create_entry(
                    title="External Blinds",
                    data=user_input,
                )
            except Exception as err:
                errors["base"] = str(err)

        return self.async_show_form(
            step_id="user",
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

    async def _validate_config(self, user_input):
        """Validate the configuration."""
        # Check if the same entity is not used for both up and down
        if user_input["up_switch"] == user_input["down_switch"]:
            raise ValueError("Up and down switches must be different")
        if user_input["up_trigger"] == user_input["down_trigger"]:
            raise ValueError("Up and down triggers must be different")

    async def is_matching(self, user_input):
        """Check if the configuration matches."""
        return True
