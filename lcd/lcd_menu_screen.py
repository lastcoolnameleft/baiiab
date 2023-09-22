# https://github.com/jplattel/upymenu/blob/master/upymenu/__init__.py
# https://github.com/jplattel/upymenu/issues/4
import math

class MenuScreen:
    def __init__(self, lcd, title="", subtitle="", options=[]):
        self.title = title
        self.subtitle = subtitle
        self.start_options = options
        self.options = options
        self.lcd = lcd 
        self.columns = lcd.num_columns  # Get the columns of the LCD
        self.lines = lcd.num_lines  # And the line

        self.active = False
        self.parent = None
        
        # Make sure that we leave room for the title 
        self.start_line = 0
        if title: self.start_line = self.start_line + 1
        if subtitle: self.start_line = self.start_line + 1

    def __str__(self):
        return self.title
    
    # Starts the menu, used at root level to start the interface.
    # Or when navigating to a submenu or parten
    def start(self):
        self.active = True  # Set the screen as active

        # We start on the first option by default (not 0 to prevent ZeroDivision errors )
        self.focus = 1
        # Chunk the list and calculate the viewport:
        self.options_chunked = list(self._chunk_options())
        print("options chunked = " + str(self.options_chunked))
        self.render()
        return self

    # Renders the menu, also when refreshing (when changing select)
    def render(self):
        print('self.render()')
        # We only render the active screen, not the others
        if not self.active or not self.options_chunked:
            return

        self.viewport = self._get_viewport()
        self.lcd.clear()
        #self.lcd.move_to(0, self.start_line)

        self._render_title()
        self._render_cursor()
        self._render_options()

    def _get_viewport(self):
        print('self.current_chunk=' + str(self._current_chunk()))
        print('self.options_chunked=' + str(self.options_chunked))
        viewport = self.options_chunked[self._current_chunk()]
        print('self.viewport=' + str(viewport))
        return viewport

    def _render_title(self):
        if self.title:
            self.lcd.move_to(0, 0)
            #print(self.title)
            self.lcd.putstr(self.title.center(self.columns))
            self.lcd.move_to(0, 1)
        if self.subtitle:
            #print(self.subtitle)
            self.lcd.putstr(self.subtitle.center(self.columns))
            self.lcd.move_to(0, 2)

    def _render_cursor(self):
        for l in range(0, self.lines - self.start_line):
            self.lcd.move_to(0, l + self.start_line)
            # If the current position matches the focus, render
            # the cursor otherwise, render an empty space
            #print('l=' + str(l) + ';self.focus=' + str(self.focus))
            if l == ((self.focus - 1) % 2):
                #print('adding >')
                self.lcd.putstr(">")
            else:
                #print('adding space')
                self.lcd.putstr(" ")

    def _render_options(self):
        # Render the options:
        for l, option in enumerate(self.viewport):
            self.lcd.move_to(2, l + self.start_line)  # Move to the line
            # And render the longest possible string on the screen
            self.lcd.putstr(option.title[: self.columns - 1])

    # Chunk the options to only render the ones in the viewport
    def _chunk_options(self):
        #print('_chunk_options')
        for i in range(0, len(self.options), self.lines - self.start_line):
            #print('yielding; i=' + str(i) + ';self.lines=' + str(self.lines))
            #print(self.options[i : i + self.lines - self.start_line])
            yield self.options[i : i + self.lines - self.start_line]

    # Get the current chunk based on the focus position
#    def _current_chunk(self):
#        return math.floor(self.focus / (self.lines + 1 - self.start_line))  # current chunk
    def _current_chunk(self):
        return int((self.focus -1) / (self.lines - self.start_line))  # current chunk

    # Focus on the next option in the menu
    def focus_next(self):
        print('focus_next()')
        self.focus += 1
        # Wrap around
        if self.focus > len(self.options):
            self.focus = 1
        self.render()

    # Focus on the previous option in the menu
    def focus_prev(self):
        print('focus_prev()')
        self.focus -= 1
        if self.focus < 1:
            self.focus = len(self.options)
        self.render()

    # Focus on the option n in the menu
    def focus_set(self, n):
        print('focus_set:' + n)
        self.focus = n
        self.render()

    # Choose the item on which the focus is applied
    def choose(self):
        chosen_option = self.options[self.focus - 1]
        print('choose()::chosen_option=' + str(chosen_option))

        if type(chosen_option) == Menu:
            print('choose()::Processing Menu')
            self.parent = chosen_option
            self.options = chosen_option.options
            self.start()
        elif type(chosen_option) == MenuAction:
            print('choose()::Processing MenuAction')
            chosen_option.cb(self)  # Execute the callback function
            self.options = self.start_options
            self.parent = None
            self.start()
        elif type(chosen_option) == MenuNoop:
            print('choose()::Processing MenuNoop')
            return self

    def _choose_menu(self, submenu):
        self.active = False
        submenu.parent_menu = self
        return submenu.start(self.lcd)  # Start the submenu or parent


class Menu:
    def __init__(self, title, options=[]):
        self.title = title
        self.options = options
        self.parent_menu = None

    def __repr__(self):
        return f'Menu(\'{self.title}\')'

    # Navigate to the parent (if the current menu is a submenu)
    def parent(self):
        if self.parent_menu:
            self.active = False
            return self.parent_menu.start(self.lcd)


class MenuAction:
    def __init__(self, title, callback):
        self.title = title
        self.callback = callback

    def cb(self, menu_screen):
        return self.callback(menu_screen, self.title)

    def __repr__(self):
        return f'MenuAction(\'{self.title}\')'


class MenuNoop:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f'MenuNoop(\'{self.title}\')'
