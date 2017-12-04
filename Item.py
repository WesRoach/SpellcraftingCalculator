# HEADER PLACE HOLDER

from Constants import SlotList


class ItemSlot:

    def __init__(self, itype = '', etype = 'Unused', effect = '', amount = '', requirement = ''):
        self.__dict__ = {
            'ItemType': str(itype),
            'SlotEffectType': '',
            'SlotEffect': '',
            'SlotEffectAmount': '',
            'SlotRequirement': '',
        }

        self.SlotEffect = ''
        self.SlotEffectType = ''
        self.SlotEffectAmount = ''
        self.SlotRequirement = ''
        self.CraftOkay = bool

        self.setAll(etype, effect, amount, requirement)

    def setAll(self, etype = 'Unused', effect = '', amount = '0', requirement = ''):
        self.SlotEffect = str(effect)
        self.SlotEffectType = str(etype)
        self.SlotEffectAmount = str(amount)
        self.SlotRequirement = str(requirement)

    def getAttribute(self, attribute):
        if attribute in self.__dict__:
            return self.__dict__[attribute]

    def setAttribute(self, attribute, value):
        self.CraftOkay = False

        if attribute in self.__dict__:
            self.__dict__[attribute] = str(value)


class Item:
    def __init__(self, state = '', location = '', realm = 'All', index =- 1):
        self.__dict__ = {
            'ActiveState': state,
            'Equipped': '0',
            'ItemLocation': location,
            'ItemRealm': realm,
            'ItemLevel': '51',
            'ItemQuality': '100',
            'ItemName': '',
            'ItemAFDPS': '',
            'ItemSpeed': '',
            'ItemBonus': '',
            'ItemType': '',
            'ItemSource': '',
            'LeftHand': '',
            'ItemDamageType': '',
            'ItemRestrictions': list(),
            'ItemNotes': '',
            'BonusRequirement': '',
            'TemplateIndex': index,
        }

        self.ItemSlotList = list()

        if location in SlotList['Jewelery']:
            self.ActiveState = 'drop'
            self.ItemEquipped = '1'
        elif location in SlotList['Armor']:
            self.ActiveState = 'crafted'
            self.ItemEquipped = '1'
        elif location in SlotList['Weapons']:
            self.ActiveState = 'drop'
            self.ItemEquipped = '0'
        elif location in SlotList['Mythical']:
            self.ActiveState = 'drop'
            self.ItemEquipped = '1'

        self.ItemSlotList = self.makeItemSlots()

    def makeItemSlots(self):
        ItemType = self.ActiveState
        ItemSlots = []

        if ItemType == 'drop':
            for slot in range(0, 12):
                ItemSlots.append(ItemSlot(ItemType))

        elif ItemType == 'crafted':
            for slot in range (0, 4):
                ItemSlots.append(ItemSlot(ItemType))

            ItemSlots.append(ItemSlot('effect'))
            ItemSlots.append(ItemSlot('unused'))

        return ItemSlots
