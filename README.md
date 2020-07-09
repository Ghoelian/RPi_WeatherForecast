# Dependencies
- Python >= 3
- libopenjp 2.7
- libtiff 5
- pipenv
pipenv will get all the Python dependencies

# .env vars
- API_KEY - Your OpenWeatherMap API key, this script only uses the onecall endpoint, so no subscription required.
- NOMINATIM_USERAGENT - The user agent sent to Nominatim, can be whatever, but should not be the default "useragent".
- LOCATION - Location you want to get the weather for, like Amsterdam, Noord-Holland.
- TIMEZONE_OFFSET - Timezone offset used for calculating the unix timestamp for next day 12:00.
