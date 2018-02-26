# MAIN

import i18n

from lib.db import get_tags, get_stations_by_tag, get_countries, get_stations_by_country, get_languages, \
    get_stations_by_language, get_stations_by_text, get_station_by_url
from lib.createdb import check_db
from lib.keypad import FisicKeyboard
from lib.menu import ConsoleMenu
from lib.keyboard import ConsoleKeyboard
from lib.application import Application
from lib.config import config


class WebRadioApp(Application):

    # helpers

    def get_stations_menu(self, stations):
        result = []
        for station in stations:
            station_menu = self.get_station_menu(station[1])
            if station[2] != 0:
                result.append(self.get_menu_option(station[0] + '|' + str(station[2]) + 'kbps', station_menu))
            else:
                result.append(self.get_menu_option(station[0], station_menu))
        return result

    def get_list_menu(self, items, options):
        result = [self.get_menu_option(item[0] + ' (' + str(item[1]) + ')', options) for item in items]
        return result

    # station

    def play(self, url):
        def play_(self):
            # add to recents
            if url not in config.recents:
                config.recents.insert(0, url)
                maxrecent = config.maxrecents if config.maxrecents > 0 else 1
                config.recents = config.recents[:maxrecent]
            # play
            pass
        return play_

    def add_favorite(self, url):
        def add_(self):
            if url not in config.favorites:
                config.favorites = config.favorites + [url]
        return add_

    def remove_favorite(self, url):
        def del_(self):
            if url in config.favorites:
                config.favorites.remove(url)
        return del_

    def more(self, url):
        def more_(self):
            pass
        return more_

    def get_station_menu(self, url):
        station_is_favorite = url in config.favorites
        menu = [self.get_menu_option(i18n.PLAY, self.play(url))]
        if not station_is_favorite:
            menu.append(self.get_menu_option(i18n.ADD_FAVORITES, self.add_favorite(url)))
        menu.append(self.get_menu_option(i18n.MORE_INFO, self.more))
        if station_is_favorite:
            menu.append(self.get_menu_option(i18n.REMOVE_FAVORITES, self.remove_favorite(url)))
        return menu

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

    # favorites

    def favorites(self, title):
        stations = []
        for favorite in config.favorites:
            station = get_station_by_url(favorite)
            if station:
                stations.append(station)
        menu = self.get_stations_menu(stations)
        return self.get_menu_option(title, menu)

    # recent

    def recent(self, title):
        stations = []
        for recent in config.recents:
            station = get_station_by_url(recent)
            if station:
                stations.append(station)
        menu = self.get_stations_menu(stations)
        return self.get_menu_option(title, menu)

    #
    # constructor
    #
    
    def __init__(self, *args, **kargs):
        super(WebRadioApp, self).__init__(*args, **kargs)
        empty = []
        radio = [
            self.get_menu_option(i18n.FAVORITES, self.favorites),
            self.get_menu_option(i18n.RECENT, self.recent),
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
app = WebRadioApp(ConsoleMenu(),
                  ConsoleKeyboard(),
                  FisicKeyboard())
app.start()
