# HEADER PLACE HOLDER

from Singleton import Singleton
from configparser import ConfigParser


class Settings(Singleton):

    def __init__(self):
        Singleton.__init__(self)
        self.Settings = ConfigParser()
        self.Settings.optionxform = str
        self.Settings.read(r'settings.ini')

    def load(self):
        return
