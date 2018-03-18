# HEADER PLACE HOLDER

from Character import Realms

__all__ = [
    'Cap',
    'CraftedTypeList',
    'CraftedEffectList',
    'CraftedValuesList',
    'DropTypeList',
    'DropEffectList',
    'EnhancedTypeList',
    'EnhancedEffectList',
    'EnhancedValuesList',
    'GemMaterial',
    'GemMaterialOrder',
    'GemTierName',
    'ImbuePoints',
    'MythicalBonusCap',
    'OverchargeBasePercent',
    'OverchargeSkillBonus',
    'PVEBonusCap',
    'TOABonusCap',
]

UnusedList = ()
UnusedValues = ()

# =============================================== #
#             SKILL RELATED CONSTANTS             #
# =============================================== #

CraftedSkillList = {

    'All': set(),

    'Albion': (
        'All Magic Skills',
        'All Melee Weapon Skills',
        'Archery',
        'Aura Manipulation',
        'Body Magic',
        'Chants',
        'Cold Magic',
        'Critical Strike',
        'Crossbow',
        'Crush',
        'Death Servant',
        'Deathsight',
        'Dual Wield',
        'Earth Magic',
        'Enhancement',
        'Envenom',
        'Flexible',
        'Fire Magic',
        'Fist Wraps',
        'Instruments',
        'Magnetism',
        'Matter Magic',
        'Mauler Staff',
        'Mind Magic',
        'Painworking',
        'Parry',
        'Polearm',
        'Power Strikes',
        'Rejuvenation',
        'Shield',
        'Slash',
        'Smite',
        'Soulrending',
        'Spirit Magic',
        'Staff',
        'Stealth',
        'Thrust',
        'Two-Handed',
        'Wind Magic',
    ),

    'Hibernia': (
        'All Magic Skills',
        'All Melee Weapon Skills',
        'Arboreal Path',
        'Archery',
        'Aura Manipulation',
        'Blades',
        'Blunt',
        'Celtic Dual',
        'Celtic Spear',
        'Creeping Path',
        'Critical Strike',
        'Dementia',
        'Enchantments',
        'Envenom',
        'Ethereal Shriek',
        'Fist Wraps',
        'Large Weaponry',
        'Light',
        'Magnetism',
        'Mana',
        'Mauler Staff',
        'Mentalism',
        'Music',
        'Nature',
        'Nurture',
        'Parry',
        'Phantasmal Wail',
        'Piercing',
        'Power Strikes',
        'Regrowth',
        'Scythe',
        'Shadow Mastery',
        'Shield',
        'Spectral Guard',
        'Staff',
        'Stealth',
        'Valor',
        'Vampiiric Embrace',
        'Verdant Path',
        'Void',
    ),

    'Midgard': (
        'All Magic Skills',
        'All Melee Weapon Skills',
        'Archery',
        'Augmentation',
        'Aura Manipulation',
        'Axe',
        'Battlesongs',
        'Beastcraft',
        'Bone Army',
        'Cave Magic',
        'Critical Strike',
        'Cursing',
        'Darkness',
        'Envenom',
        'Fist Wraps',
        'Hammer',
        'Hand To Hand',
        'Hexing',
        'Left Axe',
        'Magnetism',
        'Mauler Staff',
        'Mending',
        'Odin\'s Will',
        'Parry',
        'Power Strikes',
        'Runecarving',
        'Shield',
        'Spear',
        'Staff',
        'Stealth',
        'Stormcalling',
        'Summoning',
        'Suppression',
        'Sword',
        'Thrown Weapons',
    ),
}

