# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import QAction, Qt, QKeySequence
from PyQt5.QtCore import QSize, QModelIndex, QVariant
from PyQt5.QtGui import QFontMetrics, QIcon, QIntValidator
from PyQt5.QtWidgets import QFileDialog, QLabel, QListWidgetItem, QMainWindow, QMenu, QMessageBox, QToolBar, QTreeWidgetItem, QTreeWidgetItemIterator, QStyle, QStyleOptionComboBox
from Character import AllBonusList, AllRealms, ClassList, ItemDamageTypes, ItemOrigins, ItemTypes, Races, Realms
from Constants import Cap, CraftedTypeList, CraftedEffectList, CraftedValuesList, DropTypeList, DropEffectList
from Constants import EnhancedTypeList, EnhancedEffectList, EnhancedValuesList, MythicalBonusCap, PVEBonusCap, TOABonusCap
from Item import Item
from CraftBarDialog import CraftBarDialog
from ReportWindow import ReportWindow
from lxml import etree
import os
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
        self.ItemLoadMenu = QMenu('Load Item', self)
        self.ItemNewMenu = QMenu('&New Item', self)
        self.ItemTypeMenu = QMenu('Item &Type', self)
        self.ItemSwapMenu = QMenu('S&wap Gems with', self)
        self.ItemMoveMenu = QMenu('&Move Item to', self)
        self.RecentMenu = QMenu('Recent Templates', self)
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
        self.ItemInfoWidgets = {}

        self.SlotLabel = []
        self.Effect = []
        self.EffectType = []
        self.AmountEdit = []
        self.AmountStatic = []
        self.Requirement = []
        self.ImbuePoints = []
        self.GemName = []
        self.GemNameLabel = []
        self.SwitchOnType = {}
        self.BuildUtility = QLabel()

        self.CurrentRealm = ''
        self.CurrentClass = ''
        self.CurrentRace = ''
        self.CurrentItemLabel = ''

        self.TemplateName = None
        self.TemplatePath = None
        self.TemplateModified = False

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
        self.FileMenu.addAction('New Template', self.newTemplate)
        self.FileMenu.addAction('Open Template ...', self.openTemplate)
        self.FileMenu.addAction('Save Template', self.saveTemplate)
        self.FileMenu.addAction('Save Template As ...', self.saveTemplateAs)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction('Import Loki Template ...', self.importLokiTemplate)
        self.FileMenu.addAction('Export Gem\'s to Quickbar ...', self.exportGemsToQuickbar)
        self.FileMenu.addSeparator()
        self.FileMenu.addMenu(self.RecentMenu)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction('E&xit', self.close, QKeySequence(Qt.CTRL + Qt.Key_X))

        self.ItemLoadMenu.addAction('Item XML File ...', self.loadItem)
        self.ItemLoadMenu.addAction('Item Database ...', self.showItemDatabase)

        self.EditMenu.addMenu(self.ItemLoadMenu)
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

        self.ViewMenu.addAction('&Material Report ...', self.showMaterialsReport)
        self.ViewMenu.addAction('&Template Report ...', self.showTemplateReport)
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
        self.ToolBar.addAction('New Template', self.newTemplate)
        self.ToolBar.addAction('Open Template', self.openTemplate)
        self.ToolBar.addAction('Save Template', self.saveTemplate)
        self.ToolBar.addAction('Save Template As', self.saveTemplateAs)
        self.ToolBar.addSeparator()
        self.ToolBar.addAction('Export Gems', self.exportGemsToQuickbar)
        self.ToolBar.addSeparator()
        self.ToolBar.addAction('Materials Report', self.showMaterialsReport)
        self.ToolBar.addAction('Template Report', self.showTemplateReport)
        self.addToolBar(self.ToolBar)

    def initItemToolBar(self):
        self.ItemNewButton.setMenu(self.ItemNewMenu)
        self.ItemNewButton.setToolTip('Add New Item')
        self.ItemNewButton.clicked.connect(self.ItemNewButton.showMenu)

        self.ItemTypeButton.setMenu(self.ItemTypeMenu)
        self.ItemTypeButton.setToolTip('Change Item Type')
        self.ItemTypeButton.clicked.connect(self.ItemTypeButton.showMenu)

        self.ItemLoadButton.setMenu(self.ItemLoadMenu)
        self.ItemLoadButton.setToolTip('Load Item')
        self.ItemLoadButton.clicked.connect(self.ItemLoadButton.showMenu)

        self.ItemDeleteButton.setToolTip('Delete Item')
        self.ItemSaveButton.setToolTip('Save Item')

    def initLayout(self):
        self.setWindowTitle('Kort\'s Spellcrafting Calculator')

        # MAKE SURE WE ARE TESTING WIDTH AND HEIGHT
        # VALUES BASED ON THE FONT BEING USED ...
        testFont = QFontMetrics(self.font())

        defaultFixedHeight = 20
        buttonFixedHeight = 22
        buttonFixedWidth = 35

        width = self.setMinimumWidth(['Necromancer'])
        self.CharacterName.setFixedSize(QSize(width, defaultFixedHeight))
        self.CharacterRealm.setFixedSize(QSize(width, defaultFixedHeight))
        self.CharacterClass.setFixedSize(QSize(width, defaultFixedHeight))
        self.CharacterRace.setFixedSize(QSize(width, defaultFixedHeight))
        self.CharacterLevel.setFixedSize(QSize(width, defaultFixedHeight))
        self.CharacterRealmRank.setFixedSize(QSize(width, defaultFixedHeight))
        self.CharacterChampLevel.setFixedSize(QSize(width, defaultFixedHeight))

        for attribute in DropEffectList['All']['Attribute'] + ('ArmorFactor', 'Fatigue', 'PowerPool'):
            attribute = attribute.replace(' ', '')
            self.StatLabel[attribute] = getattr(self, attribute + 'Label')
            self.StatValue[attribute] = getattr(self, attribute)
            self.StatCap[attribute] = getattr(self, attribute + 'Cap')

            try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
                self.StatMythicalCap[attribute] = getattr(self, attribute + 'MythicalCap')
            except AttributeError:
                pass

        width = testFont.size(Qt.TextSingleLine, "CON: ", tabArray = None).width()
        self.AttributesGroup.layout().setColumnMinimumWidth(0, width)
        width = testFont.size(Qt.TextSingleLine, "-400", tabArray = None).width()
        self.AttributesGroup.layout().setColumnMinimumWidth(1, width)
        width = testFont.size(Qt.TextSingleLine, "(400)", tabArray = None).width()
        self.AttributesGroup.layout().setColumnMinimumWidth(2, width)
        width = testFont.size(Qt.TextSingleLine, "(-26)", tabArray = None).width()
        self.AttributesGroup.layout().setColumnMinimumWidth(3, width)

        for resist in DropEffectList['All']['Resistance']:
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

        for key, locations in ItemTypes.items():
            parent = QTreeWidgetItem(self.SlotListTreeView, [key])
            parent.setFlags(parent.flags() & ~Qt.ItemIsUserCheckable & ~Qt.ItemIsSelectable)
            if key == 'Jewelery':
                parent.setExpanded(True)
            for location in locations:
                child = QTreeWidgetItem([location])
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setCheckState(0, Qt.Unchecked)
                parent.addChild(child)

        # TODO: SET A DYNAMIC MINIMAL WIDTH ...
        self.SlotListTreeView.setMinimumWidth(142)
        self.CharacterRealm.insertItems(0, Realms)

        self.SwitchOnType = {

            'Crafted': [
                self.ImbuePointsLabel,
                self.ItemImbuePoints,
                self.ItemImbuePointsTotal,
                self.ItemImbuePointsLabel,
                self.ItemOvercharge,
                self.ItemOverchargeLabel,
            ],

            'Legendary': [
                self.ImbuePointsLabel,
                self.ItemImbuePoints,
                self.ItemImbuePointsTotal,
                self.ItemImbuePointsLabel,
                self.ItemOvercharge,
                self.ItemOverchargeLabel,
            ],

            'Dropped': [
                self.RequirementLabel,
            ]
        }

        self.ItemNewButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemTypeButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemLoadButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemDeleteButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemSaveButton.setFixedSize(QSize(buttonFixedWidth, buttonFixedHeight))
        self.ItemName.setFixedHeight(defaultFixedHeight)

        width = testFont.size(Qt.TextSingleLine, "Slot 12: ", tabArray = None).width()
        self.ItemStatsGroup.layout().setColumnMinimumWidth(0, width)

        width = self.setMinimumWidth([' Mythical Resist & Cap '])
        for index in range(0, 12):
            self.EffectType.append(getattr(self, 'EffectType%d' % index))
            self.EffectType[index].setFixedSize(QSize(width, defaultFixedHeight))
            self.EffectType[index].activated[str].connect(self.EffectTypeChanged)

        width = self.setMinimumWidth(['100'])
        for index in range(0, 12):
            self.AmountEdit.append(getattr(self, 'AmountEdit%d' % index))
            self.AmountEdit[index].setFixedSize(QSize(width, defaultFixedHeight))
            self.AmountEdit[index].setValidator(QIntValidator(-999, +999, self))
            self.AmountEdit[index].textEdited[str].connect(self.EffectAmountChanged)

        width = self.setMinimumWidth(['100'])
        for index in range(0, 5):
            self.AmountStatic.append(getattr(self, 'AmountStatic%d' % index))
            self.AmountStatic[index].setFixedSize(QSize(width, defaultFixedHeight))
            self.AmountStatic[index].activated[str].connect(self.EffectAmountChanged)

        width = self.setMinimumWidth([' Neg. Effect Duration Reduction '])
        for index in range(0, 12):
            self.SlotLabel.append(getattr(self, 'SlotLabel%d' % index))
            self.Effect.append(getattr(self, 'Effect%d' % index))
            self.Effect[index].setFixedSize(QSize(width, defaultFixedHeight))
            self.Effect[index].activated[str].connect(self.EffectChanged)

        width = self.setMinimumWidth(['vs. Enemy Players'])
        for index in range(0, 12):
            self.Requirement.append(getattr(self, 'Requirement%d' % index))
            self.Requirement[index].setFixedSize(QSize(width, defaultFixedHeight))
            self.Requirement[index].editingFinished.connect(self.EffectRequirementChanged)

        width = self.setMinimumWidth(['-'])
        for index in range(0, 4):
            self.ImbuePoints.append(getattr(self, 'ImbuePoints%d' % index))
            self.ImbuePoints[index].setFixedSize(QSize(width, defaultFixedHeight))
            self.GemNameLabel.append(getattr(self, 'GemNameLabel%d' % index))

        for index in range(0, 7):
            self.GemName.append(getattr(self, 'GemName%d' % index))

        width = self.Requirement[0].width()
        for index in range(4, 7):
            self.GemName[index].setFixedSize(QSize(width, defaultFixedHeight))

        width = testFont.size(Qt.TextSingleLine, "37.5", tabArray = None).width()
        self.ItemImbuePointsTotal.setFixedWidth(width)

        testItem = Item('Crafted')
        for index in range(0, testItem.getSlotCount()):
            self.SwitchOnType['Crafted'].append(self.SlotLabel[index])
            self.SwitchOnType['Crafted'].append(self.EffectType[index])
            self.SwitchOnType['Crafted'].append(self.AmountStatic[index])
            self.SwitchOnType['Crafted'].append(self.Effect[index])
            self.SwitchOnType['Crafted'].append(self.GemName[index])
            if index < 4:
                self.SwitchOnType['Crafted'].append(self.ImbuePoints[index])
                self.SwitchOnType['Crafted'].append(self.GemNameLabel[index])

        testItem = Item('Legendary')
        for index in range(0, testItem.getSlotCount()):
            self.SwitchOnType['Legendary'].append(self.SlotLabel[index])
            self.SwitchOnType['Legendary'].append(self.EffectType[index])
            self.SwitchOnType['Legendary'].append(self.Effect[index])
            self.SwitchOnType['Legendary'].append(self.GemName[index])
            if index < 4:
                self.SwitchOnType['Legendary'].append(self.AmountStatic[index])
                self.SwitchOnType['Legendary'].append(self.ImbuePoints[index])
                self.SwitchOnType['Legendary'].append(self.GemNameLabel[index])
            if index > 3:
                self.SwitchOnType['Legendary'].append(self.AmountEdit[index])

        testItem = Item('Dropped')
        for index in range(0, testItem.getSlotCount()):
            self.SwitchOnType['Dropped'].append(self.SlotLabel[index])
            self.SwitchOnType['Dropped'].append(self.EffectType[index])
            self.SwitchOnType['Dropped'].append(self.AmountEdit[index])
            self.SwitchOnType['Dropped'].append(self.Effect[index])
            self.SwitchOnType['Dropped'].append(self.Requirement[index])

        # COLLECTING GARBAGE
        del testItem

        self.ItemInfoWidgets = {

            'All': [
                self.ItemRealm,
                self.ItemRealmLabel,
                self.ItemType,
                self.ItemTypeLabel,
                self.ItemOrigin,
                self.ItemOriginLabel,
                self.ItemDamageType,
                self.ItemDamageTypeLabel,
                self.ItemLevel,
                self.ItemLevelLabel,
                self.ItemQuality,
                self.ItemQualityLabel,
                self.ItemBonus,
                self.ItemBonusLabel,
                self.ItemAFDPS,
                self.ItemAFDPSLabel,
                self.ItemSpeed,
                self.ItemSpeedLabel,
                self.ItemLeftHand
            ],

            'Jewelery': [
                self.ItemDamageType,
                self.ItemDamageTypeLabel,
                self.ItemAFDPS,
                self.ItemAFDPSLabel,
                self.ItemSpeed,
                self.ItemSpeedLabel,
                self.ItemLeftHand],

            'Armor': [
                self.ItemDamageType,
                self.ItemDamageTypeLabel,
                self.ItemSpeed,
                self.ItemSpeedLabel,
                self.ItemLeftHand
            ],

            'Weapons': [],

            'Mythical': [
                self.ItemDamageType,
                self.ItemDamageTypeLabel,
                self.ItemAFDPS,
                self.ItemAFDPSLabel,
                self.ItemSpeed,
                self.ItemSpeedLabel,
                self.ItemLeftHand
            ],
        }

        self.ItemRealm.setFixedHeight(defaultFixedHeight)
        self.ItemType.setFixedHeight(defaultFixedHeight)
        self.ItemOrigin.setFixedHeight(defaultFixedHeight)
        self.ItemDamageType.setFixedHeight(defaultFixedHeight)

        width = self.setMinimumWidth([' - '])
        self.ItemLevel.setFixedSize(QSize(width, defaultFixedHeight))
        self.ItemQuality.setFixedSize(QSize(width, defaultFixedHeight))
        self.ItemBonus.setFixedSize(QSize(width, defaultFixedHeight))
        self.ItemAFDPS.setFixedSize(QSize(width, defaultFixedHeight))
        self.ItemSpeed.setFixedSize(QSize(width, defaultFixedHeight))

        self.ItemInformationGroup.setFixedWidth(186)
        self.ItemRestrictionsGroup.setFixedWidth(135)

        width = testFont.size(Qt.TextSingleLine, "1999.9", tabArray=None).width()
        self.BuildUtility.setFixedWidth(width)
        self.BuildUtility.setAlignment(Qt.AlignRight)
        self.StatusBar.setStyleSheet('QStatusBar::item {border: None;}')
        self.StatusBar.addPermanentWidget(QLabel('Build Utility: '))
        self.StatusBar.addPermanentWidget(self.BuildUtility)

    def initialize(self):
        self.TemplateName = None
        self.TemplatePath = None
        self.CharacterName.setText('')
        self.CharacterLevel.setText('50')

        # SETUP THE INITIAL REALM ...
        self.CharacterRealm.setCurrentText('Midgard')
        self.CharacterRealmChanged()

        for parent, locations in ItemTypes.items():
            for location in locations:
                if parent == 'Armor':
                    item = Item('Crafted', location, self.CurrentRealm, self.ItemIndex)
                    item.Name = item.ActiveState + ' Item'
                    self.ItemIndex += 1
                else:
                    item = Item('Dropped', location, 'All', self.ItemIndex)
                    item.Name = item.ActiveState + ' Item'
                    self.ItemIndex += 1
                self.ItemAttributeList[location] = item
                self.ItemDictionary[location] = [item]

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
        self.SlotListTreeView.itemClicked.connect(self.ItemSelected)
        self.SlotListTreeView.itemChanged.connect(self.ItemStateChanged)
        self.CharacterRealm.activated[int].connect(self.CharacterRealmChanged)
        self.CharacterClass.activated[int].connect(self.CharacterClassChanged)
        self.CharacterRace.activated[int].connect(self.CharacterRaceChanged)
        self.CharacterLevel.editingFinished.connect(self.calculate)
        self.ItemRealm.activated.connect(self.ItemRealmChanged)
        self.ItemType.activated.connect(self.ItemTypeChanged)
        self.ItemOrigin.activated.connect(self.ItemOriginChanged)
        self.ItemLevel.editingFinished.connect(self.ItemLevelChanged)
        self.ItemQuality.editingFinished.connect(self.ItemQualityChanged)
        self.ItemDamageType.activated.connect(self.ItemDamageTypeChanged)
        self.ItemBonus.editingFinished.connect(self.ItemBonusChanged)
        self.ItemAFDPS.editingFinished.connect(self.ItemAFDPSChanged)
        self.ItemSpeed.editingFinished.connect(self.ItemSpeedChanged)
        self.ItemLeftHand.stateChanged.connect(self.ItemLeftHandChanged)
        self.ItemRequirement.editingFinished.connect(self.ItemRequirementChanged)
        self.ItemNotes.textChanged.connect(self.ItemNotesChanged)
        self.ItemRestrictionsList.itemChanged.connect(self.ItemRestrictionsChanged)
        self.ItemName.activated[int].connect(self.changeItem)
        self.ItemName.editTextChanged[str].connect(self.ItemNameChanged)
        self.ItemSaveButton.clicked.connect(self.saveItem)
        self.ItemDeleteButton.clicked.connect(self.deleteItem)

    def LoadOptions(self):
        pass

    def SaveOptions(self):
        pass

