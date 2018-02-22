from iniconfig import IniConfig

CONFIG_FILE = './data/config.ini'

class Config(IniConfig):

    favorites = IniConfig.iniproperty('web-radio', 'favorites', [])
    recent = IniConfig.iniproperty('web-radio', 'recent', [])

config = Config(CONFIG_FILE)