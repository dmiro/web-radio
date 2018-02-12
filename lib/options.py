#
# Generic Options
# Allow to create an options tree and navigate it
#


class OptionsTree(object):

    #
    # private
    #

    DISPLAY = 0
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
        return {'type': self.DISPLAY, 'title': title, 'options': options}

    def get_keyboard_option(self, title, options):
        return {'type': self.KEYBOARD, 'title': title, 'options': options}

    def current_option_is_display(self):
        return self.atop['type']  == self.DISPLAY

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

    def forward(self, index):
        """forward in the options tree"""
        if self.atop['options']:
            self.atop['selected'] = index
            selected = self.atop['options'][index]
            if callable(selected['options']):
                selected['options'](selected['title'])
            else:
                self.stack.append(selected)