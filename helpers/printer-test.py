#!/usr/bin/python
import sys, textwrap
from pathlib import Path
#from PIL import Image

sys.path.append(str(Path(f"{__file__}").parent.parent))

import gfx.azure_monochrome as azure
from dotenv import load_dotenv
from adafruit.Adafruit_Thermal import *

load_dotenv()

#printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
printer = Adafruit_Thermal('/dev/ttyS0', 19200, timeout=3)
#p = Serial(devfile='/dev/ttyS0', baudrate=9600, bytesize=8, parity='N', timeout=3)

def print_logo():
    #img = '/home/pi/baiiab/gfx/azure-monochrome.bmp'
    #printer.printImage(Image.open(img), True)
    printer.justify('C')
    printer.printBitmap(azure.width, azure.height, azure.data)
    printer.justify('L')
    printer.feed(2)

def print_thinking():
    printer.begin()
    printer.justify('C')
    printer.doubleHeightOn()
    printer.setSize('M')   # Set type size, accepts 'S', 'M', 'L'
    printer.println("THINKING...")
    printer.setSize('S') 
    printer.feed(2)

def test():
    printer.begin()
    printer.flush()
    printer.justify('C')
    printer.setSize('M2')   # Set type size, accepts 'S', 'M', 'L'
    printer.println("BAD AI")
    printer.justify('L')
    printer.setSize('S')   # Set type size, accepts 'S', 'M', 'L'
    printer.println("HEllo world")
    printer.feed(2)

def print_advice_short(advice, topic = None):
    print("print_advice_small(" + advice + ")")
    #self.print_thinking()
    printer.setDefault()
    if topic:
        printer.justify('C')
        printer.println("Your " + topic)
        printer.feed(1)

#        self._printer.justify('C')
#        self._printer.println("YOUR ADVICE")
    printer.setSize('S') 
    printer.justify('L')
    content = prepare_advice_for_printer(advice)
    printer.println(content)
    printer.feed(5)

def prepare_advice_for_printer(advice):
    lines = [] 
    # Prevent line-breaks (30 char) from splitting words
    for line in advice.split("\n"):
        lines.append("\n".join(textwrap.wrap(line, 30)))
    return "\n".join(lines)

def print_advice_long(advice, topic = None):
    print(topic)
    print(advice)
    printer.setDefault() # Restore printer to defaults
    # Centered but lighter
    #self._printer.printBitmap(sheep.width, sheep.height, sheep.data)

    # Test inverse on & off
    printer.feed(1)
    printer.justify('C')
    printer.doubleHeightOn()
    printer.setSize('M')   # Set type size, accepts 'S', 'M', 'L'
    printer.println("Bad AI In A Box")
    printer.setSize('S')
    printer.justify('L')
    printer.feed(1)
    printer.doubleHeightOff()

    if topic:
        printer.justify('C')
        printer.doubleHeightOn()
        printer.println("Your " + topic)
        printer.doubleHeightOff()
        printer.feed(1)
        printer.justify('L')

    content = prepare_advice_for_printer(advice)
    printer.println(content)

    printer.feed(1)
    printer.justify('C')
    printer.doubleHeightOn()
    printer.println("DISCLAIMER")
    printer.justify('L')
    printer.feed(1)
    printer.doubleHeightOff()
    printer.println("This uses AI to generate")
    printer.println("responses and should not be")
    printer.println("taken literally or followed")
    printer.feed(1)
    printer.println("http://bit.ly/baiiab")
    printer.feed(4)

#test()
#print_thinking() # This works
print_logo() # This works
#print_advice_short("advice", "topic")
#print_advice_long("advice", "topic")
