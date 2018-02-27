# -*- coding: utf-8 -*-
import i18n
from datetime import datetime

#
# generic screen play info
#


class GenericPlayInfo(object):

    #
    # constructor
    #

    def __init__(self, station='', title='', time='', audio='', bitrate=''):
        object.__init__(self)
        self.station = station
        self.title = title
        self.time = time
        self.audio = audio
        self.bitrate = bitrate

    @property
    def time(self):
        if self.__time:
            seconds = int(self.__time.split(':')[0])

            dif = datetime.now() - self.datetimestart
            seconds = dif.seconds + seconds

            m, s = divmod(seconds, 60)
            time = str(m).zfill(2) + ':' + str(s).zfill(2)
            return time
        else:
            return ' : '

    @time.setter
    def time(self, value):
        self.datetimestart = datetime.now()
        self.__time = value

    #
    # to override
    #

    def display(self):
        """     
        [] Station
        [] Title
        [] Time
        audio + bitrate
        """
        pass


#
# console screen play info
#


class ConsolePlayInfo(GenericPlayInfo):

        # http://ascii-table.com/ansi-escape-sequences-vt-100.php
        NEW_LINE = '\33[20h'
        MOVE_UP_FIVE_LINES = '\33[5A'
        CLEAR_ENTIRE_LINE = '\33[K'

        def __init__(self, *args, **kwargs):
            GenericPlayInfo.__init__(self, *args, **kwargs)
            print self.NEW_LINE
            print self.NEW_LINE
            print self.NEW_LINE
            print self.NEW_LINE

        def display(self):
            print self.MOVE_UP_FIVE_LINES
            print self.CLEAR_ENTIRE_LINE + i18n.STATION + ': ' + self.station
            print self.CLEAR_ENTIRE_LINE + i18n.TITLE + ': ' + self.title
            print self.CLEAR_ENTIRE_LINE + i18n.TIME + ': ' + self.time
            print self.CLEAR_ENTIRE_LINE + str(self.audio) + ' | ' + str(self.bitrate) + ' kbps'


#
# test
#

if __name__ == '__main__':
    c = ConsolePlayInfo(station='my station', title='my title', time='1:00', audio='128', bitrate='19000')
    c.display()
    import time
    for i in range(10):
        time.sleep(1)
        c.display()
