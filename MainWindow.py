# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QFontMetrics, QIcon, QIntValidator
from PyQt5.QtWidgets import QLabel, QMainWindow, QMenu, QToolBar, QTreeWidgetItem, QTreeWidgetItemIterator, QStyle, QStyleOptionComboBox
from Character import AllBonusList, ClassList, Races, Realms
from Constants import Cap, CraftLists, CraftTypeList, DropLists, DropTypeList, EffectTypeList, EnhancedLists, EnhancedTypeList, MythicalCap
from Item import Item, SlotList
from ItemInfoDialog import ItemInformationDialog

Ui_MainWindow = uic.loadUiType(r'interface/MainWindow.ui')[0]


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

        self.SlotLabel = []
        self.Effect = []
        self.EffectType = []
        self.AmountEdit = []
        self.AmountStatic = []
        self.Requirement = []
        self.ImbuePoints = []
        self.GemName = []
        self.SwitchOnType = {}

        # PLACE HOLDER
        self.ItemImbuePoints = QLabel()
        self.ItemImbuePointsTotal = QLabel()
        self.ItemImbuePointsLabel = QLabel()
        self.ItemOvercharge = QLabel()
        self.ItemOverchargeLabel = QLabel()

        self.CurrentRealm = ''
        self.CurrentItem = {}
        self.CurrentItemLabel = {}

        self.initMenuBar()
        self.initToolBar()
        self.initLayout()
        self.initialize()
        self.initControls()

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

        self.setWindowTitle('Spellcrafting Calculator')

        # MAKE SURE WE ARE TESTING WIDTH AND HEIGHT
        # VALUES BASED ON THE FONT BEING USED ...
        testFont = QFontMetrics(self.font())

        # TODO: DYNAMICALLY ASSIGN SIZE
        defaultFixedWidth = 100
        defaultFixedHeight = 20
        effectWidth = self.setMinimumWidth(["Archery and Casting Speed"])
        effectTypeWidth = self.setMinimumWidth(list(DropTypeList))
        amountEditWidth = self.setMinimumWidth(['100'])
        amountStaticWidth = self.setMinimumWidth(['100'])

        self.CharacterName.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterRealm.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterClass.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterRace.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterLevel.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterRealmRank.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.OutfitName.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))

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

        self.SwitchOnType = {

            'craft': [
                self.GemNameLabel,
                self.ImbuePointsLabel,
                # self.ItemImbuePoints,
                # self.ItemImbuePointsTotal,
                # self.ItemImbuePointsLabel,
                # self.ItemOvercharge,
                # self.ItemOverchargeLabel,
            ],

            'drop': [self.RequirementLabel]}

        for i in range(0, 12):
            self.SlotLabel.append(getattr(self, 'SlotLabel%d' % i))
            self.Effect.append(getattr(self, 'Effect%d' % i))
            self.Effect[i].setFixedSize(QSize(effectWidth, defaultFixedHeight))
            self.Effect[i].activated.connect(self.EffectChanged)
            self.Effect[i].editTextChanged.connect(self.EffectChanged)

            self.EffectType.append(getattr(self, 'EffectType%d' % i))
            self.EffectType[i].setFixedSize(QSize(effectTypeWidth, defaultFixedHeight))
            self.EffectType[i].activated.connect(self.EffectTypeChanged)

            self.AmountEdit.append(getattr(self, 'AmountEdit%d' % i))
            self.AmountEdit[i].setFixedSize(QSize(amountEditWidth, defaultFixedHeight))
            self.AmountEdit[i].setValidator(QIntValidator(-999, +999, self))
            self.AmountEdit[i].editingFinished.connect(self.EffectAmountChanged)
            self.SwitchOnType['drop'].append(self.AmountEdit[i])

            self.Requirement.append(getattr(self, 'Requirement%d' % i))
            self.Requirement[i].setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
            self.Requirement[i].editingFinished.connect(self.EffectRequirementChanged)
            self.SwitchOnType['drop'].append(self.Requirement[i])

        for i in range(0, 6):
            self.AmountStatic.append(getattr(self, 'AmountStatic%d' % i))
            self.AmountStatic[i].setFixedSize(QSize(amountStaticWidth, defaultFixedHeight))
            self.AmountStatic[i].activated.connect(self.EffectAmountChanged)
            self.SwitchOnType['craft'].append(self.AmountStatic[i])
            self.GemName.append(getattr(self, 'GemName%d' % i))
            self.SwitchOnType['craft'].append(self.GemName[i])

        for i in range(0, 4):
            self.ImbuePoints.append(getattr(self, 'ImbuePoints%d' % i))
            self.SwitchOnType['craft'].append(self.ImbuePoints[i])

        for i in range(6, 12):
            self.SwitchOnType['drop'].append(self.SlotLabel[i])
            self.SwitchOnType['drop'].append(self.EffectType[i])
            self.SwitchOnType['drop'].append(self.Effect[i])

    def initialize(self):
        self.CharacterName.setText('')
        self.CharacterLevel.setText('50')
        self.CharacterRealmRank.setText('10')

        # SETUP THE INITIAL CHARACTER ...
        self.CharacterRealm.setCurrentIndex(2)
        self.CharacterRealmChanged()
        self.CharacterClass.setCurrentIndex(7)
        self.CharacterClassChanged()
        self.CharacterRace.setCurrentIndex(2)
        self.CharacterRaceChanged()

        for key, value in SlotList.items():
            for val in value:
                if key == 'Armor':
                    item = Item('crafted', val, self.CurrentRealm, self.ItemIndex)
                    item.ItemName = 'Crafted Item'
                    self.ItemIndex += 1
                    self.ItemAttributeList[val] = item
                else:
                    item = Item('drop', val, self.CurrentRealm, self.ItemIndex)
                    item.ItemName = 'Dropped Item'
                    self.ItemIndex += 1
                    self.ItemAttributeList[val] = item

        # SET THE INITIAL SLOT
        self.ItemSelected('Neck')

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

    def initControls(self):
        self.ItemInfoButton.clicked.connect(self.showItemInfoDialog)
        self.SlotListTreeView.itemClicked.connect(self.ItemSelected)
        self.SlotListTreeView.itemChanged.connect(self.ItemStateChanged)
        self.CharacterRealm.activated[int].connect(self.CharacterRealmChanged)
        self.CharacterClass.activated[int].connect(self.CharacterClassChanged)
        self.CharacterRace.activated[int].connect(self.CharacterRaceChanged)
        self.ItemLevel.editingFinished.connect(self.ItemLevelChanged)

    def LoadOptions(self):
        pass

    def SaveOptions(self):
        pass

