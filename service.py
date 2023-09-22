#!/usr/bin/python

from dotenv import load_dotenv
from adafruit.Adafruit_Thermal import *
from Baiiab import Baiiab
from lcd.i2c_lcd import I2cLcd # Example LCD interface used
from lcd.lcd_menu_screen import Menu, MenuAction, MenuNoop, MenuScreen
from gpiozero import Button, RotaryEncoder
from functools import partial
from ast import literal_eval
import time

load_dotenv()

#printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

# Example config for LCD via i2c, you will need this 
# for the menu to function, the screen size is required
# to render the menu correctly on the screen.
DEFAULT_I2C_ADDR = 0x27
lcd = I2cLcd(1, DEFAULT_I2C_ADDR, 4, 20)


def clockwise_cb():
    print("prev")
    screen.focus_prev()

def counter_clockwise_cb():
    print("next")
    screen.focus_next()

def button_cb():
    print("push")
    screen.choose()

def action_callback(prompt, menu_screen, title):
    topic = menu_screen.parent.title
    subtopic = title
    print("callback action chosen.  topic=" + topic + ";subtopic=" + subtopic)
    columns = menu_screen.columns
    menu_screen.lcd.clear()
    menu_screen.lcd.move_to(0, 0)
    menu_screen.lcd.putstr("PRINTING YOU A:\n".center(columns) + topic.center(columns) + "\n" + subtopic.center(columns))
    try:
        advice = baiiab.create_oai_completion(prompt)
    except:
        print("GOT EXCEPTION")
        advice = baiiab.get_offline_advice(topic, subtopic)
        baiiab.print_offline()

    baiiab.print_advice_long(advice, subtopic + " " + topic)


baiiab = Baiiab(printer)
screen = MenuScreen(lcd, "Welcome to", "Bad AI In A Box", baiiab.get_menu(action_callback))

encoder = RotaryEncoder(10,9, bounce_time=0.1)
button = Button(11)

screen.start()

encoder.when_rotated_clockwise = counter_clockwise_cb  # backwards for some reason
encoder.when_rotated_counter_clockwise = clockwise_cb
button.when_pressed = button_cb

time.sleep(10000000)