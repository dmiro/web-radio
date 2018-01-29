
#
# generic screen keyboard
#

class GenericKeyboard(object):

    #
    # constructor
    #
    
    def __init__(self, title='', text='', language='es'):
        """
        param:title: 'search'
        param:language: 'es'
        """
        object.__init__(self)
        self.text = text
        self.title = title 
        self.language = language
        self.__selected = [0, 0]

    #
    # public
    #

    END = '<END>'
    CANCEL = '<CANCEL>'

    def enter(self):
	"""
	return: '<end>', '<cancel>' or key pressed
	"""
        return '<end>'

    @property
    def up(self):
        pass

    @up.setter
    def up(self, value):
        pass

    @property
    def down(self):
        pass

    @up.setter
    def down(self, value):
        pass

    @property
    def left(self):
        pass

    @up.setter
    def left(self, value):
        pass

    @property
    def right(self):
        pass

    @up.setter
    def right(self, value):
        pass


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

    def __init__(self, title='', text='', language='es'):
        GenericKeyboard.__init__(self, title, text, language)

    def display(self):
        print ConsoleKeyboard.RED + 'hola' + ConsoleKeyboard.DEFCOLOR + 'adios'



c = ConsoleKeyboard()
c.display()

