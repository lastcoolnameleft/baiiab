#!/usr/bin/python

from dotenv import load_dotenv
from adafruit.Adafruit_Thermal import *
from Baiiab import Baiiab
from lcd.i2c_lcd import I2cLcd # Example LCD interface used
from lcd.lcd_menu_screen import Menu, MenuAction, MenuNoop, MenuScreen
from gpiozero import Button, RotaryEncoder
from functools import partial
from ast import literal_eval
import time, os, logging
from logging.handlers import TimedRotatingFileHandler
from openai import AzureOpenAI

load_dotenv()

logging.basicConfig(encoding='utf-8', level=logging.DEBUG,
                    handlers=[TimedRotatingFileHandler("/home/pi/baiiab/logs/baiiab.log", when="H", interval=1)])

#printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

# Example config for LCD via i2c, you will need this 
# for the menu to function, the screen size is required
# to render the menu correctly on the screen.
DEFAULT_I2C_ADDR = 0x27
lcd = I2cLcd(1, DEFAULT_I2C_ADDR, 4, 20)


def clockwise_cb():
    logging.debug("prev")
    screen.focus_prev()

def counter_clockwise_cb():
    logging.debug("next")
    screen.focus_next()

def button_cb():
    logging.debug("push")
    screen.choose()

def action_callback(messages, menu_screen, title):
    topic = menu_screen.parent.title
    subtopic = title
    logging.info("callback action chosen.  topic=" + topic + ";subtopic=" + subtopic)
    columns = menu_screen.columns
    menu_screen.lcd.clear()
    menu_screen.lcd.move_to(0, 0)
    menu_screen.lcd.putstr("PRINTING YOU A:\n".center(columns) + subtopic.center(columns) + "\n" + topic.center(columns))
    try:
        advice = baiiab.create_oai_chat_completion(messages, azure_openai_deployment)
    except:
        logging.error("GOT EXCEPTION")
        advice = baiiab.get_offline_advice(topic, subtopic)
        baiiab.print_offline()

    baiiab.print_advice_long(advice, subtopic + " " + topic)

oai_client = AzureOpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    api_version="2024-02-01",
    timeout=3.0,
)
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

baiiab = Baiiab(printer, oai_client)

encoder = RotaryEncoder(10,9, bounce_time=0.1)
button = Button(11)


encoder.when_rotated_clockwise = counter_clockwise_cb  # backwards for some reason
encoder.when_rotated_counter_clockwise = clockwise_cb
button.when_pressed = button_cb

time.sleep(5) # Wait for 1 core system to catch up
screen = MenuScreen(lcd, "Welcome to", os.getenv("TITLE"), baiiab.get_menu(action_callback))
screen.start()
time.sleep(10000000)