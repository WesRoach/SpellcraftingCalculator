# HEADER PLACE HOLDER

from Character import armorTypes, ItemTypes
from Constants import SlotList


class Item:

    def __init__(self, state = '', location = '', realm = 'All', index = 0):
        self.ActiveState = state
        self.ItemEquipped = int
        self.ItemLocation = location
        self.ItemRealm = realm
        self.ItemLevel = ''
        self.ItemQuality = ''
        self.ItemType = ''
        self.ItemName = ''
        self.ItemAFDPS = ''
        self.ItemSpeed = ''
        self.ItemBonus = ''
        self.ItemSource = ''
        self.LeftHand = ''
        self.ItemDamageType = ''
        self.ItemRestrictions = list()
        self.ItemNotes = ''
        self.ItemRequirement = ''
        self.TemplateIndex = index
        self.ItemSlotList = self.makeItemSlots()

        # SET THE INITIAL ITEM PROPERTIES
        self.setInitialItemProperties()

    def setInitialItemProperties(self):
        self.ItemLevel = '51'
        self.ItemQuality = '100'

        if self.ItemLocation in SlotList['Jewelery']:
            for key, value in ItemTypes.items():
                if self.ItemLocation == key:
                    self.ItemType = ItemTypes[key][0]
            self.ItemEquipped = 2
        elif self.ItemLocation in SlotList['Armor']:
            for key, value in ItemTypes.items():
                if self.ItemLocation == key:
                    self.ItemType = ItemTypes[key][self.ItemRealm][0]
            self.ItemEquipped = 2
        elif self.ItemLocation in SlotList['Weapons']:
            for key, value in ItemTypes.items():
                if self.ItemLocation == key:
                    self.ItemType = ItemTypes[key][self.ItemRealm][0]
            self.ItemEquipped = 0
        elif self.ItemLocation in SlotList['Mythical']:
            for key, value in ItemTypes.items():
                if self.ItemLocation in SlotList['Mythical'] == value:
                    self.ItemType = ItemTypes[key][0]
            self.ItemEquipped = 2

    def makeItemSlots(self):
        ItemSlots = []
        if self.ActiveState == 'drop':
            for slot in range(0, 12):
                ItemSlots.append(ItemSlot(self.ActiveState))
        elif self.ActiveState == 'crafted':
            for slot in range(0, 4):
                ItemSlots.append(ItemSlot(self.ActiveState))
            ItemSlots.append(ItemSlot('enhanced'))
            ItemSlots.append(ItemSlot('effect'))
        return ItemSlots

    def getSlotIndex(self, index):
        return self.ItemSlotList[index]

    def getSlotCount(self):
        return len(self.ItemSlotList)

    def getSlotList(self):
        return list(self.ItemSlotList)


class ItemSlot:

    def __init__(self, itype = '', etype = 'Unused', effect = '', amount = '', requirement = ''):
        self.SlotType = itype
        self.EffectType = etype
        self.Effect = effect
        self.EffectAmount = amount
        self.Requirement = requirement
        self.Craftable = False

    def setAll(self, etype='Unused', effect='', amount='0', requirement=''):
        self.EffectType = etype
        self.Effect = effect
        self.EffectAmount = amount
        self.Requirement = requirement
        self.Craftable = False

    def setEffectType(self, etype):
        self.EffectType = etype

    def setEffect(self, effect):
        self.Effect = effect

    def setEffectAmount(self, amount):
        self.EffectAmount = amount

    def getEffectType(self):
        return self.EffectType

    def getEffect(self):
        return self.Effect

    def getEffectAmount(self):
        return self.EffectAmount

    def getSlotType(self):
        return self.SlotType
