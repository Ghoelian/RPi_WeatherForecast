# Dependencies
- Python >= 3
- libtiff-dev
- libjpeg-dev
- libfreetype6-dev
- pipenv <br />
pipenv will get all the Python dependencies. <br />

Also, SPI needs to be enabled in raspi-config, else you will get a file not found error.

# Installation
Let pipenv install all the dependencies:
```bash
$ pipenv install
```
Run the script with pipenv:
```bash
$ pipenv run python3 script.py
```

# .env vars
These are required for the script to run.
- API_KEY - Your OpenWeatherMap API key, this script only uses the onecall endpoint, so no subscription required.
- NOMINATIM_USERAGENT - The user agent sent to Nominatim, can be whatever, but should not be the default "useragent".
- LOCATION - Location you want to get the weather for, like Amsterdam, Noord-Holland.
- TIMEZONE_OFFSET - Timezone offset used for calculating the unix timestamp for next day 12:00.
