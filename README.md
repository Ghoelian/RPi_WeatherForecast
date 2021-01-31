# Dependencies
Install with your package manager (specific package names based on APT)

- Python 3.7
- libtiff-dev
- libjpeg-dev
- libfreetype6-dev
- libopenjp2-7

# Python dependencies
Install with PIP

- python-dotenv
- geopy
- pillow
- spidev
- RPi.GPIO
- gpiozero

Also, SPI needs to be enabled in raspi-config, else you will get a file not found error.

# .env vars
These are required for the script to run.
- API_KEY - Your OpenWeatherMap API key, this script only uses the onecall endpoint, so no subscription required.
- NOMINATIM_USERAGENT - The user agent sent to Nominatim, can be whatever, but should not be the default "useragent".
- LOCATION - Location you want to get the weather for, like Amsterdam, Noord-Holland.
- TIMEZONE_OFFSET - Timezone offset used for calculating the unix timestamp for next day 12:00.

# Running
A start.sh script is included, you can add this to your crontab to run it every hour, for example.
