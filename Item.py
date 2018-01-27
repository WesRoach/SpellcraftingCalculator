# HEADER PLACE HOLDER

from Character import ItemTypes
from Constants import CraftedEffectTable, CraftedValuesList, GemNames, ImbuePoints, SlotList


class Item:

    def __init__(self, state = '', location = '', realm = 'All', index = -1):
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
        if self.ItemLocation in SlotList['Jewelery']:
            self.ItemLevel = '50'
            for key, value in ItemTypes.items():
                if self.ItemLocation == key:
                    self.ItemType = ItemTypes[key][0]
            self.ItemEquipped = 2
        elif self.ItemLocation in SlotList['Armor']:
            self.ItemLevel = '51'
            for key, value in ItemTypes.items():
                if self.ItemLocation == key:
                    self.ItemType = ItemTypes[key][self.ItemRealm][0]
            self.ItemEquipped = 2
        elif self.ItemLocation in SlotList['Weapons']:
            self.ItemLevel = '51'
            for key, value in ItemTypes.items():
                if self.ItemLocation == key:
                    self.ItemType = ItemTypes[key][self.ItemRealm][0]
            self.ItemEquipped = 0
        elif self.ItemLocation in SlotList['Mythical']:
            self.ItemLevel = '50'
            for key, value in ItemTypes.items():
                if self.ItemLocation in SlotList['Mythical'] == value:
                    self.ItemType = ItemTypes[key][0]
            self.ItemEquipped = 2

    # TODO: THIS NEEDS TO BE CLEANED UP ...
    def makeItemSlots(self):
        ItemSlots = []
        if self.ActiveState == 'Crafted':
            for slot in range(0, 4):
                ItemSlots.append(ItemSlot('Craftable'))
            ItemSlots.append(ItemSlot('Enhanced'))
        elif self.ActiveState == 'Legendary':
            for slot in range(0, 4):
                ItemSlots.append(ItemSlot('Craftable'))
            ItemSlots.append(ItemSlot('Dropped'))
            ItemSlots.append(ItemSlot('Dropped'))
            ItemSlots.append(ItemSlot('Dropped'))
        elif self.ActiveState == 'Dropped':
            for slot in range(0, 12):
                ItemSlots.append(ItemSlot('Dropped'))
        return ItemSlots

    def addSlot(self, itype):
        self.ItemSlotList.append(ItemSlot(itype))

    def removeSlot(self, index):
        del self.ItemSlotList[index]

    def getSlot(self, index):
        return self.ItemSlotList[index]

    def getSlotCount(self):
        return len(self.ItemSlotList)

    def getSlotList(self):
        return list(self.ItemSlotList)

    def clearSlots(self):
        self.ItemSlotList = self.makeItemSlots()

    # TODO: ADJUST FOR LEGENDARY ...
    def getSlotImbueValues(self):
        if self.ActiveState not in ('Crafted', 'Legendary'):
            return 0.0, 0.0, 0.0, 0.0

        values = []
        for index in range(0, self.getSlotCount() - 1):
            if self.getSlot(index).getSlotType() == 'Craftable':
                values.append(self.getSlot(index).getImbueValue())

        maxValue = max(values)
        for index in range(0, self.getSlotCount() - 1):
            if self.getSlot(index).getSlotType() == 'Craftable':
                if index == values.index(maxValue): continue
                values[index] /= 2.0

        return values

    # TODO: ADJUST FOR LEGENDARY (USE SLOT TYPE) ...
    def getItemImbueValue(self):
        if self.ActiveState != 'Crafted':
            return 0.0
        if int(self.ItemLevel) < 1 or int(self.ItemLevel) > 51:
            return 0.0
        return ImbuePoints[int(self.ItemLevel) - 1]


class ItemSlot:

    def __init__(self, itype = '', etype = 'Unused', effect = '', amount = '', requirement = ''):
        self.SlotType = itype
        self.EffectType = etype
        self.Effect = effect
        self.EffectAmount = amount
        self.Requirement = requirement

    def isCraftable(self):
        if self.getSlotType() == 'Craftable':
            return True if (self.getEffectType() != 'Unused') else False

    def setEffectType(self, etype):
        self.EffectType = etype

    def setEffect(self, effect):
        self.Effect = effect

    def setEffectAmount(self, amount):
        self.EffectAmount = amount

    def setEffectRequirement(self, value):
        self.Requirement = value

    def getSlotType(self):
        return self.SlotType

    def getEffectType(self):
        return self.EffectType

    def getEffect(self):
        return self.Effect

    def getEffectAmount(self):
        return self.EffectAmount

    def getEffectRequirement(self):
        return self.Requirement

    # TODO: POSSIBLY MOVE AWAY FROM 'isCrafted'
    def getImbueValue(self, value = 0):
        if not self.isCraftable(): return 0.0
        if self.getEffectType() == 'Stat':
            if self.getEffect() not in ('Hits', 'Power'):
                value = round((int(self.getEffectAmount()) - 1) / 1.7)
                print(str(value))
            elif self.getEffect() == 'Hits':
                value = int(self.getEffectAmount()) / 4.0
            elif self.getEffect() == 'Power':
                value = (int(self.getEffectAmount()) - 1) * 2.0
        elif self.getEffectType() == 'Resist':
            value = (int(self.getEffectAmount()) - 1) * 2.0
        elif self.getEffectType() == 'Skill':
            value = (int(self.getEffectAmount()) - 1) * 5.0
        return 1.0 if value < 1.0 else value

    def getGemIndex(self):
        if self.getEffect() in CraftedValuesList[self.getEffectType()]:
            return CraftedValuesList[self.getEffectType()][self.getEffect()].index(self.getEffectAmount())
        elif self.getEffectType() in CraftedValuesList:
            return CraftedValuesList[self.getEffectType()].index(self.getEffectAmount())

    # TODO: UPDATE VARIABLE NAMES, IMPLEMENT ENHANCED ITEMS
    def getGemName(self, realm):
        if self.getSlotType() == 'Enhanced':
            if self.getEffectType() == 'Unused':
                return 'Unused'
            return 'ARMOR NAME'
        if self.getSlotType() == 'Dropped':
            return 'Non-Craftable Bonus'
        if not self.isCraftable():
            return '--> SET THE COLUMN WIDTH'
        tier = GemNames[self.getGemIndex()]
        prefix = CraftedEffectTable[realm][self.EffectType][self.Effect][0]
        suffix = CraftedEffectTable[realm][self.EffectType][self.Effect][1]
        return tier + ' ' + prefix + ' ' + suffix
