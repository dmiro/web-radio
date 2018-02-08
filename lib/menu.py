
#
# generic menu
#

class GenericMenu(object):

    EMPTY_MESSAGE = '(empty)'
    OPTIONS_LINES = 3

    #
    # constructor
    #
    
    def __init__(self, title='', options=[]):
        """
        param:title: 'radio'
        param:options: ['00s', '128kbps', '1920s']
        """
        object.__init__(self)
        self.display_options = None
        self.display_selected = None
        self.title = title 
        self.options = options

    #
    # private
    #

    def __set_selected(self, value):

        num = len(self.options)
        
        # empty
        if num == 0:
            self.__selected = -1
            self.display_options = [GenericMenu.EMPTY_MESSAGE] + [''] * 2
            self.display_selected = None
        # first
        elif value <= 0:
            self.__selected = 0
            self.display_options = self.options[0:min(num, GenericMenu.OPTIONS_LINES)]
            self.display_selected = 0
        # last
        elif value >= num - 1:
            self.__selected = num - 1
            self.display_options = self.options[max(0, num - GenericMenu.OPTIONS_LINES):num]
            self.display_selected = min(num - 1, GenericMenu.OPTIONS_LINES - 1)
        # in the middle
        else:
            self.__selected = value
            self.display_options = self.options[self.__selected - 1:self.__selected + 2]
            self.display_selected = 1

    #
    # public
    #

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, value):
        self.__set_selected(value)

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        self.__options = value
        self.__set_selected(0)
        
    @property
    def item_selected(self):
        if self.selected >= 0:
            return self.options[self.selected]
        else:
            return None

    #
    # to override
    #

    def display(self):
        """     
        radio > etiquetas
        00s
        *128kbps*
        192s
        """
        pass


#
# console menu
#


class ConsoleMenu(GenericMenu):
    
    #http://ascii-table.com/ansi-escape-sequences-vt-100.php
    NEW_LINE = '\33[20h'
    MOVE_UP_FIVE_LINES = '\33[5A'
    CLEAR_ENTIRE_LINE = '\33[K'
    
    def __init__(self, *args, **kwargs):
        GenericMenu.__init__(self, *args, **kwargs)
        print self.NEW_LINE
        print self.NEW_LINE
        print self.NEW_LINE
        print self.NEW_LINE
 
    def display(self):
        print self.MOVE_UP_FIVE_LINES
        print self.CLEAR_ENTIRE_LINE + self.title
     
        for index, value in enumerate(self.display_options):            
            if index == self.display_selected:
                print self.CLEAR_ENTIRE_LINE + '*' + value + '*'
            else:
                print self.CLEAR_ENTIRE_LINE + value

        for index in range(len(self.display_options), 3):
            print self.CLEAR_ENTIRE_LINE



#
# oled menu
#


class OledMenu(GenericMenu):
    
    def __init__(self, *args, **kwargs):
        GenericMenu.__init__(self, *args, **kwargs)

    def display(self, *args, **kwargs):
        pass


