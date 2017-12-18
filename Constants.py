# HEADER PLACE HOLDER

# TODO: COMBINE ALL CONSTANTS INTO ONE FILE

from BonusConstants import *
from Character import *
from CapConstants import *
from CraftingConstants import *
from FocusConstants import *
from SlotConstants import *
from ResistConstants import *
from StatConstants import *
from SkillConstants import *
from TupleTwo import *
from DictionaryTwo import *

__all__ = [
    'CraftLists',
    'CraftTables',
    'DropLists',
    'GemTables',
    'GemLists',
    'ValuesLists',
    'EnhancedLists',
    'EnhancedValuesLists',
]

UnusedTable = d2({})
UnusedList = t2()
UnusedValues = t2()

CraftLists = {  # GemLists

    'All': {

        'Unused': UnusedList,
        'Stat': CraftStatList,
        'Resist': CraftResistList,
        # 'Charged Effect': chargedEffectList,
        # 'Offensive Effect': offensiveEffectList,
        # 'Reactive Effect': reactiveEffectList,
    }
}

CraftTables = {  # GemTables

    'All': {

        'Unused': UnusedTable,
        'Stat': CraftStatTable,
        'Resist': CraftResistTable,
    }
}

EnhancedLists = {  # CraftedLists

    'All': d2({

        'Unused': UnusedList,

        'Focus': t2((
            'All Spell Lines',
        )),

        'Skill': t2((
            'All Archery Skills',
            'All Dual Wield Skills',
            'All Magic Skills',
            'All Melee Weapon Skills',
            'Shield',
        )),

        'Stat': t2(DropStatList[0:4] + DropStatList[9:]),

        'Cap Increase': t2((
            'Strength',
            'Constitution',
            'Dexterity',
            'Quickness',
            'Acuity',
            'Hits',
            'Power',
            'Fatigue',
        )),

        'Other Bonus': t2((
            '% Power Pool',
            'Fatigue',
            'AF',
            'Archery Damage',
            'Melee Damage',
            'Spell Damage',
            'Duration of Spells',
            'Healing Effectiveness',
            'Stat Buff Effectiveness',
        )),

        'PvE Bonus': t2((
            'Defensive',
            'To Hit',
        )),

        'Charged Effect': t2((  # WHY ARE THESE HERE!?!
            'Dmg w/Resist Debuff (Fire)',
            'Dmg w/Resist Debuff (Cold)',
            'Dmg w/Resist Debuff (Matter)',
            'Dmg w/Resist Debuff (Spirit)',
        )),

        'Offensive Effect': t2((  # WHY ARE THESE HERE!?!
            'Direct Damage (Fire)',
            'Direct Damage (Cold)',
            'Direct Damage (Energy)',
            'Dmg w/Resist Debuff (Fire)',
            'Dmg w/Resist Debuff (Cold)',
            'Dmg w/Resist Debuff (Matter)',
            'Dmg w/Resist Debuff (Spirit)',
        )),
    }),
}

DropLists = {  # DropLists

    'All': {
        'Unused': UnusedList,
        'Resist': DropResistList,
        'Stat': DropStatList,
        'Cap Increase': CapList,
        'Mythical Cap Increase': MythicalCapList,
        'Mythical Bonus': MythicalBonusList,
        'PvE Bonus': PVEBonusList,
        'Other Bonus': OtherBonusList,
        # 'Charged Effect': otherEffectList,
        # 'Reactive Effect': otherEffectList,
        # 'Offensive Effect': otherEffectList,
        # 'Other Effect': otherEffectList,
    }
}

for realm in Realms:
    CraftTables[realm] = {}
    CraftTables[realm].update(CraftTables['All'])
    CraftLists[realm] = {}
    CraftLists[realm].update(CraftLists['All'])
    DropLists[realm] = {}
    DropLists[realm].update(DropLists['All'])

for realm in list(CraftTables.keys()):
    CraftTables[realm]['Focus'] = FocusTable[realm]
    CraftTables[realm]['Skill'] = SkillTable[realm]
    CraftTables[realm] = d2(CraftTables[realm])
    CraftLists[realm]['Focus'] = FocusList[realm]
    CraftLists[realm]['Skill'] = CraftSkillList[realm]
    CraftLists[realm] = d2(CraftLists[realm])
    DropLists[realm]['Focus'] = FocusList[realm]
    DropLists[realm]['Skill'] = DropSkillList[realm]
    DropLists[realm] = d2(DropLists[realm])

GemTables = d2(CraftTables)
GemLists = d2(CraftLists)
DropLists = d2(DropLists)

ValuesLists = d2({  # ValuesLists

    'Stat': d2({
        None: StatValues,
        'Hits': HitsValues,
        'Power': PowerValues,
    }),

    'Resist': ResistValues,
    'Focus': FocusValues,
    'Skill': SkillValues,
    # 'Charged Effect': chargedEffectValues,
    # 'Offensive Effect': offensiveEffectValues,
    # 'Reactive Effect': reactiveEffectValues,
    'Unused': UnusedValues,
})

# THIS IS A MESS
EnhancedValuesLists = d2({  # CraftedValuesLists
    'Unused': UnusedValues,
    'Focus': t2(('50',)),
    'Skill': t2(('3',)),
    'Stat': d2({
        None: t2(('15',)),
        'Hits': t2(('40',)),
    }),
    'Cap Increase': d2({
        None: t2(('5',)),
        'Hits': t2(('40',)),
    }),
    'PvE Bonus': t2(('5',)),
    'PvE Bonus': d2({
        None: t2(('5',)),
        'To Hit': t2(('3',)),
    }),
    'Other Bonus': d2({
        None: t2(('5',)),
        'AF': t2(('10',)),
        'Archery Damage': t2(('2',)),
        'Melee Damage': t2(('2',)),
        'Spell Damage': t2(('2',)),
    }),
    'Charged Effect': t2(("60",)),
    'Offensive Effect': t2(("60", "25", "20",)),
})

if __name__ == "__main__":
    pass
