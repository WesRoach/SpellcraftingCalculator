# HEADER PLACE HOLDER

from configparser import ConfigParser, NoOptionError
from Singleton import Singleton
from pathlib import Path


class Settings(Singleton):

    def __init__(self):
        Singleton.__init__(self)
        self.settings = ConfigParser()

    def get(self, option, value):
        pass

    def set(self, option, value):
        pass

    def write(self):
        pass

    def parse(self):
        pass

    def load(self):
        if Path(r'settings.ini').exists():
            self.settings.read(r'settings.ini')
        else:
            pass

    def save(self):
        pass
