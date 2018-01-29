from os.path import isfile
from lib.keypad import Keyboard 
from lib.menu import ConsoleMenu
from lib.db import get_tags, get_stations_by_tag, get_countries, get_stations_by_country, get_languages, get_stations_by_language
from lib.createdb import check_db
import i18n.es as literals

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

    def stations_by_tag(self, title):
        tag = title[:title.rfind(" (")]
        stationlist = get_stations_by_tag(tag)
        options = [{'title':station[0] + '|' +  str(station[2]) + 'kbps', 'options':self.final} for station in stationlist]
        self.stack.append({'title':tag, 'options':options})
        
    def tags(self, title):
        taglist = get_tags()
        options = [{'title':tag[0] + ' ('+str(tag[1])+')', 'options':self.stations_by_tag} for tag in taglist]
        self.stack.append({'title':title, 'options':options})

    def stations_by_country(self, title):
        country = title[:title.rfind(" (")]
        stationlist = get_stations_by_country(country)
        options = [{'title':station[0] + '|' +  str(station[2]) + 'kbps', 'options':self.final} for station in stationlist]
        self.stack.append({'title':country, 'options':options})

    def countries(self, title):
        countrieslist = get_countries()
        options = [{'title':country[0] + ' ('+str(country[1])+')', 'options':self.stations_by_country} for country in countrieslist]
        self.stack.append({'title':title, 'options':options})

    def stations_by_language(self, title):
        language = title[:title.rfind(" (")]
        stationlist = get_stations_by_language(language)
        options = [{'title':station[0] + '|' +  str(station[2]) + 'kbps', 'options':self.final} for station in stationlist]
        self.stack.append({'title':language, 'options':options})

    def languages(self, title):
        languageslist = get_languages()
        options = [{'title':language[0] + ' ('+str(language[1])+')', 'options':self.stations_by_language} for language in languageslist]
        self.stack.append({'title':title, 'options':options})

    #
    # constructor
    #
    
    def __init__(self):

        empty = []
        radio = [
            {'title':literals.FAVORITES, 'options':empty},
            {'title':literals.RECENT   , 'options':empty},
            {'title':literals.TAGS     , 'options':self.tags},
            {'title':literals.COUNTRIES, 'options':self.countries},
            {'title':literals.LANGUAGES, 'options':self.languages}
            ]
        main = [
            {'title':literals.RADIO    , 'options':radio},
            {'title':literals.FM       , 'options':empty},
            {'title':literals.BLUETOOTH, 'options':empty},
            {'title':literals.OPTIONS  , 'options':empty}
            ]
        menu = {'title':literals.MENU, 'options':main}
        
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
  
            
