from TupleTwo import *
from DictionaryTwo import *

__all__ = [
    'SlotList',
    'FocusSlotList',
    'CraftTypeList',
    'DamageTypeList',
    'DropTypeList',
    'FifthSlotTypeList',
    'SourceTypeList',
]

SlotList = d2({

    'Jewelery': t2((

        'Neck',
        'Cloak',
        'Jewel',
        'Belt',
        'Left Ring',
        'Right Ring',
        'Left Wrist',
        'Right Wrist',
    )),

    'Armor': t2((

        'Chest',
        'Arms',
        'Head',
        'Legs',
        'Hands',
        'Feet',
    )),

    'Weapons': t2((

        'Right Hand',
        'Left Hand',
        'Two-Handed',
        'Ranged',
        'Spare',
    )),

    'Mythical': t2((

        'Mythirian',
    ))
})

FocusSlotList = t2((
    'Two-Handed',
    'Spare',
))

CraftTypeList = t2((  # TypeList
    'Unused',
    'Stat',
    'Resist',
    'Focus',
    'Skill',
))

DropTypeList = t2((  # DropTypeList
    'Unused',
    'Stat',
    'Resist',
    'Focus',
    'Skill',
    'Cap Increase',
    'Mythical Cap Increase'
    'Mythical Bonus',
    'PvE Bonus',
    'Other Bonus',
    # 'Offensive Effect',
    # 'Reactive Effect',
    # 'Charged Effect',
    # 'Other Effect',
))

FifthSlotTypeList = t2((  # CraftedTypeList
    'Unused',
    'Focus',
    'Skill',
    'Stat',
    'Cap Increase',
    'PvE Bonus',
    'Other Bonus',
    # 'Charged Effect',
    # 'Offensive Effect',
))

DamageTypeList = d2({

    'Craft': t2((
        'Slash',
        'Thrust',
        'Crush',
        'Elemental',
    )),

    'Drop': t2((
        'Slash',
        'Thrust',
        'Crush',
        'Body',
        'Cold',
        'Heat',
        'Energy',
        'Matter',
        'Spirit',
    )),
})

SourceTypeList = d2({

    'Craft': t2((
        'Crafted',
    )),

    'Drop': t2((
        'Drop',
        'Quest',
        'Artifact',
        'Merchant',
    )),
})

if __name__ == "__main__":
    pass