# =============================================== #
#             DIALOG & WINDOW METHODS             #
# =============================================== #

    def showItemDatabase(self):
        pass

    def showMaterialsReport(self):
        self.MaterialsReport = ReportWindow(self, Qt.WindowCloseButtonHint)
        self.MaterialsReport.materialsReport(self.ItemAttributeList, self.CurrentRealm)
        self.MaterialsReport.exec_()

    def showTemplateReport(self):
        self.TemplateReport = ReportWindow(self, Qt.WindowCloseButtonHint)
        self.TemplateReport.templateReport(self.exportAsXML(None, True, True))
        self.TemplateReport.exec_()

# =============================================== #
#              XML IMPORT AND EXPORT              #
# =============================================== #

    def importFromXML(self, filename):
        self.initialize()
        items = list()
        tree = etree.parse(filename)
        if tree.getroot().tag == 'Template':
            elements = tree.getroot().getchildren()
            for element in elements:
                if element.tag == 'Name':
                    self.CharacterName.setText(element.text)
                elif element.tag == 'Realm':
                    self.CharacterRealm.setCurrentText(element.text)
                    self.CharacterRealmChanged()
                elif element.tag == 'Class':
                    self.CharacterClass.setCurrentText(element.text)
                    self.CharacterClassChanged()
                elif element.tag == 'Race':
                    self.CharacterRace.setCurrentText(element.text)
                    self.CharacterRaceChanged()
                elif element.tag == 'Level':
                    self.CharacterLevel.setText(element.text)
                elif element.tag == 'RealmRank':
                    self.CharacterRealmRank.setText(element.text)
                elif element.tag == 'Item':
                    items.append(element)
        else:
            return -1

        self.ItemDictionary.clear()
        self.ItemAttributeList.clear()
        for parent, locations in ItemTypes.items():
            for location in locations:
                self.ItemDictionary[location] = []

        for item_xml in items:
            item = Item('Imported')
            item.importFromXML(item_xml, True)
            if int(item_xml.attrib['Index']) == 0:
                self.ItemAttributeList[item.Location] = item
            self.ItemDictionary[item.Location].insert(int(item_xml.attrib['Index']), item)
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

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

    def exportAsXML(self, filename, export = False, report = False):
        template = etree.Element('Template')
        etree.SubElement(template, 'Name').text = self.CharacterName.text()
        etree.SubElement(template, 'Realm').text = self.CharacterRealm.currentText()
        etree.SubElement(template, 'Class').text = self.CharacterClass.currentText()
        etree.SubElement(template, 'Race').text = self.CharacterRace.currentText()
        etree.SubElement(template, 'Level').text = self.CharacterLevel.text()
        etree.SubElement(template, 'RealmRank').text = self.CharacterRealmRank.text()

        for slot, items in self.ItemDictionary.items():
            for item in items:
                if report:
                    element = item.exportAsXML(None, True, True)
                else:
                    element = item.exportAsXML(None, True)
                element.set('Index', str(items.index(item)))
                template.append(element)

        if report:
            total = self.summarize()

            for key in (key for key in total.keys() if key != 'Utility'):
                element = etree.SubElement(template, key)
                if key[-7:] == 'Bonuses':
                    element.attrib['Text'] = key[:-7] + ' ' + key[-7:]
                for attribute, bonuses in total[key].items():
                    tag = ''.join(x for x in attribute if x.isalnum())
                    if tag != attribute:
                        root = etree.SubElement(element, tag, Text = attribute)
                    else:
                        root = etree.SubElement(element, tag)
                    for bonus, value in bonuses.items():
                        etree.SubElement(root, bonus).text = str(value)

        if not export:

            # TODO: CONVERT TO PYTHON 3.6 STANDARD (F-STRING) AND
            # USE ETREE.UNICODE INSTEAD OF ENCODING ...
            with open(filename, 'wb') as document:
                document.write(etree.tostring(template, encoding='UTF-8', pretty_print = True, xml_declaration = True))
        else:
            return template

