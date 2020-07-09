Requirements:
	- libopenjp2-7
	- libtiff5
	- pipenv

.env file needs the following variables:
	API_KEY=openweathermap_api_key - Your OpenWeatherMap API key, this script only uses the onecall endpoint, so no subscription required.
	NOMINATIM_USERAGENT=useragent - The user agent sent to Nominatim, can be whatever, but should not be the default "useragent".
	LOCATION=Amsterdam, Noord-Holland - Location you want to get the weather for.

