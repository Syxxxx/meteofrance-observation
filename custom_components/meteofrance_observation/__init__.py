"""The Météo-France Observation integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MeteoFranceApi, ApiError
from .const import DOMAIN, CONF_API_KEY, CONF_STATION_ID, UPDATE_INTERVAL_MINUTES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Météo-France Observation from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    api = MeteoFranceApi(
        session=async_get_clientsession(hass),
        api_key=entry.data[CONF_API_KEY],
        station_id=entry.data[CONF_STATION_ID],
    )

    async def async_update_data():
        """Fetch data from API."""
        try:
            return await api.async_get_data()
        except ApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"MeteoFrance Obs {entry.data[CONF_STATION_ID]}",
        update_method=async_update_data,
        update_interval=timedelta(minutes=UPDATE_INTERVAL_MINUTES),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR]):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
