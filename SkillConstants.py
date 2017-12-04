# HEADER PLACE HOLDER

from TupleTwo import *
from DictionaryTwo import *
from Character import Realms
from CraftingConstants import GemDusts, GemLiquids

__all__ = [
    'CraftSkillList',
    'DropSkillList',
    'SkillTable',
    'SkillValues',
]

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
        'Two Handed': ('Heated', 'War Sigil',),
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

CraftSkillList = {}
DropSkillList = {}
for realm in list(SkillTable.keys()):
    skills = list(SkillTable[realm].keys())
    skills.sort()
    CraftSkillList[realm] = t2(skills)
    skills.insert(2, 'All Archery Skills')
    skills.insert(3, 'All Dual Wield Skills')
    if realm == 'Midgard':  # ADD NON-CRAFTABLE 'Witchcraft' SKILL
        skills.append('Witchcraft')
    DropSkillList[realm] = t2(skills)
CraftSkillList = d2(CraftSkillList)
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

if __name__ == "__main__":
    pass
