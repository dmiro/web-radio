from iniconfig import IniConfig

CONFIG_FILE = './data/config.ini'


class Config(IniConfig):

    # general
    language = IniConfig.iniproperty('general', 'language', 'es')  # es or en

    # web-radio
    favorites = IniConfig.iniproperty('web-radio', 'favorites', ['http://streaming3.radiocat.net:80/',
                                                                 'http://streams.90s90s.de/main/mp3-192/streams.90s90s.de/'])
    recents = IniConfig.iniproperty('web-radio', 'recents', ['http://streaming3.radiocat.net:80/',
                                                            'http://streams.90s90s.de/main/mp3-192/streams.90s90s.de/'])
    maxrecents = IniConfig.iniproperty('web-radio', 'maxrecents', 25)

    # wifi
    wifi_ssid = IniConfig.iniproperty('wifi', 'ssid', 'demo')
    wifi_password = IniConfig.iniproperty('wifi', 'password', 'demo')

    # mpd
    mpd_host = IniConfig.iniproperty('mpd', 'host', 'localhost')
    mpd_port = IniConfig.iniproperty('mpd', 'port', 6600)
    mpd_timeout = IniConfig.iniproperty('mpd', 'timeout', 10)  # network timeout in seconds (floats allowed), default: None


config = Config(CONFIG_FILE)
