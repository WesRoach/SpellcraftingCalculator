# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QDialog, QMainWindow, QMenu, QToolBar, QTreeWidgetItem, QTreeWidgetItemIterator, QListWidgetItem
from Character import AllBonusList, AllRealms, ClassList, Races, Realms
from Constants import Cap, DropLists, MythicalCap, DamageTypeList, SourceTypeList
from Item import Item, SlotList

Ui_MainWindow = uic.loadUiType(r'interface/MainWindow.ui')[0]
Ui_ItemInfoDialog = uic.loadUiType(r'interface/ItemInfoDialog.ui')[0]


class ItemInformationDialog(QDialog, Ui_ItemInfoDialog):
    def __init__(self, parent = None, flags = Qt.Dialog):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None, flags = Qt.Window):
        QMainWindow.__init__(self, parent, flags)
        self.setupUi(self)

        self.FileMenu = QMenu('&File', self)
        self.EditMenu = QMenu('&Edit', self)
        self.ViewMenu = QMenu('&View', self)
        self.ErrorMenu = QMenu('&Errors', self)
        self.HelpMenu = QMenu('&Help', self)
        self.ToolBar = QToolBar("Crafting")

        self.StatLabel = {}
        self.StatValue = {}
        self.StatCap = {}
        self.StatMythicalCap = {}
        self.StatBonus = {}

        self.ItemIndex = 0
        self.ItemAttributeList = {}
        self.ItemInfoDialog = ItemInformationDialog(self)

        self.CurrentRealm = ''
        self.CurrentItem = {}
        self.CurrentItemLabel = {}

        self.initMenuBar()
        self.initToolBar()
        self.initLayout()
        self.initControls()
        self.initialize(False)

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initMenuBar(self):
        self.FileMenu.addAction('E&xit', self.close)

        self.menuBar().addMenu(self.FileMenu)
        self.menuBar().addMenu(self.EditMenu)
        self.menuBar().addMenu(self.ViewMenu)
        self.menuBar().addMenu(self.ErrorMenu)
        self.menuBar().addMenu(self.HelpMenu)

    def initToolBar(self):
        self.ToolBar.setObjectName("Crafting")
        self.ToolBar.setFloatable(False)
        self.ToolBar.addAction('New')

        self.addToolBar(self.ToolBar)

    def initLayout(self):
        font = QFont(self.font())
        font.setFamily("Trebuchet MS")
        font.setPointSize(8)
        self.setFont(font)

        # TODO: DYNAMICALLY ASSIGN SIZE
        # self.setMinimumSize(780, 520)
        self.setWindowTitle('Spellcrafting Calculator')

        # MAKE SURE WE ARE TESTING WIDTH AND HEIGHT
        # VALUES BASED ON THE FONT BEING USED ...
        testFont = QFontMetrics(self.font())

        # TODO: DYNAMICALLY ASSIGN SIZE
        width = 100
        height = 20

        self.CharacterName.setFixedSize(QSize(width, height))
        self.CharacterRealm.setFixedSize(QSize(width, height))
        self.CharacterClass.setFixedSize(QSize(width, height))
        self.CharacterRace.setFixedSize(QSize(width, height))
        self.CharacterLevel.setFixedSize(QSize(width, height))
        self.CharacterRealmRank.setFixedSize(QSize(width, height))
        self.OutfitName.setFixedSize(QSize(width, height))

        for stat in (DropLists['All']['Stat'] + ('ArmorFactor', 'Fatigue', 'PowerPool',)):
            self.StatLabel[stat] = getattr(self, stat + 'Label')
            self.StatValue[stat] = getattr(self, stat)
            self.StatCap[stat] = getattr(self, stat + 'Cap')

            try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
                self.StatMythicalCap[stat] = getattr(self, stat + 'MythicalCap')
            except AttributeError:
                pass

        width = testFont.size(Qt.TextSingleLine, "CON: ", tabArray = None).width()
        self.StatsGroup.layout().setColumnMinimumWidth(0, width)
        width = testFont.size(Qt.TextSingleLine, "400", tabArray = None).width()
        self.StatsGroup.layout().setColumnMinimumWidth(1, width)
        width = testFont.size(Qt.TextSingleLine, "(400)", tabArray = None).width()
        self.StatsGroup.layout().setColumnMinimumWidth(2, width)
        width = testFont.size(Qt.TextSingleLine, "(26)", tabArray = None).width()
        self.StatsGroup.layout().setColumnMinimumWidth(3, width)

        for resist in (DropLists['All']['Resist']):
            self.StatLabel[resist] = getattr(self, resist + 'Label')
            self.StatValue[resist] = getattr(self, resist)
            self.StatBonus[resist] = getattr(self, resist + 'Cap')

            try:  # NOT ALL RESISTS HAVE MYTHICAL CAP ...
                self.StatMythicalCap[resist] = getattr(self, resist + 'MythicalCap')
            except AttributeError:
                pass

        width = testFont.size(Qt.TextSingleLine, "Essence: ", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(0, width)
        width = testFont.size(Qt.TextSingleLine, "26", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(1, width)
        width = testFont.size(Qt.TextSingleLine, "(15)", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(2, width)
        width = testFont.size(Qt.TextSingleLine, "+5", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(3, width)

        for key, value in SlotList.items():
            parent = QTreeWidgetItem(self.SlotListTreeView, [key])
            parent.setFlags(parent.flags() & ~Qt.ItemIsUserCheckable)
            for val in value:
                child = QTreeWidgetItem([val])
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setCheckState(0, Qt.Unchecked)
                parent.addChild(child)

        self.CharacterRealm.insertItems(0, list(Realms))

        tableEntry = QListWidgetItem('All')
        tableEntry.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        tableEntry.setCheckState(Qt.Unchecked)
        self.ItemInfoDialog.ItemRestrictionGroup.setFixedWidth(135)
        self.ItemInfoDialog.ItemClassRestrictionList.clear()
        self.ItemInfoDialog.ItemClassRestrictionList.addItem(tableEntry)

        for key in ClassList['All']:
            tableEntry = QListWidgetItem(key)
            tableEntry.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            tableEntry.setCheckState(Qt.Unchecked)
            self.ItemInfoDialog.ItemClassRestrictionList.addItem(tableEntry)

    def initControls(self):
        self.ItemInformationButton.clicked.connect(self.showItemInfoDialog)
        self.SlotListTreeView.itemClicked.connect(self.ItemSelected)
        self.SlotListTreeView.itemChanged.connect(self.ItemStateChanged)
        self.CharacterRealm.activated[int].connect(self.CharacterRealmChanged)
        self.CharacterClass.activated[int].connect(self.CharacterClassChanged)
        self.CharacterRace.activated[int].connect(self.CharacterRaceChanged)



    def LoadOptions(self):
        pass

    def SaveOptions(self):
        pass

    def initialize(self, boolean):
        self.CharacterName.setText('')
        self.CharacterLevel.setText('50')
        self.CharacterRealmRank.setText('10')

        # SETUP THE INITIAL CHARACTER ...
        self.CharacterRealm.setCurrentIndex(2)
        self.CharacterRealmChanged(self.CharacterRealm.currentIndex())
        self.CharacterClass.setCurrentIndex(7)
        self.CharacterClassChanged(self.CharacterClass.currentIndex())
        self.CharacterRace.setCurrentIndex(2)
        self.CharacterRaceChanged(self.CharacterRace.currentIndex())

        for key, value in SlotList.items():
            for val in value:
                if key == 'Armor':
                    item = Item('crafted', val, self.CurrentRealm, self.ItemIndex)
                    item.ItemName = "Crafted Item"
                    self.ItemIndex += 1
                    self.ItemAttributeList[val] = item
                else:
                    item = Item('drop', val, self.CurrentRealm, self.ItemIndex)
                    item.ItemName = "Dropped Item"
                    self.ItemIndex += 1
                    self.ItemAttributeList[val] = item

        # SET THE INITIAL SLOT
        self.ItemSelected('Neck')

# =============================================== #
#             DIALOG & WINDOW METHODS             #
# =============================================== #

    # TODO: OVER-RIDE `MainWindow` ICON WITH 'ItemInformation' ICON
    def showItemInfoDialog(self):
        self.ItemInfoDialog.setFont(self.font())
        self.ItemInfoDialog.setWindowFlags(self.ItemInfoDialog.windowFlags() | Qt.WindowCloseButtonHint)

        self.ItemInfoDialog.ItemRealm.activated[int].connect(self.ItemRealmChanged)
        self.ItemInfoDialog.ItemClassRestrictionList.itemChanged['QListWidgetItem *'].connect(self.ClassRestrictionsChanged)
        self.ItemInfoDialog.CloseButton.clicked.connect(self.ItemInfoDialog.accept)

        self.ItemInfoDialog.exec_()

# =============================================== #
#          LAYOUT CHANGE/UPDATE METHODS           #
# =============================================== #

    def showStat(self, stat, show):
        if self.StatLabel[stat].isHidden() != show:
            return
        self.StatLabel[stat].setVisible(show)
        self.StatValue[stat].setVisible(show)
        self.StatCap[stat].setVisible(show)

        try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
            self.StatMythicalCap[stat].setVisible(show)
        except KeyError:
            pass

    def showDropWidgets(self, item):
        self.ItemGroup.hide()
        for i in range(0, item.getSlotCount()):
            if item.getSlotIndex(i).getSlotType() == 'drop':
                getattr(self, "SlotLabel{}".format(i)).setText('Slot &%d:' % (i + 1))
                getattr(self, "SlotLabel{}".format(i)).show()
                getattr(self, "EffectType{}".format(i)).show()
                getattr(self, "AmountEdit{}".format(i)).show()
                getattr(self, "Effect{}".format(i)).show()
                getattr(self, "Requirement{}".format(i)).show()
            if i < 6:
                getattr(self, "GemName{}".format(i)).hide()
                getattr(self, "AmountStatic{}".format(i)).hide()
                getattr(self, "AmountEdit{}".format(i)).show()
            if i < 4:
                getattr(self, "ImbuePoints{}".format(i)).hide()

        getattr(self, "ImbuePointsLabel").hide()
        getattr(self, "GemNameLabel").hide()
        getattr(self, "RequirementLabel").show()
        self.ItemGroup.updateGeometry()
        self.ItemGroup.show()

    def showCraftWidgets(self, item):
        self.ItemGroup.hide()

        # TODO: LETS GET AWAY FROM THE GETTERS AND SETTERS
        for i in range(0, item.getSlotCount()):
            if item.getSlotIndex(i).getSlotType() == 'crafted':
                getattr(self, "SlotLabel{}".format(i)).setText('Gem &%d:' % (i + 1))
            elif item.getSlotIndex(i).getSlotType() == 'enhanced':
                getattr(self, "SlotLabel{}".format(i)).setText('Slot &%d:' % (i + 1))
            elif item.getSlotIndex(i).getSlotType() == 'effect':
                getattr(self, "SlotLabel{}".format(i)).setText('Slot &%d:' % (i + 1))

            getattr(self, "GemName{}".format(i)).show()
            getattr(self, "AmountEdit{}".format(i)).hide()
            getattr(self, "AmountStatic{}".format(i)).show()

            if i < 4:
                getattr(self, "Requirement{}".format(i)).hide()
                getattr(self, "ImbuePoints{}".format(i)).show()

        for i in range(6, 12):
            getattr(self, "SlotLabel{}".format(i)).hide()
            getattr(self, "EffectType{}".format(i)).hide()
            getattr(self, "AmountEdit{}".format(i)).hide()
            getattr(self, "Effect{}".format(i)).hide()
            getattr(self, "Requirement{}".format(i)).hide()

        getattr(self, "RequirementLabel").hide()
        getattr(self, "ImbuePointsLabel").show()
        getattr(self, "GemNameLabel").show()
        self.ItemGroup.updateGeometry()
        self.ItemGroup.show()

    def showClassRestrictions(self, item):
        allRealmList = []
        for value in range(self.ItemInfoDialog.ItemClassRestrictionList.count()):
            allRealmList.append(self.ItemInfoDialog.ItemClassRestrictionList.item(value))
        for value in allRealmList:
            value.setHidden(True)
        for key in allRealmList:
            for value in ClassList[item.ItemRealm]:
                if key.text() == 'All':
                    key.setHidden(False)
                if key.text() == value:
                    key.setHidden(False)

    # TODO: NEED TO RE-THINK THIS ...
    def RestoreItem(self, item):
        realmList = {}
        sourceTypes = []
        damageTypes = []

        if item.ActiveState == 'crafted':
            realmList = Realms
            sourceTypes = list(SourceTypeList['Craft'])
            damageTypes = list(DamageTypeList['Craft'])
            self.showCraftWidgets(item)
        elif item.ActiveState == 'drop':
            realmList = AllRealms
            sourceTypes = list(SourceTypeList['Drop'])
            damageTypes = list(DamageTypeList['Drop'])
            self.showDropWidgets(item)

        if item.ItemLocation in SlotList['Jewelery']:
            self.ItemInfoDialog.ItemAFDPS.hide()
            self.ItemInfoDialog.ItemAFDPSLabel.hide()
            self.ItemInfoDialog.ItemDamageType.hide()
            self.ItemInfoDialog.ItemDamageTypeLabel.hide()
            self.ItemInfoDialog.ItemSpeed.hide()
            self.ItemInfoDialog.ItemSpeedLabel.hide()
            self.ItemInfoDialog.ItemLeftHand.hide()
        elif item.ItemLocation in SlotList['Armor']:
            self.ItemInfoDialog.ItemAFDPS.show()
            self.ItemInfoDialog.ItemAFDPSLabel.show()
            self.ItemInfoDialog.ItemAFDPSLabel.setText('AF:')
            self.ItemInfoDialog.ItemDamageType.hide()
            self.ItemInfoDialog.ItemDamageTypeLabel.hide()
            self.ItemInfoDialog.ItemSpeed.hide()
            self.ItemInfoDialog.ItemSpeedLabel.hide()
            self.ItemInfoDialog.ItemLeftHand.hide()
        elif item.ItemLocation in SlotList['Weapons']:
            self.ItemInfoDialog.ItemAFDPS.show()
            self.ItemInfoDialog.ItemAFDPSLabel.show()
            self.ItemInfoDialog.ItemAFDPSLabel.setText('DPS:')
            self.ItemInfoDialog.ItemDamageType.show()
            self.ItemInfoDialog.ItemDamageTypeLabel.show()
            self.ItemInfoDialog.ItemSpeed.show()
            self.ItemInfoDialog.ItemSpeedLabel.show()
            self.ItemInfoDialog.ItemLeftHand.show()

        self.ItemName.clear()
        self.ItemName.addItem(item.ItemName)
        self.ItemName.setCurrentIndex(0)

        iterator = QTreeWidgetItemIterator(self.SlotListTreeView)
        while iterator.value():
            selection = iterator.value()
            if selection.flags() & Qt.ItemIsUserCheckable:
                currentState = self.ItemAttributeList[selection.text(0)].ItemEquipped
                if currentState == 2:
                    selection.setCheckState(0, Qt.Checked)
                elif currentState == 0:
                    selection.setCheckState(0, Qt.Unchecked)
            iterator += 1

        self.ItemInfoDialog.ItemRealm.clear()
        self.ItemInfoDialog.ItemRealm.insertItems(0, realmList)
        self.ItemInfoDialog.ItemRealm.setCurrentIndex(realmList.index(item.ItemRealm))

        # TODO: BASE `currentIndex` ON `item.ItemSource`
        self.ItemInfoDialog.ItemSource.clear()
        self.ItemInfoDialog.ItemSource.insertItems(0, sourceTypes)
        self.ItemInfoDialog.ItemDamageType.clear()
        self.ItemInfoDialog.ItemDamageType.insertItems(0, damageTypes)
        self.ItemInfoDialog.ItemRequirement.setText(item.ItemRequirement)
        self.ItemInfoDialog.ItemNotes.setPlainText(item.ItemNotes)

        self.showClassRestrictions(item)

# =============================================== #
#        SUMMARIZER AND CALCULATOR METHODS        #
# =============================================== #

    def summarize(self):
        Level = int(self.CharacterLevel.text())
        Total = {
            'Utility': 0.0,
            'Stats': {},
            'Resists': {},
            'Skills': {},
            'Focus': {},
            'MythicalBonuses': {},
            'OtherBonuses': {},
            'PvEBonuses': {}
        }

        for effect in DropLists['All']['Resist']:
            Total['Resists'][effect] = {}
            Total['Resists'][effect]['Bonus'] = 0
            Total['Resists'][effect]['TotalBonus'] = 0
            Total['Resists'][effect]['MythicalCapBonus'] = 0
            Total['Resists'][effect]['TotalMythicalCapBonus'] = 0
            Race = str(self.CharacterRace.currentText())

            if effect in Races['All'][Race]['Resists']:
                Total['Resists'][effect]['RacialBonus'] = Races['All'][Race]['Resists'][effect]

            Base = Cap['Resist']
            BaseMythicalCap = MythicalCap['Resist Cap']
            Total['Resists'][effect]['Base'] = int(Level * Base[0]) + Base[1]
            Total['Resists'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        for effect in DropLists['All']['Stat'] + ('Armor Factor', 'Fatigue', '% Power Pool'):
            Total['Stats'][effect] = {}
            Total['Stats'][effect]['Bonus'] = 0
            Total['Stats'][effect]['TotalBonus'] = 0
            Total['Stats'][effect]['CapBonus'] = 0
            Total['Stats'][effect]['TotalCapBonus'] = 0
            Total['Stats'][effect]['MythicalCapBonus'] = 0
            Total['Stats'][effect]['TotalMythicalCapBonus'] = 0

            if effect in Cap:
                Base = Cap[effect]
                BaseCap = Cap[effect + ' Cap']

            else:
                Base = Cap['Stat']
                BaseCap = Cap['Stat Cap']

            Total['Stats'][effect]['Base'] = int(Level * Base[0]) + Base[1]
            Total['Stats'][effect]['BaseCap'] = int(Level * BaseCap[0]) + BaseCap[1]

            if effect in DropLists['All']['Mythical Cap Increase']:
                BaseMythicalCap = MythicalCap['Stat Cap']
                Total['Stats'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

            if effect in MythicalCap:
                BaseMythicalCap = MythicalCap[effect]
                Total['Stats'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        return Total

    def calculate(self):
        Realm = str(self.CharacterRealm.currentText())
        Class = str(self.CharacterClass.currentText())
        Total = self.summarize()

        for key, amounts in list(Total['Resists'].items()):
            Base = amounts['Base']
            TotalBonus = amounts['TotalBonus']
            BaseMythicalCap = amounts['BaseMythicalCap']
            TotalMythicalCapBonus = amounts['TotalMythicalCapBonus']
            self.StatValue[key].setText(str(int(Base - TotalBonus)))
            self.StatMythicalCap[key].setText('(' + str(int(BaseMythicalCap - TotalMythicalCapBonus)) + ')')

        for (key, datum) in list(Total['Stats'].items()):
            Acuity = AllBonusList[Realm][Class]["Acuity"]
            TotalBonus = datum['TotalBonus']

            if key == "Armor Factor":
                key = "ArmorFactor"

            if key == "% Power Pool":
                key = "PowerPool"

            if key[:5] == "Power":
                Skills = AllBonusList[Realm][Class]["All Magic Skills"]
                self.showStat(key, (datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0)
                              or (len(Skills) > 0))

            elif key == "Fatigue":
                Skills = AllBonusList[Realm][Class]["All Melee Weapon Skills"]
                self.showStat(key, (datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0)
                              or (len(Skills) > 0))

            elif key == "Acuity":
                self.showStat(key, ((datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0))
                              and (len(Acuity) == 0))

            elif key in ("Charisma", "Empathy", "Intelligence", "Piety"):
                self.showStat(key, (datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0)
                              or (key in Acuity))

            Base = datum['Base']
            BaseCap = datum['BaseCap']

            try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
                BaseMythicalCap = datum['BaseMythicalCap']
            except KeyError:
                BaseMythicalCap = 0

            if datum['TotalCapBonus'] > 0:
                TotalCapBonus = datum['TotalCapBonus']

            if datum['TotalMythicalCapBonus'] > 0:
                TotalMythicalCapBonus = datum['TotalMythicalCapBonus']

            else:
                TotalCapBonus = 0
                TotalMythicalCapBonus = 0

            if TotalCapBonus > BaseCap:
                TotalCapBonus = BaseCap

            if TotalMythicalCapBonus > BaseMythicalCap:
                TotalMythicalCapBonus = BaseMythicalCap

            self.StatValue[key].setText(str(int(Base + TotalCapBonus) - TotalBonus))
            self.StatCap[key].setText('(' + str(int(BaseCap - TotalCapBonus)) + ')')
            self.StatMythicalCap[key].setText('(' + str(int(BaseMythicalCap - TotalMythicalCapBonus)) + ')')

            if BaseMythicalCap == 0:
                self.StatMythicalCap[key].setText('--  ')

# =============================================== #
#       MISCELLANEOUS METHODS AND FUNCTIONS       #
# =============================================== #

    def placeHolder(self):
        pass

# =============================================== #
#              SLOT/SIGNAL METHODS                #
# =============================================== #

    def CharacterRealmChanged(self, realm):
        Realm = str(self.CharacterRealm.currentText())
        self.CharacterClass.clear()
        self.CharacterClass.insertItems(0, list(ClassList[Realm]))
        self.CharacterClassChanged(self.CharacterClass.currentIndex())
        self.CurrentRealm = Realm

    def CharacterClassChanged(self, realm):
        Realm = str(self.CharacterRealm.currentText())
        Class = str(self.CharacterClass.currentText())
        self.CharacterRace.clear()
        self.CharacterRace.insertItems(0, AllBonusList[Realm][Class]['Races'])
        self.CharacterRaceChanged(self.CharacterRace.currentIndex())
        self.calculate()

    def CharacterRaceChanged(self, realm):
        Race = str(self.CharacterRace.currentText())
        for Resist in DropLists['All']['Resist']:
            if Resist in Races['All'][Race]['Resists']:
                self.StatBonus[Resist].setText('+ ' + str(Races['All'][Race]['Resists'][Resist]))
            else:
                self.StatBonus[Resist].setText('-')

    def ItemTypeChanged(self, item = None):
        pass
        if item is None:
            item = self.ItemAttributeList[self.CurrentItemLabel]
            item.ItemType = self.ItemInfoDialog.ItemType.currentText()

        # DEBUGGING
        print(item.getSlotIndex(0).__dict__)
        print(item.__dict__)

        pass

    def ItemRealmChanged(self, index = None, item = None):
        if item is None:
            item = self.ItemAttributeList[self.CurrentItemLabel]
            item.ItemRealm = self.ItemInfoDialog.ItemRealm.currentText()
        self.showClassRestrictions(item)

    def ClassRestrictionsChanged(self, selection = None):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        if selection.text() == 'All':
            if selection.checkState() == Qt.Checked:
                for count in range(1, self.ItemInfoDialog.ItemClassRestrictionList.count()):
                    self.ItemInfoDialog.ItemClassRestrictionList.item(count).setCheckState(Qt.Unchecked)
                item.ItemRestrictions = ['All']
            elif 'All' in item.ItemRestrictions:
                index = item.ItemRestrictions.index('All')
                del item.ItemRestrictions[index]
        elif selection.checkState() == Qt.Checked:
            self.ItemInfoDialog.ItemClassRestrictionList.item(0).setCheckState(Qt.Unchecked)
            if 'All' in item.ItemRestrictions:
                index = item.ItemRestrictions.index('All')
                del item.ItemRestrictions[index]
            elif selection.text() not in item.ItemRestrictions:
                item.ItemRestrictions.append(selection.text())
        elif selection.text() in item.ItemRestrictions:
            index = item.ItemRestrictions.index(selection.text())
            del item.ItemRestrictions[index]

    def ItemSelected(self, selection):
        for index in self.SlotListTreeView.selectedIndexes():
            selection = index.data()
        for key, value in SlotList.items():
            for val in value:
                if selection == val:
                    self.CurrentItemLabel = val
                    self.CurrentItem = self.ItemAttributeList[self.CurrentItemLabel]
                    self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    def ItemStateChanged(self, selection, column):
        for key, value in SlotList.items():
            for val in value:
                if selection.text(column) == val:
                    self.ItemAttributeList[selection.text(column)].ItemEquipped = selection.checkState(column)
