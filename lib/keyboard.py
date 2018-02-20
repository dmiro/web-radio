# -*- coding: utf-8 -*-
import i18n

#
# generic screen keyboard
#


class GenericKeyboard(object):

    END_MSG = '<END>'
    CANCEL_MSG = '<CANCEL>'
    KEYPRESS_MSG = '<KEY>'

    #
    # constructor
    #

    def __init__(self, title='', text=''):
        object.__init__(self)
        self.kid = 0
        self.text = text
        self.title = title
        self.x = 0
        self.y = 0
        self.display()

    #
    # private
    #

    def __resolve_x(self, x, y1, y2):

        # calculate virtual keyboard

        vkb = []
        for line in self.keyboard:
            virtual_keys = []
            for index, key in enumerate(line):
                num_virtual_keys = (len(key) / 2) + 1
                virtual_keys = virtual_keys + [index] * num_virtual_keys
            vkb.append(virtual_keys)

        # get x from virtual keyboard

        n = vkb[y1].index(x)
        if n >= len(vkb[y2]):
            return vkb[y2][-1]
        else:
            return vkb[y2][n]

    def __move_x(self, offset):
        self.x = self.x + offset
        num_chars = len(self.keyboard[self.y]) - 1
        if self.x < 0:
            self.x = num_chars
        elif self.x > num_chars:
            self.x = 0

    def __move_y(self, offset):
        old_y = self.y
        self.y = self.y + offset
        num_lines = len(self.keyboard) - 1
        if self.y < 0:
            self.y = num_lines
        elif self.y > num_lines:
            self.y = 0
        self.x = self.__resolve_x(self.x, old_y, self.y)

    #
    # public
    #

    @property
    def keyboard(self):
        return i18n.KEYBOARDS[self.kid]

    def enter(self):
        """return <end>, <cancel> or <key>"""

        ENTER_KEY = u'▼'
        CANCEL_KEY = u'◄'
        DEL_KEY = '<'
        SWITCH_KEY = '^'
        SPACE_KEY = u'═══'

        if self.selected() == SWITCH_KEY:
            self.kid = self.kid + 1
            if self.kid >= len(i18n.KEYBOARDS):
                self.kid = 0
            return
        elif self.selected() == ENTER_KEY:
            return self.END_MSG
        elif self.selected() == CANCEL_KEY:
            return self.CANCEL_MSG
        elif self.selected() == DEL_KEY:
            self.text = self.text[:-1]
        elif self.selected() == SPACE_KEY:
            self.text = self.text + ' '
            return self.KEYPRESS_MSG
        else:
            self.text = self.text + self.selected()
            return self.KEYPRESS_MSG

    def selected(self):
        return self.keyboard[self.y][self.x]

    def up(self):
        self.__move_y(-1)

    def down(self):
        self.__move_y(+1)

    def left(self):
        self.__move_x(-1)

    def right(self):
        self.__move_x(+1)

    #
    # to override
    #

    def display(self):
        """     
        title: [my text]
        q w e r t y u i o p
        R a s d f g h j k l
        * ^ z x c v b n m <
        """
        pass


#
# console screen keyboard
#


class ConsoleKeyboard(GenericKeyboard):

    #http://ascii-table.com/ansi-escape-sequences-vt-100.php
    RED = '\033[31m'
    DEFCOLOR = '\033[0m'
    MOVE_UP_N_LINES = '\33[{0}A'
    CLEAR_ENTIRE_LINE = '\33[K'

    def display(self):
        num_lines = len(self.keyboard)
        key = self.selected()
        shine = self.RED + key + self.DEFCOLOR
        print self.MOVE_UP_N_LINES.format(num_lines + 2)
        print self.CLEAR_ENTIRE_LINE + self.title + ':' + self.text
        for index in range(num_lines):
            print self.CLEAR_ENTIRE_LINE + ' '.join(self.keyboard[index]).replace(key, shine)

#
# main
#

if __name__ == '__main__':
    c = ConsoleKeyboard('title', 'my text')
    c.display()
    c.right()
    c.display()
    c.right()
    c.display()