# =============================================== #
#   LAYOUT CHANGE/UPDATE METHODS AND FUNCTIONS    #
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
            if item.getSlot(index).getSlotType() == 'Enhanced':
                self.EffectType[index].setDisabled(False)
                self.Effect[index].setDisabled(False)
                self.AmountEdit[index].setDisabled(False)

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

    def showItemInfoWidgets(self, item):
        for widget in (
                self.ItemRealm,
                self.ItemType,
                self.ItemOrigin,
                self.ItemDamageType
        ): widget.clear()

        for widget in self.ItemInfoWidgets[item.getParent()]:
            widget.setDisabled(True)

        if item.ActiveState == 'Dropped':
            self.ItemRealm.insertItems(0, AllRealms)
            self.ItemOrigin.insertItems(0, ('',) + ItemOrigins[item.ActiveState])
        elif item.ActiveState in ('Crafted', 'Legendary'):
            self.ItemRealm.insertItems(0, Realms)
            self.ItemOrigin.insertItems(0, ItemOrigins[item.ActiveState])

        if item.Realm in ItemTypes[item.getParent()][item.Location]:
            self.ItemType.insertItems(0, ('',) + ItemTypes[item.getParent()][item.Location][item.Realm])
        elif 'All' in ItemTypes[item.getParent()][item.Location]:
            self.ItemType.insertItems(0, ('',) + ItemTypes[item.getParent()][item.Location]['All'])

        if item.getParent() == 'Weapons':
            self.ItemDamageType.insertItems(0, ('',) + ItemDamageTypes[item.ActiveState])

        self.ItemRealm.setCurrentText(item.Realm)
        self.ItemOrigin.setCurrentText(item.Origin)
        self.ItemDamageType.setCurrentText(item.DamageType)
        self.ItemType.setCurrentText(item.Type)
        self.ItemBonus.setText(item.Bonus)
        self.ItemAFDPS.setText(item.AFDPS)
        self.ItemSpeed.setText(item.Speed)

        if item.LeftHand == 2:
            self.ItemLeftHand.setCheckState(Qt.Checked)
        else:
            self.ItemLeftHand.setCheckState(Qt.Unchecked)

        self.ItemRequirement.setText(item.Requirement)
        self.ItemNotes.setPlainText(item.Notes)
        self.showItemRestrictions(item)

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
        self.ItemName.setCurrentIndex(0)
        self.ItemLevel.setText(item.Level)
        self.ItemQuality.setText(item.Quality)

        # CHANGES TO THE 'EffectType' ARE CASCADED ...
        for index in range(0, item.getSlotCount()):
            self.EffectTypeChanged(item.getSlot(index).getEffectType(), index)

        for widget in self.ItemInfoWidgets['All']:
            widget.setEnabled(True)

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

        self.showItemInfoWidgets(item)
        self.updateMenus(item)

