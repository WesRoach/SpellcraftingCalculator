# HEADER PLACE HOLDER

from Character import ItemTypes
from Constants import CraftedValuesList, GemMaterials, GemMaterialsOrder, GemTierName
from Constants import ImbuePoints, OverchargeBasePercent, OverchargeSkillBonus
from lxml import etree
from math import floor


class Item:

    def __init__(self, state = '', location = '', realm = ''):
        self.State = state
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
        self.SlotList = self.createSlots()

        if self.getParent() == 'Jewelery':
            self.setEquipped(True)
        elif self.getParent() == 'Armor':
            self.setEquipped(True)
        elif self.getParent() == 'Weapons':
            self.setEquipped(False)
        elif self.getParent() == 'Mythical':
            self.setEquipped(False)

        if self.isPlayerCrafted():
            self.setLevel('51')
            self.setOrigin('Crafted')

        if self.getParent() in ('Jewelery', 'Mythical') and self.getState() != 'Imported':
            self.setType(ItemTypes[self.getParent()][location][realm][-1])

        if self.getLocation() == 'Left Hand':
            self.setLeftHand(True)

# =============================================== #
#             BOOLEAN CHECK METHODS               #
# =============================================== #

    def isCrafted(self):
        return True if self.getState() == 'Crafted' else False

    def isLegendary(self):
        return True if self.getState() == 'Legendary' else False

    def isDropped(self):
        return True if self.getState() == 'Dropped' else False

    def isPlayerCrafted(self):
        return True if self.getState() in ('Crafted', 'Legendary') else False

    def isEquipped(self):
        return True if self.Equipped else False

    def isLeftHand(self):
        return True if self.LeftHand else False

# =============================================== #
#                 SETTER METHODS                  #
# =============================================== #

    def setState(self, state):
        self.State = str(state)

    def setEquipped(self, boolean):
        self.Equipped = int(2) if boolean else int(0)

    def setLocation(self, location):
        self.Location = str(location)

    def setRealm(self, realm):
        self.Realm = str(realm)

    def setLevel(self, level):
        self.Level = str(level)

    def setQuality(self, quality):
        self.Quality = str(quality)

    def setType(self, item_type):
        self.Type = str(item_type)

    def setName(self, name):
        self.Name = str(name)

    def setAFDPS(self, af_dps):
        self.AFDPS = str(af_dps)

    def setSpeed(self, speed):
        self.Speed = str(speed)

    def setBonus(self, bonus):
        self.Bonus = str(bonus)

    def setOrigin(self, origin):
        self.Origin = str(origin)

    def setLeftHand(self, boolean):
        self.LeftHand = int(2) if boolean else int(0)

    def setDamageType(self, damage_type):
        self.DamageType = str(damage_type)

    def setNotes(self, notes):
        self.Notes = str(notes)

    def setRequirement(self, requirement):
        self.Requirement = str(requirement)

    def addClassRestriction(self, restriction):
        self.Restrictions.append(restriction)

    def removeClassRestriction(self, restriction):
        self.Restrictions.remove(restriction)

# =============================================== #
#                 GETTER METHODS                  #
# =============================================== #

    def getParent(self):
        for parent, locations in ItemTypes.items():
            if self.getLocation() in locations:
                return parent

    def getState(self):
        return str(self.State)

    def getLocation(self):
        return str(self.Location)

    def getRealm(self):
        return str(self.Realm)

    def getLevel(self):
        return str(self.Level)

    def getQuality(self):
        return str(self.Quality)

    def getType(self):
        return str(self.Type)

    def getName(self):
        return str(self.Name)

    def getAFDPS(self):
        return str(self.AFDPS)

    def getSpeed(self):
        return str(self.Speed)

    def getBonus(self):
        return str(self.Bonus)

    def getOrigin(self):
        return str(self.Origin)

    def getDamageType(self):
        return str(self.DamageType)

    def getRestrictions(self):
        return list(self.Restrictions)

    def getNotes(self):
        return str(self.Notes)

    def getRequirement(self):
        return str(self.Requirement)

    def getSlot(self, index):
        return self.SlotList[index]

    def getSlotList(self):
        return list(self.SlotList)

    def getSlotCount(self):
        return len(self.SlotList)

    def getImbueValues(self):
        imbue_values = []
        for slot in (x for x in self.getSlotList() if x.isCrafted()):
            imbue_values.append(slot.getImbueValue())
        max_value = max(imbue_values)
        for index in range(0, self.getSlotCount()):
            if self.getSlot(index).isCrafted():
                if index == imbue_values.index(max_value): continue
                imbue_values[index] /= 2.0
        return list(imbue_values)

    def getMaxImbueValue(self):
        if 1 <= int(self.getLevel()) <= 51:
            return float(ImbuePoints[int(self.getLevel()) - 1])
        else:
            return float(0.0)

    def getUtility(self):
        return sum([x.getGemUtility() for x in self.getSlotList()])

    def getOverchargeSuccess(self, skill = 1000):
        if sum(self.getImbueValues()) == 0:
            return str('N/A')
        elif sum(self.getImbueValues()) <= (self.getMaxImbueValue() + 1.0):
            return int(100)
        elif sum(self.getImbueValues()) < (self.getMaxImbueValue() + 6.0):
            bonus = OverchargeSkillBonus[(floor(skill / 50) - 1)]
            overcharge = int(floor(sum(self.getImbueValues())) - self.getMaxImbueValue())
            success = OverchargeBasePercent[overcharge] + 44 + 26 + bonus
            return int(success) if int(success) <= 100 else int(100)
        else:
            return int(0)

