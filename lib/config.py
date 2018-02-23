from iniconfig import IniConfig

CONFIG_FILE = './data/config.ini'


class Config(IniConfig):

    language = IniConfig.iniproperty('general', 'language', 'es')  # es or en

    favorites = IniConfig.iniproperty('web-radio', 'favorites', ['http://streaming3.radiocat.net:80/',
                                                                 'http://streams.90s90s.de/main/mp3-192/streams.90s90s.de/'])
    recents = IniConfig.iniproperty('web-radio', 'recents', ['http://streaming3.radiocat.net:80/',
                                                            'http://streams.90s90s.de/main/mp3-192/streams.90s90s.de/'])

config = Config(CONFIG_FILE)
