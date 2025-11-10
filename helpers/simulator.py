#!/usr/bin/env python3
"""
Terminal-based simulator for the Baiiab box interface.
Simulates the 20x4 LCD display and rotary encoder interactions.
"""

import os
import sys

# Add parent directory to path so we can import from project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ast import literal_eval
from functools import partial
from lcd.lcd_menu_screen import Menu, MenuAction, MenuNoop, MenuScreen
from dotenv import load_dotenv
from openai import AzureOpenAI
from Baiiab import Baiiab

load_dotenv()

# Initialize OpenTelemetry with file output for simulator
# Telemetry will be logged to file instead to avoid interfering with LCD display
try:
    from otel import setup_telemetry, get_tracer, get_meter
    import logging
    
    # Set up telemetry logging to file
    otel_log_file = "logs/simulator_telemetry.log"
    os.makedirs("logs", exist_ok=True)
    
    # Check if telemetry is enabled
    enabled = os.getenv("OTEL_ENABLED", "true").lower() == "true"
    
    if enabled:
        # Set up file-based telemetry (no console output for simulator)
        tracer, meter = setup_telemetry(
            service_name=os.getenv("OTEL_SERVICE_NAME", "baiiab-simulator"),
            service_version=os.getenv("OTEL_SERVICE_VERSION", "1.0.0"),
            use_console_exporter=False,  # Disable console to avoid garbled display
            use_file_exporter=True,  # Enable file export
            file_path=otel_log_file,
            use_otlp_exporter=bool(os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")),
            otlp_endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        )
        
        simulator_tracer = get_tracer(__name__) if tracer else None
        
        if meter:
            simulator_interaction_counter = meter.create_counter(
                "baiiab.simulator_interactions",
                description="Number of simulator interactions",
                unit="1"
            )
        else:
            simulator_interaction_counter = None
        
        # Show telemetry status
        telemetry_status = f"[Telemetry: ENABLED] → {otel_log_file}"
    else:
        simulator_tracer = None
        simulator_interaction_counter = None
        telemetry_status = "[Telemetry: DISABLED]"
        
except ImportError as e:
    simulator_tracer = None
    simulator_interaction_counter = None
    telemetry_status = "[Telemetry: NOT AVAILABLE - run: pip install -r requirements.txt]"


class TerminalLCD:
    """Simulates a 20x4 LCD display in the terminal."""
    
    def __init__(self, i2c_bus=1, i2c_addr=0x27, num_lines=4, num_columns=20):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.buffer = [[' ' for _ in range(num_columns)] for _ in range(num_lines)]
        self.cursor_x = 0
        self.cursor_y = 0
    
    def clear(self):
        """Clear the display buffer."""
        self.buffer = [[' ' for _ in range(self.num_columns)] for _ in range(self.num_lines)]
        self.cursor_x = 0
        self.cursor_y = 0
    
    def move_to(self, x, y):
        """Move cursor to position (x, y)."""
        self.cursor_x = x
        self.cursor_y = y
    
    def putstr(self, text):
        """Put string at current cursor position."""
        for char in text:
            if char == '\n':
                self.cursor_y += 1
                self.cursor_x = 0
                if self.cursor_y >= self.num_lines:
                    self.cursor_y = self.num_lines - 1
            else:
                if self.cursor_y < self.num_lines and self.cursor_x < self.num_columns:
                    self.buffer[self.cursor_y][self.cursor_x] = char
                    self.cursor_x += 1
    
    def display(self, telemetry_info=None):
        """Render the LCD display to terminal."""
        # Clear terminal screen
        print("\033[2J\033[H", end='')
        
        # Draw telemetry status at top if available
        if telemetry_info:
            print(f"╔{'═' * 78}╗")
            print(f"║ {telemetry_info:<76} ║")
            print(f"╚{'═' * 78}╝")
            print()
        
        # Draw LCD display title
        print("╔" + "═" * (self.num_columns + 2) + "╗")
        print("║ " + "LCD DISPLAY".center(self.num_columns) + " ║")
        print("╠" + "═" * (self.num_columns + 2) + "╣")
        
        # Draw LCD content
        for line in self.buffer:
            print("║ " + ''.join(line) + " ║")
        
        # Draw bottom border
        print("╚" + "═" * (self.num_columns + 2) + "╝")
        
        # Draw controls
        print("\n" + "─" * 80)
        print("CONTROLS:")
        print("  [w] or [↑] - Turn knob counter-clockwise (previous item)")
        print("  [s] or [↓] - Turn knob clockwise (next item)")
        print("  [e] or [Enter] - Press knob (select)")
        print("  [q] - Quit simulator")
        print("─" * 80)
        print("\nCommand: ", end='', flush=True)


def action_callback(messages, menu_screen, title, baiiab, azure_openai_deployment):
    """Callback when an action is selected."""
    topic = menu_screen.parent.title
    subtopic = title
    columns = menu_screen.columns
    
    if simulator_tracer:
        with simulator_tracer.start_as_current_span("simulator.action_callback") as span:
            span.set_attribute("topic", topic)
            span.set_attribute("subtopic", subtopic)
            span.set_attribute("mode", "simulator")
            simulator_interaction_counter.add(1, {"interaction_type": "action_selected", "topic": topic, "subtopic": subtopic})
            
            menu_screen.lcd.clear()
            menu_screen.lcd.move_to(0, 0)
            menu_screen.lcd.putstr("GENERATING:\n".center(columns) + subtopic.center(columns) + "\n" + topic.center(columns))
            menu_screen.lcd.display(telemetry_status)
            
            print("\n\n[SIMULATOR] Generating content...")
            print(f"  Topic: {topic}")
            print(f"  Subtopic: {subtopic}")
            print(f"  Telemetry: Logged to logs/simulator_telemetry.log")
            
            try:
                advice = baiiab.create_oai_chat_completion(messages, azure_openai_deployment)
                span.set_attribute("response_source", "api")
                print(f"\n[RESPONSE]")
                print("=" * 60)
                print(advice)
                print("=" * 60)
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("response_source", "offline")
                print(f"\n[ERROR] Failed to generate: {e}")
                print("Falling back to offline response...")
                advice = baiiab.get_offline_advice(topic, subtopic)
                print(f"\n[OFFLINE RESPONSE]")
                print("=" * 60)
                print(advice)
                print("=" * 60)
            
            print("\nPress Enter to return to menu...", end='', flush=True)
            input()
    else:
        menu_screen.lcd.clear()
        menu_screen.lcd.move_to(0, 0)
        menu_screen.lcd.putstr("GENERATING:\n".center(columns) + subtopic.center(columns) + "\n" + topic.center(columns))
        menu_screen.lcd.display(telemetry_status)
        
        print("\n\n[SIMULATOR] Generating content...")
        print(f"  Topic: {topic}")
        print(f"  Subtopic: {subtopic}")
        print(f"  Telemetry: Not enabled")
        
        try:
            advice = baiiab.create_oai_chat_completion(messages, azure_openai_deployment)
            print(f"\n[RESPONSE]")
            print("=" * 60)
            print(advice)
            print("=" * 60)
        except Exception as e:
            print(f"\n[ERROR] Failed to generate: {e}")
            print("Falling back to offline response...")
            advice = baiiab.get_offline_advice(topic, subtopic)
            print(f"\n[OFFLINE RESPONSE]")
            print("=" * 60)
            print(advice)
            print("=" * 60)
        
        print("\nPress Enter to return to menu...", end='', flush=True)
        input()


def get_input():
    """Get single character input (with fallback for different systems)."""
    try:
        # Try to use termios for Unix-like systems
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            # Handle escape sequences (arrow keys)
            if ch == '\x1b':
                # Read the rest of the escape sequence
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except (ImportError, AttributeError):
        # Fallback for Windows or if termios not available
        return input().lower()


def main():
    """Main simulator loop."""
    # Check if menu.json exists
    if not os.path.exists("conf/menu.json"):
        print("Error: conf/menu.json not found!")
        print("Please run this script from the baiiab directory.")
        sys.exit(1)
    
    # Initialize OpenAI client
    oai_client = AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2024-02-01",
        timeout=3.0,
    )
    azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    # Initialize components (no printer for simulator)
    lcd = TerminalLCD(num_lines=4, num_columns=20)
    baiiab = Baiiab(printer=None, oai_client=oai_client)
    
    # Create callback with baiiab and deployment parameters
    callback = partial(action_callback, baiiab=baiiab, azure_openai_deployment=azure_openai_deployment)
    
    # Create menu screen
    screen = MenuScreen(
        lcd, 
        "Welcome to", 
        "BAIIAB Simulation",
        baiiab.get_menu(callback)
    )
    screen.start()
    
    # Display initial state
    lcd.display(telemetry_status)
    
    # Main interaction loop
    running = True
    while running:
        try:
            command = get_input()
            
            if command in ['q', 'Q']:
                running = False
                print("\nExiting simulator...")
            elif command in ['w', 'W', '\x1b[A']:  # w or up arrow
                # Counter-clockwise (previous item)
                if simulator_tracer:
                    with simulator_tracer.start_as_current_span("simulator.navigation.previous"):
                        simulator_interaction_counter.add(1, {"interaction_type": "navigation_up"})
                        screen.focus_prev()
                else:
                    screen.focus_prev()
                lcd.display(telemetry_status)
            elif command in ['s', 'S', '\x1b[B']:  # s or down arrow
                # Clockwise (next item)
                if simulator_tracer:
                    with simulator_tracer.start_as_current_span("simulator.navigation.next"):
                        simulator_interaction_counter.add(1, {"interaction_type": "navigation_down"})
                        screen.focus_next()
                else:
                    screen.focus_next()
                lcd.display(telemetry_status)
            elif command in ['e', 'E', '\r', '\n']:  # e or Enter
                # Press knob (select)
                if simulator_tracer:
                    with simulator_tracer.start_as_current_span("simulator.select"):
                        simulator_interaction_counter.add(1, {"interaction_type": "select"})
                        screen.choose()
                else:
                    screen.choose()
                lcd.display(telemetry_status)
            elif command == '\x03':  # Ctrl+C
                running = False
                print("\nExiting simulator...")
            else:
                # Invalid command, just redisplay
                lcd.display(telemetry_status)
                
        except KeyboardInterrupt:
            running = False
            print("\nExiting simulator...")
        except Exception as e:
            print(f"\nError: {e}")
            running = False
    
    print("Goodbye!")


if __name__ == "__main__":
    main()
