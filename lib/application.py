#
# Generic Options
# Allow to create an options tree and navigate it
#


class OptionsTree(object):

    #
    # private
    #

    MENU = 0
    KEYBOARD = 1

    @property
    def atop(self):
        index = len(self.stack) - 1
        return self.stack[index]

    @atop.setter
    def atop(self, value):
        index = len(self.stack) - 1
        self.stack[index] = value

    #
    # constructor
    #

    def __init__(self):
        object.__init__(self)
        self.stack = []

    #
    # public
    #

    def set_menu(self, menu):
        self.stack = []
        self.stack.append(menu)

    def append_option(self, option):
        self.stack.append(option)

    def final(self, title):
        """useful for options that do nothing"""
        pass

    def get_menu_option(self, title, options):
        return {'type': self.MENU, 'title': title, 'options': options}

    def get_keyboard_option(self, title, options):
        return {'type': self.KEYBOARD, 'title': title, 'options': options}

    def current_option_is_menu(self):
        return self.atop['type']  == self.MENU

    def current_option_is_keyboard(self):
        return self.atop['type'] == self.KEYBOARD

    def current_menu_title(self):
        return self.atop['title']

    def current_menu_options(self):
        return [op['title'] for op in self.atop['options']]

    def current_menu_selected(self):
        if 'selected' in self.atop:
            return self.atop['selected']
        else:
            return 0

    def back(self):
        """back in the options tree"""
        if len(self.stack) > 1:
            self.stack.pop()
            #"""
            if self.current_option_is_keyboard():
                self.back()
            #"""

    def forward(self, index):
        """forward in the options tree"""

        #"""
        if self.current_option_is_keyboard():
            options = self.atop['options'](index)
            self.stack.append(options)
            return
        #"""

        if self.atop['options']:
            self.atop['selected'] = index
            selected = self.atop['options'][index]

            #"""
            if selected['type'] == self.KEYBOARD:
                self.stack.append(selected)
                return
            #"""

            if callable(selected['options']):
                options = selected['options'](selected['title'])
                if options:
                    self.stack.append(options)
            else:
                self.stack.append(selected)


#
# Application
# handle entire flow of application
#


class Application(OptionsTree):

    #
    # constructor
    #

    def __init__(self, menudisplay, keyboard, keypad):
        """
        constructor
        :param menudisplay: menu for display options
        :param keyboard: keyboard in display
        :param keypad: keypad
        """
        super(Application, self).__init__()
        self.menudisplay = menudisplay
        self.keyboard = keyboard
        self.keypad = keypad

    #
    # private
    #

    def refresh_menu(self):
        self.menudisplay.title = self.current_menu_title()
        self.menudisplay.options = self.current_menu_options()
        self.menudisplay.selected = self.current_menu_selected()
        self.menudisplay.display()

    def refresh_keyboard(self):
        self.keyboard.title = self.current_menu_title()
        self.keyboard.display()

    def handle_menu(self, key):
        # up
        if key == self.keypad.UP:
            self.menudisplay.selected = self.menudisplay.selected - 1
            self.menudisplay.display()

        # down
        if key == self.keypad.DOWN:
            self.menudisplay.selected = self.menudisplay.selected + 1
            self.menudisplay.display()

        # left
        if key == self.keypad.LEFT:
            self.back()
            return True

        # right or enter
        if key == self.keypad.RIGHT or key == self.keypad.ENTER:
            self.forward(self.menudisplay.selected)
            return True

        return False

    def handle_keyboard(self, key):
        # up
        if key == self.keypad.UP:
            self.keyboard.up()
            self.keyboard.display()

        # down
        if key == self.keypad.DOWN:
            self.keyboard.down()
            self.keyboard.display()

        # left
        if key == self.keypad.LEFT:
            self.keyboard.left()
            self.keyboard.display()

        # right
        if key == self.keypad.RIGHT:
            self.keyboard.right()
            self.keyboard.display()

        # enter
        if key == self.keypad.ENTER:
            text = self.keyboard.enter()
            # end
            if text == self.keyboard.END_MSG:
                self.forward(self.keyboard.text)
                return True
            # cancel
            elif text == self.keyboard.CANCEL_MSG:
                self.back()
                return True
            # key pressed
            else:
                self.keyboard.display()

        return False

    def keypress_event(self, key):
        """handle key pressed
        :return: true, it's necessary refresh display 
        """
        if self.current_option_is_menu():
            return self.handle_menu(key)
        elif self.current_option_is_keyboard():
            return self.handle_keyboard(key)

    def refresh(self):
        if self.current_option_is_menu():
            self.refresh_menu()
        elif self.current_option_is_keyboard():
            self.refresh_keyboard()

    #
    # public
    #

    def start(self):

        self.refresh()
        key = self.keypad.UNKNOWN

        while key != self.keypad.QUIT:

            key = self.keypad.get_key()
            if self.keypress_event(key):
                self.refresh()
