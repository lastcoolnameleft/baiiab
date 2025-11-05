from dotenv import load_dotenv
load_dotenv()

import os, openai, textwrap, random, importlib, logging
import time
icon = importlib.import_module('gfx.' + os.getenv('LOGO_IMG'))

from functools import partial
from lcd.lcd_menu_screen import Menu, MenuAction, MenuNoop, MenuScreen
from tenacity import retry, stop_after_attempt, wait_random, stop_after_delay
from ast import literal_eval
#from adafruit.Adafruit_Thermal import *

# OpenTelemetry imports
try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    from otel import get_tracer, get_meter
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    logging.warning("OpenTelemetry not available - telemetry disabled")

DEPLOYMENT_NAME = 'text-davinci-003' # https://openai.com/pricing

class Baiiab:

    def __init__(self, printer = None, oai_client = None):
        self._printer = printer
        self._oai_client = oai_client
        
        # Initialize telemetry
        if OTEL_AVAILABLE:
            self.tracer = get_tracer(__name__)
            self.meter = get_meter(__name__)
            
            # Create metrics
            self.api_call_counter = self.meter.create_counter(
                "baiiab.api_calls",
                description="Number of API calls made",
                unit="1"
            )
            self.offline_fallback_counter = self.meter.create_counter(
                "baiiab.offline_fallbacks",
                description="Number of offline fallback responses",
                unit="1"
            )
            self.api_duration_histogram = self.meter.create_histogram(
                "baiiab.api_duration",
                description="API call duration",
                unit="ms"
            )
            self.error_counter = self.meter.create_counter(
                "baiiab.errors",
                description="Number of errors encountered",
                unit="1"
            )
        else:
            self.tracer = None
            self.meter = None

    def get_offline_location(self, topic, subtopic):
        return "./offline/" + topic.lower().replace(" ", "_") + "/" + subtopic.lower().replace(" ", "_") + ".json"

    def get_offline_advice(self, topic, subtopic):
        if self.tracer:
            with self.tracer.start_as_current_span("get_offline_advice") as span:
                span.set_attribute("topic", topic)
                span.set_attribute("subtopic", subtopic)
                self.offline_fallback_counter.add(1, {"topic": topic, "subtopic": subtopic})
                
                with open(self.get_offline_location(topic, subtopic), "r") as f:
                    offline_advice = literal_eval(f.read())
                advice = random.choice(offline_advice)
                span.set_attribute("response_length", len(advice))
                return advice
        else:
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
                messages = menu_data[menu_folder][menu_action]
                menu_options.append(MenuAction(menu_action, callback=partial(callback, messages)))
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
        logging.info("print_advice_small(" + advice + ")")
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
        logging.info(topic)
        logging.info(advice)
        self._printer.setDefault() # Restore printer to defaults
        # Centered but lighter
        self._printer.printBitmap(icon.width, icon.height, icon.data)

        # Test inverse on & off
        self._printer.feed(1)
        self._printer.justify('C')
        self._printer.doubleHeightOn()
        self._printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
        self._printer.println(os.getenv('TITLE'))
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
        logging.info(f'create_oai_completion({prompt})')
        response = openai.Completion.create(
            engine=DEPLOYMENT_NAME,
    #            model="text-davinci-003",
            prompt=prompt,
            temperature=1.2,
            max_tokens=100,
            request_timeout=3
        )
        logging.info(f'response={response}')
        if response.choices[0].finish_reason != 'stop':
            logging.error(f'REQUEST RESPONSE NOT VALID: {response.choices[0].finish_reason}')
            raise Exception
        result = self.cleanse_advice(response.choices[0].text) 
        if not result:
            logging.error('Unable to parse result')
            raise Exception
        logging.info(f'create_oai_completion()::result={result}')
        return result
    
    
    # @retry(stop=(stop_after_delay(10) | stop_after_attempt(5)), wait=wait_random(min=1, max=2))
    def create_oai_chat_completion(self, messages, deployment):
        if self.tracer:
            with self.tracer.start_as_current_span("create_oai_chat_completion") as span:
                span.set_attribute("model", deployment)
                span.set_attribute("max_tokens", 100)
                span.set_attribute("temperature", 1.3)
                
                # Extract topic/subtopic from messages if available
                if messages and len(messages) > 0:
                    span.set_attribute("system_prompt", messages[0].get("content", "")[:100])
                
                start_time = time.time()
                try:
                    self.api_call_counter.add(1, {"model": deployment})
                    
                    response = self._oai_client.chat.completions.create(
                        model=deployment,
                        messages=messages,
                        max_tokens=100,
                        temperature=1.3,
                        top_p=0.95,
                        frequency_penalty=0.37,
                        presence_penalty=0.63,
                        stop=None,
                        stream=False
                    )
                    
                    duration_ms = (time.time() - start_time) * 1000
                    self.api_duration_histogram.record(duration_ms, {"model": deployment})
                    span.set_attribute("duration_ms", duration_ms)
                    
                    print(response, flush=True)
                    content = response.choices[0].message.content
                    
                    if content is None:
                        span.set_status(Status(StatusCode.ERROR, "Null response content"))
                        self.error_counter.add(1, {"error_type": "null_response"})
                        raise Exception("Null response from API")
                    
                    result = content.strip()
                    
                    if not result:
                        span.set_status(Status(StatusCode.ERROR, "Empty response"))
                        self.error_counter.add(1, {"error_type": "empty_response"})
                        raise Exception("Empty response from API")
                    
                    span.set_attribute("response_length", len(result))
                    span.set_attribute("finish_reason", response.choices[0].finish_reason)
                    span.set_status(Status(StatusCode.OK))
                    
                    return result
                except Exception as e:
                    duration_ms = (time.time() - start_time) * 1000
                    span.set_attribute("duration_ms", duration_ms)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    self.error_counter.add(1, {"error_type": type(e).__name__})
                    raise
        else:
            # Non-instrumented version
            response = self._oai_client.chat.completions.create(
                model=deployment,
                messages=messages,
                max_tokens=100,
                temperature=1.3,
                top_p=0.95,
                frequency_penalty=0.37,
                presence_penalty=0.63,
                stop=None,
                stream=False
            )
            print(response, flush=True)
            content = response.choices[0].message.content
            if content is None:
                raise Exception("Null response from API")
            result = content.strip()
            if not result:
                raise Exception("Empty response from API")
            return result 