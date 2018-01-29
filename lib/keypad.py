

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
# keyboard
#

class Keyboard(GenericKeypad):

    #
    # constructor
    #
    
    def __init__(self):
        GenericKeypad.__init__(self)

    #
    # public
    #

    def get_key(self):

        from getch import getch

        m = getch()
        if ord(m) == 27:
            m = getch()
            if ord(m) == 91:
                key = ord(getch())
                if key == 65: # up
                   return Keyboard.UP 
                if key == 66: # down
                   return Keyboard.DOWN 
                if key == 68: # left
                    return Keyboard.LEFT
                if key == 67: # right
                    return Keyboard.RIGHT
        # enter
        if ord(m) == 12:
            return Keyboard.ENTER
        # quit
        if m == 'q':
            return Keyboard.QUIT


#
# gpio key
#

class GPIOKeyboard(GenericKeypad):

    #
    # constructor
    #
    
    def __init__(self):
        GenericKeypad.__init__(self)

    #
    # public
    #

    def get_key(self):
	pass



