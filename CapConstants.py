# HEADER PLACE HOLDER

from TupleTwo import *
from DictionaryTwo import *

__all__ = [
    'Cap',
    'CapList',
    'MythicalCap',
    'MythicalCapList',
]

CapList = t2((
    'Strength',
    'Constitution',
    'Dexterity',
    'Quickness',
    'Intelligence',
    'Piety',
    'Charisma',
    'Empathy',
    'Power',
    'Fatigue',
))

MythicalCapList = t2((
    'Strength',
    'Constitution',
    'Dexterity',
    'Quickness',
    'Intelligence',
    'Piety',
    'Charisma',
    'Empathy',
    'Acuity',
))

Cap = d2({
    'Armor Factor': (1.00, 0),
    'Armor Factor Cap': (1.00, 0),
    'Arrow Recovery': (1.00, 0),
    'Death Experience Loss Reduction': (1.00, 0),
    'Duration of Spells': (.50, 0),
    'Fatigue': (.50, 0),
    'Fatigue Cap': (.50, 0),
    'Focus': (1.00, 0),
    'Healing Effectiveness': (.50, 0),
    'Hits': (4.00, 0),
    'Hits Cap': (8.00, 0),
    'Power': (.50, 1),
    'Power Cap': (1.00, 0),
    '% Power Pool': (.50, 0),
    '% Power Pool Cap': (1.00, 0),
    'PvE Bonus': (.20, 0),
    'Resist': (.50, 1),
    'Skill': (.20, 1),
    'Stat': (1.50, 0),
    'Stat Cap': (.50, 1),
    'Stat Buff Effectiveness': (.50, 0),
    'Stat Debuff Effectiveness': (.50, 0),
    'Other Bonus': (.20, 0),
})

MythicalCap = d2({
    'Crowd Control Reduction': (1.00, 0),
    'DPS': (.20, 0),
    'Endurance Regen': (1.00, 0),
    'Health Regen': (1.00, 0),
    'Power Regen': (1.00, 0),
    'Stat Cap': (.50, 1),
    'Resist Cap': (0, 15),
    'Mythical Bonus': (0, 0),
})

if __name__ == "__main__":
    pass
