# HEADER PLACE HOLDER

from Character import ItemTypes
from Constants import CraftedEffectTable, CraftedValuesList, GemGemsOrder, GemNames, ImbuePoints, OverchargeBasePercent, OverchargeSkillBonus
from lxml import etree

# noinspection PyUnresolvedReferences
# FIXES BUG IN PYCHARM THAT CAUSES
# AN UNRESOLVED REFERENCE ERROR
from math import floor


class Item:

    def __init__(self, state = '', location = '', realm = '', index = -1):
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
        self.Database = False
        self.Index = index
        self.SlotList = self.makeItemSlots()

        if location in ItemTypes['Jewelery']:
            self.Equipped = 2
        elif location in ItemTypes['Armor']:
            self.Equipped = 2
        elif location in ItemTypes['Weapons']:
            self.Equipped = 0
        elif location in ItemTypes['Mythical']:
            self.Equipped = 0

        if state in ('Crafted', 'Legendary'):
            self.Level = '51'
            self.Origin = 'Crafted'

        # TODO: SET ARMOR TYPE BASED ON TOP-TIER ARMOR ...
        if self.getParent() in ('Jewelery', 'Mythical') and state != 'Imported':
            self.Type = ItemTypes[self.getParent()][location][realm][0]

        if self.Location == 'Left Hand':
            self.LeftHand = 2

    def getParent(self):
        for parent, locations in ItemTypes.items():
            if self.Location in locations:
                return parent

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

    def getSlot(self, index):
        return self.SlotList[index]

    def getSlotCount(self):
        return len(self.SlotList)

    def getSlotList(self):
        return list(self.SlotList)

    def clearSlots(self):
        self.SlotList = self.makeItemSlots()

    def getImbueValues(self):
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

    def getMaxImbueValue(self):
        if self.ActiveState not in ('Crafted', 'Legendary'):
            return 0.0
        if self.Level == '' or int(self.Level) < 1 or int(self.Level) > 51:
            return 0.0
        return ImbuePoints[int(self.Level) - 1]

    def getUtility(self):
        utility = 0.0
        for slot in self.getSlotList():
            utility += slot.getGemUtility()
        return utility

    def getOverchargeSuccess(self, skill = 1000):
        if sum(self.getImbueValues()) == 0:
            return 'N/A'
        elif sum(self.getImbueValues()) >= (self.getMaxImbueValue() + 6.0):
            return 0
        elif sum(self.getImbueValues()) <= (self.getMaxImbueValue() + 1.0):
            return 100
        else:
            bonus = OverchargeSkillBonus[floor(skill / 50) - 1]
            overcharge = floor(sum(self.getImbueValues())) - self.getMaxImbueValue()
            success = OverchargeBasePercent[overcharge] + 44 + 26 + bonus
            return 100 if success > 100 else success

    def importFromXML(self, filename, export = False):
        tree = etree.parse(filename) if not export else etree.ElementTree(filename)
        if tree.getroot().tag == 'Item':
            elements = tree.getroot().getchildren()
            for element in elements:
                if element.tag not in ('Equipped', 'Restrictions', 'Slot'):
                    if element.tag in self.__dict__:
                        setattr(self, element.tag, element.text)
                    if element.tag == 'ActiveState':
                        self.SlotList = self.makeItemSlots()
                elif element.tag == 'Equipped':
                    self.Equipped = int(element.text)
                elif element.tag == 'Restrictions':
                    for restriction in element:
                        self.Restrictions.append(restriction.text)
                elif element.tag == 'Slot':
                    index = int(element.attrib['Number'])
                    for attribute in element:
                        if attribute.tag == 'Type':
                            self.getSlot(index).setEffectType(attribute.text)
                        elif attribute.tag == 'Effect':
                            self.getSlot(index).setEffect(attribute.text)
                        elif attribute.tag == 'Amount':
                            self.getSlot(index).setEffectAmount(attribute.text)
                        elif attribute.tag == 'Requirement':
                            self.getSlot(index).setEffectRequirement(attribute.text)
        else:
            return -1

        if 'All' in self.Restrictions:
            self.Restrictions = ['All']

    def exportAsXML(self, filename, export = False, report = False):
        fields = [
            ('Realm', self.Realm),
            ('ActiveState', self.ActiveState),
            ('Type', self.Type),
            ('Name', self.Name),
            ('Level', self.Level),
            ('Quality', self.Quality),
            ('Bonus', self.Bonus),
            ('AFDPS', self.AFDPS),
            ('Speed', self.Speed),
            ('Origin', self.Origin),
            ('DamageType', self.DamageType),
            ('LeftHand', self.LeftHand),
            ('Requirement', self.Requirement),
            ('Restrictions', self.Restrictions),
            ('Notes', self.Notes,)
        ]

        if export:
            fields.extend([
                ('Location', self.Location),
                ('Equipped', self.Equipped),
            ])

        if report:
            fields.extend([
                ('Utility', '%.1f' % self.getUtility()),
                ('Imbue', '%.1f' % sum(self.getImbueValues())),
                ('ImbueMax', str(self.getMaxImbueValue())),
                ('Success', str(self.getOverchargeSuccess())),
            ])

        item = etree.Element('Item')
        for key, value in fields:
            if key != 'Restrictions' and value != '':
                etree.SubElement(item, key).text = str(value)
            elif key == 'Restrictions' and value:
                restrictions = etree.SubElement(item, 'Restrictions')
                for restriction in self.Restrictions:
                    etree.SubElement(restrictions, 'Class').text = restriction
            elif key in ('Location', 'Equipped') and export:
                etree.SubElement(item, key).text = str(value)

        for index in range(0, self.getSlotCount()):
            if self.getSlot(index).getEffectType() != 'Unused':
                slot = etree.SubElement(item, 'Slot', Number = str(index), Type = self.getSlot(index).getSlotType())
                etree.SubElement(slot, 'Type').text = self.getSlot(index).getEffectType()
                etree.SubElement(slot, 'Effect').text = self.getSlot(index).getEffect()
                etree.SubElement(slot, 'Amount').text = self.getSlot(index).getEffectAmount()
                if self.getSlot(index).getEffectRequirement() != '':
                    etree.SubElement(slot, 'Requirement').text = self.getSlot(index).getEffectRequirement()
                if report and self.ActiveState in ('Crafted', 'Legendary'):
                    etree.SubElement(slot, 'GemName').text = self.getSlot(index).getGemName(self.Realm)

        if not export:
            with open(filename, 'wb') as document:
                document.write(etree.tostring(item, encoding = 'UTF-8', pretty_print = True, xml_declaration = True))
                document.close()
        else:
            return item

    def parseLog(self, filename):
        pass


