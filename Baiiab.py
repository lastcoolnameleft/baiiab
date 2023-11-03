import os, openai, textwrap, random
import gfx.sheep as sheep

from functools import partial
from lcd.lcd_menu_screen import Menu, MenuAction, MenuNoop, MenuScreen
from tenacity import retry, stop_after_attempt, wait_random, stop_after_delay
from time import sleep
from gpiozero import PWMLED, Button
from ast import literal_eval
#from adafruit.Adafruit_Thermal import *

DEPLOYMENT_NAME = 'text-davinci-003' # https://openai.com/pricing

class Baiiab:

    def __init__(self, printer = None):
        self._printer = printer

        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = os.getenv("OPENAI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15' # this may change in the future

    def get_offline_location(self, topic, subtopic):
        return "./offline/" + topic.lower() + "/" + subtopic.lower() + ".json"

    def get_offline_advice(self, topic, subtopic):
        with open(self.get_offline_location(topic, subtopic), "r") as f:
            offline_advice = literal_eval(f.read())
        return random.choice(offline_advice)

    def get_menu(self, callback):
        with open("conf/menu.json","r") as f:
            menu_data = literal_eval(f.read())
        full_menu = []
        for menu_folder in menu_data:
            menu_options = []
            for menu_action in menu_data[menu_folder]:
                prompt = menu_data[menu_folder][menu_action]
                menu_options.append(MenuAction(menu_action, callback=partial(callback, prompt)))
            full_menu.append(Menu(menu_folder, options=menu_options))
        return full_menu


    def print_thinking(self):
        self._printer.begin()
        self._printer.justify('C')
        self._printer.doubleHeightOn()
        self._printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
        self._printer.println("THINKING...")
        self._printer.setSize('S') 
        self._printer.feed(2)

    def print_offline(self):
        self._printer.println("...")

    def print_advice_short(self, advice, topic = None):
        print("print_advice_small(" + advice + ")")
        #self.print_thinking()
        self._printer.setDefault()
        if topic:
            self._printer.justify('C')
            self._printer.println("Your " + topic)
            self._printer.feed(1)

#        self._printer.justify('C')
#        self._printer.println("YOUR ADVICE")
        self._printer.setSize('S') 
        self._printer.justify('L')
        content = self.prepare_advice_for_printer(advice)
        self._printer.println(content)
        self._printer.feed(5)

    def cleanse_advice(self, advice):
        # It seems to like to start responses with: ".\n\n"
        if (advice[0] in ('.', '!', ':')):
            advice = advice[1:]
        advice = advice.strip()
        return advice

    def prepare_advice_for_printer(self, advice):
        lines = [] 
        # Prevent line-breaks (30 char) from splitting words
        for line in advice.split("\n"):
            lines.append("\n".join(textwrap.wrap(line, 30)))
        return "\n".join(lines)

    def print_advice_long(self, advice, topic = None):
        print(topic)
        print(advice)
        self._printer.setDefault() # Restore printer to defaults
        # Centered but lighter
        self._printer.printBitmap(sheep.width, sheep.height, sheep.data)

        # Test inverse on & off
        self._printer.feed(1)
        self._printer.justify('C')
        self._printer.doubleHeightOn()
        self._printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
        self._printer.println("Bad AI In A Box")
        self._printer.setSize('S')
        self._printer.justify('L')
        self._printer.feed(1)
        self._printer.doubleHeightOff()

        if topic:
            self._printer.justify('C')
            self._printer.doubleHeightOn()
            self._printer.println("Your " + topic)
            self._printer.doubleHeightOff()
            self._printer.feed(1)
            self._printer.justify('L')

        content = self.prepare_advice_for_printer(advice)
        self._printer.println(content)

        self._printer.feed(1)
        self._printer.justify('C')
        self._printer.doubleHeightOn()
        self._printer.println("DISCLAIMER")
        self._printer.justify('L')
        self._printer.feed(1)
        self._printer.doubleHeightOff()
        self._printer.println("This uses AI to generate")
        self._printer.println("responses and should not be")
        self._printer.println("taken literally or followed")
        self._printer.feed(1)
        self._printer.println("http://bit.ly/baiiab")
        self._printer.feed(4)


    @retry(stop=(stop_after_delay(10) | stop_after_attempt(5)),
           wait=wait_random(min=1, max=2))
    def create_oai_completion(self, prompt):
        print(f'create_oai_completion({prompt})')
        response = openai.Completion.create(
            engine=DEPLOYMENT_NAME,
    #            model="text-davinci-003",
            prompt=prompt,
            temperature=1.2,
            max_tokens=100,
            request_timeout=3
        )
        print(response, flush=True)
        result = self.cleanse_advice(response.choices[0].text) 
        if not result:
            raise Exception
        return result
    