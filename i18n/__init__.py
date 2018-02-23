from lib.config import config

if config.language == 'es':
    from es import *
else:
    from en import *
