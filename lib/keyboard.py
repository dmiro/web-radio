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
        self.text = text
        self.title = title
        self.x = 0
        self.y = 0

    #
    # public
    #

    def enter(self):
        """return <end>, <cancel> or <key>"""

        ENTER_KEY = '*'
        CANCEL_KEY = 'R'
        DEL_KEY = '<'

        if self.selected() == ENTER_KEY:
            return self.END_MSG
        if self.selected() == CANCEL_KEY:
            return self.CANCEL_MSG
        if self.selected() == DEL_KEY:
            self.text = self.text[:-1]
        else:
            self.text = self.text + self.selected()
        return self.KEYPRESS_MSG

    def selected(self):
        return i18n.KEYBOARD1[self.y][self.x]

    def up(self):
        if self.y > 0:
            self.y = self.y - 1
        else:
            self.y = 2

    def down(self):
        if self.y < 2:
            self.y = self.y + 1
        else:
            self.y = 0

    def left(self):
        if self.x > 0:
            self.x = self.x - 1
        else:
            self.x = 9

    def right(self):
        if self.x < 9:
            self.x = self.x + 1
        else:
            self.x = 0

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

    def __init__(self, *args, **kwargs):
        GenericKeyboard.__init__(self, *args, **kwargs)
        self.display()

    def display(self):
        key = self.selected()
        shine = self.RED + key + self.DEFCOLOR
        print self.MOVE_UP_FIVE_LINES
        print self.CLEAR_ENTIRE_LINE + self.title + ':' + self.text
        print self.CLEAR_ENTIRE_LINE + ' '.join(i18n.KEYBOARD1[0]).replace(key, shine)
        print self.CLEAR_ENTIRE_LINE + ' '.join(i18n.KEYBOARD1[1]).replace(key, shine)
        print self.CLEAR_ENTIRE_LINE + ' '.join(i18n.KEYBOARD1[2]).replace(key, shine)


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


