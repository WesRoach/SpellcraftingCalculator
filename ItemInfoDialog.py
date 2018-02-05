# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QFont, QFontMetrics, QSize
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

        self.initLayout(item)
        self.initItem(item)
        self.initControls()

        self.ItemRealm.setFixedHeight(20)
        self.ItemType.setFixedHeight(20)
        self.ItemSource.setFixedHeight(20)
        self.ItemBonus.setFixedHeight(20)
        self.ItemAFDPS.setFixedHeight(20)
        self.ItemSpeed.setFixedHeight(20)
        self.ItemLeftHand.setFixedHeight(20)
        self.ItemRequirement.setFixedHeight(20)
        self.setFixedSize(QSize(335, 435))

    def initLayout(self, item):
        font = QFont(self.font())
        font.setFamily("Trebuchet MS")
        font.setPointSize(8)
        self.setFont(font)

        self.setWindowTitle('Item Information')

        # MAKE SURE WE ARE TESTING WIDTH AND HEIGHT
        # VALUES BASED ON THE FONT BEING USED ...
        testFont = QFontMetrics(self.font())

        width = testFont.size(Qt.TextSingleLine, "Type:", tabArray = None).width()
        self.ItemInfoGroup.layout().setColumnMinimumWidth(0, width)

        if item.ActiveState == 'Crafted':
            self.RealmList = Realms
            self.SourceTypes.extend(('Crafted',))
            self.DamageTypes.extend(('Slash', 'Thrust', 'Crush', ))
        elif item.ActiveState == 'Legendary':
            self.RealmList = Realms
            self.SourceTypes.extend(('Crafted',))
            self.DamageTypes.extend(('Elemental',))
        elif item.ActiveState == 'Dropped':
            self.RealmList = AllRealms
            self.SourceTypes.extend(('Drop', 'Quest', 'Artifact', 'Merchant',))
            self.DamageTypes.extend(('Slash', 'Thrust', 'Crush',))

        if item.Location in SlotList['Jewelery']:
            self.showJeweleryWidgets()
        elif item.Location in SlotList['Armor']:
            self.showArmorWidgets()
        elif item.Location in SlotList['Weapons']:
            self.showWeaponWidgets()
        elif item.Location in SlotList['Mythical']:
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
        self.ItemRealm.setCurrentIndex(self.RealmList.index(item.Realm))

        if item.Location in SlotList['Jewelery']:
            for key, value in ItemTypes.items():
                if item.Location == key:
                    self.ItemType.clear()
                    self.ItemType.insertItems(0, value)
        elif item.Location in SlotList['Armor']:
            for key, value in ItemTypes.items():
                if item.Location == key:
                    self.ItemType.clear()
                    self.ItemType.insertItems(0, ItemTypes[key][item.Realm])
        elif item.Location in SlotList['Weapons']:
            for key, value in ItemTypes.items():
                if item.Location == key:
                    self.ItemType.clear()
                    self.ItemType.insertItems(0, ItemTypes[key][item.Realm])
        elif item.Location in SlotList['Mythical']:
            for key, value in ItemTypes.items():
                if item.Location in SlotList['Mythical'] == value:
                    self.ItemType.clear()
                    self.ItemType.insertItems(0, ItemTypes[key])

        self.ItemSource.clear()
        self.ItemSource.insertItems(0, self.SourceTypes)
        self.ItemSource.setCurrentIndex(self.SourceTypes.index(item.Origin))

        self.ItemDamageType.clear()
        self.ItemDamageType.insertItems(0, self.DamageTypes)
        self.ItemDamageType.setCurrentIndex(self.DamageTypes.index(item.DamageType))

        self.ItemBonus.setText(item.Bonus)
        self.ItemAFDPS.setText(item.AFDPS)
        self.ItemSpeed.setText(item.Speed)

        if item.LeftHand == 2:
            self.ItemLeftHand.setCheckState(Qt.Checked)
        elif item.LeftHand == 0:
            self.ItemLeftHand.setCheckState(Qt.Unchecked)

        self.ItemRequirement.setText(item.Requirement)
        self.ItemNotes.setPlainText(item.Notes)

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
        self.ItemBonus.setFixedHeight(20)
        self.ItemBonusLabel.setFixedHeight(20)

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
            if self.ItemRestrictionList.item(index).text() in ClassList[item.Realm]:
                self.ItemRestrictionList.item(index).setHidden(False)
        for index in range(self.ItemRestrictionList.count()):
            if self.ItemRestrictionList.item(index).text() in item.Restrictions:
                if self.ItemRestrictionList.item(index).text() in ClassList[item.Realm]:
                    self.ItemRestrictionList.item(index).setCheckState(Qt.Checked)
                if self.ItemRestrictionList.item(index).text() not in ClassList[item.Realm]:
                    self.ItemRestrictionList.item(index).setCheckState(Qt.Unchecked)
                if self.ItemRestrictionList.item(index).text() == 'All':
                    self.ItemRestrictionList.item(index).setCheckState(Qt.Checked)

