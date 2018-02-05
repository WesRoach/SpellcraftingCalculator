# HEADER PLACE HOLDER

from Character import ItemTypes
from Constants import CraftedEffectTable, CraftedValuesList, GemNames, ImbuePoints, SlotList
from lxml import etree


class Item:

    def __init__(self, state = '', location = '', realm = 'All', index = -1):
        self.ActiveState = state
        self.Equipped = int
        self.Location = location
        self.Realm = realm
        self.Level = ''
        self.Quality = ''
        self.Type = ''
        self.Name = ''
        self.AFDPS = ''
        self.Speed = ''
        self.Bonus = ''
        self.Origin = ''
        self.LeftHand = ''
        self.DamageType = ''
        self.Restrictions = list()
        self.Notes = ''
        self.Requirement = ''
        self.TemplateIndex = index
        self.SlotList = self.makeItemSlots()

        # SET THE INITIAL ITEM PROPERTIES
        self.setInitialItemProperties()

    def setInitialItemProperties(self):
        if self.Location in SlotList['Jewelery']:
            self.Level = '50'
            for key, value in ItemTypes.items():
                if self.Location == key:
                    self.Type = ItemTypes[key][0]
            self.Equipped = 2
        elif self.Location in SlotList['Armor']:
            self.Level = '51'
            for key, value in ItemTypes.items():
                if self.Location == key:
                    self.Type = ItemTypes[key][self.Realm][0]
            self.Equipped = 2
        elif self.Location in SlotList['Weapons']:
            self.Level = '51'
            for key, value in ItemTypes.items():
                if self.Location == key:
                    self.Type = ItemTypes[key][self.Realm][0]
            self.Equipped = 0
        elif self.Location in SlotList['Mythical']:
            self.Level = '50'
            for key, value in ItemTypes.items():
                if self.Location in SlotList['Mythical'] == value:
                    self.Type = ItemTypes[key][0]
            self.Equipped = 2

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
        self.SlotList.append(ItemSlot(itype))

    def removeSlot(self, index):
        del self.SlotList[index]

    def getSlot(self, index):
        return self.SlotList[index]

    def getSlotCount(self):
        return len(self.SlotList)

    def getSlotList(self):
        return list(self.SlotList)

    def clearSlots(self):
        self.SlotList = self.makeItemSlots()

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
        if int(self.Level) < 1 or int(self.Level) > 51:
            return 0.0
        return ImbuePoints[int(self.Level) - 1]

    def importFromXML(self, filename, label):
        tree = etree.parse(filename)
        item = tree.iter()
        for element in item:
            if element.tag in ('Gem', 'Slot'):
                index = int(element.attrib['Number'])
                for attribute in element:
                    if attribute.tag == 'EffectType':
                        self.getSlot(index).setEffectType(attribute.text)
                    elif attribute.tag == 'Effect':
                        self.getSlot(index).setEffect(attribute.text)
                    elif attribute.tag == 'Amount':
                        self.getSlot(index).setEffectAmount(attribute.text)
            elif element.tag in self.__dict__:
                setattr(self, element.tag, element.text)
            if element.tag == 'ActiveState':
                self.SlotList = self.makeItemSlots()
            if element.tag == 'Equipped':
                self.Equipped = int(element.text)

        # DEBUGGING
        print('importFromFile')

    def exportAsXML(self, filename):

        # DEBUGGING
        print('exportToFile')


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

    def setAll(self, etype, effect, amount,):
        self.EffectType = etype
        self.Effect = effect
        self.EffectAmount = amount

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

    # TODO: IMPLEMENT ENHANCED ITEMS
    def getGemName(self, realm):
        if self.getSlotType() == 'Enhanced':
            if self.getEffectType() == 'Unused':
                return 'Unused'
            return 'Craftable Item Bonus'
        if self.getSlotType() == 'Dropped':
            return 'Non-Craftable Item Bonus'
        if not self.isCraftable():
            return '--> SET THE COLUMN WIDTH'
        tier = GemNames[self.getGemIndex()]
        prefix = CraftedEffectTable[realm][self.EffectType][self.Effect][0]
        suffix = CraftedEffectTable[realm][self.EffectType][self.Effect][1]
        return tier + ' ' + prefix + ' ' + suffix
