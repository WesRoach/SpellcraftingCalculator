# HEADER PLACE HOLDER

from configparser import ConfigParser
from Singleton import Singleton


class Settings(Singleton):

    def __init__(self):
        Singleton.__init__(self)
        self.settings = ConfigParser()

    def getSetting(self, option, value):
        pass

    def setSetting(self, option, value):
        pass

    def importFromXML(self):
        pass

    def exportAsXML(self):
        pass

    def writeSetting(self):
        pass

    def parseSetting(self):
        pass

    def load(self):
        self.settings.read(r'settings.ini')

    def save(self):
        pass