# =============================================== #
#              MISCELLANEOUS METHODS              #
# =============================================== #

    def clearSlots(self):
        self.SlotList.clear()
        self.SlotList = self.createSlots()

    def createSlots(self):
        item_slots = []
        if self.isCrafted():
            item_slots.append(Slot('Crafted'))
            item_slots.append(Slot('Crafted'))
            item_slots.append(Slot('Crafted'))
            item_slots.append(Slot('Crafted'))
            item_slots.append(Slot('Enhanced'))
        elif self.isLegendary():
            item_slots.append(Slot('Crafted'))
            item_slots.append(Slot('Crafted'))
            item_slots.append(Slot('Crafted'))
            item_slots.append(Slot('Crafted'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
        elif self.isDropped():
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
            item_slots.append(Slot('Dropped'))
        return item_slots

    def getXMLFields(self, export, report):
        xml_fields = {
            'Realm': self.getRealm(),
            'State': self.getState(),
            'Type': self.getType(),
            'Name': self.getName(),
            'Level': self.getLevel(),
            'Quality': self.getQuality(),
            'Bonus': self.getBonus(),
            'AFDPS': self.getAFDPS(),
            'Speed': self.getSpeed(),
            'Origin': self.getOrigin(),
            'DamageType': self.getDamageType(),
            'LeftHand': self.isLeftHand(),
            'Requirement': self.getRequirement(),
            'Restrictions': self.getRestrictions(),
            'Notes': self.getNotes(),
        }

        if export:
            xml_fields['Location'] = self.getLocation()
            xml_fields['Equipped'] = self.isEquipped()

        if report:
            xml_fields['Utility'] = '{:.1f}'.format(self.getUtility())

        if report and self.isPlayerCrafted():
            xml_fields['Imbue'] = '{:.1f}'.format(sum(self.getImbueValues()))
            xml_fields['ImbueMax'] = self.getMaxImbueValue()
            xml_fields['Sucess'] = self.getOverchargeSuccess()

        return xml_fields

# =============================================== #
#                 XML PROCESSING                  #
# =============================================== #

    def importFromXML(self, filename, export = False):
        tree = etree.ElementTree(filename) if export else etree.parse(filename)

        # RETURN ERROR CODE ...
        if tree.getroot().tag != 'Item': return -1

        elements = tree.getroot().getchildren()
        for element in elements:
            if element.tag not in ('Equipped', 'Restrictions', 'Slot', 'State',):
                setattr(self, element.tag, element.text)
            elif element.tag == 'Equipped':
                self.setEquipped(element.text == 'True')
            elif element.tag == 'Restrictions':
                for restriction in element:
                    self.addClassRestriction(restriction.text)
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
            elif element.tag == 'State':
                self.setState(element.text)
                self.SlotList = self.createSlots()

    # TODO: MAKE SURE 'filename' INCLUDES FULL PATH ...
    def exportAsXML(self, filename, export = False, report = False):
        xml_fields = self.getXMLFields(export, report)

        item = etree.Element('Item')
        for attribute, value in xml_fields.items():
            if attribute == 'Restrictions' and value:
                restrictions = etree.SubElement(item, 'Restrictions')
                for restriction in self.getRestrictions():
                    etree.SubElement(restrictions, 'Class').text = restriction
            elif value:
                etree.SubElement(item, attribute).text = str(value)

        for index in range(0, self.getSlotCount()):
            if self.getSlot(index).isUtilized():
                slot = self.getSlot(index)
                slot_element = etree.SubElement(
                    item, 'Slot', Number = str(index), Type = slot.getSlotType()
                )
                etree.SubElement(slot_element, 'Type').text = slot.getEffectType()
                etree.SubElement(slot_element, 'Effect').text = slot.getEffect()
                etree.SubElement(slot_element, 'Amount').text = slot.getEffectAmount()
                if slot.getEffectRequirement():
                    etree.SubElement(slot_element, 'Requirement').text = slot.getEffectRequirement()

                # EXTRA ATTRIBUTES FOR REPORT ...
                if self.isPlayerCrafted() and report:
                    etree.SubElement(slot_element, 'GemName').text = slot.getGemName(self.getRealm())

        if not export:
            with open(filename, 'wb') as document:
                document.write(etree.tostring(item, encoding='UTF-8', pretty_print = True, xml_declaration = True))
        else:
            return item


class Slot:

    def __init__(self, stype = '', etype = 'Unused', effect = '', amount = '', requirement = ''):
        self.SlotType = stype
        self.EffectType = etype
        self.Effect = effect
        self.EffectAmount = amount
        self.Requirement = requirement

# =============================================== #
#             BOOLEAN CHECK METHODS               #
# =============================================== #

    def isCrafted(self):
        return True if self.getSlotType() == 'Crafted' else False

    def isEnhanced(self):
        return True if self.getSlotType() == 'Enhanced' else False

    def isDropped(self):
        return True if self.getSlotType() == 'Dropped' else False

    def isUtilized(self):
        return False if self.getEffectType() == 'Unused' else True

# =============================================== #
#                 SETTER METHODS                  #
# =============================================== #

    def setEffectType(self, etype):
        self.EffectType = str(etype)

    def setEffect(self, effect):
        self.Effect = str(effect)

    def setEffectAmount(self, amount):
        self.EffectAmount = str(amount)

    def setEffectRequirement(self, requirement):
        self.Requirement = str(requirement)

    def setAll(self, etype, effect, amount):
        self.setEffectType(etype)
        self.setEffect(effect)
        self.setEffectAmount(amount)

# =============================================== #
#                 GETTER METHODS                  #
# =============================================== #

    def getSlotType(self):
        return str(self.SlotType)

    def getSlotAttributes(self):
        return str(self.EffectType), str(self.Effect), str(self.EffectAmount)

    def getEffectType(self):
        return str(self.EffectType)

    def getEffect(self):
        return str(self.Effect)

    def getEffectAmount(self):
        return str(self.EffectAmount)

    def getEffectRequirement(self):
        return str(self.Requirement)

    def getImbueValue(self):
        if self.getEffectAmount() in ('', '0'):
            return float(0.0)

        imbue_value = float(0.0)
        if self.getEffectType() == 'Skill':
            imbue_value = (int(self.getEffectAmount()) - 1) * 5.0
        elif self.getEffectType() == 'Attribute':
            if self.getEffect() == 'Hit Points':
                imbue_value = (int(self.getEffectAmount()) / 4.0)
            elif self.getEffect() == 'Power':
                imbue_value = (int(self.getEffectAmount()) - 1) * 2.0
            else:
                imbue_value = round((int(self.getEffectAmount()) - 1) / 1.7)
        elif self.getEffectType() == 'Resistance':
            imbue_value = (int(self.getEffectAmount()) - 1) * 2.0

        return float(1.0 if imbue_value < 1.0 else imbue_value)

    def getGemUtility(self):
        if self.getEffectAmount() in ('', '0'):
            return float(0.0)

        gem_utility = float(0.0)
        if self.getEffectType() == 'Skill':
            gem_utility = float(int(self.getEffectAmount()) * 5.0)
        elif self.getEffectType() == 'Attribute':
            if self.getEffect() == 'Hit Points':
                gem_utility = float(int(self.getEffectAmount()) / 4.0)
            elif self.getEffect() == 'Power':
                gem_utility = float(int(self.getEffectAmount()) * 2.0)
            else:
                gem_utility = float((int(self.getEffectAmount()) * 2.0) / 3.0)
        elif self.getEffectType() == 'Resistance':
            gem_utility = float(int(self.getEffectAmount()) * 2.0)
        elif self.getEffectType() == 'Focus':
            gem_utility = float(int(self.getEffectAmount()) * 1.0)

        return float(gem_utility)

    def getGemIndex(self):
        etype, effect, amount = self.getSlotAttributes()
        if effect in CraftedValuesList[etype]:
            return CraftedValuesList[etype][effect].index(amount)
        elif etype in CraftedValuesList:
            return CraftedValuesList[etype].index(amount)

    def getGemName(self, realm):
        if self.isCrafted() and self.isUtilized():
            tier = GemTierName[self.getGemIndex()]
            realm = realm if (self.getEffectType() in GemMaterials[realm]) else 'All'
            return tier + ' ' + GemMaterials[realm][self.getEffectType()][self.getEffect()]['Gem']
        elif self.isEnhanced() or self.isDropped():
            return 'Crafted Bonus' if self.isUtilized() else 'Unused'
        else:
            return 'None'

    def getGemMaterials(self, realm):
        materials = {'Gems': {}, 'Dusts': {}, 'Liquids': {}}

        index = self.getGemIndex()
        realm = realm if (self.getEffectType() in GemMaterials[realm]) else 'All'
        components = GemMaterials[realm][self.getEffectType()][self.getEffect()]
        materials['Gems'][GemMaterialsOrder['Gems'][index]] = 1

        if self.getEffect().split(None)[0] == 'All':
            if self.getEffectType() == 'Focus':
                materials['Gems'][GemMaterialsOrder['Gems'][index]] = 3
            materials['Dusts'][components['Dust']] = (index * 5) + 1
            materials['Liquids'][components['Liquid'][0]] = (index * 6) + 2
            materials['Liquids'][components['Liquid'][1]] = (index * 6) + 2
            materials['Liquids'][components['Liquid'][2]] = (index * 6) + 2

        elif self.getEffectType() in ('Resistance', 'Focus'):
            materials['Dusts'][components['Dust']] = (index * 5) + 1
            materials['Liquids'][components['Liquid']] = index + 1
        else:
            materials['Dusts'][components['Dust']] = (index * 4) + 1
            materials['Liquids'][components['Liquid']] = index + 1

        return materials
