# HEADER PLACE HOLDER

from Character import *
from TupleTwo import *
from DictionaryTwo import *

__all__ = [
    'Cap',
    'CraftedTypeList',
    'CraftedEffectList',
    'CraftedEffectTable',
    'CraftedValuesList',
    'DropTypeList',
    'DropEffectList',
    'EnhancedTypeList',
    'EnhancedEffectList',
    'EnhancedValuesList',
    'GemMaterialsOrder',
    'GemTierNames',
    'ImbuePoints',
    'MythicalBonusCap',
    'OverchargeBasePercent',
    'OverchargeSkillBonus',
    'PVEBonusCap',
    'TOABonusCap',
]

UnusedList = t2()
UnusedTable = d2({})
UnusedValues = t2()

# =============================================== #
#            CRAFTING RELATED CONSTANTS           #
# =============================================== #

# GemSuffixNames = d2({
#     'Skill': '',
#     'Attribute': 'Essence Jewel',
#     'Resistance': 'Shielding Jewel',
#     'Hit Points': 'Essence Jewel',
#     'Power': 'Essence Jewel',
#     'Focus': '',
# })

GemTierNames = t2((
    'Raw',
    'Uncut',
    'Rough',
    'Flawed',
    'Imperfect',
    'Polished',
    'Faceted',
    'Precious',
    'Flawless',
    'Perfect',
))

GemLiquids = d2({
    'Fiery': 'Draconic Fire',
    'Earthen': 'Treant Blood',
    'Vapor': 'Swamp Fog',
    'Airy': 'Air Elemental Essence',
    'Heated': 'Heat From an Unearthly Pyre',
    'Icy': 'Frost From a Wasteland',
    'Watery': 'Leviathan Blood',
    'Dusty': 'Undead Ash and Holy Water',
    'Fire': 'Draconic Fire',
    'Earth': 'Treant Blood',
    'Vapor': 'Swamp Fog',
    'Air': 'Air Elemental Essence',
    'Heat': 'Heat From an Unearthly Pyre',
    'Ice': 'Frost From a Wasteland',
    'Water': 'Leviathan Blood',
    'Dust': 'Undead Ash and Holy Water',
    'Ashen': 'Undead Ash and Holy Water',
    'Vacuous': 'Swamp Fog',
    'Salt Crusted': 'Mystic Energy',
    'Steaming Spell': 'Swamp Fog',
    'Steaming Nature': 'Swamp Fog',
    'Steaming Fervor': 'Heat From an Unearthly Pyre',
    'Oozing': 'Treant Blood',
    'Mineral Encrusted': 'Heat From an Unearthly Pyre',
    'Lightning Charged': 'Leviathan Blood',
    'Molten Magma': 'Leviathan Blood',
    'Light': 'Sun Light',
    'Blood': 'Giant Blood',
    'Mystical': 'Mystic Energy',
    'Mystic': 'Mystic Energy',
    'Brilliant': ('Draconic Fire', 'Mystic Energy', 'Treant Blood'),
    'Finesse': ('Draconic Fire', 'Mystic Energy', 'Treant Blood'),
    'Ethereal Spell': 'Swamp Fog',
    'Phantasmal Spell': 'Leviathan Blood',
    'Spectral Spell': 'Draconic Fire',
    'Ethereal Arcane': 'Leviathan Blood',
    'Phantasmal Arcane': 'Draconic Fire',
    'Spectral Arcane': 'Air Elemental Essence',
    'Aberrant': 'Treant Blood',
    'Embracing': 'Frost From a Wasteland',
    'Shadowy': 'Swamp Fog',
    'Blighted Primal': 'Air Elemental Essence',
    'Blighted Rune': 'Undead Ash and Holy Water',
    'Valiant': 'Swamp Fog',
    'Unholy': 'Air Elemental Essence',
    'Glacial': 'Frost From a Wasteland',
    'Cinder': 'Draconic Fire',
    'Radiant': 'Sun Light',
    'Magnetic': 'Mystic Energy',
    'Clout': 'Giant Blood',
})

GemDusts = d2({
    'Essence Jewel': 'Essence of Life',
    'Shielding Jewel': 'Ground Draconic Scales',
    'Spell Stone': 'Ground Draconic Scales',
    'Sigil': 'Ground Draconic Scales',
    'Rune': 'Ground Draconic Scales',
    'Chaos Rune': 'Soot From Niflheim',
    'Battle Jewel': 'Bloodied Battlefield Dirt',
    'War Rune': 'Ground Giant Bone',
    'Primal Rune': 'Ground Vendo Bone',
    'Evocation Sigil': 'Ground Cave Crystal',
    'Fervor Sigil': 'Ground Blessed Undead Bone',
    'War Sigil': 'Ground Caer Stone',
    'Nature Spell Stone': 'Fairy Dust',
    'War Spell Stone': 'Unseelie Dust',
    'Arcane Spell Stone': 'Other Worldly Dust',
})

