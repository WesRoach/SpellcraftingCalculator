# HEADER PLACE HOLDER

from configparser import ConfigParser
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

    def create(self):
        pass

    def parse(self):
        pass

    def load(self):
        if Path(r'settings.ini'):
            self.settings.read(r'settings.ini')
        else:
            self.create()

    def save(self):
        pass
