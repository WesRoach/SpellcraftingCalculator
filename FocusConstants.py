# HEADER PLACE HOLDER

from TupleTwo import *
from DictionaryTwo import *
from Character import Realms
from CraftingConstants import GemDusts, GemLiquids

__all__ = [
    'FocusList',
    'FocusTable',
    'FocusValues'
]

FocusTable = {

    'Albion': {

        'All Spell Lines': ('Brilliant', 'Sigil',),
        'Body Magic': ('Heat', 'Sigil',),
        'Cold Magic': ('Ice', 'Sigil',),
        'Death Servant': ('Ashen', 'Sigil',),
        'Deathsight': ('Vacuous', 'Sigil',),
        'Earth Magic': ('Earth', 'Sigil',),
        'Fire Magic': ('Fire', 'Sigil',),
        'Matter Magic': ('Dust', 'Sigil',),
        'Mind Magic': ('Water', 'Sigil',),
        'Painworking': ('Salt Crusted', 'Sigil',),
        'Spirit Magic': ('Vapor', 'Sigil',),
        'Wind Magic': ('Air', 'Sigil',),
    },

    'Hibernia': {

        'All Spell Lines': ('Brilliant', 'Spell Stone',),
        'Arboreal Path': ('Steaming', 'Spell Stone',),
        'Creeping Path': ('Oozing', 'Spell Stone',),
        'Enchantments': ('Vapor', 'Spell Stone',),
        'Ethereal Shriek': ('Ethereal', 'Spell Stone',),
        'Light': ('Fire', 'Spell Stone',),
        'Mana': ('Water', 'Spell Stone',),
        'Mentalism': ('Earth', 'Spell Stone',),
        'Phantasmal Wail': ('Phantasmal', 'Spell Stone',),
        'Spectral Guard': ('Spectral', 'Spell Stone',),
        'Verdant Path': ('Mineral Encrusted', 'Spell Stone',),
        'Void': ('Ice', 'Spell Stone',),
    },

    'Midgard': {

        'All Spell Lines': ('Brilliant', 'Rune',),
        'Bone Army': ('Ashen', 'Rune',),
        'Cursing': ('Blighted', 'Rune',),
        'Darkness': ('Ice', 'Rune',),
        'Runecarving': ('Heat', 'Rune',),
        'Summoning': ('Vapor', 'Rune',),
        'Suppression': ('Dust', 'Rune',),
    },

    'All': {}}

for realm in Realms:
    for (key, value) in list(FocusTable[realm].items()):
        if value[0] in GemLiquids:
            liquid = GemLiquids[value[0]]
        else:
            liquid = GemLiquids[value[0] + " " + value[1].split()[0]]
        FocusTable[realm][key] = (value[0], value[1], GemDusts[value[1]], liquid,)
    FocusTable[realm] = d2(FocusTable[realm])
    FocusTable['All'].update(FocusTable[realm])
FocusTable['All'] = d2(FocusTable['All'])
FocusTable = d2(FocusTable)

FocusList = {}
for realm in list(FocusTable.keys()):
    FocusList[realm] = list(FocusTable[realm].keys())
    FocusList[realm].sort()
    FocusList[realm] = t2(FocusList[realm])
FocusList = d2(FocusList)

FocusValues = t2((
    '5',
    '10',
    '15',
    '20',
    '25',
    '30',
    '35',
    '40',
    '45',
    '50',
))

if __name__ == "__main__":
    pass