GemMaterialsOrder = {

    'Gems': (
        'Lo',
        'Um',
        'On',
        'Ee',
        'Pal',
        'Mon',
        'Ros',
        'Zo',
        'Kath',
        'Ra',
    ),

    'Liquids': (
        'Air Elemental Essence',
        'Draconic Fire',
        'Frost From a Wasteland',
        'Giant Blood',
        'Heat From an Unearthly Pyre',
        'Leviathan Blood',
        'Mystic Energy',
        'Sun Light',
        'Swamp Fog',
        'Treant Blood',
        'Undead Ash and Holy Water',),

    'Dusts': (
        'Bloodied Battlefield Dirt',
        'Essence of Life','Fairy Dust',
        'Ground Blessed Undead Bone',
        'Ground Caer Stone',
        'Ground Cave Crystal',
        'Ground Draconic Scales',
        'Ground Giant Bone',
        'Ground Vendo Bone',
        'Other Worldly Dust',
        'Soot From Niflheim',
        'Unseelie Dust',
    ),
}

OverchargeBasePercent = (-0, -10, -20, -30, -50, -70)

OverchargeSkillBonus = (-45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50,)

ImbuePoints = (
    1, 2, 2, 3, 4, 4, 5, 5, 6, 7,
    7, 8, 9, 9, 10, 10, 11, 12, 12, 13,
    13, 14, 15, 15, 16, 16, 17, 18, 18, 19,
    20, 20, 21, 21, 22, 23, 23, 24, 24, 25,
    26, 26, 27, 27, 28, 29, 29, 30, 31, 31, 32,
)

# =============================================== #
#             STAT RELATED CONSTANTS              #
# =============================================== #

AttributeTableOrdered = (
    ('Strength', 'Fiery',),
    ('Constitution', 'Earthen',),
    ('Dexterity', 'Vapor',),
    ('Quickness', 'Airy',),
    ('Intelligence', 'Dusty',),
    ('Piety', 'Watery',),
    ('Empathy', 'Heated',),
    ('Charisma', 'Icy',),
    ('Hit Points', 'Blood',),
    ('Power', 'Mystical',),
)

suffix = 'Essence Jewel'
AttributeTable = dict(AttributeTableOrdered)

for (key, value) in list(AttributeTable.items()):
    AttributeTable[key] = (value, suffix, GemDusts[suffix], GemLiquids[value],)

CraftedAttributeList = t2([x[0] for x in AttributeTableOrdered])
CraftedAttributeTable = d2(AttributeTable)
DropAttributeList = t2(CraftedAttributeList + ('Acuity',))
DropAttributeTable = dict().fromkeys(DropAttributeList)

del AttributeTableOrdered
del AttributeTable

