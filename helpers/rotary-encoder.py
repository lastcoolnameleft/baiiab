#!/usr/bin/python

import sys, time, os
from pathlib import Path
sys.path.append(str(Path(f"{__file__}").parent.parent))
from dotenv import load_dotenv
from adafruit.Adafruit_Thermal import *
from gpiozero import Button, RotaryEncoder
from functools import partial
from ast import literal_eval

load_dotenv()

def clockwise_cb():
    print("prev")

def counter_clockwise_cb():
    print("next")

def button_cb():
    print("push")


encoder = RotaryEncoder(10,9, bounce_time=0.1)
button = Button(11)

encoder.when_rotated_clockwise = counter_clockwise_cb  # backwards for some reason
encoder.when_rotated_counter_clockwise = clockwise_cb
button.when_pressed = button_cb

print('ready')

time.sleep(10000000)