DropSkillList = {

    'All': set(),

    'Albion': (
        'All Archery Skills',
        'All Dual Wield Skills',
        'All Magic Skills',
        'All Melee Weapon Skills',
        'Archery',
        'Aura Manipulation',
        'Body Magic',
        'Chants',
        'Cold Magic',
        'Critical Strike',
        'Crossbow',
        'Crush',
        'Death Servant',
        'Deathsight',
        'Dual Wield',
        'Earth Magic',
        'Enhancement',
        'Envenom',
        'Flexible',
        'Fire Magic',
        'Fist Wraps',
        'Instruments',
        'Magnetism',
        'Matter Magic',
        'Mauler Staff',
        'Mind Magic',
        'Painworking',
        'Parry',
        'Polearm',
        'Power Strikes',
        'Rejuvenation',
        'Shield',
        'Slash',
        'Smite',
        'Soulrending',
        'Spirit Magic',
        'Staff',
        'Stealth',
        'Thrust',
        'Two-Handed',
        'Wind Magic',
    ),

    'Hibernia': (
        'All Archery Skills',
        'All Dual Wield Skills',
        'All Magic Skills',
        'All Melee Weapon Skills',
        'Arboreal Path',
        'Archery',
        'Aura Manipulation',
        'Blades',
        'Blunt',
        'Celtic Dual',
        'Celtic Spear',
        'Creeping Path',
        'Critical Strike',
        'Dementia',
        'Enchantments',
        'Envenom',
        'Ethereal Shriek',
        'Fist Wraps',
        'Large Weaponry',
        'Light',
        'Magnetism',
        'Mana',
        'Mauler Staff',
        'Mentalism',
        'Music',
        'Nature',
        'Nurture',
        'Parry',
        'Phantasmal Wail',
        'Piercing',
        'Power Strikes',
        'Regrowth',
        'Scythe',
        'Shadow Mastery',
        'Shield',
        'Spectral Guard',
        'Staff',
        'Stealth',
        'Valor',
        'Vampiiric Embrace',
        'Verdant Path',
        'Void',
    ),

    'Midgard': (
        'All Archery Skills',
        'All Dual Wield Skills',
        'All Magic Skills',
        'All Melee Weapon Skills',
        'Archery',
        'Augmentation',
        'Aura Manipulation',
        'Axe',
        'Battlesongs',
        'Beastcraft',
        'Bone Army',
        'Cave Magic',
        'Critical Strike',
        'Cursing',
        'Darkness',
        'Envenom',
        'Fist Wraps',
        'Hammer',
        'Hand To Hand',
        'Hexing',
        'Left Axe',
        'Magnetism',
        'Mauler Staff',
        'Mending',
        'Odin\'s Will',
        'Parry',
        'Power Strikes',
        'Runecarving',
        'Shield',
        'Spear',
        'Staff',
        'Stealth',
        'Stormcalling',
        'Summoning',
        'Suppression',
        'Sword',
        'Thrown Weapons',
        'Witchcraft',
    ),
}

for realm in Realms:
    CraftedSkillList['All'].update(CraftedSkillList[realm])
    DropSkillList['All'].update(DropSkillList[realm])
CraftedSkillList['All'] = tuple(sorted(CraftedSkillList['All']))
DropSkillList['All'] = tuple(sorted(DropSkillList['All']))

SkillValues = (
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
)

# =============================================== #
#           ATTRIBUTE RELATED CONSTANTS           #
# =============================================== #

CraftedAttributeList = (
    'Strength',
    'Constitution',
    'Dexterity',
    'Quickness',
    'Intelligence',
    'Piety',
    'Empathy',
    'Charisma',
    'Hit Points',
    'Power',
)

DropAttributeList = (
    'Strength',
    'Constitution',
    'Dexterity',
    'Quickness',
    'Intelligence',
    'Piety',
    'Empathy',
    'Charisma',
    'Acuity',
    'Hit Points',
    'Power',
)

AttributeValues = (
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
)

HitsValues = (
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
)

PowerValues = (
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
)

# =============================================== #
#      CAP (BASE/ATTRIBUTE) RELATED CONSTANTS     #
# =============================================== #
#                                                 #
#    CALCULATED AS % OF LEVEL + CONSTANT          #
#    E.G. [.25,  1] IS THE LEVEL / 4 + 1          #
#         [  0, 10] IS A FIXED VALUE OF 10        #
#         [  4,  0] IS THE LEVEL * 4              #
#                                                 #
# =============================================== #

AttributeCapList = (
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
)

MythicalStatCapList = (
    'Strength',
    'Constitution',
    'Dexterity',
    'Quickness',
    'Intelligence',
    'Piety',
    'Charisma',
    'Empathy',
    'Acuity',
)

MythicalResistCapList = (
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
)

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
#          RESISTANCE RELATED CONSTANTS           #
# =============================================== #

CraftedResistanceList = (
    'Body',
    'Cold',
    'Heat',
    'Energy',
    'Matter',
    'Spirit',
    'Crush',
    'Thrust',
    'Slash',
)

