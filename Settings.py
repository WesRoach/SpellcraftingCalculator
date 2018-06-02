# HEADER PLACE HOLDER

from Singleton import Singleton
from pathlib import Path


class Settings(Singleton):

    def __init__(self):
        Singleton.__init__(self)

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
            pass
        else:
            self.create()

    def save(self):
        pass
