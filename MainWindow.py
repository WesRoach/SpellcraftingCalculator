# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import QAction, Qt, QKeySequence
from PyQt5.QtCore import QSize, QModelIndex, QVariant
from PyQt5.QtGui import QFont, QFontMetrics, QIcon, QIntValidator
from PyQt5.QtWidgets import QLabel, QMainWindow, QMenu, QToolBar, QTreeWidgetItem, QTreeWidgetItemIterator, QStyle, QStyleOptionComboBox
from Character import AllBonusList, ClassList, Races, Realms
from Constants import Cap,  CraftedTypeList, CraftedEffectList, CraftedValuesList, DropTypeList, DropEffectList
from Constants import EnhancedTypeList, EnhancedEffectList, EnhancedValuesList, MythicalCap, SlotList
from Item import Item
from ItemInfoDialog import ItemInformationDialog
import re

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

        self.DistanceToCap = QAction()
        self.UnusableSkills = QAction()

        self.EffectList = list()
        self.EffectTypeList = list()
        self.EnhancedTypeList = list()

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
        self.CurrentClass = ''
        self.CurrentRace = ''
        self.CurrentItemLabel = ''

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

        self.ViewMenu.addAction('&Materials Report', self.showMaterialsReport, QKeySequence(Qt.ALT + Qt.Key_M))
        self.ViewMenu.addAction('&Configuration Report', self.showConfigurationReport, QKeySequence(Qt.ALT + Qt.Key_C))

        self.ViewMenu.addSeparator()

        self.DistanceToCap = QAction('Show Distance to Cap', self)
        self.DistanceToCap.setCheckable(True)
        self.DistanceToCap.setChecked(True)
        self.ViewMenu.addAction(self.DistanceToCap)

        self.UnusableSkills = QAction('Show Unusable Skills', self)
        self.UnusableSkills.setCheckable(True)
        self.UnusableSkills.setChecked(False)
        self.ViewMenu.addAction(self.UnusableSkills)

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

        defaultFixedWidth = 100
        defaultFixedHeight = 20
        buttonFixedWidth = 35
        buttonFixedHeight = 22
        effectWidth = self.setMinimumWidth(["Crowd Control Reduction"])
        effectTypeWidth = self.setMinimumWidth(['Mythical Cap Increase'])
        amountEditWidth = self.setMinimumWidth(['100'])
        amountStaticWidth = self.setMinimumWidth(['100'])

        self.CharacterName.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterRealm.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterClass.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterRace.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterLevel.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.CharacterRealmRank.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
        self.OutfitName.setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))

        for stat in (DropEffectList['All']['Stat'] + ('ArmorFactor', 'Fatigue', 'PowerPool',)):
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
        width = testFont.size(Qt.TextSingleLine, "(-26)", tabArray = None).width()
        self.StatsGroup.layout().setColumnMinimumWidth(3, width)

        for resist in (DropEffectList['All']['Resist']):
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
        width = testFont.size(Qt.TextSingleLine, "(-15)", tabArray = None).width()
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

        self.SlotListTreeView.setFixedWidth(155)
        self.CharacterRealm.insertItems(0, list(Realms))

        self.SwitchOnType = {

            'Crafted': [
                self.GemNameLabel,
                self.ImbuePointsLabel,
                # self.ItemImbuePoints,
                # self.ItemImbuePointsTotal,
                # self.ItemImbuePointsLabel,
                # self.ItemOvercharge,
                # self.ItemOverchargeLabel,
            ],

            'Dropped': [self.RequirementLabel]}

        self.ItemLevel.setFixedSize(QSize(amountEditWidth, defaultFixedHeight))
        self.ItemAddButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemChangeButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemDeleteButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemInfoButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemName.setFixedHeight(defaultFixedHeight)

        for i in range(0, 12):
            self.SlotLabel.append(getattr(self, 'SlotLabel%d' % i))
            self.Effect.append(getattr(self, 'Effect%d' % i))
            self.Effect[i].setFixedSize(QSize(effectWidth, defaultFixedHeight))
            self.Effect[i].activated[str].connect(self.EffectChanged)

            self.EffectType.append(getattr(self, 'EffectType%d' % i))
            self.EffectType[i].setFixedSize(QSize(effectTypeWidth, defaultFixedHeight))
            self.EffectType[i].activated[str].connect(self.EffectTypeChanged)

            self.AmountEdit.append(getattr(self, 'AmountEdit%d' % i))
            self.AmountEdit[i].setFixedSize(QSize(amountEditWidth, defaultFixedHeight))
            self.AmountEdit[i].setValidator(QIntValidator(-999, +999, self))
            self.AmountEdit[i].textEdited[str].connect(self.EffectAmountChanged)
            self.SwitchOnType['Dropped'].append(self.AmountEdit[i])

            self.Requirement.append(getattr(self, 'Requirement%d' % i))
            self.Requirement[i].setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
            self.Requirement[i].editingFinished.connect(self.EffectRequirementChanged)
            self.SwitchOnType['Dropped'].append(self.Requirement[i])

        for i in range(0, 5):
            self.AmountStatic.append(getattr(self, 'AmountStatic%d' % i))
            self.AmountStatic[i].setFixedSize(QSize(amountStaticWidth, defaultFixedHeight))
            self.AmountStatic[i].activated[str].connect(self.EffectAmountChanged)
            self.SwitchOnType['Crafted'].append(self.AmountStatic[i])
            self.GemName.append(getattr(self, 'GemName%d' % i))
            self.SwitchOnType['Crafted'].append(self.GemName[i])

        for i in range(0, 4):
            self.ImbuePoints.append(getattr(self, 'ImbuePoints%d' % i))
            self.SwitchOnType['Crafted'].append(self.ImbuePoints[i])

        for i in range(5, 12):
            self.SwitchOnType['Dropped'].append(self.SlotLabel[i])
            self.SwitchOnType['Dropped'].append(self.EffectType[i])
            self.SwitchOnType['Dropped'].append(self.Effect[i])

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
                    item = Item('Crafted', val, self.CurrentRealm, self.ItemIndex)
                    item.ItemName = 'Crafted Item'
                    self.ItemIndex += 1
                    self.ItemAttributeList[val] = item
                else:
                    item = Item('Dropped', val, self.CurrentRealm, self.ItemIndex)
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
        self.DistanceToCap.triggered.connect(self.setDistanceToCap)
        self.UnusableSkills.triggered.connect(self.setUnusableSkills)
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

    def showCharacterStat(self, stat, state):
        if self.StatLabel[stat].isHidden() != state:
            return
        self.StatLabel[stat].setVisible(state)
        self.StatValue[stat].setVisible(state)
        self.StatCap[stat].setVisible(state)

        try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
            self.StatMythicalCap[stat].setVisible(state)
        except KeyError:
            pass

    def showCraftWidgets(self, item):
        for widget in self.SwitchOnType['Dropped']:
            widget.hide()
        for widget in self.SwitchOnType['Crafted']:
            widget.show()
        for index in range(0, item.getSlotCount()):
            if item.getSlot(index).getSlotType() == 'Craftable':
                self.SlotLabel[index].setText('Gem &%d:' % (index + 1))

        # DEBUGGING
        print('showCraftWidgets')

    def showDropWidgets(self, item):
        for widget in self.SwitchOnType['Crafted']:
            widget.hide()
        for widget in self.SwitchOnType['Dropped']:
            widget.show()
        for index in range(0, item.getSlotCount()):
            if item.getSlot(index).getSlotType() == 'Dropped':
                self.SlotLabel[index].setText('Slot &%d:' % (index + 1))

        # DEBUGGING
        print('showDropWidgets')

    def RestoreItem(self, item):
        if item.ActiveState == 'Crafted':
            self.showCraftWidgets(item)
        elif item.ActiveState == 'Dropped':
            self.showDropWidgets(item)

        # DEBUGGING
        testItem = self.ItemAttributeList['Chest']
        testItem.getSlot(0).setEffectType('Stat')
        testItem.getSlot(0).setEffect('Constitution')
        testItem.getSlot(0).setEffectAmount('20')
        testItem.getSlot(1).setEffectType('Skill')
        testItem.getSlot(1).setEffect('Axe')
        testItem.getSlot(1).setEffectAmount('3')

        self.ItemName.clear()
        self.ItemName.addItem(item.ItemName)
        self.ItemName.setCurrentIndex(0)
        self.ItemLevel.setText(item.ItemLevel)

        for index in range(0, item.getSlotCount()):
            self.EffectTypeChanged(item.getSlot(index).getEffectType(), index)
            # self.EffectChanged(item.getSlot(index).getEffect(), index)
            # self.EffectAmountChanged(item.getSlot(index).getEffectAmount(), index)

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

        for effect in DropEffectList['All']['Stat'] + ('Armor Factor', 'Fatigue', '% Power Pool'):
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

            if effect in DropEffectList['All']['Mythical Stat Cap']:
                BaseMythicalCap = MythicalCap['Stat Cap']
                Total['Stats'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

            if effect == 'Acuity':
                BaseMythicalCap = MythicalCap['Stat Cap']
                for value in AllBonusList[self.CurrentRealm][self.CurrentClass][effect]:
                    Total['Stats'][value]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

            if effect in MythicalCap:
                BaseMythicalCap = MythicalCap[effect]
                Total['Stats'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        for effect in DropEffectList['All']['Resist']:
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

        for effect in DropEffectList['All']['Focus']:
            Total['Focus'][effect] = {}
            Total['Focus'][effect]['Bonus'] = 0
            Total['Focus'][effect]['TotalBonus'] = 0

            Base = Cap['Focus']
            Total['Focus'][effect]['Base'] = int(Level * Base[0]) + Base[1]

        for effect in DropEffectList['All']['Skill']:
            Total['Skills'][effect] = {}
            Total['Skills'][effect]['Bonus'] = 0
            Total['Skills'][effect]['TotalBonus'] = 0

            Base = Cap['Skill']
            Total['Skills'][effect]['Base'] = int(Level * Base[0]) + Base[1]

        for effect in DropEffectList['All']['Mythical Bonus']:
            Total['MythicalBonuses'][effect] = {}
            Total['MythicalBonuses'][effect]['Bonus'] = 0
            Total['MythicalBonuses'][effect]['TotalBonus'] = 0

            try:  # NOT ALL MYTHICAL BONUSES HAVE A CAP ...
                Base = MythicalCap[effect]
            except KeyError:
                Base = MythicalCap['Mythical Bonus']

            Total['MythicalBonuses'][effect]['Base'] = int(Level * Base[0]) + Base[1]

        for effect in DropEffectList['All']['PvE Bonus']:
            Total['PvEBonuses'][effect] = {}
            Total['PvEBonuses'][effect]['Bonus'] = 0
            Total['PvEBonuses'][effect]['TotalBonus'] = 0

            try:  # NOT ALL PVE BONUSES HAVE A CAP ...
                Base = Cap[effect]
            except KeyError:
                Base = Cap['Other Bonus']

            Total['PvEBonuses'][effect]['Base'] = int(Level * Base[0]) + Base[1]

        for effect in DropEffectList['All']['Other Bonus']:
            try:  # NOT ALL BONUSES HAVE A CAP ...
                Base = Cap[effect]
            except KeyError:
                Base = Cap['Other Bonus']

            if effect in ('Armor Factor', 'Fatigue', '% Power Pool'):
                continue

            if effect in ('Casting Speed', 'Archery Speed'):
                effect = 'Archery and Casting Speed'

            if effect in ('Spell Damage', 'Archery Damage'):
                effect = 'Archery and Spell Damage'

            if effect in ('Spell Range', 'Archery Range'):
                effect = 'Archery and Spell Range'

            Total['OtherBonuses'][effect] = {}
            Total['OtherBonuses'][effect]['Bonus'] = 0
            Total['OtherBonuses'][effect]['TotalBonus'] = 0
            Total['OtherBonuses'][effect]['Base'] = int(Level * Base[0]) + Base[1]

        for key, item in self.ItemAttributeList.items():

            # DEBUGGING
            amts = ''

            if not item.ItemEquipped == 2:
                continue

            for index in range(0, item.getSlotCount()):
                effect = item.getSlot(index).getEffect()
                amount = int('0' + re.sub('[^\d]', '', item.getSlot(index).getEffectAmount()))

                if item.getSlot(index).getEffectType() == 'Stat':
                    effects = [effect, ]

                    if effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = Total['Stats'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'] + amts['CapBonus'])

                elif item.getSlot(index).getEffectType() == 'Resist':
                    amts = Total['Resists'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'] + amts['MythicalCapBonus'])

                elif item.getSlot(index).getEffectType() == 'Focus':
                    effects = [effect, ]

                    if effect[0:4] == 'All ':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = Total['Focus'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'Skill':
                    effects = [effect, ]

                    if effect[0:4] == 'All ' and effect in AllBonusList[self.CurrentRealm][self.CurrentClass]:
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = Total['Skills'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'Cap Increase':
                    effects = [effect, ]

                    if effect == 'Power':
                        effects.append('% Power Pool')

                    elif effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = Total['Stats'][effect]
                        amts['TotalCapBonus'] += amount
                        amts['CapBonus'] = min(amts['TotalCapBonus'], amts['BaseCap'])

                elif item.getSlot(index).getEffectType() == 'Mythical Stat Cap':
                    effects = [effect, ]

                    if effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = Total['Stats'][effect]
                        if amts['TotalCapBonus'] < amts['BaseCap']:
                            amts['TotalCapBonus'] += amount
                            if amts['TotalCapBonus'] > amts['BaseCap']:
                                amountOverCapLimit = amts['TotalCapBonus'] - amts['BaseCap']
                                amts['TotalMythicalCapBonus'] += amountOverCapLimit
                                amts['TotalCapBonus'] = amts['TotalCapBonus'] - amountOverCapLimit
                        else:
                            amts['TotalMythicalCapBonus'] += amount
                        amts['MythicalCapBonus'] = min(amts['TotalMythicalCapBonus'], amts['BaseMythicalCap'])

                elif item.getSlot(index).getEffectType() == 'Mythical Resist Cap':
                    amts = Total['Resists'][effect]
                    amts['TotalMythicalCapBonus'] += amount
                    amts['MythicalCapBonus'] = min(amts['TotalMythicalCapBonus'], amts['BaseMythicalCap'])

                elif item.getSlot(index).getEffectType() == 'Mythical Bonus':
                    amts = Total['MythicalBonuses'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'PvE Bonus':
                    amts = Total['PvEBonuses'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'Other Bonus':
                    if effect in ('Armor Factor', 'Fatigue', '% Power Pool'):
                        amts = Total['Stats'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])
                        continue

                    if effect in ('Casting Speed', 'Archery Speed'):
                        effect = 'Archery and Casting Speed'

                    if effect in ('Spell Damage', 'Archery Damage'):
                        effect = 'Archery and Spell Damage'

                    if effect in ('Spell Range', 'Archery Range'):
                        effect = 'Archery and Spell Range'

                    amts = Total['OtherBonuses'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

            # DEBUGGING
            if not amts == '':
                print(amts)

        # DEBUGGING
        print('summarize')

        return Total

    def calculate(self):
        Total = self.summarize()  # TODO: CHANGE TO LOWER / CAMEL CASE

        item = self.ItemAttributeList[self.CurrentItemLabel]
        if item.ActiveState == 'Crafted':
            slotImbueValues = item.getSlotImbueValues()
            itemImbuePoints = item.getItemImbueValue()

            print(slotImbueValues)
            print(str(sum(slotImbueValues)) + ' / ' + str(itemImbuePoints))

            for index in range(0, item.getSlotCount()):
                if index < len(slotImbueValues):
                    self.ImbuePoints[index].setText('%3.1f' % slotImbueValues[index])

        for (key, datum) in list(Total['Stats'].items()):
            Acuity = AllBonusList[self.CurrentRealm][self.CurrentClass]["Acuity"]
            TotalBonus = datum['TotalBonus']

            if key == "Armor Factor":
                key = "ArmorFactor"

            if key == "% Power Pool":
                key = "PowerPool"

            if key[:5] == "Power":
                Skills = AllBonusList[self.CurrentRealm][self.CurrentClass]["All Magic Skills"]
                self.showCharacterStat(key, (datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0)
                              or (len(Skills) > 0))

            elif key == "Fatigue":
                Skills = AllBonusList[self.CurrentRealm][self.CurrentClass]["All Melee Weapon Skills"]
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

            if not self.DistanceToCap.isChecked():
                self.StatValue[key].setText(str(datum['TotalBonus']))
                self.StatCap[key].setText('(' + str(datum['TotalCapBonus']) + ')')
                self.StatMythicalCap[key].setText('(' + str(datum['TotalMythicalCapBonus']) + ')')

            elif self.DistanceToCap.isChecked():

                Base = datum['Base'] + datum['CapBonus'] + datum['MythicalCapBonus']
                BaseCap = datum['BaseCap']

                try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
                    BaseMythicalCap = datum['BaseMythicalCap']
                except KeyError:
                    BaseMythicalCap = 0

                TotalCapBonus = datum['TotalCapBonus']
                TotalMythicalCapBonus = datum['TotalMythicalCapBonus']

                # if TotalCapBonus > BaseCap:
                #     TotalCapBonus = BaseCap

                # if TotalMythicalCapBonus > BaseMythicalCap:
                #    TotalMythicalCapBonus = BaseMythicalCap

                self.StatValue[key].setText(str(int(Base - TotalBonus)))
                self.StatCap[key].setText('(' + str(int(BaseCap - TotalCapBonus)) + ')')
                self.StatMythicalCap[key].setText('(' + str(int(BaseMythicalCap - TotalMythicalCapBonus)) + ')')

                if BaseMythicalCap == 0:
                    self.StatMythicalCap[key].setText('--  ')

        for key, amts in list(Total['Resists'].items()):
            Base = amts['Base'] + amts['MythicalCapBonus']
            TotalBonus = amts['TotalBonus']
            BaseMythicalCap = amts['BaseMythicalCap']
            TotalMythicalCapBonus = amts['TotalMythicalCapBonus']

            if not self.DistanceToCap.isChecked():
                self.StatValue[key].setText(str(amts['TotalBonus']))
                self.StatMythicalCap[key].setText('(' + str(amts['TotalMythicalCapBonus']) + ')')

            elif self.DistanceToCap.isChecked():
                self.StatValue[key].setText(str(int(Base - TotalBonus)))
                self.StatMythicalCap[key].setText('(' + str(int(BaseMythicalCap - TotalMythicalCapBonus)) + ')')

        self.SkillsView.model().removeRows(0, self.SkillsView.model().rowCount())

        for skill, amts in list(Total['Skills'].items()):
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0 and skill[0:4] != 'All ':
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, skill, 'Skill')

        for focus, amts in list(Total['Focus'].items()):
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0 and focus[0:4] != 'All ':
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, focus + ' Focus', 'Focus')

        for bonus, amts in list(Total['MythicalBonuses'].items()):
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0:
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, 'Mythical ' + bonus, 'Bonus')

        for bonus, amts in list(Total['PvEBonuses'].items()):
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0:
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, bonus + ' (PvE)', 'Skill')

        for bonus, amts in list(Total['OtherBonuses'].items()):
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0:
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, bonus, 'Skill')

        # DEBUGGING
        print('calculate')

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
        index = self.sender().objectName()[-2:]
        if not index.isdigit(): index = index[-1:]
        return int(index)

    def insertSkill(self, amount, bonus, group):
        self.SkillsView.model().insertRows(self.SkillsView.model().rowCount(), 1)
        width = 3 if (-10 < amount < 10) else 2
        bonus = "%*d %s" % (width, amount, bonus,)
        index = self.SkillsView.model().index(self.SkillsView.model().rowCount() - 1, 0, QModelIndex())
        self.SkillsView.model().setData(index, QVariant(bonus), Qt.DisplayRole)
        self.SkillsView.model().setData(index, QVariant(group), Qt.UserRole)

        # DEBUGGING
        print('insertSkill')

# =============================================== #
#       CONFIGURATION AND MATERIAL REPORTS        #
# =============================================== #

    def showMaterialsReport(self):

        # DEBUGGING
        print('showMaterialsReport')

    def showConfigurationReport(self):

        # DEBUGGING
        print('showConfigurationReport')

# =============================================== #
#              SLOT/SIGNAL METHODS                #
# =============================================== #

    def mousePressEvent(self, event):
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()' ...
            self.focusWidget().clearFocus()
        except AttributeError:
            pass

        # DEBUGGING
        print('mousePressEvent')

    def setDistanceToCap(self):
        self.calculate()

        # DEBUGGING
        print('setDistanceToCap')

    def setUnusableSkills(self):
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('setNonClassSkills')

    def CharacterRealmChanged(self):
        Realm = self.CharacterRealm.currentText()
        self.CharacterClass.clear()
        self.CharacterClass.insertItems(0, ClassList[Realm])
        self.CurrentRealm = Realm
        self.CharacterClassChanged()

        # DEBUGGING
        print('CharacterRealmChanged')

    def CharacterClassChanged(self):
        Realm = self.CharacterRealm.currentText()
        Class = self.CharacterClass.currentText()
        self.CharacterRace.clear()
        self.CharacterRace.insertItems(0, AllBonusList[Realm][Class]['Races'])
        self.CharacterRaceChanged()
        self.CurrentClass = Class

        if self.CurrentItemLabel != '':
            self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])
            self.calculate()

        # DEBUGGING
        print('CharacterClassChanged')

    def CharacterRaceChanged(self):
        Race = self.CharacterRace.currentText()
        for Resist in DropEffectList['All']['Resist']:
            if Resist in Races['All'][Race]['Resists']:
                self.StatBonus[Resist].setText('+ ' + str(Races['All'][Race]['Resists'][Resist]))
            else:
                self.StatBonus[Resist].setText('-')
        self.CurrentRace = Race

        # DEBUGGING
        print('CharacterRaceChanged')

    def ItemSelected(self, selection):
        for index in self.SlotListTreeView.selectedIndexes():
            selection = index.data()
        for key, value in SlotList.items():
            for val in value:
                if selection == val:
                    self.CurrentItemLabel = val
                    self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('ItemSelected' + ', Selection = ' + str(selection))

    def ItemStateChanged(self, selection, column):
        self.ItemAttributeList[selection.text(column)].ItemEquipped = selection.checkState(column)
        self.RestoreItem(self.ItemAttributeList[selection.text(column)])

        # DEBUGGING
        print('ItemStateChanged')

    def ItemLevelChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.ItemLevel = self.ItemLevel.text()
        self.ItemLevel.setModified(False)
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('ItemLevelChanged')

    def EffectTypeChanged(self, etype = None, index = -1):
        if index == -1: index = self.getSignalSlot()
        item = self.ItemAttributeList[self.CurrentItemLabel]
        self.EffectType[index].clear()

        if item.getSlot(index).getSlotType() == 'Craftable':
            self.EffectType[index].insertItems(0, CraftedTypeList)
        elif item.getSlot(index).getSlotType() == 'Enhanced':
            self.EffectType[index].insertItems(0, EnhancedTypeList)
        elif item.getSlot(index).getSlotType() == 'Dropped':
            self.EffectType[index].insertItems(0, DropTypeList)

        if item.ItemLocation not in ('Two-Handed', 'Spare'):
            self.EffectType[index].removeItem(self.EffectType[index].findText('Focus'))

        self.EffectType[index].setCurrentText(etype)
        item.getSlot(index).setEffectType(etype)

        # CASCADE THE CHANGES ...
        self.EffectChanged(item.getSlot(index).getEffect(), index)

        # DEBUGGING
        print('EffectTypeChanged, EffectType = ' + str(etype))

    # TODO: THIS IS UGLY, LETS CLEAN IT UP ...
    def EffectChanged(self, effect = None, index = -1):
        if index == -1: index = self.getSignalSlot()
        item = self.ItemAttributeList[self.CurrentItemLabel]
        self.Effect[index].clear()

        effectType = item.getSlot(index).getEffectType()
        if item.getSlot(index).getSlotType() == 'Craftable':
            if effectType == 'Skill' and self.UnusableSkills.isChecked():
                self.Effect[index].insertItems(0, AllBonusList['All'][self.CurrentClass]['All Skills'])
            else:
                self.Effect[index].insertItems(0, CraftedEffectList[self.CurrentRealm][effectType])
        elif item.getSlot(index).getSlotType() == 'Enhanced':
            self.Effect[index].insertItems(0, EnhancedEffectList['All'][effectType])
        elif item.getSlot(index).getSlotType() == 'Dropped':
            self.Effect[index].insertItems(0, DropEffectList[self.CurrentRealm][effectType])

        if self.Effect[index].findText(effect) == -1:
            effect = self.Effect[index].currentText()
        self.Effect[index].setCurrentText(effect)
        item.getSlot(index).setEffect(effect)

        # CASCADE THE CHANGES ...
        self.EffectAmountChanged(item.getSlot(index).getEffectAmount(), index)

        # DEBUGGING
        print('EffectChanged, Effect = ' + str(effect))

    # TODO: THIS IS UGLY, LETS CLEAN IT UP ...
    def EffectAmountChanged(self, amount = None, index = -1):
        if index == -1: index = self.getSignalSlot()
        item = self.ItemAttributeList[self.CurrentItemLabel]

        valuesList = list()
        if item.ActiveState == 'Crafted':
            if item.getSlot(index).getEffect()[0:5] == 'All M':
                valuesList = CraftedValuesList[item.getSlot(index).getEffectType()][:1]
            elif item.getSlot(index).getSlotType() == 'Craftable':
                valuesList = CraftedValuesList[item.getSlot(index).getEffectType()]
            elif item.getSlot(index).getSlotType() == 'Enhanced':
                valuesList = EnhancedValuesList[item.getSlot(index).getEffectType()]
            if isinstance(valuesList, dict):
                valuesList = valuesList[item.getSlot(index).getEffect()]
            self.AmountStatic[index].clear()
            self.AmountStatic[index].insertItems(0, valuesList)

            if self.AmountStatic[index].findText(amount) == -1:
                amount = self.AmountStatic[index].currentText()
            self.AmountStatic[index].setCurrentText(amount)
            item.getSlot(index).setEffectAmount(amount)

        elif item.ActiveState == 'Dropped':
            if item.getSlot(index).getEffectType() == 'Unused':
                self.AmountEdit[index].clear()
                item.getSlot(index).setEffectAmount('')
            item.getSlot(index).setEffectAmount(amount)
            self.AmountEdit[index].setText(item.getSlot(index).getEffectAmount())
            self.AmountEdit[index].setModified(False)

        # CASCADE THE CHANGES ...
        self.EffectRequirementChanged(index)
        self.calculate()

        # DEBUGGING
        print('EffectAmountChanged')

    def EffectRequirementChanged(self, index = -1):
        if index == -1: index = self.getSignalSlot()
        item = self.ItemAttributeList[self.CurrentItemLabel]
        if item.getSlot(index).getEffectType() == 'Unused':
            self.Requirement[index].setText('')
            item.getSlot(index).setEffectRequirement('')
        item.getSlot(index).setEffectRequirement(self.Requirement[index].text())
        self.Requirement[index].setText(self.Requirement[index].text())
        self.Requirement[index].setModified(False)

        # DEBUGGING
        print('EffectRequirementChanged')

    def newItem(self):

        # DEBUGGING
        print('newItem')

    def clearCurrentItem(self):

        # DEBUGGING
        print('clearCurrentItem')

    def deleteCurrentItem(self):

        # DEBUGGING
        print('deleteCurrentItem')
