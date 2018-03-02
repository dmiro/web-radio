from mpd import MPDClient, CommandError
from socket import error as SocketError


class MPDWrapper(object):


    def __init__(self):
        super(MPDWrapper, self).__init__()


    def connect(self, host, port, timeout):
        try:
            self.client = MPDClient()
            self.client.timeout = timeout
            self.client.idletimeout = None
            self.client.connect(host, port)
        except SocketError:
            return False
        return True

    def disconnect(self):
        self.client.disconnect()

    def test(self):
        print '>>', self.client.listplaylist('webradio')
        self.client.clear()
        self.client.playlistclear('webradio')
        self.client.playlistadd('webradio', 'http://streams.90s90s.de/main/mp3-192/streams.90s90s.de/')
        self.client.load('webradio')
        self.client.play()
        print '>>>', self.client.listplaylist('webradio')
        print self.client.currentsong()
        #self.client.setvol(100)
        print self.client.status()

    def play(self, uri):
        #https://github.com/Mic92/python-mpd2/issues/51
        self.client.clear()
        self.client.playlistclear('webradio')
        self.client.playlistadd('webradio', uri)
        self.client.load('webradio')
        self.client.play()

    def getCurrentSong(self):
        """
        return:
              {
              'esradio':esradio,   # True= se informan los campos 'station' y 'title' | False= se informan los campos 'title' y 'artist'
              'station':station, 
              'title':title, 
              'artist':artist, 
              'time':time, 
              'audio':audio, 
              'bitrate':bitrate
              }
        """

        currentsong = self.client.currentsong()
        status = self.client.status()

        try:
            station = currentsong['name']
        except KeyError:
            station = ''

        try:
            title = currentsong['title']
        except KeyError:
            title = ''

        try:
            artist = currentsong['artist']
        except KeyError:
            artist = ''

        try:
            time = status['time']
        except:
            time = '00:00'

        try:
            audio = status['audio']
        except KeyError:
            audio = ''

        try:
            bitrate = status['bitrate']
        except KeyError:
            bitrate = 0

        # es webradio
        esradio = (station != '')

        return {'esradio': esradio, 'station': station, 'title': title, 'artist': artist, 'time': time, 'audio': audio,
                'bitrate': bitrate}