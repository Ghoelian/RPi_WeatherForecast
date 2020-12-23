import sys

sys.path.insert(1, "./lib") # Insert path to e-ink display modules

import requests
import os
import datetime
import epd2in7b
import time
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
from geopy import geocoders
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY") # Used to make requests to OpenWeatherMap
nominatim_ua = os.getenv("NOMINATIM_USERAGENT") # Used to identify you to Nominatim
location = os.getenv("LOCATION") # Location to look up the weather for
timezone_offset = os.getenv("TIMEZONE_OFFSET") # Your timezone offset. Does not account for daylight savings

refresh_button = Button(5)

nominatim = geocoders.Nominatim(user_agent=nominatim_ua)

icons = { # Icons from https://openweathermap.org used for displaying current weather. Modified by me so it works with a 3-colour e-ink display
            0: Image.open("./images/01n.png"),
            1: Image.open("./images/02n1.png"),
            2: Image.open("./images/02n2.png"),
            3: Image.open("./images/03n.png"),
            4: Image.open("./images/04n1.png"),
            5: Image.open("./images/04n2.png"),
            6: Image.open("./images/09n1.png"),
            7: Image.open("./images/09n2.png"),
            8: Image.open("./images/10n1.png"),
            9: Image.open("./images/10n2.png"),
            10: Image.open("./images/11n1.png"),
            11: Image.open("./images/11n2.png"),
            12: Image.open("./images/13n.png"),
            13: Image.open("./images/50n.png")
        }

delay = 60 * 60 # Delay for how often to refresh the weather in seconds. 1 hour by default
width = 176 # Width and height of the e-ink display. My specific model doesn't display the edges very well, so I shrunk it a couple pixels
height = 264
iterator = 0 # Keeps track of how many times the display has been redrawn on without fully clearing it
counter = 12 # How often the display can redraw without clearing

epd = epd2in7b.EPD()
epd.init()
epd.Clear()

image = Image.new('1', (width, height), 255) # Image for drawing black/white
imageRed = Image.new('1', (width, height), 255) # Image for drawing red/white
font_small = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 15)
font_regular = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 28)

draw = ImageDraw.Draw(image) # Draw object for the images
drawRed = ImageDraw.Draw(imageRed)

def get_icon(arg, x, y): # OpenWeatherMap returns weather codes used for the icons. This gets the icon that belongs to a code
    if (arg == "01n" or arg == "01d"):
        draw_one(0, x, y)
    if (arg == "02n" or arg == "02d"):
        draw_two(1, x, y)
    if (arg == "03n" or arg == "03d"):
        draw_one(3, x, y)
    if (arg == "04n" or arg == "04d"):
        draw_two(4, x, y)
    if (arg == "09n" or arg == "09d"):
        draw_two(6, x, y)
    if (arg == "10n" or arg == "10d"):
        draw_two(8, x, y)
    if (arg == "11n" or arg == "11d"):
        draw_two(10, x, y)
    if (arg == "13n" or arg == "13d"):
        draw_two(12, x, y)
    if (arg == "50n" or arg == "50d"):
        draw_one(13, x, y)

def draw_one(index, x, y): # Used for drawing icons that only consist of one colour
    draw.bitmap((x, y), icons[index], fill=1)

def draw_two(index, x, y): # Used for drawing icons that consist of two colours, in my case red and white
    draw.bitmap((x, y), icons[index], fill=1)
    drawRed.bitmap((x, y), icons[index+1])

def get_weather(location, api_key):
    draw.rectangle((0, 0, width, height), outline=1, fill=0) # Draw white rectangles to make sure nothing is left behind from a previous draw
    drawRed.rectangle((0, 0, width, height), outline=1, fill=1)

    location = nominatim.geocode(location) # Use Nominatim to look up lat and lon that belong to a place name
    lon = location.longitude
    lat = location.latitude

    tomorrow = datetime.datetime.fromtimestamp(datetime.datetime.today().timestamp() + 86400) # 24 hrs from now

    day = tomorrow.strftime("%d")
    month = tomorrow.strftime("%m")
    year = tomorrow.strftime("%Y")

    tomorrow = datetime.datetime(int(year), int(month), int(day), 16-int(timezone_offset), 0).timestamp() # Get tomorrow's date, but at 15:00 instead of exactly 24 hrs from now. For some reason 15 - 2 (my timezone offset) results in a time of 14:00 CEST, so we subtract from 16 instead

    weather = requests.get(url=f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric").json() # Get current weather, as well as hourly forecast

    today_weather = weather["current"]

    for hour in weather["hourly"]: # Find forecast with a timestamp for tomorrow 15:00
        if (hour["dt"] == tomorrow):
            tomorrow_weather = hour

    today_time = datetime.datetime.utcfromtimestamp(today_weather["dt"]+(int(timezone_offset)*60*60)) # Get today's time, for displaying on the display

    # Boring drawing part
    draw.text((2, 0), f"Today {today_time.strftime('%H:%M')}", font=font_small, fill=1)
    draw.text((2, 15), str(round(today_weather["temp"])), font=font_regular, fill=1)
    drawRed.text((font_regular.getsize(str(round(today_weather["temp"])))[0]+2, 15), "°", font=font_regular, fill=0)
    draw.text((font_regular.getsize("°")[0]+font_regular.getsize(str(round(today_weather["temp"])))[0]+2, 15), "C", font=font_regular, fill=1)
    draw.text((width - (font_regular.getsize (today_weather["weather"][0]["main"])[0])-2, 15), today_weather["weather"][0]["main"], font=font_regular, fill=1)

    get_icon(today_weather["weather"][0]["icon"], 10, 10)
    
    tomorrow_time = datetime.datetime.utcfromtimestamp(tomorrow_weather["dt"]+(int(timezone_offset)*60*60))

    draw.text((2, height/2), f"Tomorrow {tomorrow_time.strftime('%H:%M')}", font=font_small, fill=1)
    draw.text((2, (height/2)+15), str(round(tomorrow_weather["temp"])), font=font_regular, fill=1)
    drawRed.text((font_regular.getsize(str(round(tomorrow_weather["temp"])))[0]+2, (height/2)+15), "°", font=font_regular, fill=0)
    draw.text((font_regular.getsize("°")[0]+font_regular.getsize(str(round(tomorrow_weather["temp"])))[0]+2, (height/2)+15), "C", font=font_regular, fill=1)
    draw.text((width-(font_regular.getsize(tomorrow_weather["weather"][0]["main"])[0])-2, (height/2)+15), tomorrow_weather["weather"][0]["main"], font=font_regular, fill=1)

    get_icon(tomorrow_weather["weather"][0]["icon"], 10, (height/2)+10)


    draw.line([(0, height/2), (width, height/2)], width=1, fill=1)

    epd.display(epd.getbuffer(image), epd.getbuffer(imageRed))

while True: # Main loop
    if (iterator >= counter): # Clear the display when it has been redrawn more times than the counter should allow
        epd.Clear()
        iterator = 0

    get_weather(location, api_key)

    iterator += 1

    for i in range(int(delay / 0.1)): # Check if refresh button gets pressed. Should refactor this to use events instead of constantly checking in a loop
        if (refresh_button.is_pressed):
            break

        time.sleep(0.1)
