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
    def display(self):
        if self.options.current_option_is_display():
            self.menudisplay.title = self.options.current_menu_title()
            self.menudisplay.options = self.options.current_menu_options()
            self.menudisplay.selected = self.options.current_menu_selected()
            self.menudisplay.display()
        elif self.options.current_option_is_keyboard():
            self.keyboard.title = self.options.current_menu_title()
            self.keyboard.display()

    #
    # public
    #

    def start(self):

        self.display()

        key = self.keypad.UNKNOWN

        while key != self.keypad.QUIT:

            key = self.keypad.get_key()

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
                self.display()

            # right
            if key == self.keypad.RIGHT:
                self.options.forward(self.menudisplay.selected)
                self.display()

            # enter
            if key == self.keypad.ENTER:
                pass
                # print menu.item_selected