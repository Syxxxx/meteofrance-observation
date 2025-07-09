"""Constants for the Météo-France Observation integration."""

# Le domaine de l'intégration, utilisé partout dans Home Assistant
DOMAIN = "meteofrance_observation"

PLATFORMS = ["sensor"]

# Configuration keys
CONF_API_KEY = "api_key"
CONF_STATION_ID = "station_id"

# Coordinator
UPDATE_INTERVAL_MINUTES = 6

# API
API_BASE_URL = "https://public-api.meteofrance.fr/public/DPObs/v1"
API_SERVICE = "/station/infrahoraire-6m"