DropResistanceList = (
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
)

ResistValues = (
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
)

# =============================================== #
#             FOCUS RELATED CONSTANTS             #
# =============================================== #

FocusList = {

    'All': set(),

    'Albion': (

        'All Spell Lines',
        'Body Magic',
        'Cold Magic',
        'Death Servant',
        'Deathsight',
        'Earth Magic',
        'Fire Magic',
        'Matter Magic',
        'Mind Magic',
        'Painworking',
        'Spirit Magic',
        'Wind Magic',
    ),

    'Hibernia': (
        'All Spell Lines',
        'Arboreal Path',
        'Creeping Path',
        'Enchantments',
        'Ethereal Shriek',
        'Light',
        'Mana',
        'Mentalism',
        'Phantasmal Wail',
        'Spectral Guard',
        'Verdant Path',
        'Void',
    ),

    'Midgard': (

        'All Spell Lines',
        'Bone Army',
        'Cursing',
        'Darkness',
        'Runecarving',
        'Summoning',
        'Suppression',
    ),
}

for realm in Realms:
    FocusList['All'].update(FocusList[realm])
FocusList['All'] = tuple(sorted(FocusList['All']))

FocusValues = (
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
)

# =============================================== #
#             BONUS RELATED CONSTANTS             #
# =============================================== #

TOABonusList = (
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
)

PVEBonusList = (
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
)

MythicalBonusList = (
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
)

# =============================================== #
#          EFFECT TYPE RELATED CONSTANTS          #
# =============================================== #

CraftedTypeList = (
    'Unused',
    'Skill',
    'Attribute',
    'Resistance',
    'Focus',
)

EnhancedTypeList = (
    'Unused',
    'Skill',
    'Attribute',
    'Attribute Cap',
    'Focus',
    'ToA Bonus',
    'PvE Bonus',
)

DropTypeList = (
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
)

# =============================================== #
#             EFFECT RELATED CONSTANTS            #
# =============================================== #

CraftedEffectList = {

    'All': {
        'Unused': UnusedList,
        'Skill': (),
        'Attribute': CraftedAttributeList,
        'Resistance': CraftedResistanceList,
        'Focus': (),
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
        'Skill': (),
        'Attribute': DropAttributeList,
        'Attribute Cap': AttributeCapList,
        'Resistance': DropResistanceList,
        'Focus': (),
        'ToA Bonus': TOABonusList,
        'PvE Bonus': PVEBonusList,
        'Mythical Stat Cap': MythicalStatCapList,
        'Mythical Resist Cap': MythicalResistCapList,
        'Mythical Stat & Cap': MythicalStatCapList,
        'Mythical Resist & Cap': MythicalResistCapList,
        'Mythical Bonus': MythicalBonusList,
    }}

for realm in Realms:
    CraftedEffectList[realm] = {}
    CraftedEffectList[realm].update(CraftedEffectList['All'])
    DropEffectList[realm] = {}
    DropEffectList[realm].update(DropEffectList['All'])

for realm in list(CraftedEffectList.keys()):
    CraftedEffectList[realm]['Skill'] = CraftedSkillList[realm]
    CraftedEffectList[realm]['Focus'] = FocusList[realm]
    DropEffectList[realm]['Skill'] = DropSkillList[realm]
    DropEffectList[realm]['Focus'] = FocusList[realm]

# =============================================== #
#          EFFECT VALUE RELATED CONSTANTS         #
# =============================================== #

CraftedValuesList = {

    'Unused': UnusedValues,
    'Skill': SkillValues,

    'Attribute': {
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
    },

    'Resistance': ResistValues,
    'Focus': FocusValues,
}

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
#            CRAFTING RELATED CONSTANTS           #
# =============================================== #

GemTierName = (
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
)

