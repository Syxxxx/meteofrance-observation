"""Config flow for Météo-France Observation integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MeteoFranceApi, ApiError
from .const import DOMAIN, CONF_STATION_ID

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_STATION_ID, default="59343001"): str,
        vol.Required(CONF_API_KEY): str,
    }
)

class MeteoFranceObservationConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Météo-France Observation."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_STATION_ID])
            self._abort_if_unique_id_configured()

            try:
                api = MeteoFranceApi(
                    session=async_get_clientsession(self.hass),
                    api_key=user_input[CONF_API_KEY],
                    station_id=user_input[CONF_STATION_ID],
                )
                await api.async_get_data()
            except ApiError as err:
                _LOGGER.error("API Error during validation: %s", err)
                errors["base"] = "cannot_connect"
            except Exception as exc:
                _LOGGER.exception("Unexpected exception during validation: %s", exc)
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=f"Station {user_input[CONF_STATION_ID]}",
                    data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
