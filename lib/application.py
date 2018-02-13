#
# Application
# handle entire flow of application
#


class Application(object):

    #
    # constructor
    #

    def __init__(self, menudisplay, keyboard, keypad, options):
        """
        constructor
        :param menudisplay: menu for display options
        :param keyboard: keyboard in display
        :param keypad: keypad
        :param options: options tree
        """
        object.__init__(self)
        self.menudisplay = menudisplay
        self.keyboard = keyboard
        self.keypad = keypad
        self.options = options

    #
    # private
    #

    def refresh_menu(self):
        self.menudisplay.title = self.options.current_menu_title()
        self.menudisplay.options = self.options.current_menu_options()
        self.menudisplay.selected = self.options.current_menu_selected()
        self.menudisplay.display()

    def refresh_keyboard(self):
        self.keyboard.title = self.options.current_menu_title()
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
            self.options.back()
            return True

        # right or enter
        if key == self.keypad.RIGHT or key == self.keypad.ENTER:
            self.options.forward(self.menudisplay.selected)
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
                self.options.forward(self.keyboard.text)
                return True
            # cancel
            elif text == self.keyboard.CANCEL_MSG:
                self.options.back()
                return True
            # key pressed
            else:
                self.keyboard.display()

        return False

    def keypress_event(self, key):
        """handle key pressed
        :return: true, it's necessary refresh display 
        """
        if self.options.current_option_is_menu():
            return self.handle_menu(key)
        elif self.options.current_option_is_keyboard():
            return self.handle_keyboard(key)

    def refresh(self):
        if self.options.current_option_is_menu():
            self.refresh_menu()
        elif self.options.current_option_is_keyboard():
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
