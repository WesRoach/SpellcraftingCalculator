# HEADER PLACE HOLDER

from Constants import SlotList, ItemTypes


class ItemSlot:

    def __init__(self, itype = '', etype = 'Unused', effect = '', amount = '', requirement = ''):
        self.__dict__ = {
            'ItemType': str(itype),
            'Effect': '',
            'EffectType': '',
            'EffectAmount': '',
            'Requirement': '',
        }

        self.Effect = ''
        self.EffectType = ''
        self.EffectAmount = ''
        self.Requirement = ''
        self.CraftOkay = False

        self.setAll(etype, effect, amount, requirement)

    def setAll(self, etype = 'Unused', effect = '', amount = '0', requirement = ''):
        self.Effect = str(effect)
        self.EffectType = str(etype)
        self.EffectAmount = str(amount)
        self.Requirement = str(requirement)

    def getAttribute(self, attribute):
        if attribute in self.__dict__:
            return self.__dict__[attribute]

    def setAttribute(self, attribute, value):
        self.CraftOkay = False

        if attribute in self.__dict__:
            self.__dict__[attribute] = str(value)

    def itemType(self):
        return self.ItemType

    def effectType(self):
        return self.EffectType


class Item:
    def __init__(self, state = '', location = '', realm = 'All', index =- 1):
        self.__dict__ = {
            'ActiveState': state,
            'ItemEquipped': 0,
            'ItemLocation': location,
            'ItemRealm': realm,
            'ItemLevel': '51',
            'ItemQuality': '100',
            'ItemType': '',
            'ItemName': '',
            'ItemAFDPS': '',
            'ItemSpeed': '',
            'ItemBonus': '',
            'ItemSource': '',
            'LeftHand': '',
            'ItemDamageType': '',
            'ItemRestrictions': list(),
            'ItemNotes': '',
            'ItemRequirement': '',
            'TemplateIndex': index,
        }

        self.ItemSlotList = list()

        if self.ItemLocation in SlotList['Jewelery']:
            self.ActiveState = 'drop'
            self.ItemEquipped = 2
        elif self.ItemLocation in SlotList['Armor']:
            self.ActiveState = 'crafted'
            self.ItemEquipped = 2
        elif self.ItemLocation in SlotList['Weapons']:
            self.ActiveState = 'drop'
            self.ItemEquipped = 0
        elif self.ItemLocation in SlotList['Mythical']:
            self.ActiveState = 'drop'
            self.ItemEquipped = 2

        # TODO: DETERMINE 'ItemEquipped' FOR WEAPONS BASED ON CLASS SELECTION

        self.ItemSlotList = self.makeItemSlots()

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

    def slot(self, index):
        return self.ItemSlotList[index]

    def slotCount(self):
        return len(self.ItemSlotList)

    def slots(self):
        return list(self.ItemSlotList)
