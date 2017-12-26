# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QFont, QFontMetrics
from PyQt5.QtWidgets import QDialog, QListWidgetItem
from Character import AllRealms, ClassList, ItemTypes, Realms
from Constants import SlotList

Ui_ItemInfoDialog = uic.loadUiType(r'interface/ItemInfoDialog.ui')[0]


class ItemInformationDialog(QDialog, Ui_ItemInfoDialog):
    def __init__(self, parent = None, flags = Qt.Dialog, item = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.CurrentItem = item
        self.RealmList = ()
        self.DamageTypes = ['']
        self.SourceTypes = ['']

        self.initLayout(self.CurrentItem)
        self.initItem(self.CurrentItem)
        self.initControls()

    def initLayout(self, item):
        font = QFont(self.font())
        font.setFamily("Trebuchet MS")
        font.setPointSize(8)
        self.setFont(font)

        self.setWindowTitle('Item Information')

        # MAKE SURE WE ARE TESTING WIDTH AND HEIGHT
        # VALUES BASED ON THE FONT BEING USED ...
        testFont = QFontMetrics(self.font())

        # TODO: NEED TO SET SOME SIZES FOR THE DIALOG
        width = testFont.size(Qt.TextSingleLine, "Type:", tabArray = None).width()
        self.ItemInfoGroup.layout().setColumnMinimumWidth(0, width)

        if item.ActiveState == 'Crafted':
            self.RealmList = Realms
            self.SourceTypes.extend(('Crafted',))
            self.DamageTypes.extend(('Slash', 'Thrust', 'Crush', 'Elemental',))
        elif item.ActiveState == 'Dropped':
            self.RealmList = AllRealms
            self.SourceTypes.extend(('Drop', 'Quest', 'Artifact', 'Merchant',))
            self.DamageTypes.extend(('Slash', 'Thrust', 'Crush',))

        if item.ItemLocation in SlotList['Jewelery']:
            self.showJeweleryWidgets()
        elif item.ItemLocation in SlotList['Armor']:
            self.showArmorWidgets()
        elif item.ItemLocation in SlotList['Weapons']:
            self.showWeaponWidgets()
        elif item.ItemLocation in SlotList['Mythical']:
            self.showMythicalWidgets()

        tableEntry = QListWidgetItem('All')
        tableEntry.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        tableEntry.setCheckState(Qt.Unchecked)

        self.ItemRestrictionList.clear()
        self.ItemRestrictionList.addItem(tableEntry)

        for key in ClassList['All']:
            tableEntry = QListWidgetItem(key)
            tableEntry.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            tableEntry.setCheckState(Qt.Unchecked)
            self.ItemRestrictionList.addItem(tableEntry)

        self.ItemRestrictionGroup.setFixedWidth(135)
        self.showItemRestrictions(item)

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initControls(self):
        self.CloseButton.clicked.connect(self.accept)
        self.ItemRealm.activated.connect(self.ItemRealmChanged)
        self.ItemType.activated.connect(self.ItemTypeChanged)
        self.ItemSource.activated.connect(self.ItemSourceChanged)
        self.ItemDamageType.activated.connect(self.ItemDamageTypeChanged)
        self.ItemBonus.editingFinished.connect(self.ItemBonusChanged)
        self.ItemAFDPS.editingFinished.connect(self.ItemAFDPSChanged)
        self.ItemSpeed.editingFinished.connect(self.ItemSpeedChanged)
        self.ItemLeftHand.stateChanged.connect(self.ItemLeftHandChanged)
        self.ItemRequirement.editingFinished.connect(self.ItemRequirementChanged)
        self.ItemNotes.textChanged.connect(self.ItemNotesChanged)
        self.ItemRestrictionList.itemChanged.connect(self.ItemRestrictionsChanged)

    def initItem(self, item):
        self.ItemRealm.clear()
        self.ItemRealm.insertItems(0, self.RealmList)
        self.ItemRealm.setCurrentIndex(self.RealmList.index(item.ItemRealm))

        if item.ItemLocation in SlotList['Jewelery']:
            for key, value in ItemTypes.items():
                if item.ItemLocation == key:
                    self.ItemType.clear()
                    self.ItemType.insertItems(0, value)
        elif item.ItemLocation in SlotList['Armor']:
            for key, value in ItemTypes.items():
                if item.ItemLocation == key:
                    self.ItemType.clear()
                    self.ItemType.insertItems(0, ItemTypes[key][item.ItemRealm])
        elif item.ItemLocation in SlotList['Weapons']:
            for key, value in ItemTypes.items():
                if item.ItemLocation == key:
                    self.ItemType.clear()
                    self.ItemType.insertItems(0, ItemTypes[key][item.ItemRealm])
        elif item.ItemLocation in SlotList['Mythical']:
            for key, value in ItemTypes.items():
                if item.ItemLocation in SlotList['Mythical'] == value:
                    self.ItemType.clear()
                    self.ItemType.insertItems(0, ItemTypes[key])

        self.ItemSource.clear()
        self.ItemSource.insertItems(0, self.SourceTypes)
        self.ItemSource.setCurrentIndex(self.SourceTypes.index(item.ItemSource))

        self.ItemDamageType.clear()
        self.ItemDamageType.insertItems(0, self.DamageTypes)
        self.ItemDamageType.setCurrentIndex(self.DamageTypes.index(item.ItemDamageType))

        self.ItemBonus.setText(item.ItemBonus)
        self.ItemAFDPS.setText(item.ItemAFDPS)
        self.ItemSpeed.setText(item.ItemSpeed)

        if item.LeftHand == 2:
            self.ItemLeftHand.setCheckState(Qt.Checked)
        elif item.LeftHand == 0:
            self.ItemLeftHand.setCheckState(Qt.Unchecked)

        self.ItemRequirement.setText(item.ItemRequirement)
        self.ItemNotes.setPlainText(item.ItemNotes)

# =============================================== #
#          LAYOUT CHANGE/UPDATE METHODS           #
# =============================================== #

    def showJeweleryWidgets(self):
        self.ItemDamageType.hide()
        self.ItemDamageTypeLabel.hide()
        self.ItemAFDPS.hide()
        self.ItemAFDPSLabel.hide()
        self.ItemSpeed.hide()
        self.ItemSpeedLabel.hide()
        self.ItemLeftHand.hide()
        self.setWidgetSpan(self.ItemBonus, 0, 3)
        self.ItemBonus.setFixedHeight(22)
        self.ItemBonusLabel.setFixedHeight(22)

    def showArmorWidgets(self):
        self.ItemAFDPSLabel.setText('AF:')
        self.ItemDamageType.hide()
        self.ItemDamageTypeLabel.hide()
        self.ItemSpeed.hide()
        self.ItemSpeedLabel.hide()
        self.ItemLeftHand.hide()

    def showWeaponWidgets(self):
        self.ItemAFDPSLabel.setText('DPS:')

    def showMythicalWidgets(self):
        self.ItemDamageType.hide()
        self.ItemDamageTypeLabel.hide()
        self.ItemAFDPS.hide()
        self.ItemAFDPSLabel.hide()
        self.ItemSpeed.hide()
        self.ItemSpeedLabel.hide()
        self.ItemLeftHand.hide()

    def setWidgetSpan(self, widget, rowspan, colspan):
        layout = self.ItemInfoGroup.layout()
        index = layout.indexOf(widget)
        row, column = layout.getItemPosition(index)[:2]
        layout.addWidget(widget, row, column, rowspan, colspan)

    def showItemRestrictions(self, item):
        for index in range(self.ItemRestrictionList.count()):
            self.ItemRestrictionList.item(index).setHidden(True)
            if self.ItemRestrictionList.item(index).text() == 'All':
                self.ItemRestrictionList.item(index).setHidden(False)
            if self.ItemRestrictionList.item(index).text() in ClassList[item.ItemRealm]:
                self.ItemRestrictionList.item(index).setHidden(False)
        for index in range(self.ItemRestrictionList.count()):
            if self.ItemRestrictionList.item(index).text() in item.ItemRestrictions:
                if self.ItemRestrictionList.item(index).text() in ClassList[item.ItemRealm]:
                    self.ItemRestrictionList.item(index).setCheckState(Qt.Checked)
                if self.ItemRestrictionList.item(index).text() not in ClassList[item.ItemRealm]:
                    self.ItemRestrictionList.item(index).setCheckState(Qt.Unchecked)

# =============================================== #
#              SLOT/SIGNAL METHODS                #
# =============================================== #

    def ItemRealmChanged(self):
        item = self.CurrentItem
        item.ItemRealm = self.ItemRealm.currentText()
        self.showItemRestrictions(item)
        print('ItemRealmChanged')

    def ItemTypeChanged(self):
        item = self.CurrentItem
        item.ItemType = self.ItemType.currentText()
        print('ItemTypechanged')

    def ItemSourceChanged(self):
        item = self.CurrentItem
        item.ItemSource = self.ItemSource.currentText()
        print('ItemSourceChanged')

    def ItemDamageTypeChanged(self):
        item = self.CurrentItem
        item.ItemDamageType = self.ItemDamageType.currentText()
        print('ItemDamageTypeChanged')

    def ItemBonusChanged(self):
        item = self.CurrentItem
        item.ItemBonus = self.ItemBonus.text()
        print('ItemBonusChanged')

    def ItemAFDPSChanged(self):
        item = self.CurrentItem
        item.ItemAFDPS = self.ItemAFDPS.text()
        print('ItemAFDPSChanged')

    def ItemSpeedChanged(self):
        item = self.CurrentItem
        item.ItemSpeed = self.ItemSpeed.text()
        self.ItemSpeed.setModified(False)
        print('ItemSpeedChanged')

    def ItemLeftHandChanged(self, state):
        item = self.CurrentItem
        item.LeftHand = state
        print('ItemLeftHandChanged')

    def ItemRequirementChanged(self):
        item = self.CurrentItem
        item.ItemRequirement = self.ItemRequirement.text()
        self.ItemRequirement.setModified(False)
        print('ItemRequirementChanged')

    def ItemNotesChanged(self):
        item = self.CurrentItem
        item.ItemNotes = self.ItemNotes.toPlainText()
        print('ItemNotesChanged')

    def ItemRestrictionsChanged(self, selection = None):
        item = self.CurrentItem
        if selection.text() == 'All' and selection.checkState() == Qt.Checked:
            for count in range(1, self.ItemRestrictionList.count()):
                self.ItemRestrictionList.item(count).setCheckState(Qt.Unchecked)
            item.ItemRestrictions.clear()
            item.ItemRestrictions.append(selection.text())
        elif selection.checkState() == Qt.Checked:
            if selection.text() != 'All' and 'All' in item.ItemRestrictions:
                self.ItemRestrictionList.item(0).setCheckState(Qt.Unchecked)
            item.ItemRestrictions.append(selection.text())
        elif selection.checkState() == Qt.Unchecked:
            item.ItemRestrictions.remove(selection.text())
        print('ItemRestrictionsChanged')
