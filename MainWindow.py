# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QMainWindow, QMenu, QToolBar, QTreeWidgetItem, QTreeWidgetItemIterator
from Character import AllBonusList, AllRealms, ClassList, Races, Realms, ItemTypes
from Constants import Cap, DropLists, MythicalCap, DamageTypeList, SourceTypeList
from Item import Item, SlotList


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self, None, Qt.Window)
        uic.loadUi(r'interface/MainWindow.ui', self)

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
        self.ItemInfo = uic.loadUi(r'interface/ItemInformation.ui')

        self.CurrentRealm = ''
        self.CurrentItem = {}
        self.CurrentItemLabel = {}

        self.initMenuBar()
        self.initToolBar()
        self.initLayout()
        self.initControls()
        self.initialize(False)

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

    def initControls(self):
        self.ItemInformationButton.clicked.connect(self.ItemInformation)
        self.SlotListTreeView.itemClicked.connect(self.ItemSelected)
        self.SlotListTreeView.itemChanged.connect(self.ItemStateChanged)
        self.CharacterRealm.activated[int].connect(self.RealmChanged)
        self.CharacterClass.activated[int].connect(self.ClassChanged)
        self.CharacterRace.activated[int].connect(self.RaceChanged)

    def ItemInformation(self):
        # TODO: OVER-RIDE `MainWindow` ICON WITH 'ItemInformation' ICON
        self.ItemInfo.setFont(self.font())
        self.ItemInfo.setWindowFlags(Qt.WindowCloseButtonHint)
        self.ItemInfo.CloseButton.clicked.connect(self.ItemInfo.accept)
        self.ItemInfo.exec_()

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
                    print(self.ItemAttributeList[selection.text(column)].__dict__)

    def showDropWidgets(self, item):
        self.ItemGroup.hide()
        for i in range(0, item.slotCount()):
            # print(item.slot(i).__dict__)
            if item.slot(i).itemType() == 'drop':
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
        for i in range(0, item.slotCount()):
            if item.slot(i).itemType() == 'crafted':
                getattr(self, "SlotLabel{}".format(i)).setText('Gem &%d:' % (i + 1))

            elif item.slot(i).itemType() == 'enhanced':
                getattr(self, "SlotLabel{}".format(i)).setText('Slot &%d:' % (i + 1))

            elif item.slot(i).itemType() == 'effect':
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

    def RestoreItem(self, item):

        # DEBUGGING
        print(item.__dict__)

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

        if item.ItemLocation in SlotList['Weapons']:
            self.ItemInfo.ItemAFDPSLabel.setText('DPS:')
            self.ItemInfo.ItemDamageType.show()
            self.ItemInfo.ItemDamageTypeLabel.show()
            self.ItemInfo.ItemSpeed.show()
            self.ItemInfo.ItemSpeedLabel.show()
            self.ItemInfo.ItemLeftHand.show()

        else:
            self.ItemInfo.ItemAFDPSLabel.setText('AF:')
            self.ItemInfo.ItemDamageType.hide()
            self.ItemInfo.ItemDamageTypeLabel.hide()
            self.ItemInfo.ItemSpeed.hide()
            self.ItemInfo.ItemSpeedLabel.hide()
            self.ItemInfo.ItemLeftHand.hide()

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

        self.ItemInfo.ItemRealm.clear()
        self.ItemInfo.ItemRealm.insertItems(0, realmList)
        self.ItemInfo.ItemRealm.setCurrentIndex(realmList.index(item.ItemRealm))

        # TODO: BASE `currentIndex` ON `item.ItemSource`
        self.ItemInfo.ItemSource.clear()
        self.ItemInfo.ItemSource.insertItems(0, sourceTypes)

        self.ItemInfo.ItemDamageType.clear()
        self.ItemInfo.ItemDamageType.insertItems(0, damageTypes)

        self.ItemInfo.ItemRequirement.setText(item.ItemRequirement)
        self.ItemInfo.ItemNotes.setPlainText(item.ItemNotes)

    def RealmChanged(self, realm):
        Realm = str(self.CharacterRealm.currentText())
        self.CharacterClass.clear()
        self.CharacterClass.insertItems(0, list(ClassList[Realm]))
        self.ClassChanged(self.CharacterClass.currentIndex())
        self.CurrentRealm = Realm

    def ClassChanged(self, realm):
        Realm = str(self.CharacterRealm.currentText())
        Class = str(self.CharacterClass.currentText())
        self.CharacterRace.clear()
        self.CharacterRace.insertItems(0, AllBonusList[Realm][Class]['Races'])
        self.RaceChanged(self.CharacterRace.currentIndex())
        self.calculate()

    def RaceChanged(self, realm):
        Race = str(self.CharacterRace.currentText())
        for Resist in DropLists['All']['Resist']:
            if Resist in Races['All'][Race]['Resists']:
                self.StatBonus[Resist].setText('+ ' + str(Races['All'][Race]['Resists'][Resist]))
            else:
                self.StatBonus[Resist].setText('-')

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
        self.RealmChanged(self.CharacterRealm.currentIndex())
        self.CharacterClass.setCurrentIndex(7)
        self.ClassChanged(self.CharacterClass.currentIndex())
        self.CharacterRace.setCurrentIndex(2)
        self.RaceChanged(self.CharacterRace.currentIndex())

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
