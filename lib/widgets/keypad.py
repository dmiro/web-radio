

#
# generic keypad
#

class GenericKeypad(object):

    #
    # constructor
    #
    
    def __init__(self):
        object.__init__(self)

    #
    # public
    #

    UNKNOWN = -1
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    ENTER = 4
    QUIT = 5

    #
    # to override
    #

    def get_key(self):
        """
        return UP, DOWN, BACK, etc..
        """
        pass


#
# Fisic keyboard
#

class FisicKeyboard(GenericKeypad):

    #
    # constructor
    #
    
    def __init__(self, *args, **kwargs):
        GenericKeypad.__init__(self, *args, **kwargs)

    #
    # public
    #

    def get_key(self):

        from lib.helpers.getch import getch

        m = getch()
        if ord(m) == 27:
            m = getch()
            if ord(m) == 91:
                key = ord(getch())
                if key == 65: # up
                   return self.UP
                if key == 66: # down
                   return self.DOWN
                if key == 68: # left
                    return self.LEFT
                if key == 67: # right
                    return self.RIGHT
        # enter
        if ord(m) == 13:
            return self.ENTER
        # quit
        if m == 'q':
            return self.QUIT


#
# gpio key
#

class GPIOKeyboard(GenericKeypad):

    #
    # constructor
    #
    
    def __init__(self, *args, **kwargs):
        GenericKeypad.__init__(self, *args, **kwargs)

    #
    # public
    #

    def get_key(self):
        pass


# test
if __name__ == '__main__':

    from lib.helpers.getch import getch
    m = getch()
    print ord(m)