import sys

sys.path.insert(1, "./lib")

import requests
import os
import datetime
import epd2in7b
import time
from PIL import Image, ImageDraw, ImageFont
from geopy import geocoders
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("API_KEY")
nominatim_ua = os.getenv("NOMINATIM_USERAGENT")
location = os.getenv("LOCATION")
timezone = os.getenv("TIMEZONE")

nominatim = geocoders.Nominatim(user_agent=nominatim_ua)

def get_weather(location, api_key, timezone):
    location = nominatim.geocode(location)
    lon = location.longitude
    lat = location.latitude
    
    now = datetime.date.today()
    
    day = now.strftime("%d")
    month = now.strftime("%m")
    year = now.strftime("%Y")

    tomorrow = datetime.datetime(int(year), int(month), int(day)+1, 11, 0).timestamp()

    weather = requests.get(url=f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric&timezone={timezone}").json()

    today_weather = weather["current"]
    
    for hour in weather["hourly"]:
        if (hour["dt"] == tomorrow):
            tomorrow_weather = hour
            
    
EXECUTION_PERIOD_S = 60.0 * 10.0
width = 176
height = 264
iterator = 0
counter = 10

epd = epd2in7b.EPD()
epd.init()
epd.Clear()

image = Image.new('1', (height, width), 255)
imageRed = Image.new('1', (height, width), 255)

draw = ImageDraw.Draw(image)
drawRed = ImageDraw.Draw(imageRed)

startTime = time.time() - EXECUTION_PERIOD_S

while True:
    draw.rectangle((0, 0, height, width), outline=1, fill=1)
    drawRed.rectangle((0, 0, height, width), outline=1, fill=1)
    
    get_weather(location, api_key, timezone)
    
    if (iterator >= counter):
        epd.Clear()
        iterator = 0
    
    epd.display(epd.getbuffer(image), epd.getbuffer(imageRed))
    
    iterator += 1
    timeToSleep = EXECUTION_PERIOD_S - min((time.time() - startTime), EXECUTION_PERIOD_S)
    time.sleep(timeToSleep)
    startTime = time.time()