class ItemSlot:

    def __init__(self, itype = '', etype = 'Unused', effect = '', amount = '', requirement = ''):
        self.SlotType = itype
        self.EffectType = etype
        self.Effect = effect
        self.EffectAmount = amount
        self.Requirement = requirement

    def isCraftable(self):
        if self.getSlotType() == 'Craftable':
            return True if (self.getEffectType() not in ('', 'Unused')) else False

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

    def getImbueValue(self, value = 0):
        if not self.isCraftable(): return 0.0
        if self.getEffectType() == 'Skill':
            value = (int(self.getEffectAmount()) - 1) * 5.0
        elif self.getEffectType() == 'Attribute':
            if self.getEffect() not in ('Hit Points', 'Power'):
                value = round((int(self.getEffectAmount()) - 1) / 1.7)
            elif self.getEffect() == 'Hit Points':
                value = int(self.getEffectAmount()) / 4.0
            elif self.getEffect() == 'Power':
                value = (int(self.getEffectAmount()) - 1) * 2.0
        elif self.getEffectType() == 'Resistance':
            value = (int(self.getEffectAmount()) - 1) * 2.0

        return 1.0 if value < 1.0 else value

    def getGemUtility(self):
        if not self.getEffectAmount() or self.getEffectAmount() == '0':
            return 0.0

        if self.getEffectType() == 'Skill':
            return float(int(self.getEffectAmount()) * 5.0)
        elif self.getEffectType() == 'Attribute':
            if self.getEffect() not in ('Hit Points', 'Power'):
                return float((int(self.getEffectAmount()) * 2.0) / 3.0)
            elif self.getEffect() == 'Hit Points':
                return float(int(self.getEffectAmount()) / 4.0)
            elif self.getEffect() == 'Power':
                return float(int(self.getEffectAmount()) * 2.0)
        elif self.getEffectType() == 'Resistance':
            return float(int(self.getEffectAmount()) * 2.0)
        elif self.getEffectType() == 'Focus':
            return float(int(self.getEffectAmount()) * 1.0)
        else:
            return 0.0

    def getGemIndex(self):
        if self.getEffect() in CraftedValuesList[self.getEffectType()]:
            return CraftedValuesList[self.getEffectType()][self.getEffect()].index(self.getEffectAmount())
        elif self.getEffectType() in CraftedValuesList:
            return CraftedValuesList[self.getEffectType()].index(self.getEffectAmount())

    def getGemName(self, realm):
        if self.isCraftable():
            tier = GemNames[self.getGemIndex()]
            prefix = CraftedEffectTable[realm][self.EffectType][self.Effect][0]
            suffix = CraftedEffectTable[realm][self.EffectType][self.Effect][1]
            return tier + ' ' + prefix + ' ' + suffix
        elif self.getSlotType() in ('Dropped', 'Enhanced'):
            return 'Unused' if (self.getEffectType() == 'Unused') else 'Crafted Bonus'
        else:
            return 'None'

    def getGemMaterials(self, realm):
        materials = {'Gems': {}, 'Liquids': {}, 'Dusts': {}}

        if not self.isCraftable():
            return

        table = CraftedEffectTable[realm][self.getEffectType()]
        if self.getEffect() not in table:
            table = CraftedEffectTable['All'][self.getEffectType()]

        index = self.getGemIndex()
        dust = table[self.getEffect()][2]
        liquid = table[self.getEffect()][3]
        materials['Gems'][GemGemsOrder[index]] = 1

        if self.getEffect()[0:4] == 'All ':
            if self.getEffectType() == 'Focus':
                materials['Gems'][GemGemsOrder[index]] = 3
            materials['Dusts'][dust] = (index * 5) + 1
            materials['Liquids'][liquid[0]] = (index * 6) + 2
            materials['Liquids'][liquid[1]] = (index * 6) + 2
            materials['Liquids'][liquid[2]] = (index * 6) + 2
        elif self.getEffectType() == 'Focus' or self.getEffectType() == 'Resistance':
            materials['Dusts'][dust] = (index * 5 + 1)
            materials['Liquids'][liquid] = index + 1
        else:
            materials['Dusts'][dust] = (index * 4) + 1
            materials['Liquids'][liquid] = index + 1

        print(materials.items())
        return materials
