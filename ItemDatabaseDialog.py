# HEADER PLACE HOLDER

from json import load


class ItemDatabase:
    def __init__(self):
        self.parseDatabase(r'database/ItemDatabaseMetaData.json')

    def parseDatabase(self, database):
        keys = load(open(database))

        print(keys)

        for key in keys().items():
            print(key)