# =============================================== #
#              SLOT/SIGNAL METHODS                #
# =============================================== #

    def mousePressEvent(self, event):
        focusedWidget = self.focusWidget()
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()'
            focusedWidget.clearFocus()
        except AttributeError:
            pass

    def ItemRealmChanged(self):
        item = self.CurrentItem
        item.Realm = self.ItemRealm.currentText()
        self.showItemRestrictions(item)
        print('ItemRealmChanged')

    def ItemTypeChanged(self):
        item = self.CurrentItem
        item.Type = self.ItemType.currentText()
        print('ItemTypechanged')

    def ItemSourceChanged(self):
        item = self.CurrentItem
        item.Origin = self.ItemSource.currentText()
        print('ItemSourceChanged')

    def ItemDamageTypeChanged(self):
        item = self.CurrentItem
        item.DamageType = self.ItemDamageType.currentText()
        print('ItemDamageTypeChanged')

    def ItemBonusChanged(self):
        item = self.CurrentItem
        item.Bonus = self.ItemBonus.text()
        print('ItemBonusChanged')

    def ItemAFDPSChanged(self):
        item = self.CurrentItem
        item.AFDPS = self.ItemAFDPS.text()
        print('ItemAFDPSChanged')

    def ItemSpeedChanged(self):
        item = self.CurrentItem
        item.Speed = self.ItemSpeed.text()
        self.ItemSpeed.setModified(False)
        print('ItemSpeedChanged')

    def ItemLeftHandChanged(self, state):
        item = self.CurrentItem
        item.LeftHand = state
        print('ItemLeftHandChanged')

    def ItemRequirementChanged(self):
        item = self.CurrentItem
        item.Requirement = self.ItemRequirement.text()
        self.ItemRequirement.setModified(False)
        print('ItemRequirementChanged')

    def ItemNotesChanged(self):
        item = self.CurrentItem
        item.Notes = self.ItemNotes.toPlainText()
        print('ItemNotesChanged')

    def ItemRestrictionsChanged(self, selection = None):
        item = self.CurrentItem
        if selection.text() == 'All' and selection.checkState() == Qt.Checked:
            for count in range(1, self.ItemRestrictionList.count()):
                self.ItemRestrictionList.item(count).setCheckState(Qt.Unchecked)
            item.Restrictions.clear()
            item.Restrictions.append(selection.text())
        elif selection.checkState() == Qt.Checked:
            if selection.text() != 'All' and 'All' in item.Restrictions:
                self.ItemRestrictionList.item(0).setCheckState(Qt.Unchecked)
            item.Restrictions.append(selection.text())
        elif selection.checkState() == Qt.Unchecked:
            item.Restrictions.remove(selection.text())
        print('ItemRestrictionsChanged')
