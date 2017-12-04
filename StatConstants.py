# HEADER PLACE HOLDER

from TupleTwo import *
from DictionaryTwo import *
from CraftingConstants import GemDusts, GemLiquids

__all__ = [
    'CraftStatList',
    'CraftStatTable',
    'DropStatList',
    'DropStatTable',
    'HitsValues',
    'PowerValues',
    'StatValues',
]

StatTableOrdered = (
    ('Strength', 'Fiery',),
    ('Constitution', 'Earthen',),
    ('Dexterity', 'Vapor',),
    ('Quickness', 'Airy',),
    ('Intelligence', 'Dusty',),
    ('Piety', 'Watery',),
    ('Charisma', 'Icy',),
    ('Empathy', 'Heated',),
    ('Power', 'Mystical',),
    ('Hits', 'Blood',),
)

suffix = 'Essence Jewel'
StatTable = dict(StatTableOrdered)

for (key, value) in list(StatTable.items()):
    StatTable[key] = (value, suffix, GemDusts[suffix], GemLiquids[value],)

CraftStatList = t2([x[0] for x in StatTableOrdered])
CraftStatTable = d2(StatTable)
DropStatList = t2(CraftStatList + ('Acuity',))
DropStatTable = dict().fromkeys(DropStatList)

del StatTableOrdered
del StatTable

StatValues = t2((
    '2',
    '5',
    '8',
    '11',
    '14',
    '17',
    '20',
    '23',
    '26',
    '29',
))

HitsValues = t2((
    '4',
    '12',
    '20',
    '28',
    '36',
    '44',
    '52',
    '60',
    '68',
    '76',
))

PowerValues = t2((
    '1',
    '2',
    '3',
    '5',
    '7',
    '9',
    '11',
    '13',
    '15',
    '17'
))

if __name__ == "__main__":
    pass
