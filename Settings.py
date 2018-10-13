# HEADER PLACE HOLDER

from Singleton import Singleton
from configparser import ConfigParser
import os
import sys


class Settings(Singleton):

    def __init__(self):
        Singleton.__init__(self)
        self.Settings = ConfigParser()
        self.Settings.optionxform = str

    def load(self):
        if not os.path.exists(r'settings.ini'):
            self.create()
        else:
            with open(r'settings.ini', 'r') as document:
                self.Settings.read_file(document)

    def save(self):
        with open(r'settings.ini', 'w') as document:
            self.Settings.write(document)

    def create(self):
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        directories = ('items', 'database', 'templates')
        for directory in directories:
            if not os.path.exists(os.path.join(path, directory)):
                os.mkdir(os.path.join(path, directory))

        sections = ('GENERAL', 'PATHS', 'MAIN', 'QUICKBAR', 'REPORT')
        for section in sections:
            self.Settings.add_section(section)

        # DEFAULTS FOR 'GENERAL' SECTION ...
        self.Settings.set('GENERAL', 'DistanceToCap', 'True')
        self.Settings.set('GENERAL', 'UnusableSkills', 'False')
        self.Settings.set('GENERAL', 'ToolbarSize', '16')

        # DEFAULTS FOR 'PATHS' SECTION ...
        self.Settings.set('PATHS', 'ItemPath', os.path.join(path, 'items'))
        self.Settings.set('PATHS', 'DatabasePath', os.path.join(path, 'database'))
        self.Settings.set('PATHS', 'TemplatePath', os.path.join(path, 'templates'))

        # DEFAULTS FOR 'MAIN' SECTION ...
        self.Settings.set('MAIN', 'WindowX', '')
        self.Settings.set('MAIN', 'WindowY', '')
        self.Settings.set('MAIN', 'WindowW', '')
        self.Settings.set('MAIN', 'WindowH', '')
        self.Settings.set('MAIN', 'Maximized', '')

        # DEFAULTS FOR 'QUICKBAR' SECTION ...
        self.Settings.set('QUICKBAR', 'WindowX', '')
        self.Settings.set('QUICKBAR', 'WindowY', '')
        self.Settings.set('QUICKBAR', 'WindowW', '')
        self.Settings.set('QUICKBAR', 'WindowH', '')
        self.Settings.set('QUICKBAR', 'Maximized', '')

        # DEFAULTS FOR 'REPORT' SECTION ...
        self.Settings.set('REPORT', 'WindowX', '')
        self.Settings.set('REPORT', 'WindowY', '')
        self.Settings.set('REPORT', 'WindowW', '')
        self.Settings.set('REPORT', 'WindowH', '')
        self.Settings.set('REPORT', 'Maximized', '')

    def set(self, section, option, value):
        self.Settings.set(section, option, value)
        self.save()

    def get(self, section, option):
        return self.Settings.get(section, option)