AttributeValues = t2((
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

# =============================================== #
#            RESIST RELATED CONSTANTS             #
# =============================================== #

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

CraftedResistTable = d2(ResistTable)
CraftedResistList = t2([x[0] for x in ResistTableOrdered])
DropResistList = t2(CraftedResistList + ('Essence',))
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

# =============================================== #
#             FOCUS RELATED CONSTANTS             #
# =============================================== #

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

# =============================================== #
#             SKILL RELATED CONSTANTS             #
# =============================================== #

SkillTable = {

    'Albion': {

        'All Magic Skills': ('Finesse', 'Fervor Sigil',),
        'All Melee Weapon Skills': ('Finesse', 'War Sigil',),
        'Archery': ('Airy', 'War Sigil',),
        'Aura Manipulation': ('Radiant', 'Fervor Sigil',),
        'Body Magic': ('Heated', 'Evocation Sigil',),
        'Chants': ('Earthen', 'Fervor Sigil',),
        'Cold Magic': ('Icy', 'Evocation Sigil',),
        'Critical Strike': ('Heated', 'Battle Jewel',),
        'Crossbow': ('Vapor', 'War Sigil',),
        'Crush': ('Fiery', 'War Sigil',),
        'Death Servant': ('Ashen', 'Fervor Sigil',),
        'Deathsight': ('Vacuous', 'Fervor Sigil',),
        'Dual Wield': ('Icy', 'War Sigil',),
        'Earth Magic': ('Earthen', 'Evocation Sigil',),
        'Enhancement': ('Airy', 'Fervor Sigil',),
        'Envenom': ('Dusty', 'Battle Jewel',),
        'Flexible': ('Molten Magma', 'War Sigil',),
        'Fire Magic': ('Fiery', 'Evocation Sigil',),
        'Fist Wraps': ('Glacial', 'War Sigil',),
        'Instruments': ('Vapor', 'Fervor Sigil',),
        'Magnetism': ('Magnetic', 'Fervor Sigil',),
        'Matter Magic': ('Dusty', 'Evocation Sigil',),
        'Mauler Staff': ('Cinder', 'War Sigil',),
        'Mind Magic': ('Watery', 'Evocation Sigil',),
        'Painworking': ('Salt Crusted', 'Fervor Sigil',),
        'Parry': ('Vapor', 'Battle Jewel',),
        'Polearm': ('Earthen', 'War Sigil',),
        'Power Strikes': ('Clout', 'Fervor Sigil',),
        'Rejuvenation': ('Watery', 'Fervor Sigil',),
        'Shield': ('Fiery', 'Battle Jewel',),
        'Slash': ('Watery', 'War Sigil',),
        'Smite': ('Fiery', 'Fervor Sigil',),
        'Soulrending': ('Steaming', 'Fervor Sigil',),
        'Spirit Magic': ('Vapor', 'Evocation Sigil',),
        'Staff': ('Earthen', 'Battle Jewel',),
        'Stealth': ('Airy', 'Battle Jewel',),
        'Thrust': ('Dusty', 'War Sigil',),
        'Two-Handed': ('Heated', 'War Sigil',),
        'Wind Magic': ('Airy', 'Evocation Sigil',),
    },

    'Hibernia': {

        'All Magic Skills': ('Finesse', 'Nature Spell Stone',),
        'All Melee Weapon Skills': ('Finesse', 'War Spell Stone',),
        'Arboreal Path': ('Steaming', 'Nature Spell Stone',),
        'Archery': ('Airy', 'War Spell Stone',),
        'Aura Manipulation': ('Radiant', 'Nature Spell Stone'),
        'Blades': ('Watery', 'War Spell Stone',),
        'Blunt': ('Fiery', 'War Spell Stone',),
        'Celtic Dual': ('Icy', 'War Spell Stone',),
        'Celtic Spear': ('Earthen', 'War Spell Stone',),
        'Creeping Path': ('Oozing', 'Nature Spell Stone',),
        'Critical Strike': ('Heated', 'Battle Jewel',),
        'Dementia': ('Aberrant', 'Arcane Spell Stone',),
        'Enchantments': ('Vapor', 'Arcane Spell Stone',),
        'Envenom': ('Dusty', 'Battle Jewel',),
        'Ethereal Shriek': ('Ethereal', 'Arcane Spell Stone',),
        'Fist Wraps': ('Glacial', 'War Spell Stone'),
        'Large Weaponry': ('Heated', 'War Spell Stone',),
        'Light': ('Fiery', 'Arcane Spell Stone',),
        'Magnetism': ('Magnetic', 'Nature Spell Stone'),
        'Mana': ('Watery', 'Arcane Spell Stone',),
        'Mauler Staff': ('Cinder', 'War Spell Stone'),
        'Mentalism': ('Earthen', 'Arcane Spell Stone',),
        'Music': ('Airy', 'Nature Spell Stone',),
        'Nature': ('Earthen', 'Nature Spell Stone',),
        'Nurture': ('Fiery', 'Nature Spell Stone',),
        'Parry': ('Vapor', 'Battle Jewel',),
        'Phantasmal Wail': ('Phantasmal', 'Arcane Spell Stone',),
        'Piercing': ('Dusty', 'War Spell Stone',),
        'Power Strikes': ('Clout', 'Nature Spell Stone'),
        'Regrowth': ('Watery', 'Nature Spell Stone',),
        'Scythe': ('Light', 'War Spell Stone',),
        'Shadow Mastery': ('Shadowy', 'Arcane Spell Stone',),
        'Shield': ('Fiery', 'Battle Jewel',),
        'Spectral Guard': ('Spectral', 'Arcane Spell Stone',),
        'Staff': ('Earthen', 'Battle Jewel',),
        'Stealth': ('Airy', 'Battle Jewel',),
        'Valor': ('Airy', 'Arcane Spell Stone',),
        'Vampiiric Embrace': ('Embracing', 'Arcane Spell Stone',),
        'Verdant Path': ('Mineral Encrusted', 'Nature Spell Stone',),
        'Void': ('Icy', 'Arcane Spell Stone',),
    },

    'Midgard': {

        'All Magic Skills': ('Finesse', 'Primal Rune',),
        'All Melee Weapon Skills': ('Finesse', 'War Rune',),
        'Archery': ('Airy', 'War Rune',),
        'Augmentation': ('Airy', 'Chaos Rune',),
        'Aura Manipulation': ('Radiant', 'Primal Rune',),
        'Axe': ('Earthen', 'War Rune',),
        'Battlesongs': ('Airy', 'Primal Rune',),
        'Beastcraft': ('Earthen', 'Primal Rune',),
        'Bone Army': ('Ashen', 'Primal Rune',),
        'Cave Magic': ('Fiery', 'Chaos Rune',),
        'Critical Strike': ('Heated', 'Battle Jewel',),
        'Cursing': ('Blighted', 'Primal Rune',),
        'Darkness': ('Icy', 'Chaos Rune',),
        'Envenom': ('Dusty', 'Battle Jewel',),
        'Fist Wraps': ('Glacial', 'War Rune',),
        'Hammer': ('Fiery', 'War Rune',),
        'Hand To Hand': ('Lightning Charged', 'War Rune',),
        'Hexing': ('Unholy', 'Primal Rune',),
        'Left Axe': ('Icy', 'War Rune',),
        'Magnetism': ('Magnetic', 'Primal Rune',),
        'Mauler Staff': ('Cinder', 'War Rune',),
        'Mending': ('Watery', 'Chaos Rune',),
        'Odin\'s Will': ('Valiant', 'Primal Rune',),
        'Parry': ('Vapor', 'Battle Jewel',),
        'Power Strikes': ('Clout', 'Primal Rune',),
        'Runecarving': ('Heated', 'Chaos Rune',),
        'Shield': ('Fiery', 'Battle Jewel',),
        'Spear': ('Heated', 'War Rune',),
        'Staff': ('Earthen', 'Battle Jewel',),
        'Stealth': ('Airy', 'Battle Jewel',),
        'Stormcalling': ('Fiery', 'Primal Rune',),
        'Summoning': ('Vapor', 'Chaos Rune',),
        'Suppression': ('Dusty', 'Chaos Rune',),
        'Sword': ('Watery', 'War Rune',),
        'Thrown Weapons': ('Vapor', 'War Rune',),

    }, 'All': {}}

for realm in Realms:
    for (key, value) in list(SkillTable[realm].items()):
        if value[0] in GemLiquids:
            liquid = GemLiquids[value[0]]
        else:
            liquid = GemLiquids[value[0] + " " + value[1].split()[0]]
        SkillTable[realm][key] = (value[0], value[1], GemDusts[value[1]], liquid,)
    SkillTable[realm] = d2(SkillTable[realm])
    SkillTable['All'].update(SkillTable[realm])
SkillTable['All'] = d2(SkillTable['All'])
SkillTable = d2(SkillTable)

CraftedSkillList = {}
DropSkillList = {}
for realm in list(SkillTable.keys()):
    skills = list(SkillTable[realm].keys())
    skills.sort()
    CraftedSkillList[realm] = t2(skills)
    skills.insert(2, 'All Archery Skills')
    skills.insert(3, 'All Dual Wield Skills')
    if realm == 'Midgard':  # ADD NON-CRAFTABLE 'Witchcraft' SKILL
        skills.append('Witchcraft')
    DropSkillList[realm] = t2(skills)
CraftedSkillList = d2(CraftedSkillList)
DropSkillList = d2(DropSkillList)

SkillValues = t2((
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
))

# =============================================== #
#              CAP RELATED CONSTANTS              #
# =============================================== #
#                                                 #
#    CALCULATED AS % OF LEVEL + CONSTANT          #
#    E.G. [.25,  1] IS THE LEVEL / 4 + 1          #
#         [  0, 10] IS A FIXED VALUE OF 10        #
#         [  4,  0] IS THE LEVEL * 4              #
#                                                 #
# =============================================== #

AttributeCapList = t2((
    'Strength',
    'Constitution',
    'Dexterity',
    'Quickness',
    'Intelligence',
    'Piety',
    'Charisma',
    'Empathy',
    'Hit Points',
    'Power',
    'Acuity',
    'Fatigue',
))

MythicalStatCapList = t2((
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

MythicalResistCapList = t2((
    'Body',
    'Cold',
    'Heat',
    'Energy',
    'Matter',
    'Spirit',
    'Crush',
    'Thrust',
    'Slash',
    'Essence',
))

Cap = {
    'Skill': (0.20, 1),
    'Attribute': (1.50, 0),
    'Resistance': (0.50, 1),
    'Hit Points': (4.00, 0),
    'Power': (0.50, 1),
    'Focus': (1.00, 0),
}

TOABonusCap = {
    'Attribute Cap': (0.50, 1),
    'Hit Points Cap': (8.00, 0),
    'Power Cap': (1.00, 0),
    '% Power Pool': (0.50, 0),
    '% Power Pool Cap': (1.00, 0),
    'Armor Factor': (1.00, 0),
    'Fatigue': (0.50, 0),
    'Fatigue Cap': (.50, 0),
    'Spell Duration': (.50, 0),
    'Healing Effectiveness': (.50, 0),
    'Enhancement Effectiveness': (.50, 0),
    'Debuff Effectiveness': (.50, 0),
    'ToA Bonus': (0.20, 0),
    'None': (0.00, 0),
}

PVEBonusCap = {
    'Death Exp. Loss Reduction': (1.00, 0),
    'PvE Bonus': (0.20, 0),
}

MythicalBonusCap = {
    'Stat Cap': (1, 2),
    'Resist Cap': (0, 15),
    'Endurance Regen': (1.00, 0),
    'Health Regen': (1.00, 0),
    'Power Regen': (1.00, 0),
    'CC Duration Decrease': (1.00, 0),
    'DPS': (.20, 0),
    'Mythical Bonus': (1.00, 0),
}

# =============================================== #
#             BONUS RELATED CONSTANTS             #
# =============================================== #

TOABonusList = t2((
    '% Power Pool',
    'Armor Factor',
    'Conversion',
    'Fatigue',
    'Melee Combat Speed',
    'Melee Damage',
    'Style Damage',
    'Casting Speed',
    'Magic Damage',
    'Spell Pierce',
    'Spell Range',
    'Spell Duration',
    'Arcane Siphone',
    'Healing Effectiveness',
    'Enhancement Effectiveness',
    'Debuff Effectiveness',
    'Health Regeneration',
    'Power Regeneration',
))

PVEBonusList = t2((
    'Block',
    'Evade',
    'Parry',
    'Defensive Bonus',
    'To Hit Bonus',
    'Reactionary Style Damage',
    'Pierce Ablative',
    'Concentration',
    'Bladeturn Reinforcement',
    'Style Cost Reduction',
    'Spell Power Cost Reduction',
    'Death Exp. Loss Reduction',
    'Neg. Effect Duration Reduction',
))

MythicalBonusList = t2((
    'Coin',
    'Bounty Points',
    'Realm Points',
    'Encumbrance',
    'Safe Fall',
    'Endurance Regen',
    'Health Regen',
    'Power Regen',
    'Spell Increase',
    'Physical Defense',
    'Seige Speed',
    'Seige Damage Ablative',
    'CC Duration Decrease',
    'DPS',
    'Block',
    'Evade',
    'Parry',
))

# =============================================== #
#          EFFECT TYPE RELATED CONSTANTS          #
# =============================================== #

CraftedTypeList = t2((
    'Unused',
    'Skill',
    'Attribute',
    'Resistance',
    'Focus',
))

EnhancedTypeList = t2((
    'Unused',
    'Skill',
    'Attribute',
    'Attribute Cap',
    'Focus',
    'ToA Bonus',
    'PvE Bonus',
))

DropTypeList = t2((
    'Unused',
    'Skill',
    'Attribute',
    'Attribute Cap',
    'Resistance',
    'Focus',
    'ToA Bonus',
    'PvE Bonus',
    'Mythical Stat Cap',
    'Mythical Resist Cap',
    'Mythical Stat & Cap',
    'Mythical Resist & Cap',
    'Mythical Bonus',
))

# =============================================== #
#             EFFECT RELATED CONSTANTS            #
# =============================================== #

CraftedEffectTable = {

    'All': {
        'Unused': UnusedTable,
        'Attribute': CraftedAttributeTable,
        'Resistance': CraftedResistTable,
    }}

CraftedEffectList = {

    'All': {
        'Unused': UnusedList,
        'Attribute': CraftedAttributeList,
        'Resistance': CraftedResistList,
    }}

EnhancedEffectList = {

    'All': {

        'Unused': UnusedList,

        'Skill': (
            'All Archery Skills',
            'All Dual Wield Skills',
            'All Magic Skills',
            'All Melee Weapon Skills',
            'Shield',
        ),

        'Attribute': (
            'Strength',
            'Constitution',
            'Dexterity',
            'Quickness',
            'Acuity',
            'Hit Points',
        ),

        'Attribute Cap': (
            'Strength',
            'Constitution',
            'Dexterity',
            'Quickness',
            'Acuity',
            'Hit Points',
            'Power',
            'Fatigue',
        ),

        'Focus': (
            'All Spell Lines',
        ),

        'ToA Bonus': (
            '% Power Pool',
            'Armor Factor',
            'Fatigue',
            'Melee Damage',
            'Magic Damage',
            'Spell Duration',
            'Healing Effectiveness',
            'Enhancement Effectiveness',
        ),

        'PvE Bonus': (
            'Defensive Bonus',
            'To Hit Bonus',
         ),
    }}

DropEffectList = {

    'All': {
        'Unused': UnusedList,
        'Resistance': DropResistList,
        'Attribute': DropAttributeList,
        'Attribute Cap': AttributeCapList,
        'ToA Bonus': TOABonusList,
        'PvE Bonus': PVEBonusList,
        'Mythical Stat Cap': MythicalStatCapList,
        'Mythical Resist Cap': MythicalResistCapList,
        'Mythical Stat & Cap': MythicalStatCapList,
        'Mythical Resist & Cap': MythicalResistCapList,
        'Mythical Bonus': MythicalBonusList,
    }}

for realm in Realms:
    CraftedEffectTable[realm] = {}
    CraftedEffectTable[realm].update(CraftedEffectTable['All'])
    CraftedEffectList[realm] = {}
    CraftedEffectList[realm].update(CraftedEffectList['All'])
    DropEffectList[realm] = {}
    DropEffectList[realm].update(DropEffectList['All'])

for realm in list(CraftedEffectTable.keys()):
    CraftedEffectTable[realm]['Focus'] = FocusTable[realm]
    CraftedEffectTable[realm]['Skill'] = SkillTable[realm]
    CraftedEffectTable[realm] = d2(CraftedEffectTable[realm])
    CraftedEffectList[realm]['Focus'] = FocusList[realm]
    CraftedEffectList[realm]['Skill'] = CraftedSkillList[realm]
    CraftedEffectList[realm] = d2(CraftedEffectList[realm])
    DropEffectList[realm]['Focus'] = FocusList[realm]
    DropEffectList[realm]['Skill'] = DropSkillList[realm]
    DropEffectList[realm] = d2(DropEffectList[realm])

CraftedEffectTable = d2(CraftedEffectTable)
CraftedEffectList = d2(CraftedEffectList)
DropEffectList = d2(DropEffectList)

# =============================================== #
#          EFFECT VALUE RELATED CONSTANTS         #
# =============================================== #

CraftedValuesList = d2({

    'Unused': UnusedValues,
    'Skill': SkillValues,

    'Attribute': d2({
        'Strength': AttributeValues,
        'Constitution': AttributeValues,
        'Dexterity': AttributeValues,
        'Quickness': AttributeValues,
        'Intelligence': AttributeValues,
        'Piety': AttributeValues,
        'Empathy': AttributeValues,
        'Charisma': AttributeValues,
        'Hit Points': HitsValues,
        'Power': PowerValues,
    }),

    'Resistance': ResistValues,
    'Focus': FocusValues,
})

EnhancedValuesList = {

    'Unused': UnusedValues,
    'Skill': ('3',),

    'Attribute': {
        'Strength': ('15',),
        'Constitution': ('15',),
        'Dexterity': ('15',),
        'Quickness': ('15',),
        'Acuity': ('15',),
        'Hit Points': ('40',),
    },

    'Attribute Cap': {
        'Strength': ('5',),
        'Constitution': ('5',),
        'Dexterity': ('5',),
        'Quickness': ('5',),
        'Acuity': ('5',),
        'Hit Points': ('40',),
        'Power': ('5',),
        'Fatigue': ('5',),
    },

    'Focus': ('50',),

    'PvE Bonus': {
        'Defensive Bonus': ('5',),
        'To Hit Bonus': ('3',),
    },

    'ToA Bonus': {
        '% Power Pool': ('5',),
        'Armor Factor': ('10',),
        'Fatigue': ('5',),
        'Archery Damage': ('2',),
        'Melee Damage': ('2',),
        'Magic Damage': ('2',),
        'Spell Duration': ('5',),
        'Healing Effectiveness': ('5',),
        'Enhancement Effectiveness': ('5',),
    }}

# =============================================== #
#             GAME RELATED CONSTANTS              #
# =============================================== #

GemHotkeyValues = d2({

    'Albion': d2({

        'Fiery Essence Jewel': 0,
        'Earthen Essence Jewel': 2,
        'Vapor Essence Jewel': 4,
        'Airy Essence Jewel': 6,
        'Watery Essence Jewel': 8,
        'Heated Essence Jewel': 10,
        'Dusty Essence Jewel': 12,
        'Icy Essence Jewel': 14,
        'Earthen Shielding Jewel': 16,
        'Icy Shielding Jewel': 18,
        'Heated Shielding Jewel': 20,
        'Light Shielding Jewel': 22,
        'Airy Shielding Jewel': 24,
        'Vapor Shielding Jewel': 26,
        'Dusty Shielding Jewel': 28,
        'Fiery Shielding Jewel': 30,
        'Watery Shielding Jewel': 32,
        'Vapor Battle Jewel': 34,
        'Fiery Battle Jewel': 36,
        'Earthen Battle Jewel': 38,
        'Airy Battle Jewel': 40,
        'Dusty Battle Jewel': 42,
        'Heated Battle Jewel': 44,
        'Watery War Sigil': 46,
        'Fiery War Sigil': 48,
        'Dusty War Sigil': 50,
        'Heated War Sigil': 52,
        'Earthen War Sigil': 54,
        'Airy War Sigil': 56,
        'Vapor War Sigil': 58,
        'Icy War Sigil': 60,
        'Fiery Fervor Sigil': 62,
        'Airy Fervor Sigil': 64,
        'Watery Fervor Sigil': 66,
        'Earthen Fervor Sigil': 68,
        'Vapor Fervor Sigil': 70,
        'Earthen Evocation Sigil': 72,
        'Icy Evocation Sigil': 74,
        'Fiery Evocation Sigil': 76,
        'Airy Evocation Sigil': 78,
        'Heated Evocation Sigil': 80,
        'Dusty Evocation Sigil': 82,
        'Vapor Evocation Sigil': 84,
        'Watery Evocation Sigil': 86,
        'Blood Essence Jewel': 88,
        'Mystical Essence Jewel': 90,
        'Earth Sigil': 92,
        'Ice Sigil': 94,
        'Fire Sigil': 96,
        'Air Sigil': 98,
        'Heat Sigil': 100,
        'Dust Sigil': 102,
        'Vapor Sigil': 104,
        'Water Sigil': 106,
        'Molten Magma War Sigil': 108,
        'Vacuous Fervor Sigil': 110,
        'Salt Crusted Fervor Sigil': 112,
        'Ashen Fervor Sigil': 114,
        'Steaming Fervor Sigil': 116,
        'Vacuous Sigil': 118,
        'Salt Crusted Sigil': 120,
        'Ashen Sigil': 122,
        'Brilliant Sigil': 124,
        'Finesse War Sigil': 126,
        'Finesse Fervor Sigil': 128,
        'Glacial War Sigil': 130,
        'Cinder War Sigil': 132,
        'Radiant Fervor Sigil': 134,
        'Magnetic Fervor Sigil': 136,
        'Clout Fervor Sigil': 138,
    }),

    'Hibernia': d2({

        'Fiery Essence Jewel': 0,
        'Earthen Essence Jewel': 2,
        'Vapor Essence Jewel': 4,
        'Airy Essence Jewel': 6,
        'Watery Essence Jewel': 8,
        'Heated Essence Jewel': 10,
        'Dusty Essence Jewel': 12,
        'Icy Essence Jewel': 14,
        'Earthen Shielding Jewel': 16,
        'Icy Shielding Jewel': 18,
        'Heated Shielding Jewel': 20,
        'Light Shielding Jewel': 22,
        'Airy Shielding Jewel': 24,
        'Vapor Shielding Jewel': 26,
        'Dusty Shielding Jewel': 28,
        'Fiery Shielding Jewel': 30,
        'Watery Shielding Jewel': 32,
        'Vapor Battle Jewel': 34,
        'Fiery Battle Jewel': 36,
        'Earthen Battle Jewel': 38,
        'Airy Battle Jewel': 40,
        'Dusty Battle Jewel': 42,
        'Heated Battle Jewel': 44,
        'Watery War Spell Stone': 46,
        'Fiery War Spell Stone': 48,
        'Dusty War Spell Stone': 50,
        'Heated War Spell Stone': 52,
        'Earthen War Spell Stone': 54,
        'Icy War Spell Stone': 56,
        'Airy War Spell Stone': 58,
        'Fiery Nature Spell Stone': 60,
        'Watery Nature Spell Stone': 62,
        'Earthen Nature Spell Stone': 64,
        'Airy Nature Spell Stone': 66,
        'Airy Arcane Spell Stone': 68,
        'Fiery Arcane Spell Stone': 70,
        'Watery Arcane Spell Stone': 72,
        'Vapor Arcane Spell Stone': 74,
        'Icy Arcane Spell Stone': 76,
        'Earthen Arcane Spell Stone': 78,
        'Blood Essence Jewel': 80,
        'Mystical Essence Jewel': 82,
        'Fire Spell Stone': 84,
        'Water Spell Stone': 86,
        'Vapor Spell Stone': 88,
        'Ice Spell Stone': 90,
        'Earth Spell Stone': 92,
        'Light War Spell Stone': 94,
        'Steaming Nature Spell Stone': 96,
        'Oozing Nature Spell Stone': 98,
        'Mineral Encrusted Nature Spell Stone': 100,
        'Steaming Spell Stone': 102,
        'Oozing Spell Stone': 104,
        'Mineral Encrusted Spell Stone': 106,
        'Spectral Spell Stone': 108,
        'Phantasmal Spell Stone': 110,
        'Ethereal Spell Stone': 112,
        'Spectral Arcane Spell Stone': 114,
        'Phantasmal Arcane Spell Stone': 116,
        'Ethereal Arcane Spell Stone': 118,
        'Shadowy Arcane Spell Stone': 120,
        'Embracing Arcane Spell Stone': 122,
        'Aberrant Arcane Spell Stone': 124,
        'Brilliant Spell Stone': 126,
        'Finesse War Spell Stone': 128,
        'Finesse Nature Spell Stone': 130,
        'Glacial War Spell Stone': 132,
        'Cinder War Spell Stone': 134,
        'Radiant Nature Spell Stone': 136,
        'Magnetic Nature Spell Stone': 138,
        'Clout Nature Spell Stone': 140,
    }),

    'Midgard': d2({

        'Fiery Essence Jewel': 0,
        'Earthen Essence Jewel': 2,
        'Vapor Essence Jewel': 4,
        'Airy Essence Jewel': 6,
        'Watery Essence Jewel': 8,
        'Heated Essence Jewel': 10,
        'Dusty Essence Jewel': 12,
        'Icy Essence Jewel': 14,
        'Earthen Shielding Jewel': 16,
        'Icy Shielding Jewel': 18,
        'Heated Shielding Jewel': 20,
        'Light Shielding Jewel': 22,
        'Airy Shielding Jewel': 24,
        'Vapor Shielding Jewel': 26,
        'Dusty Shielding Jewel': 28,
        'Fiery Shielding Jewel': 30,
        'Watery Shielding Jewel': 32,
        'Vapor Battle Jewel': 34,
        'Fiery Battle Jewel': 36,
        'Earthen Battle Jewel': 38,
        'Airy Battle Jewel': 40,
        'Dusty Battle Jewel': 42,
        'Heated Battle Jewel': 44,
        'Watery War Rune': 46,
        'Fiery War Rune': 48,
        'Earthen War Rune': 50,
        'Heated War Rune': 52,
        'Airy War Rune': 54,
        'Vapor War Rune': 56,
        'Icy War Rune': 58,
        'Earthen Primal Rune': 60,
        'Airy Primal Rune': 62,
        'Fiery Primal Rune': 64,
        'Icy Chaos Rune': 66,
        'Dusty Chaos Rune': 68,
        'Heated Chaos Rune': 70,
        'Vapor Chaos Rune': 72,
        'Watery Chaos Rune': 74,
        'Airy Chaos Rune': 76,
        'Fiery Chaos Rune': 78,
        'Blood Essence Jewel': 82,
        'Mystical Essence Jewel': 84,
        'Ice Rune': 86,
        'Dust Rune': 88,
        'Heat Rune': 90,
        'Vapor Rune': 92,
        'Lightning Charged War Rune': 94,
        'Ashen Primal Rune': 96,
        'Ashen Rune': 98,
        'Blighted Rune': 100,
        'Valiant Primal Rune': 104,
        'Blighted Primal Rune': 106,
        'Unholy Primal Rune': 108,
        'Brilliant Rune': 110,
        'Finesse War Rune': 112,
        'Finesse Primal Rune': 114,
        'Glacial War Rune': 116,
        'Cinder War Rune': 118,
        'Radiant Primal Rune': 120,
        'Magnetic Primal Rune': 122,
        'Clout Primal Rune': 124,
    }),
})

# SERVER CODES (*.IGN)
ServerIgnCodes = d2({
    'Pendragon': '74',
    'Gaheris': '95',
    'Ywain': '143',
})

# SERVER CODES (*.INI)
ServerCodes = d2({
    '5': 'Pendragon',
    '23': 'Gaheris',
    '41': 'Ywain-1',
    '49': 'Ywain-2',
    '50': 'Ywain-3',
    '51': 'Ywain-4',
    '52': 'Ywain-5',
    '53': 'Ywain-6',
    '54': 'Ywain-7',
    '55': 'Ywain-8',
    '56': 'Ywain-9',
    '57': 'Ywain-10',
})

if __name__ == "__main__":
    pass
