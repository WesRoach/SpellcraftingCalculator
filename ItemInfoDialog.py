# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDialog, QListWidgetItem
from Constants import AllRealms, ClassList, DamageTypeList, SlotList, SourceTypeList, Realms

Ui_ItemInfoDialog = uic.loadUiType(r'interface/ItemInfoDialog.ui')[0]


class ItemInformationDialog(QDialog, Ui_ItemInfoDialog):
    def __init__(self, parent = None, flags = Qt.Dialog, item = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.RealmList = {}
        self.DamageTypes = ['']
        self.SourceTypes = ['']

        self.initLayout(item)
        self.initControls()
        self.initItem(item)

    def initLayout(self, item):
        tableEntry = QListWidgetItem('All')
        tableEntry.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        tableEntry.setCheckState(Qt.Unchecked)

        self.ItemRestrictionGroup.setFixedWidth(135)
        self.ItemRestrictionList.clear()
        self.ItemRestrictionList.addItem(tableEntry)

        for key in ClassList['All']:
            tableEntry = QListWidgetItem(key)
            tableEntry.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            tableEntry.setCheckState(Qt.Unchecked)
            self.ItemRestrictionList.addItem(tableEntry)

        self.showItemRestrictions(item)

        if item.ItemLocation in SlotList['Jewelery']:
            pass  # ADD & DELETE WIDGETS
        elif item.ItemLocation in SlotList['Armor']:
            pass  # ADD & DELETE WIDGETS
        elif item.ItemLocation in SlotList['Weapons']:
            pass  # ADD & DELETE WIDGETS
        elif item.ItemLocation in SlotList['Mythical']:
            pass  # ADD & DELETE WIDGETS

        if item.ActiveState == 'crafted':
            self.RealmList = Realms
            self.SourceTypes.extend(list(SourceTypeList['Craft']))
            self.DamageTypes.extend(list(DamageTypeList['Craft']))
        elif item.ActiveState == 'drop':
            self.RealmList = AllRealms
            self.SourceTypes.extend(list(SourceTypeList['Drop']))
            self.DamageTypes.extend(list(DamageTypeList['Drop']))

    def initControls(self):
        self.CloseButton.clicked.connect(self.accept)

    def initItem(self, item):
        self.ItemRealm.clear()
        self.ItemRealm.insertItems(0, self.RealmList)
        self.ItemRealm.setCurrentIndex(self.RealmList.index(item.ItemRealm))

        self.ItemSource.clear()
        self.ItemSource.insertItems(0, self.SourceTypes)
        self.ItemSource.setCurrentIndex(self.SourceTypes.index(item.ItemSource))

        self.ItemDamageType.clear()
        self.ItemDamageType.insertItems(0, self.DamageTypes)
        self.ItemDamageType.setCurrentIndex(self.DamageTypes.index(item.ItemDamageType))

        self.ItemBonus.setText(item.ItemBonus)
        self.ItemAFDPS.setText(item.ItemAFDPS)
        self.ItemSpeed.setText(item.ItemSpeed)
        self.ItemRequirement.setText(item.ItemRequirement)
        self.ItemNotes.setPlainText(item.ItemNotes)

    def showJeweleryWidgets(self, item):
        pass

    def showArmorWidgets(self, item):
        pass

    def showWeaponWidgets(self, item):
        pass

    # TODO: MISSING RESTORE FUNCTION
    def showItemRestrictions(self, item):
        allRealmList = []
        for value in range(self.ItemRestrictionList.count()):
            allRealmList.append(self.ItemRestrictionList.item(value))
            self.ItemRestrictionList.item(value).setCheckState(Qt.Unchecked)
        for value in allRealmList:
            value.setHidden(True)
        for key in allRealmList:
            for value in ClassList[item.ItemRealm]:
                if key.text() == 'All':
                    key.setHidden(False)
                if key.text() == value:
                    key.setHidden(False)

    def ItemRealmChanged(self, item):
        item.ItemRealm = self.ItemRealm.currentText()
        self.ItemRestrictionsChanged()
        print('ItemRealmChanged')

    def ItemTypeChanged(self, item):
        item.ItemType = self.ItemType.currentText()
        print('ItemTypechanged')

    def ItemSourceChanged(self, item):
        item.ItemSource = self.ItemSource.currentText()
        print('ItemSourceChanged')

    def ItemDamageTypeChanged(self, item):
        item.ItemDamageType = self.ItemDamageType.currentText()
        print('ItemDamageTypeChanged')

    def ItemBonusChanged(self, item):
        item.ItemBonus = self.ItemBonus.text()
        print('ItemBonusChanged')

    def ItemAFDPSChanged(self, item):
        item.ItemAFDPS = self.ItemAFDPS.text()
        print('ItemAFDPSChanged')

    def ItemSpeedChanged(self, item):
        item.ItemSpeed = self.ItemSpeed.text()
        self.ItemSpeed.setModified(False)
        print('ItemSpeedChanged')

    def ItemLeftHandChanged(self, state, item):
        item.LeftHand = state
        print('ItemLeftHandChanged')

    def ItemRequirementChanged(self, item):
        item.ItemRequirement = self.ItemRequirement.text()
        self.ItemRequirement.setModified(False)
        print('ItemRequirementChanged')

    def ItemNotesChanged(self, item):
        item.ItemNotes = self.ItemNotes.toPlainText()
        print('ItemNotesChanged')

    def ItemRestrictionsChanged(self, selection = None):
        print('ItemRestrictionsChanged')