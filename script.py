import sys

sys.path.insert(1, "./lib")

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

api_key = os.getenv("API_KEY")
nominatim_ua = os.getenv("NOMINATIM_USERAGENT")
location = os.getenv("LOCATION")
timezone_offset = os.getenv("TIMEZONE_OFFSET")

refresh_button = Button(5)

nominatim = geocoders.Nominatim(user_agent=nominatim_ua)

a = Image.open("./images/01n.png")
icons = {
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

delay = 60 * 60
width = 176
height = 264
iterator = 0
counter = 1

epd = epd2in7b.EPD()
epd.init()
epd.Clear()

image = Image.new('1', (width, height), 255)
imageRed = Image.new('1', (width, height), 255)
font_small = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 15)
font_regular = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 28)
font_big = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 34)

draw = ImageDraw.Draw(image)
drawRed = ImageDraw.Draw(imageRed)

def get_icon(arg, x, y):
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

def draw_one(index, x, y):
    draw.bitmap((x, y), icons[index], fill=1)

def draw_two(index, x, y):
    draw.bitmap((x, y), icons[index], fill=1)
    drawRed.bitmap((x, y), icons[index+1])

def get_weather(location, api_key):
    draw.rectangle((0, 0, width, height), outline=1, fill=0)
    drawRed.rectangle((0, 0, width, height), outline=1, fill=1)

    location = nominatim.geocode(location)
    lon = location.longitude
    lat = location.latitude

    now = datetime.date.today()

    day = now.strftime("%d")
    month = now.strftime("%m")
    year = now.strftime("%Y")

    tomorrow = datetime.datetime(int(year), int(month), int(day)+1, 16-int(timezone_offset), 0).timestamp()

    weather = requests.get(url=f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric").json()

    today_weather = weather["current"]

    for hour in weather["hourly"]:
        if (hour["dt"] == tomorrow):
            tomorrow_weather = hour

    draw.text((2, 0), "Today", font=font_small, fill=1)
    draw.text((2, 15), str(round(today_weather["temp"])), font=font_regular, fill=1)
    drawRed.text((font_regular.getsize(str(round(today_weather["temp"])))[0]+2, 15), "°", font=font_regular, fill=0)
    draw.text((font_regular.getsize("°")[0]+font_regular.getsize(str(round(today_weather["temp"])))[0]+2, 15), "C", font=font_regular, fill=1)
    draw.text((width - (font_regular.getsize (today_weather["weather"][0]["main"])[0])-2, 15), today_weather["weather"][0]["main"], font=font_regular, fill=1)

    get_icon(today_weather["weather"][0]["icon"], 10, 10)

    draw.text((2, height/2), "Tomorrow", font=font_small, fill=1)
    draw.text((2, (height/2)+15), str(round(tomorrow_weather["temp"])), font=font_regular, fill=1)
    drawRed.text((font_regular.getsize(str(round(tomorrow_weather["temp"])))[0]+2, (height/2)+15), "°", font=font_regular, fill=0)
    draw.text((font_regular.getsize("°")[0]+font_regular.getsize(str(round(tomorrow_weather["temp"])))[0]+2, (height/2)+15), "C", font=font_regular, fill=1)
    draw.text((width-(font_regular.getsize(tomorrow_weather["weather"][0]["main"])[0])-2, (height/2)+15), tomorrow_weather["weather"][0]["main"], font=font_regular, fill=1)

    get_icon(tomorrow_weather["weather"][0]["icon"], 10, (height/2)+10)


    draw.line([(0, height/2), (width, height/2)], width=1, fill=1)

    epd.display(epd.getbuffer(image), epd.getbuffer(imageRed))

while True:
    if (iterator >= counter):
        epd.Clear()
        iterator = 0

    get_weather(location, api_key)

    iterator += 1

    for i in range(int(delay / 0.1)):
        if (refresh_button.is_pressed):
            break

        time.sleep(0.1)
