# HEADER PLACE HOLDER

from configparser import ConfigParser
from Singleton import Singleton
from pathlib import Path


class Settings(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    def get(self, option):
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
        if not Path(r'settings.ini').exists():
            self.create()

        settings = ConfigParser()
        settings.optionxform = str
        settings.read(r'settings.ini')

        for section in settings.keys():
            for option, value in settings[section].items():
                globals()[option] = settings.get(section, option)

    def save(self):
        pass