# =============================================== #
#             DIALOG & WINDOW METHODS             #
# =============================================== #

    def showItemInfoDialog(self):
        currentItem = self.ItemAttributeList[self.CurrentItemLabel]
        self.ItemInfoDialog = ItemInformationDialog(self, Qt.WindowCloseButtonHint, item = currentItem)
        self.ItemInfoDialog.setWindowIcon(QIcon(None))
        self.ItemInfoDialog.exec_()

# =============================================== #
#          LAYOUT CHANGE/UPDATE METHODS           #
# =============================================== #

    def showCharacterStat(self, stat, show):
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
        for widget in self.SwitchOnType['craft']:
            widget.hide()
        for widget in self.SwitchOnType['drop']:
            widget.show()
        for index in range(0, item.getSlotCount() - 3):
            if item.getSlotIndex(index).getSlotType() == 'drop':
                self.SlotLabel[index].setText('Slot &%d:' % (index + 1))

        # DEBUGGING
        print('showDropWidgets')

    def showCraftWidgets(self, item):
        for widget in self.SwitchOnType['drop']:
            widget.hide()
        for widget in self.SwitchOnType['craft']:
            widget.show()
        for index in range(0, item.getSlotCount()):
            if item.getSlotIndex(index).getSlotType() == 'crafted':
                self.SlotLabel[index].setText('Gem &%d:' % (index + 1))
        self.Requirement[4].show()
        self.Requirement[5].show()

        # DEBUGGING
        print('showCraftWidgets')

    def showEffectTypes(self, item):
        activeTypeList = list()
        for slot in range(0, item.getSlotCount()):
            currentSlot = self.EffectType[slot]
            currentSlot.clear()
            if item.ActiveState == 'crafted':
                if item.getSlotIndex(slot).getSlotType() == 'crafted':
                    activeTypeList = list(CraftTypeList)
                if item.getSlotIndex(slot).getSlotType() == 'effect':
                    activeTypeList = list(EffectTypeList)
                if item.getSlotIndex(slot).getSlotType() == 'enhanced':
                    activeTypeList = list(EnhancedTypeList)
            elif item.ActiveState == 'drop':
                activeTypeList = list(DropTypeList)
            currentSlot.insertItems(0, activeTypeList)

        # DEBUGGING
        print('showEffectTypes')

    def RestoreItem(self, item):
        if item.ActiveState == 'crafted':
            self.showCraftWidgets(item)
        elif item.ActiveState == 'drop':
            self.showDropWidgets(item)

        self.ItemName.clear()
        self.ItemName.addItem(item.ItemName)
        self.ItemName.setCurrentIndex(0)
        self.ItemLevel.setText(item.ItemLevel)

        self.showEffectTypes(item)

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
                self.showCharacterStat(key, (datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0)
                              or (len(Skills) > 0))

            elif key == "Fatigue":
                Skills = AllBonusList[Realm][Class]["All Melee Weapon Skills"]
                self.showCharacterStat(key, (datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0)
                              or (len(Skills) > 0))

            elif key == "Acuity":
                self.showCharacterStat(key, ((datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0))
                              and (len(Acuity) == 0))

            elif key in ("Charisma", "Empathy", "Intelligence", "Piety"):
                self.showCharacterStat(key, (datum['TotalCapBonus'] > 0)
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

    def setMinimumWidth(self, items = None):
        font = QFontMetrics(self.font())
        option = QStyleOptionComboBox()
        style = self.style()
        maxWidth = 0
        if items is not None:
            for value in items:
                option.currentText = value
                size = QSize(font.width(option.currentText), font.height())
                maxWidth = max(maxWidth, style.sizeFromContents(QStyle.CT_ComboBox, option, size, self).width())
        elif maxWidth == 0 and self.count() > 0:
            for i in range(0, self.count()):
                option.currentText = self.itemText(i)
                size = QSize(font.width(option.currentText), font.height())
                maxWidth = max(maxWidth, style.sizeFromContents(QStyle.CT_ComboBox, option, size, self).width())
        elif maxWidth == 0:
            option.currentText = ' '
            size = QSize(font.width(option.currentText), font.height())
            maxWidth = max(maxWidth, style.sizeFromContents(QStyle.CT_ComboBox, option, size, self).width())
        return maxWidth

    def getSignalSlot(self):
        index = self.sender().objectName()[-1:]
        return int(index)

# =============================================== #
#              SLOT/SIGNAL METHODS                #
# =============================================== #

    def CharacterRealmChanged(self):
        Realm = self.CharacterRealm.currentText()
        self.CharacterClass.clear()
        self.CharacterClass.insertItems(0, ClassList[Realm])
        self.CharacterClassChanged()
        self.CurrentRealm = Realm

        # DEBUGGING
        print('CharacterRealmChanged')

    def CharacterClassChanged(self):
        Realm = self.CharacterRealm.currentText()
        Class = self.CharacterClass.currentText()
        self.CharacterRace.clear()
        self.CharacterRace.insertItems(0, AllBonusList[Realm][Class]['Races'])
        self.CharacterRaceChanged()
        self.calculate()

        # DEBUGGING
        print('CharacterClassChanged')

    def CharacterRaceChanged(self):
        Race = self.CharacterRace.currentText()
        for Resist in DropLists['All']['Resist']:
            if Resist in Races['All'][Race]['Resists']:
                self.StatBonus[Resist].setText('+ ' + str(Races['All'][Race]['Resists'][Resist]))
            else:
                self.StatBonus[Resist].setText('-')

        # DEBUGGING
        print('CharacterRaceChanged')

    def ItemSelected(self, selection):
        for index in self.SlotListTreeView.selectedIndexes():
            selection = index.data()
        for key, value in SlotList.items():
            for val in value:
                if selection == val:
                    self.CurrentItemLabel = val
                    self.CurrentItem = self.ItemAttributeList[self.CurrentItemLabel]
                    self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('ItemSelected')

    def ItemStateChanged(self, selection, column):
        for key, value in SlotList.items():
            for val in value:
                if selection.text(column) == val:
                    self.ItemAttributeList[selection.text(column)].ItemEquipped = selection.checkState(column)

        # DEBUGGING
        print('ItemStateChanged')

    def ItemLevelChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.ItemLevel = self.ItemLevel.text()
        self.ItemLevel.setModified(False)

        # DEBUGGING
        print('ItemLevelChanged')

    def EffectChanged(self, value = None, slot = -1):

        # DEBUGGING
        print('EffectChanged')

    def EffectTypeChanged(self, value = None, index = -1):

        # DEBUGGING
        print('EffectTypeChanged')

    def EffectAmountChanged(self, amount = None, slot = -1):

        # DEBUGGING
        print('EffectAmountChanged')

    def EffectRequirementChanged(self):

        # DEBUGGING
        print('EffectRequirementChanged')