# =============================================== #
#        SUMMARIZER AND CALCULATOR METHODS        #
# =============================================== #

    def summarize(self):
        Level = int(self.CharacterLevel.text())
        total = {
            'Skills': {},
            'Attributes': {},
            'Resistances': {},
            'Focus': {},
            'TOABonuses': {},
            'PVEBonuses': {},
            'MythicalBonuses': {},
            'Utility': 0.0
        }

        for effect in DropEffectList['All']['Attribute'] + ('Armor Factor', 'Fatigue', '% Power Pool'):
            total['Attributes'][effect] = {}
            total['Attributes'][effect]['Bonus'] = 0
            total['Attributes'][effect]['TotalBonus'] = 0
            total['Attributes'][effect]['CapBonus'] = 0
            total['Attributes'][effect]['TotalCapBonus'] = 0
            total['Attributes'][effect]['MythicalCapBonus'] = 0
            total['Attributes'][effect]['TotalMythicalCapBonus'] = 0

            if effect in ('Armor Factor', 'Fatigue', '% Power Pool'):
                Base = TOABonusCap[effect]

                try:  # NOT ALL ATTRIBUTES HAVE A CAP
                    BaseCap = TOABonusCap[effect + ' Cap']
                except KeyError:
                    BaseCap = TOABonusCap['None']

            elif effect in Cap:
                Base = Cap[effect]
                BaseCap = TOABonusCap[effect + ' Cap']
            else:
                Base = Cap['Attribute']
                BaseCap = TOABonusCap['Attribute Cap']

            total['Attributes'][effect]['Base'] = int(Level * Base[0]) + Base[1]
            total['Attributes'][effect]['BaseCap'] = int(Level * BaseCap[0]) + BaseCap[1]

            if effect in DropEffectList['All']['Mythical Stat Cap']:
                BaseMythicalCap = MythicalBonusCap['Stat Cap']
                total['Attributes'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

            if effect in MythicalBonusCap:
                BaseMythicalCap = MythicalBonusCap[effect]
                total['Attributes'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        for effect in DropEffectList['All']['Resistance']:
            total['Resistances'][effect] = {}
            total['Resistances'][effect]['Bonus'] = 0
            total['Resistances'][effect]['TotalBonus'] = 0
            total['Resistances'][effect]['MythicalCapBonus'] = 0
            total['Resistances'][effect]['TotalMythicalCapBonus'] = 0
            Race = str(self.CharacterRace.currentText())

            if effect in Races['All'][Race]['Resistances']:
                total['Resistances'][effect]['RacialBonus'] = Races['All'][Race]['Resistances'][effect]

            Base = Cap['Resistance']
            BaseMythicalCap = MythicalBonusCap['Resist Cap']
            total['Resistances'][effect]['Base'] = int(Level * Base[0]) + Base[1]
            total['Resistances'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        for key, item in self.ItemAttributeList.items():
            if not item.Equipped == 2:
                continue

            total['Utility'] += item.getUtility()

            for index in range(0, item.getSlotCount()):
                effect = item.getSlot(index).getEffect()
                amount = int('0' + re.sub('[^\d]', '', item.getSlot(index).getEffectAmount()))

                if item.getSlot(index).getEffectType() == 'Skill':
                    effects = [effect, ]

                    if effect[0:4] == 'All ' and effect in AllBonusList[self.CurrentRealm][self.CurrentClass]:
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        if effect in total['Skills']:
                            amts = total['Skills'][effect]
                            amts['TotalBonus'] += amount
                        else:
                            total['Skills'][effect] = {}
                            total['Skills'][effect]['Bonus'] = 0
                            total['Skills'][effect]['TotalBonus'] = amount
                            total['Skills'][effect]['Base'] = int(Level * Cap['Skill'][0]) + Cap['Skill'][1]
                            amts = total['Skills'][effect]

                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'Attribute':
                    effects = [effect, ]

                    if effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = total['Attributes'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'] + amts['CapBonus'])

                elif item.getSlot(index).getEffectType() == 'Attribute Cap':
                    effects = [effect, ]

                    if effect == 'Power':
                        effects.append('% Power Pool')

                    elif effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = total['Attributes'][effect]
                        amts['TotalCapBonus'] += amount
                        amts['CapBonus'] = min(amts['TotalCapBonus'], amts['BaseCap'])

                elif item.getSlot(index).getEffectType() == 'Resistance':
                    amts = total['Resistances'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'] + amts['MythicalCapBonus'])

                elif item.getSlot(index).getEffectType() == 'Focus':
                    effects = [effect, ]

                    if effect[0:4] == 'All ':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        if effect in total['Focus']:
                            amts = total['Focus'][effect]
                            amts['TotalBonus'] += amount
                        else:
                            total['Focus'][effect] = {}
                            total['Focus'][effect]['Bonus'] = 0
                            total['Focus'][effect]['TotalBonus'] = amount
                            total['Focus'][effect]['Base'] = int(Level * Cap['Focus'][0]) + Cap['Focus'][1]
                            amts = total['Focus'][effect]

                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'ToA Bonus':

                    if effect in ('Armor Factor', 'Fatigue', '% Power Pool'):
                        amts = total['Attributes'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])
                        continue

                    if effect == 'Casting Speed':
                        effect = "Archery and Casting Speed"

                    if effect == 'Magic Damage':
                        effect = "Archery and Magic Damage"

                    if effect == 'Spell Range':
                        effect = "Archery and Spell Range"

                    if effect in total['TOABonuses']:
                        amts = total['TOABonuses'][effect]
                        amts['TotalBonus'] += amount
                    else:
                        total['TOABonuses'][effect] = {}
                        total['TOABonuses'][effect]['Bonus'] = 0
                        total['TOABonuses'][effect]['TotalBonus'] = amount
                        amts = total['TOABonuses'][effect]

                        try:  # NOT ALL BONUSES HAVE A CAP ...
                            Base = TOABonusCap[effect]
                        except KeyError:
                            Base = TOABonusCap['ToA Bonus']

                        total['TOABonuses'][effect]['Base'] = int(Level * Base[0]) + Base[1]

                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'PvE Bonus':

                    if effect in total['PVEBonuses']:
                        amts = total['PVEBonuses'][effect]
                        amts['TotalBonus'] += amount
                    else:
                        total['PVEBonuses'][effect] = {}
                        total['PVEBonuses'][effect]['Bonus'] = 0
                        total['PVEBonuses'][effect]['TotalBonus'] = amount
                        amts = total['PVEBonuses'][effect]

                        try:  # NOT ALL PVE BONUSES HAVE A CAP ...
                            Base = PVEBonusCap[effect]
                        except KeyError:
                            Base = PVEBonusCap['PvE Bonus']

                        total['PVEBonuses'][effect]['Base'] = int(Level * Base[0]) + Base[1]

                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

                elif item.getSlot(index).getEffectType() == 'Mythical Stat Cap':
                    effects = [effect, ]

                    if effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = total['Attributes'][effect]
                        amts['TotalMythicalCapBonus'] += amount
                        amts['MythicalCapBonus'] = min(amts['TotalMythicalCapBonus'], amts['BaseMythicalCap'])

                elif item.getSlot(index).getEffectType() == 'Mythical Resist Cap':
                    amts = total['Resistances'][effect]
                    amts['TotalMythicalCapBonus'] += amount
                    amts['MythicalCapBonus'] = min(amts['TotalMythicalCapBonus'], amts['BaseMythicalCap'])

                elif item.getSlot(index).getEffectType() == 'Mythical Stat & Cap':
                    effects = [effect, ]

                    if effect == 'Acuity':
                        effects.extend(AllBonusList[self.CurrentRealm][self.CurrentClass][effect])

                    for effect in effects:
                        amts = total['Attributes'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'] + amts['CapBonus'])
                        amts['TotalMythicalCapBonus'] += amount
                        amts['MythicalCapBonus'] = min(amts['TotalMythicalCapBonus'], amts['BaseMythicalCap'])

                elif item.getSlot(index).getEffectType() == 'Mythical Resist & Cap':
                    amts = total['Resistances'][effect]
                    amts['TotalBonus'] += amount
                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'] + amts['MythicalCapBonus'])
                    amts['TotalMythicalCapBonus'] += amount
                    amts['MythicalCapBonus'] = min(amts['TotalMythicalCapBonus'], amts['BaseMythicalCap'])

                elif item.getSlot(index).getEffectType() == 'Mythical Bonus':

                    if effect in total['MythicalBonuses']:
                        amts = total['MythicalBonuses'][effect]
                        amts['TotalBonus'] += amount
                    else:
                        total['MythicalBonuses'][effect] = {}
                        total['MythicalBonuses'][effect]['Bonus'] = 0
                        total['MythicalBonuses'][effect]['TotalBonus'] = amount
                        amts = total['MythicalBonuses'][effect]

                        try:  # NOT ALL MYTHICAL BONUSES HAVE A CAP ...
                            Base = MythicalBonusCap[effect]
                        except KeyError:
                            Base = MythicalBonusCap['Mythical Bonus']

                        total['MythicalBonuses'][effect]['Base'] = int(Level * Base[0]) + Base[1]

                    amts['Bonus'] = min(amts['TotalBonus'], amts['Base'])

        # THIS IS DIRTY ...
        for attribute, amts in total['Attributes'].items():
            if attribute in DropEffectList['All']['Mythical Stat Cap']:
                amts['BaseMythicalCap'] = amts['BaseMythicalCap'] - amts['CapBonus']
                amts['MythicalCapBonus'] = min(amts['TotalMythicalCapBonus'], amts['BaseMythicalCap'])

        return total

    def calculate(self):
        total = self.summarize()

        item = self.ItemAttributeList[self.CurrentItemLabel]
        self.BuildUtility.setText('%3.1f' % total['Utility'])
        self.ItemUtility.setText('%3.1f' % item.getUtility())

        if item.ActiveState in ('Crafted', 'Legendary'):
            self.ItemImbuePointsTotal.setText('%3.1f' % sum(item.getImbueValues()))
            self.ItemImbuePoints.setText('/ ' + str(item.getMaxImbueValue()))

            for index in range(0, item.getSlotCount()):
                if index < len(item.getImbueValues()):
                    self.ImbuePoints[index].setText('%3.1f' % item.getImbueValues()[index])
                self.GemName[index].setText(item.getSlot(index).getGemName(self.CurrentRealm))

            if isinstance(item.getOverchargeSuccess(), int):
                self.ItemOvercharge.setText('%d%%' % item.getOverchargeSuccess())
            else:
                self.ItemOvercharge.setText(item.getOverchargeSuccess())

        for key, datum in total['Attributes'].items():
            Acuity = AllBonusList[self.CurrentRealm][self.CurrentClass]["Acuity"]
            TotalBonus = datum['TotalBonus']

            if key == 'Hit Points':
                key = "HitPoints"

            if key == 'Armor Factor':
                key = "ArmorFactor"

            if key == '% Power Pool':
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

                self.StatValue[key].setText(str(int(Base - TotalBonus)))
                self.StatCap[key].setText('(' + str(int(BaseCap - TotalCapBonus)) + ')')
                self.StatMythicalCap[key].setText('(' + str(int(BaseMythicalCap - TotalMythicalCapBonus)) + ')')

                if BaseMythicalCap == 0:
                    self.StatMythicalCap[key].setText('--  ')
                if BaseCap == 0:
                    self.StatCap[key].setText('--  ')

        for key, amts in total['Resistances'].items():
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

        for skill, amts in total['Skills'].items():
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0 and skill[0:4] != 'All ':
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, skill, 'Skill')

        for focus, amts in total['Focus'].items():
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0 and focus[0:4] != 'All ':
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, focus + ' Focus', 'Focus')

        for bonus, amts in total['PVEBonuses'].items():
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0:
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, bonus + ' (PvE)', 'Skill')

        for bonus, amts in total['TOABonuses'].items():
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0:
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, bonus, 'Skill')

        for bonus, amts in total['MythicalBonuses'].items():
            amount = amts['TotalBonus']
            if amts['Bonus'] > 0:
                if self.DistanceToCap.isChecked():
                    amount = amts['Base'] - amts['TotalBonus']
                self.insertSkill(amount, 'Mythical ' + bonus, 'Bonus')

        # VALIDATE 'self.ItemAttributeList'
        self.validateItemAttributes()

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

    def getSlotIndex(self):
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

    def updateMenus(self, item):
        self.ItemNewMenu.clear()
        self.ItemTypeMenu.clear()
        options = []

        if item.getParent() in ('Armor', 'Weapons'):
            self.ItemTypeMenu.setEnabled(True)
            self.ItemTypeButton.setEnabled(True)

        if item.Location in ItemTypes['Armor']:
            options.extend([
                'Crafted Item',
                'Dropped Item',
            ])
        elif item.Location in ('Right Hand', 'Left Hand'):
            options.extend([
                'Crafted Item',
                'Dropped Item',
                'Legendary Weapon',
            ])
        elif item.Location == 'Two-Handed':
            options.extend([
                'Crafted Item',
                'Dropped Item',
                'Legendary Staff',
                'Legendary Weapon',
            ])
        elif item.Location == 'Ranged':
            options.extend([
                'Crafted Item',
                'Dropped Item',
                'Legendary Bow',
            ])
        else:
            self.ItemTypeMenu.setDisabled(True)
            self.ItemTypeButton.setDisabled(True)
            options.extend(['Dropped'])

        for value in options:
            self.ItemNewMenu.addAction(value)
            self.ItemTypeMenu.addAction(value)

    def validateItemAttributes(self):
        self.ErrorMenu.clear()
        pass

# =============================================== #
#        SLOT/SIGNAL METHODS AND FUNCTIONS        #
# =============================================== #

    def mousePressEvent(self, event):
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()' ...
            self.focusWidget().clearFocus()
        except AttributeError:
            pass

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

    def setDistanceToCap(self):
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    def setUnusableSkills(self):
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    def CharacterRealmChanged(self):
        Realm = self.CharacterRealm.currentText()
        self.CharacterClass.clear()
        self.CharacterClass.insertItems(0, ClassList[Realm])
        self.CurrentRealm = Realm
        self.CharacterClassChanged()

        for location in self.ItemAttributeList.keys():
            for item in self.ItemDictionary[location]:
                if item.ActiveState in ('Crafted', 'Legendary'):
                    item.Realm = self.CurrentRealm

        # FIXES A BUG THAT CAUSES THE APPLICATION TO CRASH ON LAUNCH
        # BECAUSE 'self.CurrentItemLabel' HAS NOT BEEN INSTANTIATED ...
        if self.CurrentItemLabel != '':
            self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])
            self.calculate()

    def CharacterClassChanged(self):
        Realm = self.CharacterRealm.currentText()
        Class = self.CharacterClass.currentText()
        self.CharacterRace.clear()
        self.CharacterRace.insertItems(0, AllBonusList[Realm][Class]['Races'])
        if self.CurrentRace in AllBonusList[Realm][Class]['Races']:
            self.CharacterRace.setCurrentText(self.CurrentRace)
        else:
            self.CharacterRaceChanged()
        self.CurrentClass = Class

        # FIXES A BUG THAT CAUSES THE APPLICATION TO CRASH ON LAUNCH
        # BECAUSE 'self.CurrentItemLabel' HAS NOT BEEN INSTANTIATED ...
        if self.CurrentItemLabel != '':
            self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])
            self.calculate()

        # BUG: INVALID SKILLS ON NON-CURRENT ITEMS DO NOT RESET
        # WHEN THE CLASS CHANGES. CREATE 'validateItem' ...

    def CharacterRaceChanged(self):
        Race = self.CharacterRace.currentText()
        for resist in DropEffectList['All']['Resistance']:
            if resist in Races['All'][Race]['Resistances']:
                self.StatBonus[resist].setText('+ ' + str(Races['All'][Race]['Resistances'][resist]))
            else:
                self.StatBonus[resist].setText('-')
        self.CurrentRace = Race

    def ItemSelected(self, selection = None):
        for index in self.SlotListTreeView.selectedIndexes():
            selection = index.data()
        if not isinstance(selection, str):
            if selection.text(0) in ItemTypes.keys():
                selection = self.CurrentItemLabel
        if not self.SlotListTreeView.selectedIndexes():
            for slot in self.SlotListTreeView.findItems(selection, Qt.MatchRecursive):
                slot.setSelected(True)
        for parent, locations in ItemTypes.items():
            for location in locations:
                if selection == location:
                    self.CurrentItemLabel = location
                    self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    def ItemNameChanged(self):
        if self.ItemName.currentIndex() != 0: return
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Name = str(self.ItemName.lineEdit().text())
        cursorPosition = self.ItemName.lineEdit().cursorPosition()
        self.ItemName.setItemText(0, item.Name)
        self.ItemName.lineEdit().setCursorPosition(cursorPosition)

    def ItemStateChanged(self, selection, column):
        self.ItemAttributeList[selection.text(column)].Equipped = selection.checkState(column)
        for item in self.ItemDictionary[selection.text(column)]:
            item.Equipped = selection.checkState(column)
        if selection.text(column) == self.SlotListTreeView.selectedIndexes():
            self.RestoreItem(self.ItemAttributeList[selection.text(column)])

    def ItemRealmChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Realm = self.ItemRealm.currentText()
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    def ItemTypeChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Type = self.ItemType.currentText()

    def ItemOriginChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Origin = self.ItemOrigin.currentText()

    def ItemLevelChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Level = self.ItemLevel.text()
        self.ItemLevel.setModified(False)
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    def ItemQualityChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Quality = self.ItemQuality.text()
        self.ItemQuality.setModified(False)

    def ItemDamageTypeChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.DamageType = self.ItemDamageType.currentText()

    def ItemBonusChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Bonus = self.ItemBonus.text()
        self.ItemBonus.setModified(False)

    def ItemAFDPSChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.AFDPS = self.ItemAFDPS.text()
        self.ItemAFDPS.setModified(False)

    def ItemSpeedChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Speed = self.ItemSpeed.text()
        self.ItemSpeed.setModified(False)

    def ItemLeftHandChanged(self, state):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.LeftHand = state

    def ItemRequirementChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Requirement = self.ItemRequirement.text()
        self.ItemRequirement.setModified(False)

    def ItemNotesChanged(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        item.Notes = self.ItemNotes.toPlainText()

    def ItemRestrictionsChanged(self, selection = None):
        item = self.ItemAttributeList[self.CurrentItemLabel]
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

    # TODO: 5TH SLOT SELECTION BASED ON TYPE / LOCATION ...
    def EffectTypeChanged(self, etype = None, index = -1):
        if index == -1: index = self.getSlotIndex()
        item = self.ItemAttributeList[self.CurrentItemLabel]
        self.EffectType[index].clear()

        if item.getSlot(index).getSlotType() == 'Craftable':
            self.EffectType[index].insertItems(0, CraftedTypeList)
        elif item.getSlot(index).getSlotType() == 'Enhanced':
            self.EffectType[index].insertItems(0, EnhancedTypeList)
        elif item.getSlot(index).getSlotType() == 'Dropped':
            self.EffectType[index].insertItems(0, DropTypeList)
        if item.Location != 'Two-Handed':
            self.EffectType[index].removeItem(self.EffectType[index].findText('Focus'))
        self.EffectType[index].setCurrentText(etype)
        item.getSlot(index).setEffectType(etype)

        # CASCADE THE CHANGES ...
        self.EffectChanged(item.getSlot(index).getEffect(), index)

    def EffectChanged(self, effect = None, index = -1):
        if index == -1: index = self.getSlotIndex()
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
            if item.getSlot(index).getSlotType() == 'Craftable' and effectType == 'Skill':
                for i in range(0, self.Effect[index].count()):
                    if self.Effect[index].itemText(i)[:5] != 'All M':
                        effect = self.Effect[index].itemText(i)
                        break
            else:
                effect = self.Effect[index].currentText()

        item.getSlot(index).setEffect(effect)
        self.Effect[index].setCurrentText(item.getSlot(index).getEffect())

        # CASCADE THE CHANGES ...
        self.EffectAmountChanged(item.getSlot(index).getEffectAmount(), index)

    def EffectAmountChanged(self, amount = None, index = -1):
        if index == -1: index = self.getSlotIndex()
        item = self.ItemAttributeList[self.CurrentItemLabel]

        valuesList = list()
        if item.getSlot(index).getSlotType() in ('Craftable', 'Enhanced'):
            if item.getSlot(index).getSlotType() == 'Craftable':
                if item.getSlot(index).getEffect()[0:9] in ('All Melee', 'All Magic'):
                    valuesList = CraftedValuesList[item.getSlot(index).getEffectType()][:1]
                else:
                    valuesList = CraftedValuesList[item.getSlot(index).getEffectType()]
            elif item.getSlot(index).getSlotType() == 'Enhanced':
                valuesList = EnhancedValuesList[item.getSlot(index).getEffectType()]
            if isinstance(valuesList, dict):
                valuesList = valuesList[item.getSlot(index).getEffect()]
            self.AmountStatic[index].clear()
            self.AmountStatic[index].insertItems(0, valuesList)
            if self.AmountStatic[index].findText(amount) == -1:
                amount = self.AmountStatic[index].currentText()
            item.getSlot(index).setEffectAmount(amount)
            self.AmountStatic[index].setCurrentText(item.getSlot(index).getEffectAmount())

        elif item.getSlot(index).getSlotType() == 'Dropped':
            if item.getSlot(index).getEffectType() == 'Unused':
                item.getSlot(index).setEffectAmount('')
                self.AmountEdit[index].clear()
            else:
                item.getSlot(index).setEffectAmount(amount)
                self.AmountEdit[index].setText(item.getSlot(index).getEffectAmount())
            self.AmountEdit[index].setModified(False)

        # CASCADE THE CHANGES ...
        self.EffectRequirementChanged(item.getSlot(index).getEffectRequirement(), index)
        self.calculate()

    def EffectRequirementChanged(self, requirement = None, index = -1):
        if index == -1: index = self.getSlotIndex()
        item = self.ItemAttributeList[self.CurrentItemLabel]

        if item.getSlot(index).getEffectType() == 'Unused':
            item.getSlot(index).setEffectRequirement('')
            self.Requirement[index].clear()
        else:
            if requirement is None:
                requirement = self.Requirement[index].text()
            item.getSlot(index).setEffectRequirement(requirement)
            self.Requirement[index].setText(item.getSlot(index).getEffectRequirement())
        self.Requirement[index].setModified(False)

    def newItem(self, action):
        newItemType = action.text().split(None, 1)[0]
        equipped = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        if newItemType in ('Crafted', 'Legendary'):
            item = Item(newItemType, self.CurrentItemLabel, self.CurrentRealm, self.ItemIndex)
        else:
            item = Item(newItemType, self.CurrentItemLabel, 'All', self.ItemIndex)
        item.Name = action.text()
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = equipped

        if newItemType == 'Legendary':
            if action.text().split(None, 1)[1] == 'Staff':
                item.getSlot(4).setAll('Focus', 'All Spell Lines', '50')
                item.getSlot(5).setAll('ToA Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Magic Damage', '3')
            elif action.text().split(None, 1)[1] == 'Bow':
                item.getSlot(4).setAll('ToA Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('ToA Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Magic Damage', '3')
            elif action.text().split(None, 1)[1] == 'Weapon':
                item.getSlot(4).setAll('ToA Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('ToA Bonus', 'Melee Damage', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Style Damage', '3')

        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])
        self.ItemIndex += 1

    def changeItem(self, index):
        equipped = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = 0

        try:  # FIXES BUG IN 'QComboBox' WHEN PRESSING ENTER ...
            item = self.ItemDictionary[self.CurrentItemLabel][index]
        except IndexError:
            item = self.ItemDictionary[self.CurrentItemLabel][0]

        self.ItemDictionary[self.CurrentItemLabel].remove(item)
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = equipped
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    def changeItemType(self, action):
        newItemType = action.text().split(None, 1)[0]
        equipped = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        index = self.ItemAttributeList[self.CurrentItemLabel].Index
        if newItemType in ('Crafted', 'Legendary'):
            item = Item(newItemType, self.CurrentItemLabel, self.CurrentRealm, index)
        else:
            item = Item(newItemType, self.CurrentItemLabel, 'All', index)
        item.Name = action.text()
        del self.ItemDictionary[self.CurrentItemLabel][0]
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = equipped

        if newItemType == 'Legendary':
            if action.text().split(None, 1)[1] == 'Staff':
                item.getSlot(4).setAll('Focus', 'All Spell Lines', '50')
                item.getSlot(5).setAll('ToA Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Magic Damage', '3')
            elif action.text().split(None, 1)[1] == 'Bow':
                item.getSlot(4).setAll('ToA Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('ToA Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Magic Damage', '3')
            elif action.text().split(None, 1)[1] == 'Weapon':
                item.getSlot(4).setAll('ToA Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('ToA Bonus', 'Melee Damage', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Style Damage', '3')

        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    def clearItem(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        itemState = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        self.ItemDictionary[self.CurrentItemLabel].remove(item)
        if item.ActiveState in ('Crafted', 'Legendary'):
            item = Item(item.ActiveState, self.CurrentItemLabel, self.CurrentRealm, item.Index)
        else:
            item = Item(item.ActiveState, self.CurrentItemLabel, 'All', item.Index)
        item.Name = item.ActiveState + ' Item'
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = itemState
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    def clearItemSlots(self):
        self.ItemAttributeList[self.CurrentItemLabel].clearSlots()
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    # TODO: LOAD PATH FROM SAVED SETTINGS ...
    # TODO: PREVENT CRAFTED ITEMS FROM BEING IMPORTED TO
    # TO NON-CRAFTABLE LOCATIONS. SET A DEFAULT PATH ...
    def loadItem(self):
        options = QFileDialog.Options()
        filename, filters = QFileDialog.getOpenFileName(
            self, 'Load Item:', '', 'Items (*.xml);; All Files (*.*)', options = options,)
        if filename == '': return

        item = Item('Imported', self.CurrentItemLabel, self.CurrentRealm, self.ItemIndex)
        if item.importFromXML(filename) != -1:
            self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
            self.ItemAttributeList[self.CurrentItemLabel] = item
            self.ItemAttributeList[self.CurrentItemLabel].Equipped = item.Equipped
            self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])
            self.ItemIndex += 1
        else:
            QMessageBox.warning(
                None, 'Error!', 'The item you are attempting to import\n is using an unsupported XML format.')
            return

    # TODO: LOAD PATH FROM SAVED SETTINGS ...
    def saveItem(self):
        item = self.ItemAttributeList[self.CurrentItemLabel]
        if not item.Name:
            QMessageBox.warning(
                None, 'Error!', 'You must specify a name before saving this item!')
            return
        options = QFileDialog.Options()
        filename, filters = QFileDialog.getSaveFileName(
            self, 'Save Item', item.Name, 'Items (*.xml);; All Files (*.*)', options = options)
        if filename: item.exportAsXML(filename)

    def deleteItem(self):
        if len(self.ItemDictionary[self.CurrentItemLabel]) == 1:
            self.clearItem()
            return
        equipped = self.ItemAttributeList[self.CurrentItemLabel].Equipped
        del self.ItemDictionary[self.CurrentItemLabel][0]
        item = self.ItemDictionary[self.CurrentItemLabel][0]
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.ItemAttributeList[self.CurrentItemLabel].Equipped = equipped
        self.RestoreItem(self.ItemAttributeList[self.CurrentItemLabel])

    # TODO: NEED TO ENSURE THAT ALL VARIABLE
    # DECLARATIONS ARE GETTING RESET ...
    def newTemplate(self):
        self.initialize()

    # TODO: LOAD PATH FROM SAVED SETTINGS ...
    def openTemplate(self):
        options = QFileDialog.Options()
        filename, filters = QFileDialog.getOpenFileName(
            self, "Open Template", '', 'Templates (*.ktf);; All Files (*.*)', options = options)

        if filename:
            self.importFromXML(filename)
            self.TemplateName = os.path.basename(filename)
            self.TemplatePath = os.path.dirname(filename)
            self.TemplateModified = False

    def saveTemplate(self):
        if None in (self.TemplateName, self.TemplatePath):
            self.saveTemplateAs()
        else:
            self.exportAsXML(os.path.join(self.TemplatePath, self.TemplateName))
            self.TemplateModified = False

    # TODO: LOAD PATH FROM SAVED SETTINGS ...
    def saveTemplateAs(self):
        options = QFileDialog.Options()
        filename, filters = QFileDialog.getSaveFileName(
            self, 'Save Item', '', 'Templates (*.ktf);; All Files (*.*)', options = options)

        if filename:
            self.exportAsXML(filename)
            self.TemplateName = os.path.basename(filename)
            self.TemplatePath = os.path.dirname(filename)
            self.TemplateModified = False

    def importLokiTemplate(self):
        pass

    def exportGemsToQuickbar(self):
        self.CraftBarDialog = CraftBarDialog(self, Qt.WindowCloseButtonHint, self.ItemAttributeList)
        self.CraftBarDialog.exec_()
