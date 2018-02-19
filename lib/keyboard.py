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

    def __adjust_x(self):
        if self.x >= self.__numchars -1:
            self.x = self.__numchars - 1

    def __move_x(self, offset):
        self.x = self.x + offset
        num_chars = len(self.keyboard[self.y])
        if self.x < 0:
            self.x = num_chars - 1
        elif self.x > num_chars - 1:
            self.x = 0

    def __move_y(self, offset):
        self.y = self.y + offset
        num_lines = len(self.keyboard)
        if self.y < 0:
            self.y = num_lines - 1
        elif self.y > num_lines - 1:
            self.y = 0
        self.__move_x(0)

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
    UP = '\33A'
    DOWN = '\33B'
    LEFT = '\33C'
    RIGHT = '\33D'
    RED = '\033[31m'
    DEFCOLOR = '\033[0m'
    MOVE_UP_FIVE_LINES = '\33[5A'
    CLEAR_ENTIRE_LINE = '\33[K'

    def display(self):
        key = self.selected()
        shine = self.RED + key + self.DEFCOLOR
        print self.MOVE_UP_FIVE_LINES
        print self.CLEAR_ENTIRE_LINE + self.title + ':' + self.text
        print self.CLEAR_ENTIRE_LINE + ' '.join(self.keyboard[0]).replace(key, shine)
        print self.CLEAR_ENTIRE_LINE + ' '.join(self.keyboard[1]).replace(key, shine)
        print self.CLEAR_ENTIRE_LINE + ' '.join(self.keyboard[2]).replace(key, shine)


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


