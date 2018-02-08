from os.path import isfile
from lib.keypad import Keyboard 
from lib.menu import ConsoleMenu
from lib.db import get_tags, get_stations_by_tag, get_countries, get_stations_by_country, get_languages, get_stations_by_language
from lib.createdb import check_db
import i18n


class Options(object):
    
    #
    # private
    #
     
    @property
    def atop(self):
        index = len(self.stack) - 1
        return self.stack[index]

    @atop.setter
    def atop(self, value):
        index = len(self.stack) - 1
        self.stack[index] = value

    def final(self, title):
        pass

    def get_stations_menu(self, stations, options):
        result = []
        for station in stations:
            if station[2] != 0:
                result.append({'title': station[0] + '|' + str(station[2]) + 'kbps', 'options': options})
            else:
                result.append({'title': station[0], 'options': options})
        return result

    def get_list_menu(self, items, options):
        result = [{'title': item[0] + ' (' + str(item[1]) + ')', 'options': options} for item in items]
        return result

    def stations_by_tag(self, title):
        tag = title[:title.rfind(" (")]
        stations = get_stations_by_tag(tag)
        menu = self.get_stations_menu(stations, self.final)
        self.stack.append({'title': tag, 'options': menu})
        
    def tags(self, title):
        tags = get_tags()
        menu = self.get_list_menu(tags, self.stations_by_tag)
        self.stack.append({'title': title, 'options': menu})

    def stations_by_country(self, title):
        country = title[:title.rfind(" (")]
        stations = get_stations_by_country(country)
        menu = self.get_stations_menu(stations, self.final)
        self.stack.append({'title': country, 'options': menu})

    def countries(self, title):
        tags = get_countries()
        menu = self.get_list_menu(tags, self.stations_by_country)
        self.stack.append({'title': title, 'options': menu})

    def stations_by_language(self, title):
        language = title[:title.rfind(" (")]
        stations = get_stations_by_language(language)
        menu = self.get_stations_menu(stations, self.final)
        self.stack.append({'title': language, 'options': menu})

    def languages(self, title):
        tags = get_languages()
        menu = self.get_list_menu(tags, self.stations_by_language)
        self.stack.append({'title': title, 'options': menu})

    #
    # constructor
    #
    
    def __init__(self):

        empty = []
        radio = [
            {'title': i18n.FAVORITES, 'options': empty},
            {'title': i18n.RECENT,    'options': empty},
            {'title': i18n.TAGS,      'options': self.tags},
            {'title': i18n.COUNTRIES, 'options': self.countries},
            {'title': i18n.LANGUAGES, 'options': self.languages}
            ]
        main = [
            {'title': i18n.RADIO,     'options': radio},
            {'title': i18n.FM,        'options': empty},
            {'title': i18n.BLUETOOTH, 'options': empty},
            {'title': i18n.OPTIONS,   'options': empty}
            ]
        menu = {'title': i18n.MENU, 'options': main}
        
        self.stack = []
        self.stack.append(menu)

    #
    # public
    #
    
    def menu_title(self):
        return self.atop['title']
    
    def menu_options(self):
        return [op['title'] for op in self.atop['options']]

    def menu_selected(self):
        if 'selected' in self.atop:
            return self.atop['selected']
        else:
            return 0

    def back(self):
        if len(self.stack) > 1:
            self.stack.pop()

    def forward(self, index):
        if self.atop['options']:
            self.atop['selected'] = index
            selected = self.atop['options'][index]
            if callable(selected['options']):
                selected['options'](selected['title'])
            else:
                self.stack.append(selected)
        

class App(object):
    
    #
    # constructor
    #
    
    def __init__(self, menudisplay, keypad):
        object.__init__(self)
        self.menudisplay = menudisplay
        self.keypad = keypad
        self.options = Options()

    #
    # private
    #
    def display(self):
        self.menudisplay.title = self.options.menu_title()
        self.menudisplay.options = self.options.menu_options()
        self.menudisplay.selected = self.options.menu_selected()
        self.menudisplay.display()

    #
    # public
    #

    def start(self):

        self.display()
        
        key = self.keypad.UNKNOWN
        
        while key != self.keypad.QUIT:
            
            key = self.keypad.get_key()

            # up
            if key == self.keypad.UP:
                self.menudisplay.selected = self.menudisplay.selected - 1
                self.menudisplay.display()

            # down
            if key == self.keypad.DOWN:
                self.menudisplay.selected = self.menudisplay.selected + 1
                self.menudisplay.display()

            # left
            if key == self.keypad.LEFT:
                self.options.back()
                self.display()

            # right
            if key == self.keypad.RIGHT:
                self.options.forward(self.menudisplay.selected)
                self.display()

            # enter
            if key == self.keypad.ENTER:
                pass        
                #print menu.item_selected

    
#
# main
#

check_db()
app = App(ConsoleMenu(), Keyboard())
app.start()
