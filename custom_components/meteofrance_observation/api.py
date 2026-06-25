"""API Client for Météo-France Public API."""
import asyncio
import logging
from datetime import datetime, timedelta, timezone
import urllib.parse
from typing import Any

from aiohttp import ClientSession, ClientError, ClientResponseError

from .const import API_BASE_URL, API_SERVICE

_LOGGER = logging.getLogger(__name__)

class ApiError(Exception):
    """Exception to indicate a general API error."""

class InvalidAuthError(ApiError):
    """Exception to indicate the API rejected the credentials."""

class EmptyResponseError(ApiError):
    """Exception to indicate the API returned no data for any tried slot."""

class MeteoFranceApi:
    """API Client for Météo-France station data."""

    def __init__(self, session: ClientSession, api_key: str, station_id: str) -> None:
        """Initialize the API client."""
        self._session = session
        self._api_key = api_key
        self._station_id = station_id

    # Météo-France publishes observations with a delay of several minutes.
    # We start from a slot that is already published, then walk further back
    # if the API still returns an empty list (e.g., a missed measurement).
    PUBLICATION_DELAY = timedelta(minutes=12)
    MAX_SLOT_RETRIES = 5
    SLOT_INTERVAL = timedelta(minutes=6)

    async def async_get_data(self) -> dict[str, Any]:
        """Fetch the latest data from the API."""
        # The API requires the date to be at the format AAAA-MM-JJThh:mm:00Z
        # with minutes being a multiple of 6 (00, 06, 12, ..., 54) and seconds
        # equal to 00. Round down to a valid 6-minute slot, taking the API
        # publication delay into account.
        now = datetime.now(timezone.utc) - self.PUBLICATION_DELAY
        slot = now - timedelta(
            minutes=now.minute % 6,
            seconds=now.second,
            microseconds=now.microsecond,
        )

        last_error: str | None = None
        for attempt in range(self.MAX_SLOT_RETRIES):
            datage = slot.strftime("%Y-%m-%dT%H:%M:00Z")
            params = {
                'id_station': self._station_id,
                'date': datage,
                'format': 'json',
                'apikey': self._api_key,
            }
            url = f"{API_BASE_URL}{API_SERVICE}?{urllib.parse.urlencode(params)}"

            _LOGGER.debug(
                "Requesting data from URL (attempt %d): %s", attempt + 1, url
            )

            try:
                async with self._session.get(url) as response:
                    if response.status in (401, 403):
                        raise InvalidAuthError(
                            f"API rejected credentials (HTTP {response.status})"
                        )
                    response.raise_for_status()
                    data = await response.json()
                    _LOGGER.debug("API Response received: %s", data)

                    if data:
                        return self._process_data(data[0])

                    last_error = f"API returned an empty list for slot {datage}"
                    _LOGGER.debug(
                        "Empty response for slot %s, trying previous slot",
                        datage,
                    )

            except ClientResponseError as err:
                if err.status in (401, 403):
                    raise InvalidAuthError(
                        f"API rejected credentials (HTTP {err.status})"
                    ) from err
                _LOGGER.error("API request error: %s", err)
                raise ApiError(f"API request error: {err}") from err
            except ClientError as err:
                _LOGGER.error("API request error: %s", err)
                raise ApiError(f"API request error: {err}") from err

            slot -= self.SLOT_INTERVAL

        raise EmptyResponseError(
            last_error
            or "API returned an empty list for all attempted slots"
        )

    def _process_data(self, resp: dict[str, Any]) -> dict[str, Any]:
        """Process the raw API data into a clean dictionary."""
        
        def kelvin_to_celsius(k_temp: float | None) -> float | None:
            return round(k_temp - 273.15, 2) if k_temp is not None else None

        def ms_to_kmh(speed_ms: float | None) -> float | None:
            return round(speed_ms * 3.6, 2) if speed_ms is not None else None
            
        def pa_to_hpa(pressure_pa: float | None) -> float | None:
            return round(pressure_pa / 100, 2) if pressure_pa is not None else None

        def jm2_to_wm2(rad_jm2: float | None) -> float | None:
            return round(rad_jm2 / 360, 2) if rad_jm2 is not None else None

        return {
            'reference_time': resp.get('reference_time'),
            'temperature': kelvin_to_celsius(resp.get('t')),
            'temperature_10cm': kelvin_to_celsius(resp.get('t_10')),
            'temperature_20cm': kelvin_to_celsius(resp.get('t_20')),
            'temperature_100cm': kelvin_to_celsius(resp.get('t_100')),
            'humidity': resp.get('u'),
            'pressure': pa_to_hpa(resp.get('pres')),
            'wind_direction': resp.get('dd'),
            'wind_speed': ms_to_kmh(resp.get('ff')),
            'gust_direction': resp.get('dxi10'),
            'gust_speed': ms_to_kmh(resp.get('fxi10')),
            'precipitation': resp.get('rr_per'),
            'solar_radiation': jm2_to_wm2(resp.get('ray_glo01')),
            'sunshine_duration': resp.get('insolh'),
            'visibility': resp.get('vv'),
        }
