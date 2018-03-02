# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QFontMetrics, QIcon, QSize
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
        self.OriginTypes = ['']

        self.initLayout(item)
        self.initItem(item)
        self.initControls()

    def initLayout(self, item):
        self.setWindowTitle('Item Information')
        self.setWindowIcon(QIcon(None))

        # MAKE SURE WE ARE TESTING WIDTH AND HEIGHT
        # VALUES BASED ON THE FONT BEING USED ...
        testFont = QFontMetrics(self.font())

        width = testFont.size(Qt.TextSingleLine, "Type:", tabArray = None).width()
        self.ItemInfoGroup.layout().setColumnMinimumWidth(0, width)

        defaultFixedHeight = 20
        self.ItemRealm.setFixedHeight(defaultFixedHeight)
        self.ItemType.setFixedHeight(defaultFixedHeight)
        self.ItemOrigin.setFixedHeight(defaultFixedHeight)
        self.ItemBonus.setFixedHeight(defaultFixedHeight)
        self.ItemAFDPS.setFixedHeight(defaultFixedHeight)
        self.ItemSpeed.setFixedHeight(defaultFixedHeight)
        self.ItemLeftHand.setFixedHeight(defaultFixedHeight)
        self.ItemRequirement.setFixedHeight(defaultFixedHeight)
        self.setFixedSize(QSize(335, 435))

        if item.ActiveState == 'Crafted':
            self.RealmList = Realms
            self.OriginTypes.extend(('Crafted',))
            self.DamageTypes.extend(('Slash', 'Thrust', 'Crush', ))
        elif item.ActiveState == 'Legendary':
            self.RealmList = Realms
            self.OriginTypes.extend(('Crafted',))
            self.DamageTypes.extend(('Elemental',))
        elif item.ActiveState == 'Dropped':
            self.RealmList = AllRealms
            self.OriginTypes.extend(('Drop', 'Quest', 'Artifact', 'Merchant',))
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

        self.ItemRestrictionsList.clear()
        self.ItemRestrictionsList.addItem(tableEntry)

        for key in ClassList['All']:
            tableEntry = QListWidgetItem(key)
            tableEntry.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            tableEntry.setCheckState(Qt.Unchecked)
            self.ItemRestrictionsList.addItem(tableEntry)

        self.ItemRestrictionsGroup.setFixedWidth(135)
        self.showItemRestrictions(item)

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initControls(self):
        self.CloseButton.clicked.connect(self.accept)
        self.ItemRealm.activated.connect(self.ItemRealmChanged)
        self.ItemType.activated.connect(self.ItemTypeChanged)
        self.ItemOrigin.activated.connect(self.ItemOriginChanged)
        self.ItemDamageType.activated.connect(self.ItemDamageTypeChanged)
        self.ItemBonus.editingFinished.connect(self.ItemBonusChanged)
        self.ItemAFDPS.editingFinished.connect(self.ItemAFDPSChanged)
        self.ItemSpeed.editingFinished.connect(self.ItemSpeedChanged)
        self.ItemLeftHand.stateChanged.connect(self.ItemLeftHandChanged)
        self.ItemRequirement.editingFinished.connect(self.ItemRequirementChanged)
        self.ItemNotes.textChanged.connect(self.ItemNotesChanged)
        self.ItemRestrictionsList.itemChanged.connect(self.ItemRestrictionsChanged)

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
        self.ItemType.setCurrentText(item.Type)

        self.ItemOrigin.clear()
        self.ItemOrigin.insertItems(0, self.OriginTypes)
        self.ItemOrigin.setCurrentIndex(self.OriginTypes.index(item.Origin))

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
        for index in range(self.ItemRestrictionsList.count()):
            self.ItemRestrictionsList.item(index).setHidden(True)
            if self.ItemRestrictionsList.item(index).text() == 'All':
                self.ItemRestrictionsList.item(index).setHidden(False)
            if self.ItemRestrictionsList.item(index).text() in ClassList[item.Realm]:
                self.ItemRestrictionsList.item(index).setHidden(False)
        for index in range(self.ItemRestrictionsList.count()):
            if self.ItemRestrictionsList.item(index).text() in item.Restrictions:
                if self.ItemRestrictionsList.item(index).text() in ClassList[item.Realm]:
                    self.ItemRestrictionsList.item(index).setCheckState(Qt.Checked)
                if self.ItemRestrictionsList.item(index).text() not in ClassList[item.Realm]:
                    self.ItemRestrictionsList.item(index).setCheckState(Qt.Unchecked)
                if self.ItemRestrictionsList.item(index).text() == 'All':
                    self.ItemRestrictionsList.item(index).setCheckState(Qt.Checked)

# =============================================== #
#              SLOT/SIGNAL METHODS                #
# =============================================== #

    def mousePressEvent(self, event):
        focusedWidget = self.focusWidget()
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()'
            focusedWidget.clearFocus()
        except AttributeError:
            pass

    # TODO: UPDATE ITEM TYPE AND DAMAGE LIST WHEN REALM CHANGES
    def ItemRealmChanged(self):
        item = self.CurrentItem
        item.Realm = self.ItemRealm.currentText()
        self.showItemRestrictions(item)
        print('ItemRealmChanged')

    # TODO: ACCOUNT FOR MIS-LABELED ITEMS
    def ItemTypeChanged(self):
        item = self.CurrentItem
        item.Type = self.ItemType.currentText()
        print('ItemTypeChanged')

    def ItemOriginChanged(self):
        item = self.CurrentItem
        item.Origin = self.ItemOrigin.currentText()
        print('ItemOriginChanged')

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
            for count in range(1, self.ItemRestrictionsList.count()):
                self.ItemRestrictionsList.item(count).setCheckState(Qt.Unchecked)
            item.Restrictions.clear()
            item.Restrictions.append(selection.text())
        elif selection.checkState() == Qt.Checked:
            if selection.text() != 'All' and 'All' in item.Restrictions:
                self.ItemRestrictionsList.item(0).setCheckState(Qt.Unchecked)
            item.Restrictions.append(selection.text())
        elif selection.checkState() == Qt.Unchecked:
            item.Restrictions.remove(selection.text())
        print('ItemRestrictionsChanged')
