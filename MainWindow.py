# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import QAction, Qt, QKeySequence
from PyQt5.QtCore import QSize, QModelIndex, QVariant
from PyQt5.QtGui import QFontMetrics, QIcon, QIntValidator
from PyQt5.QtWidgets import QFileDialog, QLabel, QMainWindow, QMenu, QToolBar, QTreeWidgetItem, QTreeWidgetItemIterator, QStyle, QStyleOptionComboBox
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
        self.ItemNewMenu = QMenu('&New Item', self)
        self.ItemTypeMenu = QMenu('Item &Type', self)
        self.ItemSwapMenu = QMenu('S&wap Gems with',self)
        self.ItemMoveMenu = QMenu('&Move Item to', self)
        self.ToolBarMenu = QMenu('&Toolbar', self)
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
        self.ItemDictionary = {}

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
        self.initItemToolBar()
        self.initLayout()
        self.initialize()
        self.initControls()

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def getIcon(self, name):
        icon = QIcon()

        for size in (16, 24, 32):
            icon.addFile(r'images/normal/' + name + str(size) + '.png', QSize(size, size), QIcon.Normal, QIcon.Off)
            icon.addFile(r'images/active/' + name + str(size) + '.png', QSize(size, size), QIcon.Active, QIcon.Off)
            icon.addFile(r'images/disabled/' + name + str(size) + '.png', QSize(size, size), QIcon.Disabled, QIcon.Off)

        return icon

    def initMenuBar(self):
        self.FileMenu.addAction('E&xit', self.close, QKeySequence(Qt.CTRL + Qt.Key_X))

        self.EditMenu.addAction('Load Item ...', self.loadItem)
        self.EditMenu.addAction('Save Item ...', self.saveItem)
        self.EditMenu.addSeparator()
        self.EditMenu.addMenu(self.ItemTypeMenu)
        self.EditMenu.addMenu(self.ItemMoveMenu)
        self.EditMenu.addMenu(self.ItemSwapMenu)
        self.EditMenu.addSeparator()
        self.EditMenu.addMenu(self.ItemNewMenu)
        self.EditMenu.addAction('Delete Item', self.deleteItem)
        self.EditMenu.addAction('Clear Item', self.clearItem)
        self.EditMenu.addAction('Clear Slots', self.clearItemSlots)

        self.ViewMenu.addAction('&Materials Report', self.showMaterialsReport, QKeySequence(Qt.ALT + Qt.Key_M))
        self.ViewMenu.addAction('&Configuration Report', self.showConfigurationReport, QKeySequence(Qt.ALT + Qt.Key_C))

        self.ViewMenu.addSeparator()

        for (title, res) in (("Large", 32,), ("Normal", 24,), ("Small", 16,), ("Hide", 0,),):
            action = QAction(title, self)
            action.setData(QVariant(res))
            action.setCheckable(True)
            self.ToolBarMenu.addAction(action)

        self.ToolBarMenu.actions()[1].setChecked(True)
        self.ViewMenu.addMenu(self.ToolBarMenu)

        self.ViewMenu.addSeparator()

        self.DistanceToCap = QAction('&Distance to Cap', self)
        self.DistanceToCap.setShortcut(QKeySequence(Qt.ALT + Qt.Key_D))
        self.DistanceToCap.setCheckable(True)
        self.DistanceToCap.setChecked(True)
        self.ViewMenu.addAction(self.DistanceToCap)

        self.UnusableSkills = QAction('&Unusable Skills', self)
        self.UnusableSkills.setShortcut(QKeySequence(Qt.ALT + Qt.Key_U))
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
        self.ToolBar.addAction('New Template')
        self.ToolBar.addAction('Open Template')
        self.ToolBar.addAction('Save Template')
        self.ToolBar.addAction('Save Template As')
        self.ToolBar.addSeparator()
        self.ToolBar.addAction('Export Gems')
        self.ToolBar.addSeparator()
        self.ToolBar.addAction('Material Report', self.showMaterialsReport)
        self.ToolBar.addAction('Configuration Report', self.showConfigurationReport)
        self.addToolBar(self.ToolBar)

    def initItemToolBar(self):
        self.ItemNewButton.setMenu(self.ItemNewMenu)
        self.ItemNewButton.setToolTip('Create New Item')
        self.ItemNewButton.clicked.connect(self.ItemNewButton.showMenu)

        self.ItemTypeButton.setMenu(self.ItemTypeMenu)
        self.ItemTypeButton.setToolTip('Change Item Type')
        self.ItemTypeButton.clicked.connect(self.ItemTypeButton.showMenu)

        self.ItemLoadButton.setToolTip('Load Item')
        self.ItemDeleteButton.setToolTip('Delete Item')
        self.ItemSaveButton.setToolTip('Save Item')
        self.ItemInfoButton.setToolTip('Item Information')

    def initLayout(self):
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
        width = testFont.size(Qt.TextSingleLine, "Imbue", tabArray=None).width()
        self.ItemFrame.layout().setColumnMinimumWidth(4, width)

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

            'Legendary': [
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
        self.ItemQuality.setFixedSize(QSize(amountEditWidth, defaultFixedHeight))
        self.ItemNewButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemTypeButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemLoadButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemDeleteButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemSaveButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemInfoButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemName.setFixedHeight(defaultFixedHeight)

        for index in range(0, 12):
            self.SlotLabel.append(getattr(self, 'SlotLabel%d' % index))
            self.Effect.append(getattr(self, 'Effect%d' % index))
            self.Effect[index].setFixedSize(QSize(effectWidth, defaultFixedHeight))
            self.Effect[index].activated[str].connect(self.EffectChanged)

            self.AmountEdit.append(getattr(self, 'AmountEdit%d' % index))
            self.AmountEdit[index].setFixedSize(QSize(amountEditWidth, defaultFixedHeight))
            self.AmountEdit[index].setValidator(QIntValidator(-999, +999, self))
            self.AmountEdit[index].textEdited[str].connect(self.EffectAmountChanged)

            self.EffectType.append(getattr(self, 'EffectType%d' % index))
            self.EffectType[index].setFixedSize(QSize(effectTypeWidth, defaultFixedHeight))
            self.EffectType[index].activated[str].connect(self.EffectTypeChanged)

            self.Requirement.append(getattr(self, 'Requirement%d' % index))
            self.Requirement[index].setFixedSize(QSize(defaultFixedWidth, defaultFixedHeight))
            self.Requirement[index].editingFinished.connect(self.EffectRequirementChanged)

        for index in range(0, 7):
            self.GemName.append(getattr(self, 'GemName%d' % index))

        for index in range(0, 5):
            self.AmountStatic.append(getattr(self, 'AmountStatic%d' % index))
            self.AmountStatic[index].setFixedSize(QSize(amountStaticWidth, defaultFixedHeight))
            self.AmountStatic[index].activated[str].connect(self.EffectAmountChanged)

        for index in range(0, 4):
            self.ImbuePoints.append(getattr(self, 'ImbuePoints%d' % index))

        testItem = Item('Crafted', 'None')
        for index in range(0, testItem.getSlotCount()):
            self.SwitchOnType['Crafted'].append(self.SlotLabel[index])
            self.SwitchOnType['Crafted'].append(self.EffectType[index])
            self.SwitchOnType['Crafted'].append(self.AmountStatic[index])
            self.SwitchOnType['Crafted'].append(self.Effect[index])
            self.SwitchOnType['Crafted'].append(self.GemName[index])
            if index < 4:
                self.SwitchOnType['Crafted'].append(self.ImbuePoints[index])

        testItem = Item('Legendary', 'None')
        for index in range(0, testItem.getSlotCount()):
            self.SwitchOnType['Legendary'].append(self.SlotLabel[index])
            self.SwitchOnType['Legendary'].append(self.EffectType[index])
            self.SwitchOnType['Legendary'].append(self.Effect[index])
            self.SwitchOnType['Legendary'].append(self.GemName[index])
            if index < 4:
                self.SwitchOnType['Legendary'].append(self.AmountStatic[index])
                self.SwitchOnType['Legendary'].append(self.ImbuePoints[index])
            if index > 3:
                self.SwitchOnType['Legendary'].append(self.AmountEdit[index])

        testItem = Item('Dropped', 'None')
        for index in range(0, testItem.getSlotCount()):
            self.SwitchOnType['Dropped'].append(self.SlotLabel[index])
            self.SwitchOnType['Dropped'].append(self.EffectType[index])
            self.SwitchOnType['Dropped'].append(self.AmountEdit[index])
            self.SwitchOnType['Dropped'].append(self.Effect[index])
            self.SwitchOnType['Dropped'].append(self.Requirement[index])

        # COLLECTING GARBAGE
        del testItem

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
                    item.Name = item.ActiveState + ' Item'
                    self.ItemIndex += 1
                    self.ItemAttributeList[val] = item
                    self.ItemDictionary[val] = [item]
                else:
                    item = Item('Dropped', val, self.CurrentRealm, self.ItemIndex)
                    item.Name = item.ActiveState + ' Item'
                    self.ItemIndex += 1
                    self.ItemAttributeList[val] = item
                    self.ItemDictionary[val] = [item]

        # SET THE INITIAL SLOT
        self.ItemSelected('Neck')

        iterator = QTreeWidgetItemIterator(self.SlotListTreeView)
        while iterator.value():
            selection = iterator.value()
            if selection.flags() & Qt.ItemIsUserCheckable:
                currentState = self.ItemAttributeList[selection.text(0)].Equipped
                if currentState == 2:
                    selection.setCheckState(0, Qt.Checked)
                elif currentState == 0:
                    selection.setCheckState(0, Qt.Unchecked)
            iterator += 1

    def initControls(self):
        self.ItemNewMenu.triggered.connect(self.newItem)
        self.ItemTypeMenu.triggered.connect(self.changeItemType)
        self.ToolBarMenu.triggered.connect(self.setToolBarOptions)
        self.DistanceToCap.triggered.connect(self.setDistanceToCap)
        self.UnusableSkills.triggered.connect(self.setUnusableSkills)
        self.ItemInfoButton.clicked.connect(self.showItemInfoDialog)
        self.SlotListTreeView.itemClicked.connect(self.ItemSelected)
        self.SlotListTreeView.itemChanged.connect(self.ItemStateChanged)
        self.CharacterRealm.activated[int].connect(self.CharacterRealmChanged)
        self.CharacterClass.activated[int].connect(self.CharacterClassChanged)
        self.CharacterRace.activated[int].connect(self.CharacterRaceChanged)
        self.ItemLevel.editingFinished.connect(self.ItemLevelChanged)
        self.ItemQuality.editingFinished.connect(self.ItemQualityChanged)
        self.ItemName.activated[int].connect(self.changeItem)
        self.ItemName.editTextChanged[str].connect(self.ItemNameChanged)
        self.ItemLoadButton.clicked.connect(self.loadItem)
        self.ItemSaveButton.clicked.connect(self.saveItem)
        self.ItemDeleteButton.clicked.connect(self.deleteItem)

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
        for widget in self.SwitchOnType['Legendary']:
            widget.hide()
        for widget in self.SwitchOnType['Dropped']:
            widget.hide()
        for widget in self.SwitchOnType['Crafted']:
            widget.show()
        for index in range(0, item.getSlotCount()):
            if item.getSlot(index).getSlotType() == 'Craftable':
                self.SlotLabel[index].setText('Gem &%d:' % (index + 1))
            if item.getSlot(index).getSlotType() == 'Dropped':
                self.EffectType[index].setDisabled(False)
                self.Effect[index].setDisabled(False)
                self.AmountEdit[index].setDisabled(False)

        # DEBUGGING
        print('showCraftWidgets')

    def showLegendaryWidgets(self, item):
        for widget in self.SwitchOnType['Dropped']:
            widget.hide()
        for widget in self.SwitchOnType['Crafted']:
            widget.hide()
        for widget in self.SwitchOnType['Legendary']:
            widget.show()
        for index in range(0, item.getSlotCount()):
            if item.getSlot(index).getSlotType() == 'Craftable':
                self.SlotLabel[index].setText('Gem &%d:' % (index + 1))
            if item.getSlot(index).getSlotType() == 'Dropped':
                self.EffectType[index].setDisabled(True)
                self.Effect[index].setDisabled(True)
                self.AmountEdit[index].setDisabled(True)

        # DEBUGGING
        print('showLegendaryWidgets')

    def showDropWidgets(self, item):
        for widget in self.SwitchOnType['Crafted']:
            widget.hide()
        for widget in self.SwitchOnType['Legendary']:
            widget.hide()
        for widget in self.SwitchOnType['Dropped']:
            widget.show()
        for index in range(0, item.getSlotCount()):
            if item.getSlot(index).getSlotType() == 'Dropped':
                self.SlotLabel[index].setText('Slot &%d:' % (index + 1))
                self.EffectType[index].setDisabled(False)
                self.Effect[index].setDisabled(False)
                self.AmountEdit[index].setDisabled(False)

        # DEBUGGING
        print('showDropWidgets')

    def RestoreItem(self, item):
        if item.ActiveState == 'Crafted':
            self.showCraftWidgets(item)
        elif item.ActiveState == 'Legendary':
            self.showLegendaryWidgets(item)
        elif item.ActiveState == 'Dropped':
            self.showDropWidgets(item)

        self.ItemName.clear()
        for value in self.ItemDictionary[item.Location]:
            self.ItemName.addItem(value.Name)

        # itemNameList = item
        # while itemNameList is not None:
        #     self.ItemName.addItem(itemNameList.ItemName)
        #     itemNameList = itemNameList.NextItem

        self.ItemName.setCurrentIndex(0)
        self.ItemLevel.setText(item.Level)

        for index in range(0, item.getSlotCount()):
            self.EffectTypeChanged(item.getSlot(index).getEffectType(), index)
            # self.EffectChanged(item.getSlot(index).getEffect(), index)
            # self.EffectAmountChanged(item.getSlot(index).getEffectAmount(), index)

        self.UpdateMenus(item)
        print(item.__dict__)

        # DEBUGGING
        print('RestoreItem')

# =============================================== #
#        SUMMARIZER AND CALCULATOR METHODS        #
# =============================================== #

    def summarize(self):
        Level = int(self.CharacterLevel.text())
        total = {
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
            total['Stats'][effect] = {}
            total['Stats'][effect]['Bonus'] = 0
            total['Stats'][effect]['TotalBonus'] = 0
            total['Stats'][effect]['CapBonus'] = 0
            total['Stats'][effect]['TotalCapBonus'] = 0
            total['Stats'][effect]['MythicalCapBonus'] = 0
            total['Stats'][effect]['TotalMythicalCapBonus'] = 0

            if effect in Cap:
                Base = Cap[effect]
                BaseCap = Cap[effect + ' Cap']

            else:
                Base = Cap['Stat']
                BaseCap = Cap['Stat Cap']

            total['Stats'][effect]['Base'] = int(Level * Base[0]) + Base[1]
            total['Stats'][effect]['BaseCap'] = int(Level * BaseCap[0]) + BaseCap[1]

            if effect in DropEffectList['All']['Mythical Stat Cap']:
                BaseMythicalCap = MythicalCap['Stat Cap']
                total['Stats'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

            if effect == 'Acuity':
                BaseMythicalCap = MythicalCap['Stat Cap']
                for value in AllBonusList[self.CurrentRealm][self.CurrentClass][effect]:
                    total['Stats'][value]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

            if effect in MythicalCap:
                BaseMythicalCap = MythicalCap[effect]
                total['Stats'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        for effect in DropEffectList['All']['Resist']:
            total['Resists'][effect] = {}
            total['Resists'][effect]['Bonus'] = 0
            total['Resists'][effect]['TotalBonus'] = 0
            total['Resists'][effect]['MythicalCapBonus'] = 0
            total['Resists'][effect]['TotalMythicalCapBonus'] = 0
            Race = str(self.CharacterRace.currentText())

            if effect in Races['All'][Race]['Resists']:
                total['Resists'][effect]['RacialBonus'] = Races['All'][Race]['Resists'][effect]

            Base = Cap['Resist']
            BaseMythicalCap = MythicalCap['Resist Cap']
            total['Resists'][effect]['Base'] = int(Level * Base[0]) + Base[1]
            total['Resists'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        for effect in DropEffectList['All']['Focus']:
            total['Focus'][effect] = {}
            total['Focus'][effect]['Bonus'] = 0
            total['Focus'][effect]['TotalBonus'] = 0

            Base = Cap['Focus']
            total['Focus'][effect]['Base'] = int(Level * Base[0]) + Base[1]

        for effect in DropEffectList['All']['Skill']:
            total['Skills'][effect] = {}
            total['Skills'][effect]['Bonus'] = 0
            total['Skills'][effect]['TotalBonus'] = 0

            Base = Cap['Skill']
            total['Skills'][effect]['Base'] = int(Level * Base[0]) + Base[1]

        for effect in DropEffectList['All']['Mythical Bonus']:
            total['MythicalBonuses'][effect] = {}
            total['MythicalBonuses'][effect]['Bonus'] = 0
            total['MythicalBonuses'][effect]['TotalBonus'] = 0

            try:  # NOT ALL MYTHICAL BONUSES HAVE A CAP ...
                Base = MythicalCap[effect]
            except KeyError:
                Base = MythicalCap['Mythical Bonus']

            total['MythicalBonuses'][effect]['Base'] = int(Level * Base[0]) + Base[1]

        for effect in DropEffectList['All']['PvE Bonus']:
            total['PvEBonuses'][effect] = {}
            total['PvEBonuses'][effect]['Bonus'] = 0
            total['PvEBonuses'][effect]['TotalBonus'] = 0

            try:  # NOT ALL PVE BONUSES HAVE A CAP ...
                Base = Cap[effect]
            except KeyError:
                Base = Cap['Other Bonus']

            total['PvEBonuses'][effect]['Base'] = int(Level * Base[0]) + Base[1]

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

            total['OtherBonuses'][effect] = {}
            total['OtherBonuses'][effect]['Bonus'] = 0
            total['OtherBonuses'][effect]['TotalBonus'] = 0
            total['OtherBonuses'][effect]['Base'] = int(Level * Base[0]) + Base[1]

        for key, item in self.ItemAttributeList.items():

            # DEBUGGING
            amts = ''

            if not item.Equipped == 2:
                continue

            for index in range(0, item.getSlotCount()):
                effect = item.getSlot(index).getEffect()
                amount = int('0' + re.sub('[^\d]', '', item.getSlot(index).getEffectAmount()))

                if item.getSlot(index).getEffectType() == 'Stat':
                    effects = [effect, ]

                    if effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = total['Stats'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'] + amts['CapBonus'])

                elif item.getSlot(index).getEffectType() == 'Resist':
                    amts = total['Resists'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'] + amts['MythicalCapBonus'])

                elif item.getSlot(index).getEffectType() == 'Focus':
                    effects = [effect, ]

                    if effect[0:4] == 'All ':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = total['Focus'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'Skill':
                    effects = [effect, ]

                    if effect[0:4] == 'All ' and effect in AllBonusList[self.CurrentRealm][self.CurrentClass]:
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = total['Skills'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'Cap Increase':
                    effects = [effect, ]

                    if effect == 'Power':
                        effects.append('% Power Pool')

                    elif effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = total['Stats'][effect]
                        amts['TotalCapBonus'] += amount
                        amts['CapBonus'] = min(amts['TotalCapBonus'], amts['BaseCap'])

                elif item.getSlot(index).getEffectType() == 'Mythical Stat Cap':
                    effects = [effect, ]

                    if effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = total['Stats'][effect]
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
                    amts = total['Resists'][effect]
                    amts['TotalMythicalCapBonus'] += amount
                    amts['MythicalCapBonus'] = min(amts['TotalMythicalCapBonus'], amts['BaseMythicalCap'])

                elif item.getSlot(index).getEffectType() == 'Mythical Bonus':
                    amts = total['MythicalBonuses'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'PvE Bonus':
                    amts = total['PvEBonuses'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'Other Bonus':
                    if effect in ('Armor Factor', 'Fatigue', '% Power Pool'):
                        amts = total['Stats'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])
                        continue

                    if effect in ('Casting Speed', 'Archery Speed'):
                        effect = 'Archery and Casting Speed'

                    if effect in ('Spell Damage', 'Archery Damage'):
                        effect = 'Archery and Spell Damage'

                    if effect in ('Spell Range', 'Archery Range'):
                        effect = 'Archery and Spell Range'

                    amts = total['OtherBonuses'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

            # DEBUGGING
            if not amts == '':
                print(amts)

        # DEBUGGING
        print('summarize')

        return total

    def calculate(self):
        total = self.summarize()

        item = self.ItemAttributeList[self.CurrentItemLabel]
        if item.ActiveState in ('Crafted', 'Legendary'):
            slotImbueValues = item.getSlotImbueValues()
            itemImbuePoints = item.getItemImbueValue()

            print(slotImbueValues)
            print(str(sum(slotImbueValues)) + ' / ' + str(itemImbuePoints))

            for index in range(0, item.getSlotCount()):
                if index < len(slotImbueValues):
                    self.ImbuePoints[index].setText('%3.1f' % slotImbueValues[index])
                self.GemName[index].setText(item.getSlot(index).getGemName(self.CurrentRealm))

        for (key, datum) in list(total['Stats'].items()):
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

        for key, amts in list(total['Resists'].items()):
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

        for skill, amts in list(total['Skills'].items()):
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0 and skill[0:4] != 'All ':
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, skill, 'Skill')

        for focus, amts in list(total['Focus'].items()):
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0 and focus[0:4] != 'All ':
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, focus + ' Focus', 'Focus')

        for bonus, amts in list(total['MythicalBonuses'].items()):
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0:
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, 'Mythical ' + bonus, 'Bonus')

        for bonus, amts in list(total['PvEBonuses'].items()):
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0:
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, bonus + ' (PvE)', 'Skill')

        for bonus, amts in list(total['OtherBonuses'].items()):
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
            for index in range(0, self.count()):
                option.currentText = self.itemText(index)
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

    # TODO: NOT COMPLETE
    def UpdateMenus(self, item):
        self.ItemNewMenu.clear()
        self.ItemTypeMenu.clear()

        itemTypesList = [
            'Crafted Item',
            'Dropped Item',
            'Legendary Bow',
            'Legendary Staff',
            'Legendary Weapon',
        ]

        for value in itemTypesList:
            self.ItemNewMenu.addAction(value)
            self.ItemTypeMenu.addAction(value)

        # DEBUGGING
        print('UpdateMenus')

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

    def setToolBarOptions(self, action):
        for act in self.ToolBarMenu.actions():
            if act.data() == action.data() and not act.isChecked():
                act.setChecked(True)
            elif act.data() != action.data() and act.isChecked():
                act.setChecked(False)
        if action.data() == 0:
            self.ToolBar.hide()
        else:
            self.setIconSize(QSize(action.data(), action.data()))
            self.ToolBar.show()

        # DEBUGGING
        print('setToolBarOptions')

    def setDistanceToCap(self):
        self.calculate()

        # DEBUGGING
        print('setDistanceToCap')

    def setUnusableSkills(self):
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('setUnusableSkills')

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

    def ItemNameChanged(self):
        if self.ItemName.currentIndex() != 0: return
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Name = str(self.ItemName.lineEdit().text())
        cursorPosition = self.ItemName.lineEdit().cursorPosition()
        self.ItemName.setItemText(0, item.Name)
        self.ItemName.lineEdit().setCursorPosition(cursorPosition)

        # DEBUGGING
        print('ItemNameChanged')

    def ItemStateChanged(self, selection, column):
        self.ItemAttributeList[selection.text(column)].Equipped = selection.checkState(column)
        if selection.text(column) == self.SlotListTreeView.selectedIndexes():
            self.RestoreItem(self.ItemAttributeList[selection.text(column)])

        # DEBUGGING
        print('ItemStateChanged')

    def ItemLevelChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Level = self.ItemLevel.text()
        self.ItemLevel.setModified(False)
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('ItemLevelChanged')

    def ItemQualityChanged(self):

        # DEBUGGING
        print('ItemQualityChanged')

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

        if item.Location not in ('Two-Handed', 'Spare'):
            self.EffectType[index].removeItem(self.EffectType[index].findText('Focus'))

        self.EffectType[index].setCurrentText(etype)
        item.getSlot(index).setEffectType(etype)

        # CASCADE THE CHANGES ...
        self.EffectChanged(item.getSlot(index).getEffect(), index)

        # DEBUGGING
        print('EffectTypeChanged, EffectType = ' + str(etype))

    def EffectChanged(self, effect = None, index = -1):
        if index == -1: index = self.getSignalSlot()
        item = self.ItemAttributeList[self.CurrentItemLabel]
        self.Effect[index].clear()

        effectType = item.getSlot(index).getEffectType()
        if item.getSlot(index).getSlotType() == 'Craftable':
            if effectType == 'Skill' and not self.UnusableSkills.isChecked():
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

    def EffectAmountChanged(self, amount = None, index = -1):
        if index == -1: index = self.getSignalSlot()
        item = self.ItemAttributeList[self.CurrentItemLabel]

        valuesList = list()
        if item.getSlot(index).getSlotType() in ('Craftable', 'Enhanced'):
            if item.getSlot(index).getEffect()[0:9] in ('All Melee', 'All Magic'):
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

        elif item.getSlot(index).getSlotType() == 'Dropped':
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

    def newItem(self, action):
        newItemType = action.text().split(None, 1)[0]
        itemState = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        item = Item(newItemType, self.CurrentItemLabel, self.CurrentRealm, self.ItemIndex)
        item.Name = action.text()
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = itemState

        if newItemType == 'Legendary':
            if action.text().split(None, 1)[1] == 'Staff':
                item.getSlot(4).setAll('Focus', 'All Spell Lines', '50')
                item.getSlot(5).setAll('Other Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('Other Bonus', 'Spell Damage', '3')
            elif action.text().split(None, 1)[1] == 'Bow':
                item.getSlot(4).setAll('Other Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('Other Bonus', 'Archery Speed', '3')
                item.getSlot(6).setAll('Other Bonus', 'Archery Damage', '3')
            elif action.text().split(None, 1)[1] == 'Weapon':
                item.getSlot(4).setAll('Other Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('Other Bonus', 'Melee Damage', '3')
                item.getSlot(6).setAll('Other Bonus', 'Style Damage', '3')

        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])
        self.ItemIndex += 1

        # DEBUGGING
        print('newItem')

    def changeItem(self, index):
        itemState = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = 0

        try:  # FIXES BUG IN 'QComboBox' WHEN PRESSING ENTER ...
            item = self.ItemDictionary[self.CurrentItemLabel][index]
        except IndexError:
            item = self.ItemDictionary[self.CurrentItemLabel][0]

        self.ItemDictionary[self.CurrentItemLabel].remove(item)
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = itemState
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('changeItem, Selected Item = %s' % item.Name)

    def changeItemType(self, action):
        newItemType = action.text().split(None, 1)[0]
        itemState = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        itemIndex = self.ItemAttributeList[self.CurrentItemLabel].TemplateIndex
        item = Item(newItemType, self.CurrentItemLabel, self.CurrentRealm, itemIndex)
        item.Name = action.text()
        del self.ItemDictionary[self.CurrentItemLabel][0]
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = itemState

        if newItemType == 'Legendary':
            if action.text().split(None, 1)[1] == 'Staff':
                item.getSlot(4).setAll('Focus', 'All Spell Lines', '50')
                item.getSlot(5).setAll('Other Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('Other Bonus', 'Spell Damage', '3')
            elif action.text().split(None, 1)[1] == 'Bow':
                item.getSlot(4).setAll('Other Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('Other Bonus', 'Archery Speed', '3')
                item.getSlot(6).setAll('Other Bonus', 'Archery Damage', '3')
            elif action.text().split(None, 1)[1] == 'Weapon':
                item.getSlot(4).setAll('Other Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('Other Bonus', 'Melee Damage', '3')
                item.getSlot(6).setAll('Other Bonus', 'Style Damage', '3')

        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('changeItemType')

    def clearItem(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        itemState = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        self.ItemDictionary[self.CurrentItemLabel].remove(item)
        item = Item(item.ActiveState, self.CurrentItemLabel, self.CurrentRealm, item.TemplateIndex)
        item.Name = item.ActiveState + ' Item'
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = itemState
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('clearItem')

    def clearItemSlots(self):
        self.ItemAttributeList[self.CurrentItemLabel].clearSlots()
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('clearItemSlots')

    def loadItem(self):
        options = QFileDialog.Options()
        filename, filters = QFileDialog.getOpenFileName(
            self, 'Load Item:', '', 'Items (*.xml);; All Files (*.*)', options = options,)
        item = Item('Imported', self.CurrentItemLabel, self.CurrentRealm, self.ItemIndex)
        item.importFromXML(filename)

        # DEBUGGING
        print('loadItem')

    def saveItem(self):

        # DEBUGGING
        print('saveItem')

    def deleteItem(self):
        if len(self.ItemDictionary[self.CurrentItemLabel]) == 1:
            self.clearItem()
            return
        itemState = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        del self.ItemDictionary[self.CurrentItemLabel][0]
        item = self.ItemDictionary[self.CurrentItemLabel][0]
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = itemState
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

        # DEBUGGING
        print('deleteItem')
