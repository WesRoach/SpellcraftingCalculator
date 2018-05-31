# HEADER PLACE HOLDER

from configparser import ConfigParser
from Singleton import Singleton


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
        pass

    def save(self):
        pass
