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