from iniconfig import IniConfig

CONFIG_FILE = './data/config.ini'


class Config(IniConfig):

    language = IniConfig.iniproperty('general', 'language', 'es')  # es or en

    favorites = IniConfig.iniproperty('web-radio', 'favorites', ['http://streaming3.radiocat.net:80/',
                                                                 'http://streams.90s90s.de/main/mp3-192/streams.90s90s.de/'])
    recents = IniConfig.iniproperty('web-radio', 'recents', ['http://streaming3.radiocat.net:80/',
                                                            'http://streams.90s90s.de/main/mp3-192/streams.90s90s.de/'])
    maxrecents = IniConfig.iniproperty('web-radio', 'maxrecents', 25)

    wifi_ssid = IniConfig.iniproperty('wifi', 'ssid', 'demo')
    wifi_password = IniConfig.iniproperty('wifi', 'password', 'demo')

config = Config(CONFIG_FILE)
