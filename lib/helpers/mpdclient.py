from mpd import MPDClient, CommandError
from socket import error as SocketError
from singleton import Singleton

class MPDWrapper(Singleton):

    PLAYLIST_RADIO = 'webradio'

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

    def stop(self):
        self.client.stop()
        self.client.clear()
        self.client.playlistclear(self.PLAYLIST_RADIO)

    def play(self, uri):
        #https://github.com/Mic92/python-mpd2/issues/51
        self.stop()
        self.client.playlistadd(self.PLAYLIST_RADIO, uri)
        self.client.load(self.PLAYLIST_RADIO)
        self.client.play()

    def getCurrentSong(self):
        """
        return:
              {
              'isradio':isradio,   # True= fields informed are 'station' y 'title'
                                   # False= fields informed are 'title' y 'artist'
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

        # is webradio?
        isradio = (station != '')

        return {'isradio': isradio, 'station': station, 'title': title, 'artist': artist, 'time': time, 'audio': audio,
                'bitrate': bitrate}


mpd_client = MPDWrapper()