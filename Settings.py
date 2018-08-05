# HEADER PLACE HOLDER

from configparser import ConfigParser
from Singleton import Singleton
import os
import sys

# SINGLETON IS NOT REQUIRED ...


class Settings(Singleton):

    def __init__(self):
        Singleton.__init__(self)

    def get(self, option):
        pass

    def set(self, option, value):
        pass

    def write(self):
        pass

    @staticmethod
    def create():
        with open(r'settings.ini', 'w') as document:
            settings = ConfigParser()
            settings.optionxform = str
            sections = ['GENERAL', 'PATHS']

            for section in sections:
                settings.add_section(section)

            # DEFAULTS FOR 'GENERAL' SECTION
            settings.set('GENERAL', 'DistanceToCap', 'True')
            settings.set('GENERAL', 'UnusableSkills', 'False')
            settings.set('GENERAL', 'ToolbarSize', '16')

            # TODO: TEST AND CREATE DIRECTORIES IF THEY ARE NOT THERE ...

            # DEFAULTS FOR 'PATHS' SECTION
            default_path = os.path.dirname(os.path.abspath(sys.argv[0]))
            settings.set('PATHS', 'ItemPath', os.path.join(default_path, 'items'))
            settings.set('PATHS', 'DatabasePath', os.path.join(default_path, 'database'))
            settings.set('PATHS', 'TemplatePath', os.path.join(default_path, 'templates'))

            # CREATE DEFAULT 'settings.ini'
            settings.write(document)

    def parse(self):
        pass

    def load(self):
        if not os.path.exists(r'settings.ini'):
            self.create()

        settings = ConfigParser()
        settings.optionxform = str
        settings.read(r'settings.ini')

        # MAYBE RETURN SETTINGS AND JUST CALL PARSE EACH TIME?

        for section in settings.keys():
            for option, value in settings[section].items():
                globals()[option] = settings.get(section, option)

    def save(self):
        pass
