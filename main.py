# MAIN

from lib.db import get_tags, get_stations_by_tag, get_countries, get_stations_by_country, get_languages, get_stations_by_language, get_stations_by_text
from lib.createdb import check_db
from lib.options import OptionsTree
import i18n

from lib.keypad import FisicKeyboard
from lib.menu import ConsoleMenu
from lib.keyboard import ConsoleKeyboard
from lib.application import Application


class Options(OptionsTree):

    # helpers

    def get_stations_menu(self, stations):
        station_menu = [self.get_menu_option(i18n.PLAY, self.final),
                        self.get_menu_option(i18n.ADD_FAVORITES, self.final),
                        self.get_menu_option(i18n.MORE_INFO, self.final),
                        self.get_menu_option(i18n.REMOVE_FAVORITES, self.final)] # todo: remove if station is not favorites
        result = []
        for station in stations:
            if station[2] != 0:
                result.append(self.get_menu_option(station[0] + '|' + str(station[2]) + 'kbps', station_menu))
            else:
                result.append(self.get_menu_option(station[0], station_menu))
        return result

    def get_list_menu(self, items, options):
        result = [self.get_menu_option(item[0] + ' (' + str(item[1]) + ')', options) for item in items]
        return result

    # stations by tag

    def stations_by_tag(self, title):
        tag = title[:title.rfind(" (")]
        stations = get_stations_by_tag(tag)
        menu = self.get_stations_menu(stations)
        return self.get_menu_option(tag, menu)

    def tags(self, title):
        tags = get_tags()
        menu = self.get_list_menu(tags, self.stations_by_tag)
        return self.get_menu_option(title, menu)

    # stations by country

    def stations_by_country(self, title):
        country = title[:title.rfind(" (")]
        stations = get_stations_by_country(country)
        menu = self.get_stations_menu(stations)
        return self.get_menu_option(country, menu)

    def countries(self, title):
        tags = get_countries()
        menu = self.get_list_menu(tags, self.stations_by_country)
        return self.get_menu_option(title, menu)

    # stations by language

    def stations_by_language(self, title):
        language = title[:title.rfind(" (")]
        stations = get_stations_by_language(language)
        menu = self.get_stations_menu(stations)
        return self.get_menu_option(language, menu)

    def languages(self, title):
        tags = get_languages()
        menu = self.get_list_menu(tags, self.stations_by_language)
        return self.get_menu_option(title, menu)

    # search stations

    def search(self, title):
        stations = get_stations_by_text(title)
        menu = self.get_stations_menu(stations)
        return self.get_menu_option(title, menu)

    #
    # constructor
    #
    
    def __init__(self):
        OptionsTree.__init__(self)
        empty = []
        radio = [
            self.get_menu_option(i18n.FAVORITES, empty),
            self.get_menu_option(i18n.RECENT, empty),
            self.get_keyboard_option(i18n.SEARCH, self.search),
            self.get_menu_option(i18n.TAGS, self.tags),
            self.get_menu_option(i18n.COUNTRIES, self.countries),
            self.get_menu_option(i18n.LANGUAGES, self.languages)
            ]
        main = [
            self.get_menu_option(i18n.RADIO, radio),
            self.get_menu_option(i18n.FM, empty),
            self.get_menu_option(i18n.BLUETOOTH, empty),
            self.get_menu_option(i18n.OPTIONS, empty)
            ]
        menu = self.get_menu_option(i18n.MENU, main)
        self.set_menu(menu)

#
# main
#

check_db()
app = Application(ConsoleMenu(),
                  ConsoleKeyboard(),
                  FisicKeyboard(),
                  Options())
app.start()
