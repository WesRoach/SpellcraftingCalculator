# HEADER PLACE HOLDER

from TupleTwo import *
from DictionaryTwo import *
from CraftingConstants import GemDusts, GemLiquids

__all__ = [
    'CraftResistList',
    'CraftResistTable',
    'DropResistList',
    'DropResistTable',
    'ResistValues',
]

ResistTableOrdered = (
    ('Body', 'Dusty',),
    ('Cold', 'Icy',),
    ('Heat', 'Heated',),
    ('Energy', 'Light',),
    ('Matter', 'Earthen',),
    ('Spirit', 'Vapor',),
    ('Crush', 'Fiery',),
    ('Thrust', 'Airy',),
    ('Slash', 'Watery',),
)

suffix = 'Shielding Jewel'
ResistTable = dict(ResistTableOrdered)

for (key, value) in list(ResistTable.items()):
    ResistTable[key] = (value, suffix, GemDusts[suffix], GemLiquids[value])

CraftResistTable = d2(ResistTable)
CraftResistList = t2([x[0] for x in ResistTableOrdered])
DropResistList = t2(CraftResistList + ('Essence',))
DropResistTable = dict().fromkeys(DropResistList)

del ResistTableOrdered
del ResistTable

ResistValues = t2((
    '1',
    '2',
    '3',
    '5',
    '7',
    '9',
    '11',
    '13',
    '15',
    '17',
))

if __name__ == "__main__":
    pass