GemMaterial = {

    'All': {

        'Skill': {

            'Critical Strike': {
                'Gem': 'Heated Battle Jewel',
                'Dust': 'Bloodied Battlefield Dirt',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Envenom': {
                'Gem': 'Dusty Battle Jewel',
                'Dust': 'Bloodied Battlefield Dirt',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Parry': {
                'Gem': 'Vapor Battle Jewel',
                'Dust': 'Bloodied Battlefield Dirt',
                'Liquid': 'Swamp Fog',
            },

            'Shield': {
                'Gem': 'Fiery Battle Jewel',
                'Dust': 'Bloodied Battlefield Dirt',
                'Liquid': 'Draconic Fire',
            },

            'Staff': {
                'Gem': 'Earthen Battle Jewel',
                'Dust': 'Bloodied Battlefield Dirt',
                'Liquid': 'Treant Blood',
            },

            'Stealth': {
                'Gem': 'Airy Battle Jewel',
                'Dust': 'Bloodied Battlefield Dirt',
                'Liquid': 'Air Elemental Essence',
            }},

        'Attribute': {

            'Strength': {
                'Gem': 'Fiery Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Draconic Fire',
            },

            'Constitution': {
                'Gem': 'Earthen Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Treant Blood',
            },

            'Dexterity': {
                'Gem': 'Vapor Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Swamp Fog',
            },

            'Quickness': {
                'Gem': 'Airy Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Air Elemental Essence',
            },

            'Intelligence': {
                'Gem': 'Dusty Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Piety': {
                'Gem': 'Watery Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Leviathan Blood',
            },

            'Empathy': {
                'Gem': 'Heated Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Charisma': {
                'Gem': 'Icy Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Frost From a Wasteland',
            },

            'Hit Points': {
                'Gem': 'Blood Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Giant Blood',
            },

            'Power': {
                'Gem': 'Mystical Essence Jewel',
                'Dust': 'Essence of Life',
                'Liquid': 'Mystic Energy',
            }},

        'Resistance': {

            'Body': {
                'Gem': 'Dusty Shielding Jewel',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Cold': {
                'Gem': 'Icy Shielding Jewel',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Frost From a Wasteland',
            },

            'Heat': {
                'Gem': 'Heated Shielding Jewel',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Energy': {
                'Gem': 'Light Shielding Jewel',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Sun Light',
            },

            'Matter': {
                'Gem': 'Earthen Shielding Jewel',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Treant Blood',
            },

            'Spirit': {
                'Gem': 'Vapor Shielding Jewel',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Swamp Fog',
            },

            'Crush': {
                'Gem': 'Fiery Shielding Jewel',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Draconic Fire',
            },

            'Thrust': {
                'Gem': 'Airy Shielding Jewel',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Air Elemental Essence',
            },

            'Slash': {
                'Gem': 'Watery Shielding Jewel',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Leviathan Blood',
            }}},

    'Albion': {

        'Skill': {

            'All Magic Skills': {
                'Gem': 'Finesse Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': (
                    'Draconic Fire',
                    'Mystic Energy',
                    'Treant Blood',
                )},

            'All Melee Weapon Skills': {
                'Gem': 'Finesse War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': (
                    'Draconic Fire',
                    'Mystic Energy',
                    'Treant Blood',
                )},

            'Archery': {
                'Gem': 'Airy War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Air Elemental Essence',
            },

            'Aura Manipulation': {
                'Gem': 'Radiant Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Sun Light',
            },

            'Body Magic': {
                'Gem': 'Heated Evocation Sigil',
                'Dust': 'Ground Cave Crystal',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Chants': {
                'Gem': 'Earthen Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Treant Blood',
            },

            'Cold Magic': {
                'Gem': 'Icy Evocation Sigil',
                'Dust': 'Ground Cave Crystal',
                'Liquid': 'Frost From a Wasteland',
            },

            'Crossbow': {
                'Gem': 'Vapor War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Swamp Fog',
            },

            'Crush': {
                'Gem': 'Fiery War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Draconic Fire',
            },

            'Death Servant': {
                'Gem': 'Ashen Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Deathsight': {
                'Gem': 'Vacuous Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Swamp Fog',
            },

            'Dual Wield': {
                'Gem': 'Icy War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Frost From a Wasteland',
            },

            'Earth Magic': {
                'Gem': 'Earthen Evocation Sigil',
                'Dust': 'Ground Cave Crystal',
                'Liquid': 'Treant Blood',
            },

            'Enhancement': {
                'Gem': 'Airy Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Air Elemental Essence',
            },

            'Flexible': {
                'Gem': 'Molten Magma War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Leviathan Blood',
            },

            'Fire Magic': {
                'Gem': 'Fiery Evocation Sigil',
                'Dust': 'Ground Cave Crystal',
                'Liquid': 'Draconic Fire',
            },

            'Fist Wraps': {
                'Gem': 'Glacial War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Frost From a Wasteland',
            },

            'Instruments': {
                'Gem': 'Vapor Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Swamp Fog',
            },

            'Magnetism': {
                'Gem': 'Magnetic Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Mystic Energy',
            },

            'Matter Magic': {
                'Gem': 'Dusty Evocation Sigil',
                'Dust': 'Ground Cave Crystal',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Mauler Staff': {
                'Gem': 'Cinder War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Draconic Fire',
            },

            'Mind Magic': {
                'Gem': 'Watery Evocation Sigil',
                'Dust': 'Ground Cave Crystal',
                'Liquid': 'Leviathan Blood',
            },

            'Painworking': {
                'Gem': 'Salt Crusted Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Mystic Energy',
            },

            'Polearm': {
                'Gem': 'Earthen War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Treant Blood',
            },

            'Power Strikes': {
                'Gem': 'Clout Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Giant Blood',
            },

            'Rejuvenation': {
                'Gem': 'Watery Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Leviathan Blood',
            },

            'Slash': {
                'Gem': 'Watery War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Leviathan Blood',
            },

            'Smite': {
                'Gem': 'Fiery Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Draconic Fire',
            },

            'Soulrendering': {
                'Gem': 'Steaming Fervor Sigil',
                'Dust': 'Ground Blessed Undead Bone',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Spirit Magic': {
                'Gem': 'Vapor Evocation Sigil',
                'Dust': 'Ground Cave Crystal',
                'Liquid': 'Swamp Fog',
            },

            'Thrust': {
                'Gem': 'Dusty War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Two Handed': {
                'Gem': 'Heated War Sigil',
                'Dust': 'Ground Caer Stone',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Wind Magic': {
                'Gem': 'Airy Evocation Sigil',
                'Dust': 'Ground Cave Crystal',
                'Liquid': 'Air Elemental Essence',
            }},

        'Focus': {

            'All Spell Lines': {
                'Gem': 'Brilliant Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': (
                    'Draconic Fire',
                    'Mystic Energy',
                    'Treant Blood',
                )},

            'Body Magic': {
                'Gem': 'Heat Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Cold Magic': {
                'Gem': 'Ice Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Frost From a Wasteland',
            },

            'Death Servant': {
                'Gem': 'Ashen Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Deathsight': {
                'Gem': 'Vacuous Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Swamp Fog',
            },

            'Earth Magic': {
                'Gem': 'Earth Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Treant Blood',
            },

            'Fire Magic': {
                'Gem': 'Fire Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Draconic Fire',
            },

            'Matter Magic': {
                'Gem': 'Dust Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Mind Magic': {
                'Gem': 'Water Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Leviathan Blood',
            },

            'Painworking': {
                'Gem': 'Salt Crusted Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Mystic Energy',
            },

            'Spirit Magic': {
                'Gem': 'Vapor Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Swamp Fog',
            },

            'Wind Magic': {
                'Gem': 'Air Sigil',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Air Elemental Essence',
            }}},

    'Hibernia': {

        'Skill': {

            'All Magic Skills': {
                'Gem': 'Finesse Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': (
                    'Draconic Fire',
                    'Mystic Energy',
                    'Treant Blood',
                )},

            'All Melee Weapon Skills': {
                'Gem': 'Finesse War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': (
                    'Draconic Fire',
                    'Mystic Energy',
                    'Treant Blood',
                )},

            'Arboreal Path': {
                'Gem': 'Steaming Nature Spell Stone',
                'Dust': 'Fiary Dust',
                'Liquid': 'Swamp Fog',
            },

            'Archery': {
                'Gem': 'Airy War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Air Elemental Essence',
            },

            'Aura Manipulation': {
                'Gem': 'Radiant Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': 'Sun Light',
            },

            'Blades': {
                'Gem': 'Watery War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Leviathan Blood',
            },

            'Blunt': {
                'Gem': 'Fiery War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Draconic Fire',
            },

            'Celtic Dual': {
                'Gem': 'Icy War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Frost From a Wasteland',
            },

            'Celtic Spear': {
                'Gem': 'Earthen War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Treant Blood',
            },

            'Creeping Path': {
                'Gem': 'Oozing Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': 'Treant Blood',
            },

            'Dementia': {
                'Gem': 'Aberrant Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Treant Blood',
            },

            'Enchantments': {
                'Gem': 'Vapor Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Swamp Fog',
            },

            'Ethereal Shriek': {
                'Gem': 'Ethereal Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Leviathan Blood',
            },

            'Fist Wraps': {
                'Gem': 'Glacial War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Frost From a Wasteland',
            },

            'Large Weaponry': {
                'Gem': 'Heated War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Light': {
                'Gem': 'Fiery Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Draconic Fire',
            },

            'Magnetism': {
                'Gem': 'Magnetic Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': 'Mystic Energy',
            },

            'Mana': {
                'Gem': 'Watery Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Leviathan Blood',
            },

            'Mauler Staff': {
                'Gem': 'Cinder War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Draconic Fire',
            },

            'Mentalism': {
                'Gem': 'Earthen Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Treant Blood',
            },

            'Music': {
                'Gem': 'Airy Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': 'Air Elemental Essence',
            },

            'Nature': {
                'Gem': 'Earthen Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': 'Treant Blood',
            },

            'Nurture': {
                'Gem': 'Fiery Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': 'Draconic Fire',
            },

            'Phantasmal Wail': {
                'Gem': 'Phantasmal Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Draconic Fire',
            },

            'Piercing': {
                'Gem': 'Dusty War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Power Strikes': {
                'Gem': 'Clout Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': 'Giant Blood',
            },

            'Regrowth': {
                'Gem': 'Watery Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': 'Leviathan Blood',
            },

            'Scythe': {
                'Gem': 'Light War Spell Stone',
                'Dust': 'Unseelie Dust',
                'Liquid': 'Sun Light',
            },

            'Shadow Mastery': {
                'Gem': 'Shadowy Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Swamp Fog',
            },

            'Spectral Guard': {
                'Gem': 'Spectral Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Air Elemental Essence',
            },

            'Valor': {
                'Gem': 'Airy Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Air Elemental Essence',
            },

            'Vampiiric Embrace': {
                'Gem': 'Embracing Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Frost From a Wasteland',
            },

            'Verdant Path': {
                'Gem': 'Mineral Encrusted Nature Spell Stone',
                'Dust': 'Fairy Dust',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Void': {
                'Gem': 'Icy Arcane Spell Stone',
                'Dust': 'Other Worldly Dust',
                'Liquid': 'Frost From a Wasteland',
            }},

        'Focus': {

            'All Spell Lines': {
                'Gem': 'Brilliant Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': (
                    'Draconic Fire',
                    'Mystic Energy',
                    'Treant Blood'
                )},

            'Arboreal Path': {
                'Gem': 'Steaming Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Swamp Fog'
            },

            'Creeping Path': {
                'Gem': 'Oozing Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Treant Blood'
            },

            'Enchantments': {
                'Gem': 'Vapor Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Swamp Fog'
            },

            'Ethereal Shriek': {
                'Gem': 'Ethereal Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Swamp Fog'
            },

            'Light': {
                'Gem': 'Fire Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Draconic Fire'
            },

            'Mana': {
                'Gem': 'Water Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Leviathan Blood'
            },

            'Mentalism': {
                'Gem': 'Earth Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Treant Blood'
            },

            'Phantasmal Wail': {
                'Gem': 'Phantasmal Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Leviathan Blood'
            },

            'Spectral Guard': {
                'Gem': 'Spectral Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Draconic Fire'
            },

            'Verdant Path': {
                'Gem': 'Mineral Encrusted Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Heat From an Unearthly Pyre'
            },

            'Void': {
                'Gem': 'Ice Spell Stone',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Frost From a Wasteland'
            }}},

    'Midgard': {

        'Skill': {

            'All Magic Skills': {
                'Gem': 'Finesse Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': (
                    'Draconic Fire',
                    'Mystic Energy',
                    'Treant Blood',
                )},

            'All Melee Weapon Skills': {
                'Gem': 'Finesse War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': (
                    'Draconic Fire',
                    'Mystic Energy',
                    'Treant Blood',
                )},

            'Archery': {
                'Gem': 'Airy War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Air Elemental Essence',
            },

            'Augmentation': {
                'Gem': 'Airy Chaos Rune',
                'Dust': 'Soot From Niflheim',
                'Liquid': 'Air Elemental Essence',
            },

            'Aura Manipulation': {
                'Gem': 'Radiant Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Sun Light',
            },

            'Axe': {
                'Gem': 'Earthen War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Treant Blood',
            },

            'Battlesongs': {
                'Gem': 'Airy Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Air Elemental Essence',
            },

            'Beastcraft': {
                'Gem': 'Earthen Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Treant Blood',
            },

            'Bone Army': {
                'Gem': 'Ashen Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Cave Magic': {
                'Gem': 'Fiery Chaos Rune',
                'Dust': 'Soot From Niflheim',
                'Liquid': 'Draconic Fire',
            },

            'Cursing': {
                'Gem': 'Blighted Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Air Elemental Essence',
            },

            'Darkness': {
                'Gem': 'Icy Chaos Rune',
                'Dust': 'Soot From Niflheim',
                'Liquid': 'Frost From a Wasteland',
            },

            'Fist Wraps': {
                'Gem': 'Glacial War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Frost From a Wasteland',
            },

            'Hammer': {
                'Gem': 'Fiery War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Draconic Fire',
            },

            'Hand To Hand': {
                'Gem': 'Lightning Charged War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Leviathan Blood',
            },

            'Hexing': {
                'Gem': 'Unholy Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Air Elemental Essence',
            },

            'Left Axe': {
                'Gem': 'Icy War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Frost From a Wasteland',
            },

            'Magnetism': {
                'Gem': 'Magnetic Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Mystic Energy',
            },

            'Mauler Staff': {
                'Gem': 'Cinder War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Draconic Fire',
            },

            'Mending': {
                'Gem': 'Watery Chaos Rune',
                'Dust': 'Soot From Niflheim',
                'Liquid': 'Leviathan Blood',
            },

            'Odin\'s Will': {
                'Gem': 'Valiant Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Swamp Fog',
            },

            'Power Strikes': {
                'Gem': 'Clout Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Giant Blood',
            },

            'Runecarving': {
                'Gem': 'Heated Chaos Rune',
                'Dust': 'Soot From Niflheim',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Spear': {
                'Gem': 'Heated War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Heat From an Unearthly Pyre',
            },

            'Staff': {
                'Gem': 'Earthen Battle Jewel',
                'Dust': 'Bloodied Battlefield Dirt',
                'Liquid': 'Treant Blood',
            },

            'Stormcalling': {
                'Gem': 'Fiery Primal Rune',
                'Dust': 'Ground Vendo Bone',
                'Liquid': 'Draconic Fire',
            },

            'Summoning': {
                'Gem': 'Vapor Chaos Rune',
                'Dust': 'Soot From Niflheim',
                'Liquid': 'Swamp Fog',
            },

            'Suppression': {
                'Gem': 'Dusty Chaos Rune',
                'Dust': 'Soot From Niflheim',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Sword': {
                'Gem': 'Watery War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Leviathan Blood',
            },

            'Thrown Weapons': {
                'Gem': 'Vapor War Rune',
                'Dust': 'Ground Giant Bone',
                'Liquid': 'Swamp Fog',
            }},

        'Focus': {

            'All Spell Lines': {
                'Gem': 'Brilliant Rune',
                'Dust': 'Ground Draconic Scales',
                'Liquid': (
                    'Dragonic Fire',
                    'Mystic Energy',
                    'Trent Blood'
                )},

            'Bone Army': {
                'Gem': 'Ashen Rune',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Cursing': {
                'Gem': 'Blighted Rune',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Darkness': {
                'Gem': 'Ice Rune',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Frost From a Wasteland',
            },

            'Runecarving': {
                'Gem': 'Heat Rune',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Undead Ash and Holy Water',
            },

            'Summoning': {
                'Gem': 'Vapor Rune',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Swamp Fog',
            },

            'Suppression': {
                'Gem': 'Dust Rune',
                'Dust': 'Ground Draconic Scales',
                'Liquid': 'Undead Ash and Holy Water',
            },
        },
    },
}

GemMaterialOrder = {

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
#             GAME RELATED CONSTANTS              #
# =============================================== #

GemHotkeyValues = {

    'Albion': {

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
    },

    'Hibernia': {

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
    },

    'Midgard': {

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
    },
}

# SERVER CODES (*.IGN)
ServerIgnCodes = {
    'Pendragon': '74',
    'Gaheris': '95',
    'Ywain': '143',
}

# SERVER CODES (*.INI)
ServerCodes = {
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
}

if __name__ == "__main__":
    pass
