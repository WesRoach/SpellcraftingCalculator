# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import QAction, Qt, QKeySequence
from PyQt5.QtCore import QSize, QModelIndex, QRegExp, QVariant
from PyQt5.QtGui import QFont, QFontMetrics, QIcon, QRegExpValidator
from PyQt5.QtWidgets import QComboBox, QFileDialog, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QMenu, QMessageBox, QToolBar, QTreeWidgetItem, QTreeWidgetItemIterator, QStyle
from Character import AllBonusList, ClassList, ItemTypes, Races
from Constants import Cap, CraftedTypeList, CraftedEffectList, CraftedValuesList, DropTypeList, DropEffectList
from Constants import EnhancedTypeList, EnhancedEffectList, EnhancedValuesList, MythicalBonusCap, PVEBonusCap, TOABonusCap
from Item import Item
from QuickbarDialog import QuickbarDialog
from ReportDialog import ReportDialog
from Settings import Settings
from lxml import etree
import os
import re

Ui_MainWindow = uic.loadUiType(r'interface/MainWindow.ui')[0]


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None, flags = Qt.Window):
        QMainWindow.__init__(self, parent, flags)
        self.setupUi(self)

        # BUILD - MAJOR.YEAR.MONTHDAY ...
        self.BuildDate = "3.18.1001 (Alpha)"

        font = QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(8)
        self.setFont(font)

        self.Settings = Settings()
        self.Settings.load()

        self.FileMenu = QMenu('&File', self)
        self.EditMenu = QMenu('&Edit', self)
        self.ViewMenu = QMenu('&View', self)
        self.HelpMenu = QMenu('&Help', self)
        self.PathMenu = QMenu('Configure &Paths')
        self.ItemLoadMenu = QMenu('Load Item', self)
        self.ItemTypeMenu = QMenu('Item &Type', self)
        self.ItemNewMenu = QMenu('&New Item', self)
        self.RecentMenu = QMenu('Recent Templates', self)
        self.ToolbarMenu = QMenu('&Toolbar', self)
        self.Toolbar = QToolBar("Default Toolbar")

        self.DistanceToCap = QAction()
        self.UnusableSkills = QAction()

        self.StatLabel = {}
        self.StatValue = {}
        self.StatCap = {}
        self.StatMythicalCap = {}
        self.StatBonus = {}

        self.ItemAttributeList = {}
        self.ItemDictionary = {}
        self.ItemInfoWidgets = {}
        self.CurrentItemLabel = ''

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

        self.TemplateName = None
        self.TemplatePath = None
        self.InitialValues = None

        self.initMenuBar()
        self.initToolbar()
        self.initItemToolbar()
        self.initLayout()
        self.initialize()
        self.initControls()

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    @staticmethod
    def getIcon(name):
        icon = QIcon()
        for size in (16, 24, 32):
            icon.addFile(r'images/normal/' + f'{name}{size}.png', QSize(size, size), QIcon.Normal, QIcon.Off)
            icon.addFile(r'images/active/' + f'{name}{size}.png', QSize(size, size), QIcon.Active, QIcon.Off)
            icon.addFile(r'images/disabled/' + f'{name}{size}.png', QSize(size, size), QIcon.Disabled, QIcon.Off)
        return icon

    def initMenuBar(self):
        for (action, variable) in (
                ('Template Path ...', 'TemplatePath'),
                ('Item XML File Path ...', 'ItemPath'),
                ('Item Database Path ...', 'DatabasePath')):
            action = QAction(action, self)
            action.setData(variable)
            self.PathMenu.addAction(action)

        self.FileMenu.addAction('New Template', self.newTemplate)
        self.FileMenu.addAction('Open Template ...', self.openTemplate)
        self.FileMenu.addAction('Save Template', self.saveTemplate)
        self.FileMenu.addAction('Save Template As ...', self.saveTemplateAs)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction('Export Gem\'s to Quickbar ...', self.showQuickbarDialog)
        self.FileMenu.addSeparator()
        self.FileMenu.addMenu(self.PathMenu)
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
        self.EditMenu.addSeparator()
        self.EditMenu.addMenu(self.ItemNewMenu)
        self.EditMenu.addAction('Delete Item', self.deleteItem)
        self.EditMenu.addAction('Clear Item', self.clearItem)
        self.EditMenu.addAction('Clear Slots', self.clearItemSlots)

        for (title, res) in (("Large", 32), ("Normal", 24), ("Small", 16), ("Hide", 0)):
            action = QAction(title, self)
            action.setData(QVariant(res))
            action.setCheckable(True)
            self.ToolbarMenu.addAction(action)

        self.DistanceToCap = QAction('&Distance to Cap', self)
        self.DistanceToCap.setShortcut(QKeySequence(Qt.ALT + Qt.Key_D))
        self.DistanceToCap.setCheckable(True)

        self.UnusableSkills = QAction('&Unusable Skills', self)
        self.UnusableSkills.setShortcut(QKeySequence(Qt.ALT + Qt.Key_U))
        self.UnusableSkills.setCheckable(True)

        self.ViewMenu.addAction('&Material Report ...', self.showMaterialsReport)
        self.ViewMenu.addAction('&Template Report ...', self.showTemplateReport)
        self.ViewMenu.addSeparator()
        self.ViewMenu.addMenu(self.ToolbarMenu)
        self.ViewMenu.addSeparator()
        self.ViewMenu.addAction(self.DistanceToCap)
        self.ViewMenu.addAction(self.UnusableSkills)

        empty_note = QAction('Nothing Here ...', self)
        empty_note.setDisabled(True)
        self.HelpMenu.addAction(empty_note)

        self.menuBar().addMenu(self.FileMenu)
        self.menuBar().addMenu(self.EditMenu)
        self.menuBar().addMenu(self.ViewMenu)
        self.menuBar().addMenu(self.HelpMenu)

    def initToolbar(self):
        self.Toolbar.setFloatable(False)
        self.Toolbar.addAction('New Template', self.newTemplate)
        self.Toolbar.addAction('Open Template', self.openTemplate)
        self.Toolbar.addAction('Save Template', self.saveTemplate)
        self.Toolbar.addAction('Save Template As', self.saveTemplateAs)
        self.Toolbar.addSeparator()
        self.Toolbar.addAction('Export Gems', self.showQuickbarDialog)
        self.Toolbar.addSeparator()
        self.Toolbar.addAction('Materials Report', self.showMaterialsReport)
        self.Toolbar.addAction('Template Report', self.showTemplateReport)
        self.addToolBar(self.Toolbar)

    def initItemToolbar(self):
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
        self.ItemDeleteButton.clicked.connect(self.deleteItem)
        self.ItemSaveButton.setToolTip('Save Item')
        self.ItemSaveButton.clicked.connect(self.saveItem)

    def initLayout(self):
        self.setWindowTitle(f"Kort's Spellcrafting Calculator - {self.BuildDate}")

        saved_state = int(self.Settings.get('GENERAL', 'ToolbarSize'))
        for action in self.ToolbarMenu.actions():
            if action.data() == saved_state:
                self.setToolbarOptions(action)

        saved_state = self.Settings.get('GENERAL', 'DistanceToCap') in 'True'
        self.DistanceToCap.setChecked(saved_state)

        saved_state = self.Settings.get('GENERAL', 'UnusableSkills') in 'True'
        self.UnusableSkills.setChecked(saved_state)

        # MAKE SURE WE ARE TESTING WIDTH AND HEIGHT
        # VALUES BASED ON THE FONT BEING USED ...
        test_font = QFontMetrics(self.font())

        # INTEGER AND DOUBLE VALIDATORS ...
        int_regex = QRegExp('^(?:[0-9]{0,3})$')
        int_validator = QRegExpValidator(int_regex)
        dbl_regex = QRegExp('^(?:[0-9]{3}|[0-9][0-9]?(?:\.[0-9])?)$')
        dbl_validator = QRegExpValidator(dbl_regex)

        # TODO: GET WIDTH FROM CLASS DICT ...
        width = self.getComboBoxWidth('Necromancer')
        self.CharacterName.setFixedWidth(width)
        self.CharacterRealm.setFixedWidth(width)
        self.CharacterClass.setFixedWidth(width)
        self.CharacterRace.setFixedWidth(width)
        self.CharacterLevel.setFixedWidth(width)
        self.CharacterLevel.setValidator(int_validator)
        self.CharacterRealmRank.setFixedWidth(width)
        self.CharacterRealmRank.setValidator(int_validator)
        self.CharacterChampLevel.setFixedWidth(width)
        self.CharacterChampLevel.setValidator(int_validator)

        for attribute in DropEffectList['All']['Attribute'] + ('ArmorFactor', 'Fatigue', 'PowerPool'):
            attribute = attribute.replace(' ', '')
            self.StatLabel[attribute] = getattr(self, attribute + 'Label')
            self.StatValue[attribute] = getattr(self, attribute)
            self.StatCap[attribute] = getattr(self, attribute + 'Cap')

            try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
                self.StatMythicalCap[attribute] = getattr(self, attribute + 'MythicalCap')
            except AttributeError:
                pass

        width = test_font.size(Qt.TextSingleLine, "POW:", tabArray = None).width()
        self.AttributesGroup.layout().setColumnMinimumWidth(0, width)
        width = test_font.size(Qt.TextSingleLine, "-400", tabArray = None).width()
        self.AttributesGroup.layout().setColumnMinimumWidth(1, width)
        width = test_font.size(Qt.TextSingleLine, "(-400)", tabArray = None).width()
        self.AttributesGroup.layout().setColumnMinimumWidth(2, width)
        width = test_font.size(Qt.TextSingleLine, "(-26)", tabArray = None).width()
        self.AttributesGroup.layout().setColumnMinimumWidth(3, width)

        for resist in DropEffectList['All']['Resistance']:
            self.StatLabel[resist] = getattr(self, resist + 'Label')
            self.StatValue[resist] = getattr(self, resist)
            self.StatBonus[resist] = getattr(self, resist + 'Cap')

            try:  # NOT ALL RESISTS HAVE MYTHICAL CAP ...
                self.StatMythicalCap[resist] = getattr(self, resist + 'MythicalCap')
            except AttributeError:
                pass

        width = test_font.size(Qt.TextSingleLine, "Essence:", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(0, width)
        width = test_font.size(Qt.TextSingleLine, "-26", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(1, width)
        width = test_font.size(Qt.TextSingleLine, "(-15)", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(2, width)
        width = test_font.size(Qt.TextSingleLine, "+5", tabArray = None).width()
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

        width = self.ConfigurationGroup.sizeHint().width()
        self.SlotListTreeView.setMinimumWidth(width)

        self.CharacterRealm.insertItems(0, self.getRealms())

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

        # TODO: DYNAMICALL SET THESE LATER ...
        self.ItemNewButton.setFixedWidth(34)
        self.ItemTypeButton.setFixedWidth(34)
        self.ItemLoadButton.setFixedWidth(34)
        self.ItemDeleteButton.setFixedWidth(34)
        self.ItemSaveButton.setFixedWidth(34)

        width = test_font.size(Qt.TextSingleLine, "Slot 12:", tabArray = None).width()
        self.ItemStatsGroup.layout().setColumnMinimumWidth(0, width)

        # TODO: GET WIDTH FROM EFFECT TYPE DICT ...
        width = self.getComboBoxWidth("Mythical Resists & Caps")
        for index in range(0, 12):
            self.EffectType.append(getattr(self, 'EffectType%d' % index))
            self.EffectType[index].activated[str].connect(self.changeEffectType)
            self.EffectType[index].setFixedWidth(width)

        width = self.getComboBoxWidth('76')
        for index in range(0, 12):
            self.AmountEdit.append(getattr(self, 'AmountEdit%d' % index))
            self.AmountEdit[index].textEdited[str].connect(self.changeEffectAmount)
            self.AmountEdit[index].setValidator(int_validator)
            self.AmountEdit[index].setFixedWidth(width)

        for index in range(0, 5):
            self.AmountStatic.append(getattr(self, 'AmountStatic%d' % index))
            self.AmountStatic[index].activated[str].connect(self.changeEffectAmount)
            self.AmountStatic[index].setFixedWidth(width)

        # TODO: GET WIDTH FROM EFFECT DICT ...
        width = self.getComboBoxWidth("Neg. Effect Duration Reduction")
        for index in range(0, 12):
            self.SlotLabel.append(getattr(self, 'SlotLabel%d' % index))
            self.Effect.append(getattr(self, 'Effect%d' % index))
            self.Effect[index].activated[str].connect(self.changeEffect)
            self.Effect[index].setFixedWidth(width)

        width = self.getLineEditWidth("vs. Enemy Players")
        for index in range(0, 12):
            self.Requirement.append(getattr(self, 'Requirement%d' % index))
            self.Requirement[index].textEdited.connect(self.changeEffectRequirement)
            self.Requirement[index].setFixedWidth(width)

        width = test_font.size(Qt.TextSingleLine, "-////-", tabArray=None).width()
        for index in range(0, 4):
            self.ImbuePoints.append(getattr(self, 'ImbuePoints%d' % index))
            self.GemNameLabel.append(getattr(self, 'GemNameLabel%d' % index))
            self.ImbuePoints[index].setFixedWidth(width)

        for index in range(0, 7):
            self.GemName.append(getattr(self, 'GemName%d' % index))

        width = self.Requirement[0].width()
        for index in range(4, 7):
            self.GemName[index].setFixedWidth(width)

        width = test_font.size(Qt.TextSingleLine, "37.5", tabArray = None).width()
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
                self.ItemLeftHand
            ],

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

        width = self.getLineEditWidth("16.5")
        self.ItemLevel.setFixedWidth(width)
        self.ItemLevel.setValidator(int_validator)
        self.ItemQuality.setFixedWidth(width)
        self.ItemQuality.setValidator(int_validator)
        self.ItemBonus.setFixedWidth(width)
        self.ItemBonus.setValidator(int_validator)
        self.ItemAFDPS.setFixedWidth(width)
        self.ItemAFDPS.setValidator(dbl_validator)
        self.ItemSpeed.setFixedWidth(width)
        self.ItemSpeed.setValidator(dbl_validator)

        layout = self.ItemInformationGroup.layout()
        width = test_font.width("Damage:")
        width += test_font.width("AF/DPS:")
        width += self.ItemLevel.width()
        width += self.ItemQuality.width()
        width += layout.contentsMargins().left()
        width += layout.contentsMargins().right()
        width += layout.horizontalSpacing() * 3
        self.ItemInformationGroup.setFixedWidth(width)

        # SERIOUSLY QT?! ...
        lw = self.ItemRestrictionsList
        fm = lw.fontMetrics()
        cm = lw.contentsMargins()
        gm = self.ItemRestrictionsGroup.layout().contentsMargins()
        ch = self.style().pixelMetric(QStyle.PM_DefaultChildMargin)
        fw = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        iw = self.style().pixelMetric(QStyle.PM_ListViewIconSize)
        sw = self.style().pixelMetric(QStyle.PM_ScrollBarExtent)

        width = fm.width('Necromancer')
        width += cm.left() + cm.right()
        width += gm.left() + gm.right()
        width += ch + iw + sw + fw * 4

        # NEED QListWidget Frame, QGroupBox Frame, QGroupBox Margins

        print(fm.width('Necromancer'), cm.left(), cm.right(), ch, iw, sw, fw * 2)

        # TODO: SET A DYNAMIC WIDTH ...
        self.ItemRestrictionsGroup.setFixedWidth(width)

        width = test_font.size(Qt.TextSingleLine, "1999.9", tabArray = None).width()
        self.BuildUtility.setFixedWidth(width)
        self.BuildUtility.setAlignment(Qt.AlignRight)
        self.StatusBar.setStyleSheet('QStatusBar::item {border: None;}')
        self.StatusBar.addPermanentWidget(QLabel('Build Utility: '))
        self.StatusBar.addPermanentWidget(self.BuildUtility)

    def initialize(self, new_template = True):
        self.TemplateName = None
        self.TemplatePath = None
        self.InitialValues = None

        # SET INITIAL STATS ...
        self.setCharName('')
        self.setCharLevel('50')
        self.setCharRealmRank('')
        self.setCharChampLevel('')

        # SET INITIAL REALM ...
        self.setCharRealm('Midgard')
        self.changeCharRealm(self.getCharRealm())

        for parent, locations in ItemTypes.items():
            for location in locations:
                if parent == 'Armor':
                    item = Item('Crafted', location, self.getCharRealm())
                    item.setName(f'{item.getState()} Item')
                else:
                    item = Item('Dropped', location, 'All')
                    item.setName(f'{item.getState()} Item')
                self.ItemAttributeList[location] = item
                self.ItemDictionary[location] = [item]

        # GET INITIAL TEMPLATE VALUES ...
        if new_template:
            self.InitialValues = self.exportAsXML(None, True, False)

        # SET INITIAL ITEM SLOT ...
        self.changeItemSelection('Neck')

        iterator = QTreeWidgetItemIterator(self.SlotListTreeView)
        while iterator.value():
            selection = iterator.value()
            if selection.flags() & Qt.ItemIsUserCheckable:
                if self.ItemAttributeList[selection.text(0)].isEquipped():
                    selection.setCheckState(0, Qt.Checked)
                else:
                    selection.setCheckState(0, Qt.Unchecked)
            iterator += 1

        self.calculate()

    def initControls(self):
        self.PathMenu.triggered.connect(self.changeFilePath)
        self.ItemTypeMenu.triggered.connect(self.convertItem)
        self.ItemNewMenu.triggered.connect(self.newItem)
        self.ToolbarMenu.triggered.connect(self.setToolbarOptions)
        self.DistanceToCap.triggered.connect(self.setDistanceToCap)
        self.UnusableSkills.triggered.connect(self.setUnusableSkills)
        self.CharacterLevel.editingFinished.connect(self.changeCharLevel)
        self.CharacterRealmRank.editingFinished.connect(self.changeCharRealmRank)
        self.CharacterChampLevel.editingFinished.connect(self.changeCharChampLevel)
        self.ItemLevel.editingFinished.connect(self.changeItemLevel)
        self.ItemQuality.editingFinished.connect(self.changeItemQuality)
        self.ItemBonus.editingFinished.connect(self.changeItemBonus)
        self.ItemAFDPS.editingFinished.connect(self.changeItemAFDPS)
        self.ItemSpeed.editingFinished.connect(self.changeItemSpeed)
        self.ItemRequirement.editingFinished.connect(self.changeItemRequirement)
        self.ItemNotes.textChanged.connect(self.changeItemNotes)
        self.CharacterRealm.activated[str].connect(self.changeCharRealm)
        self.CharacterClass.activated[str].connect(self.changeCharClass)
        self.CharacterRace.activated[str].connect(self.changeCharRace)
        self.ItemName.activated[int].connect(self.changeItem)
        self.ItemName.editTextChanged[str].connect(self.changeItemName)
        self.ItemRealm.activated[str].connect(self.changeItemRealm)
        self.ItemType.activated[str].connect(self.changeItemType)
        self.ItemOrigin.activated[str].connect(self.changeItemOrigin)
        self.ItemDamageType.activated[str].connect(self.changeItemDamageType)
        self.ItemLeftHand.stateChanged.connect(self.changeItemLeftHand)
        self.SlotListTreeView.itemSelectionChanged.connect(self.changeItemSelection)
        self.SlotListTreeView.itemChanged.connect(self.changeItemState)
        self.ItemRestrictionsList.itemChanged.connect(self.changeItemRestrictions)


# =============================================== #
#             DIALOG & WINDOW METHODS             #
# =============================================== #

    def showItemDatabase(self):
        pass

    def showMaterialsReport(self):
        MaterialsReport = ReportDialog(self, Qt.WindowCloseButtonHint)
        MaterialsReport.materialsReport(self.ItemAttributeList, self.getCharRealm())
        MaterialsReport.exec_()

    def showTemplateReport(self):
        TemplateReport = ReportDialog(self, Qt.WindowCloseButtonHint)
        TemplateReport.templateReport(self.exportAsXML(None, True, True))
        TemplateReport.exec_()

    def showQuickbarDialog(self):
        Dialog = QuickbarDialog(self, Qt.WindowCloseButtonHint, self.ItemAttributeList)
        Dialog.exec_()

# =============================================== #
#                 XML PROCESSING                  #
# =============================================== #

    def importFromXML(self, filename):
        tree = etree.parse(filename)

        # RETURN ERROR CODE ...
        if tree.getroot().tag == 'Template':
            self.initialize(False)
        else:
            return -1

        items = list()
        elements = tree.getroot().getchildren()
        for element in elements:
            if element.tag == 'Name':
                self.setCharName(element.text)
            elif element.tag == 'Realm':
                self.changeCharRealm(element.text)
            elif element.tag == 'Class':
                self.changeCharClass(element.text)
            elif element.tag == 'Race':
                self.changeCharRace(element.text)
            elif element.tag == 'Level':
                self.setCharLevel(element.text)
            elif element.tag == 'RealmRank':
                self.setCharRealmRank(element.text)
            elif element.tag == 'Item':
                items.append(element)

        self.ItemDictionary.clear()
        self.ItemAttributeList.clear()
        for locations in ItemTypes.values():
            for location in locations:
                self.ItemDictionary[location] = list()

        for item_xml in items:
            item = Item('Imported')
            item.importFromXML(item_xml, True)
            if int(item_xml.attrib['Index']) == 0:
                self.ItemAttributeList[item.getLocation()] = item
            self.ItemDictionary[item.getLocation()].insert(int(item_xml.attrib['Index']), item)

        # GET INITIAL TEMPLATE VALUES ...
        self.InitialValues = self.exportAsXML(None, True, False)

        # CASCADE THE CHANGES ...
        self.restoreItem(self.getItem(self.CurrentItemLabel))

    def exportAsXML(self, filename, export = False, report = False):
        template = etree.Element('Template')

        xml_fields = {
            'Name': self.getCharName(),
            'Realm': self.getCharRealm(),
            'Class': self.getCharClass(),
            'Race': self.getCharRace(),
            'Level': self.getCharLevel(),
            'RealmRank': self.getCharRealmRank(),
            'ChampLevel': self.getCharChampLevel(),
        }

        for (attribute, value) in xml_fields.items():
            if value:
                etree.SubElement(template, attribute).text = str(value)

        for items in self.ItemDictionary.values():
            for item in items:
                if report:
                    element = item.exportAsXML(None, True, True)
                else:
                    element = item.exportAsXML(None, True, False)
                element.set('Index', str(items.index(item)))
                template.append(element)

        if report:
            total = self.summarize()

            for key in (x for x in total.keys() if x != 'Utility'):
                element = etree.SubElement(template, key)
                if key[-7:] == 'Bonuses':
                    element.attrib['Text'] = str(f'{key[:-7]} {key[-7:]}')
                for attribute, bonuses in total[key].items():
                    tag = ''.join(x for x in attribute if x.isalnum())
                    if tag != attribute:
                        root = etree.SubElement(element, tag, Text = attribute)
                    else:
                        root = etree.SubElement(element, tag)
                    for bonus, value in bonuses.items():
                        etree.SubElement(root, bonus).text = str(value)

        if not export:
            with open(filename, 'wb') as document:
                document.write(etree.tostring(template, encoding='UTF-8', pretty_print = True, xml_declaration = True))
        else:
            return template

# =============================================== #
#           LAYOUT CHANGE/UPDATE METHODS          #
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
            if item.getSlot(index).getSlotType() == 'Crafted':
                self.SlotLabel[index].setText(f'Gem {index + 1}:')
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
            if item.getSlot(index).isCrafted():
                self.SlotLabel[index].setText(f'Gem {index + 1}:')
            if item.getSlot(index).isDropped():
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
            if item.getSlot(index).isDropped():
                self.SlotLabel[index].setText(f'Slot {index + 1}:')
                self.EffectType[index].setDisabled(False)
                self.Effect[index].setDisabled(False)
                self.AmountEdit[index].setDisabled(False)

    def updateMenuOptions(self, item):
        self.ItemNewMenu.clear()
        self.ItemTypeMenu.clear()
        options = []

        if item.getParent() in ('Armor', 'Weapons'):
            self.ItemTypeMenu.setEnabled(True)
            self.ItemTypeButton.setEnabled(True)

        if item.getLocation() in ItemTypes['Armor']:
            options.extend([
                'Crafted Item',
                'Dropped Item',
            ])
        elif item.getLocation() in ('Right Hand', 'Left Hand'):
            options.extend([
                'Crafted Item',
                'Dropped Item',
                'Legendary Weapon',
            ])
        elif item.getLocation() == 'Two-Handed':
            options.extend([
                'Crafted Item',
                'Dropped Item',
                'Legendary Staff',
                'Legendary Weapon',
            ])
        elif item.getLocation() == 'Ranged':
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

    def restoreItem(self, item):
        if item.isCrafted():
            self.showCraftWidgets(item)
        elif item.isLegendary():
            self.showLegendaryWidgets(item)
        elif item.isDropped():
            self.showDropWidgets(item)

        # VALIDATE ATTRIBUTES ...
        self.validateAttributes()

        # BLOCK WIDGET SIGNALS ...
        self.SlotListTreeView.blockSignals(True)

        iterator = QTreeWidgetItemIterator(self.SlotListTreeView)
        while iterator.value():
            selection = iterator.value()
            if selection.flags() & Qt.ItemIsUserCheckable:
                if self.ItemAttributeList[selection.text(0)].isEquipped():
                    selection.setCheckState(0, Qt.Checked)
                else:
                    selection.setCheckState(0, Qt.Unchecked)
            iterator += 1

        # UNBLOCK WIDGET SIGNALS ...
        self.SlotListTreeView.blockSignals(False)

        for widget in (
                self.ItemName,
                self.ItemRealm,
                self.ItemType,
                self.ItemOrigin,
                self.ItemDamageType,
        ): widget.clear()

        for index in range(len(self.EffectType)):
            self.EffectType[index].clear()
        for index in range(len(self.AmountEdit)):
            self.AmountEdit[index].clear()
        for index in range(len(self.AmountStatic)):
            self.AmountStatic[index].clear()
        for index in range(len(self.Effect)):
            self.Effect[index].clear()
        for index in range(len(self.Requirement)):
            self.Requirement[index].clear()

        for widget in self.ItemInfoWidgets['All']:
            widget.setEnabled(True)
        for widget in self.ItemInfoWidgets[item.getParent()]:
            widget.setDisabled(True)

        for item_entry in self.ItemDictionary[item.getLocation()]:
            self.ItemName.addItem(item_entry.getName())
        self.ItemName.setCurrentIndex(0)

        if item.isPlayerCrafted():
            origins = ('Crafted',)
            self.ItemRealm.insertItems(0, self.getRealms())
            self.ItemOrigin.insertItems(0, origins)
        elif item.isDropped():
            origins = ('Drop', 'Quest', 'Artifact', 'Merchant')
            self.ItemRealm.insertItems(0, ('All',) + self.getRealms())
            self.ItemOrigin.insertItems(0, ('',) + origins)

        try:  # NOT ALL ITEM TYPES HAVE A REALM ...
            item_types = ItemTypes[item.getParent()][item.getLocation()][item.getRealm()]
        except KeyError:
            item_types = ItemTypes[item.getParent()][item.getLocation()]['All']

        # UPDATE THE COMBOBOX ...
        self.ItemType.insertItems(0, ('',) + item_types)

        if item.getParent() == 'Weapons':
            if item.isCrafted():
                damage_types = ('Slash', 'Thrust', 'Crush')
                self.ItemDamageType.insertItems(0, ('',) + damage_types)
            elif item.isLegendary():
                damage_types = ('Body', 'Cold', 'Heat', 'Energy', 'Matter', 'Spirit')
                self.ItemDamageType.insertItems(0, ('',) + damage_types)
            elif item.isDropped():
                damage_types = ('Slash', 'Thrust', 'Crush')
                self.ItemDamageType.insertItems(0, ('',) + damage_types)

        self.ItemRealm.setCurrentText(item.getRealm())
        self.ItemOrigin.setCurrentText(item.getOrigin())
        self.ItemDamageType.setCurrentText(item.getDamageType())
        self.ItemType.setCurrentText(item.getType())
        self.ItemLevel.setText(item.getLevel())
        self.ItemQuality.setText(item.getQuality())
        self.ItemBonus.setText(item.getBonus())
        self.ItemAFDPS.setText(item.getAFDPS())
        self.ItemSpeed.setText(item.getSpeed())

        if item.isLeftHand():
            self.ItemLeftHand.setCheckState(Qt.Checked)
        else:
            self.ItemLeftHand.setCheckState(Qt.Unchecked)

        self.ItemRequirement.setText(item.getRequirement())
        self.ItemNotes.setPlainText(item.getNotes())

        list_entry = QListWidgetItem('All')
        list_entry.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        list_entry.setCheckState(Qt.Unchecked)

        self.ItemRestrictionsList.clear()
        self.ItemRestrictionsList.addItem(list_entry)

        for key in ClassList['All']:
            list_entry = QListWidgetItem(key)
            list_entry.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            list_entry.setCheckState(Qt.Unchecked)
            self.ItemRestrictionsList.addItem(list_entry)

        for index in range(self.ItemRestrictionsList.count()):
            lsit_entry = self.ItemRestrictionsList.item(index)
            if list_entry.text() not in (('All',) + ClassList[item.getRealm()]):
                list_entry.setHidden(True)

        # BLOCK WIDGET SIGNALS ...
        self.ItemRestrictionsList.blockSignals(True)

        for index in range(self.ItemRestrictionsList.count()):
            list_entry = self.ItemRestrictionsList.item(index)
            if list_entry.text() in item.getRestrictions():
                if list_entry.text() in (('All',) + ClassList[item.getRealm()]):
                    list_entry.setCheckState(Qt.Checked)
                else:
                    list_entry.setCheckState(Qt.Unchecked)
                    self.changeItemRestrictions(list_entry)

        # UNBLOCK WIDGET SIGNALS ...
        self.ItemRestrictionsList.blockSignals(False)

        for index in range(0, item.getSlotCount()):
            self.updateEffectTypeList(index)

        # UPDATE THE MENUS ...
        self.updateMenuOptions(item)

# =============================================== #
#        SUMMARIZER AND CALCULATOR METHODS        #
# =============================================== #

    # MOSTLY LEGACY CODE ...
    def summarize(self):

        # BUG: CRASH HERE ...
        Level = int(self.getCharLevel())

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

            race = self.getCharRace()
            if effect in Races['All'][race]['Resistances']:
                total['Resistances'][effect]['RacialBonus'] = Races['All'][race]['Resistances'][effect]

            Base = Cap['Resistance']
            BaseMythicalCap = MythicalBonusCap['Resist Cap']
            total['Resistances'][effect]['Base'] = int(Level * Base[0]) + Base[1]
            total['Resistances'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        for key, item in self.ItemAttributeList.items():
            if not item.isEquipped():
                continue

            total['Utility'] += item.getUtility()

            for index in range(0, item.getSlotCount()):
                effect = item.getSlot(index).getEffect()
                amount = int('0' + re.sub('[^\d]', '', item.getSlot(index).getEffectAmount()))

                if item.getSlot(index).getEffectType() == 'Skill':
                    effects = [effect, ]

                    if effect.split(None)[0] == 'All':
                        if effect in AllBonusList[self.getCharRealm()][self.getCharClass()]:
                            effects.extend(AllBonusList[self.getCharRealm()][self.getCharClass()][effect])

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
                        effects.extend(AllBonusList[self.getCharRealm()][self.getCharClass()][effect])

                    for effect in effects:
                        amts = total['Attributes'][effect]
                        amts['TotalBonus'] += amount
                        amts['Bonus'] = min(amts['TotalBonus'], amts['Base'] + amts['CapBonus'])

                elif item.getSlot(index).getEffectType() == 'Attribute Cap':
                    effects = [effect, ]

                    if effect == 'Power':
                        effects.append('% Power Pool')

                    elif effect == 'Acuity':
                        effects.extend(AllBonusList[self.getCharRealm()][self.getCharClass()][effect])

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

                    if effect.split(None)[0] == 'All':
                        effects.extend(AllBonusList[self.getCharRealm()][self.getCharClass()][effect])

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

                    elif effect == 'Casting Speed':
                        effect = "Archery and Casting Speed"

                    elif effect == 'Magic Damage':
                        effect = "Archery and Magic Damage"

                    elif effect == 'Spell Range':
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
                        effects.extend(AllBonusList[self.getCharRealm()][self.getCharClass()][effect])

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
                        effects.extend(AllBonusList[self.getCharRealm()][self.getCharClass()][effect])

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

        # THIS IS DIRTY ... BUT IT WORKS ...
        for attribute, amts in total['Attributes'].items():
            if attribute in DropEffectList['All']['Mythical Stat Cap']:
                amts['BaseMythicalCap'] = amts['BaseMythicalCap'] - amts['CapBonus']
                amts['MythicalCapBonus'] = min(amts['TotalMythicalCapBonus'], amts['BaseMythicalCap'])

        return total

    # MOSTLY LEGACY CODE ...
    def calculate(self):
        total = self.summarize()

        item = self.getItem()
        self.BuildUtility.setText(f'{total["Utility"]:3.1f}')
        self.ItemUtility.setText(f'{item.getUtility():3.1f}')

        if item.isPlayerCrafted():
            self.ItemImbuePointsTotal.setText(f'{sum(item.getImbueValues()):3.1f}')
            self.ItemImbuePoints.setText(f'/ {item.getMaxImbueValue()}')

            for index in range(0, item.getSlotCount()):
                if index < len(item.getImbueValues()):
                    self.ImbuePoints[index].setText(f'{item.getImbueValues()[index]:3.1f}')
                self.GemName[index].setText(item.getSlot(index).getGemName(self.getCharRealm()))

            success = item.getOverchargeSuccess()
            if isinstance(success, int):
                self.ItemOvercharge.setText(f'{success}%')
            else:
                self.ItemOvercharge.setText(f'{success}')

        for key, datum in total['Attributes'].items():
            Acuity = AllBonusList[self.getCharRealm()][self.getCharClass()]["Acuity"]
            TotalBonus = datum['TotalBonus']

            if key == 'Hit Points':
                key = "HitPoints"

            elif key == 'Armor Factor':
                key = "ArmorFactor"

            elif key == '% Power Pool':
                key = "PowerPool"

            if key[:5] == "Power":
                Skills = AllBonusList[self.getCharRealm()][self.getCharClass()]["All Magic Skills"]
                self.showCharacterStat(key, (datum['TotalCapBonus'] > 0)
                            or (datum['TotalMythicalCapBonus'] > 0)
                            or (TotalBonus > 0)
                            or (len(Skills) > 0))

            elif key == "Fatigue":
                Skills = AllBonusList[self.getCharRealm()][self.getCharClass()]["All Melee Weapon Skills"]
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
                self.StatCap[key].setText(f'({datum["TotalCapBonus"]})')
                self.StatMythicalCap[key].setText(f'({datum["TotalMythicalCapBonus"]})')

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
                self.StatCap[key].setText(f'({BaseCap - TotalCapBonus})')
                self.StatMythicalCap[key].setText(f'({BaseMythicalCap - TotalMythicalCapBonus})')

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
                self.StatMythicalCap[key].setText(f'({amts["TotalMythicalCapBonus"]})')

            elif self.DistanceToCap.isChecked():
                self.StatValue[key].setText(str(int(Base - TotalBonus)))
                self.StatMythicalCap[key].setText(f'({BaseMythicalCap - TotalMythicalCapBonus})')

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

# =============================================== #
#                COLORIZER METHOD                 #
# =============================================== #

    # TODO: IMPLEMENT ...
    def colorize(self):
        pass

# =============================================== #
#                VALIDATOR METHODS                #
# =============================================== #

    # TODO: IMPLEMENT ...
    def validateEntry(self):
        pass

    def validateAttributes(self, invalid = False):
        if not self.UnusableSkills.isChecked():
            for item in self.ItemAttributeList.values():
                for slot in [x for x in item.getSlotList() if x.isCrafted()]:
                    class_skills = AllBonusList['All'][self.getCharClass()]['All Skills']
                    if slot.getEffectType() == 'Skill' and slot.getEffect() not in class_skills:
                        slot.setEffect(self.getFirstClassSkill())
                        invalid = True
        if invalid:
            QMessageBox.information(
                self, 'Attribute Change',
                'Some attributes on equipped items were not \n'
                'available in the selected class\'s skill tree.',
                QMessageBox.Ok, QMessageBox.Ok
            )

# =============================================== #
#                  SETTER METHODS                 #
# =============================================== #

    def setCharName(self, char_name):
        self.CharacterName.setText(str(char_name))

    def setCharRealm(self, char_realm):
        self.CharacterRealm.setCurrentText(str(char_realm))

    def setCharClass(self, char_class):
        self.CharacterClass.setCurrentText(str(char_class))

    def setCharRace(self, char_race):
        self.CharacterRace.setCurrentText(str(char_race))

    def setCharLevel(self, char_level):
        self.CharacterLevel.setText(str(char_level))

    def setCharRealmRank(self, char_realm_rank):
        self.CharacterRealmRank.setText(str(char_realm_rank))

    def setCharChampLevel(self, char_champion_level):
        self.CharacterChampLevel.setText(str(char_champion_level))

    def setCurrentItem(self, item, location):
        self.ItemAttributeList[location] = item

    def setDistanceToCap(self):
        self.restoreItem(self.getItem())
        self.calculate()

    def setUnusableSkills(self):
        self.restoreItem(self.getItem())
        self.calculate()

# =============================================== #
#                  GETTER METHODS                 #
# =============================================== #

    @staticmethod
    def getRealms():
        return tuple(('Albion', 'Hibernia', 'Midgard'))

    def getClasses(self):
        return tuple(ClassList[self.getCharRealm()])

    def getRaces(self):
        return tuple(AllBonusList[self.getCharRealm()][self.getCharClass()]['Races'])

    def getCharName(self):
        return str(self.CharacterName.text())

    def getCharRealm(self):
        return str(self.CharacterRealm.currentText())

    def getCharClass(self):
        return str(self.CharacterClass.currentText())

    def getCharRace(self):
        return str(self.CharacterRace.currentText())

    def getCharLevel(self):
        return str(self.CharacterLevel.text())

    def getCharRealmRank(self):
        return str(self.CharacterRealmRank.text())

    def getCharChampLevel(self):
        return str(self.CharacterChampLevel.text())

    def getItem(self, location = None):
        location = location if location else self.CurrentItemLabel
        return self.ItemAttributeList[location]

    def getSlotIndex(self):
        index = self.sender().objectName()[-2:]
        if not index.isdigit(): index = index[-1:]
        return int(index)

    def getFirstClassSkill(self):
        for class_skill in AllBonusList['All'][self.getCharClass()]['All Skills']:
            if class_skill.split(None)[0] != 'All':
                return str(class_skill)

    # TODO: PASS IN LIST OF VALUES ...
    def getComboBoxWidth(self, value):
        cb = self.CharacterRealm
        const_values = 4 + 2
        font_metrics = cb.fontMetrics()
        cont_margins = cb.contentsMargins()
        scroll_width = self.style().pixelMetric(QStyle.PM_ScrollBarExtent)
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)

        width = font_metrics.width(value)
        width += cont_margins.left() + cont_margins.right()
        width += const_values + scroll_width + frame_width * 2
        return width

    # TODO: PASS IN LIST OF VALUES ...
    def getLineEditWidth(self, value):
        le = self.CharacterName
        const_values = 4 + 2
        font_metrics = le.fontMetrics()
        text_margins = le.textMargins()
        cont_margins = le.contentsMargins()
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)

        width = font_metrics.width(value)
        width += text_margins.left() + text_margins.right()
        width += cont_margins.left() + cont_margins.right()
        width += const_values + frame_width * 2
        return width

# =============================================== #
#                  CHANGE METHODS                 #
# =============================================== #

    def changeFilePath(self, action):
        options = QFileDialog.Options()
        path = QFileDialog.getExistingDirectory(
            QFileDialog(), "Select a Folder", '', options = options)

        if path:
            path = os.path.normpath(path)
            self.Settings.set('PATHS', action.data(), path)

    def changeCharRealm(self, char_realm):
        for location in self.ItemAttributeList.keys():
            for item in self.ItemDictionary[location]:
                if item.isPlayerCrafted():
                    item.setRealm(char_realm)

        # CASCADE THE CHANGES ...
        self.changeCharClass(self.getCharClass())

    def changeCharClass(self, char_class):
        self.CharacterClass.clear()
        self.CharacterClass.insertItems(0, self.getClasses())
        if self.CharacterClass.findText(char_class, Qt.MatchFixedString):
            self.setCharClass(char_class)
        else:
            self.setCharClass(self.getCharClass())

        # CASCADE THE CHANGES ...
        self.changeCharRace(self.getCharRace())

    def changeCharRace(self, char_race):
        self.CharacterRace.clear()
        self.CharacterRace.insertItems(0, self.getRaces())
        if self.CharacterRace.findText(char_race, Qt.MatchFixedString):
            self.setCharRace(char_race)
        else:
            self.setCharRace(self.getCharRace())

        racial_resists = Races['All'][self.getCharRace()]['Resistances']
        for resist in DropEffectList['All']['Resistance']:
            if resist in racial_resists:
                self.StatBonus[resist].setText(f'+ {racial_resists[resist]}')
            else:
                self.StatBonus[resist].setText('-')

        # FIXES A BUG THAT CAUSES THE APPLICATION TO CRASH ON LAUNCH
        # BECAUSE 'self.CurrentItemLabel' HAS NOT BEEN INSTANTIATED ...
        if self.CurrentItemLabel != '':
            self.restoreItem(self.getItem())

    def changeCharLevel(self):

        try:  # VALUE MIGHT BE INVALID ...
            char_level = int(self.getCharLevel())
        except ValueError:
            char_level = int(51)

        if char_level < 1 or char_level > 50:
            self.setCharLevel('1' if char_level < 1 else '50')
        self.CharacterLevel.setModified(False)
        self.calculate()

    def changeCharRealmRank(self):

        try:  # VALUE MIGHT BE INVALID ...
            char_realm_rank = int(self.getCharRealmRank())
        except ValueError:
            return

        if char_realm_rank > 14:
            self.setCharRealmRank('14')
        self.CharacterRealmRank.setModified(False)

    def changeCharChampLevel(self):

        try:  # VALUE MIGHT BE INVALID ...
            char_champion_level = int(self.getCharChampLevel())
        except ValueError:
            return

        if char_champion_level > 15:
            self.setCharChampLevel('15')
        self.CharacterChampLevel.setModified(False)

    def changeItemSelection(self, selection = None):
        selection = selection if selection else self.CurrentItemLabel
        if self.SlotListTreeView.selectedIndexes:
            for index in self.SlotListTreeView.selectedIndexes():
                selection = index.data()
        self.SlotListTreeView.blockSignals(True)
        for item in self.SlotListTreeView.findItems(selection, Qt.MatchRecursive):
            item.setSelected(True)
        self.SlotListTreeView.blockSignals(False)
        self.CurrentItemLabel = selection
        self.restoreItem(self.getItem())

    def changeItemState(self, selection, column):
        location = selection.text(column)
        self.getItem(location).setEquipped(selection.checkState(column) == 2)
        for item in self.ItemDictionary[location]:
            item.setEquipped(selection.checkState(column) == 2)
        if location == self.CurrentItemLabel:
            self.restoreItem(self.getItem())

    def changeItem(self, item_index):

        try:  # FIXES BUG IN 'QComboBox' WHEN PRESSING ENTER ...
            item = self.ItemDictionary[self.CurrentItemLabel][item_index]
        except IndexError:
            item = self.ItemDictionary[self.CurrentItemLabel][0]

        self.ItemDictionary[self.CurrentItemLabel].remove(item)
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.restoreItem(self.getItem())

    def changeItemName(self):
        if self.ItemName.currentIndex() == 0:
            item = self.getItem()
            item.setName(str(self.ItemName.lineEdit().text()))
            cursor_position = self.ItemName.lineEdit().cursorPosition()
            self.ItemName.setItemText(0, item.getName())
            self.ItemName.lineEdit().setCursorPosition(cursor_position)
        else:
            return

    def changeItemRealm(self, item_realm):
        self.getItem().setRealm(item_realm)
        self.restoreItem(self.getItem())

    def changeItemType(self, item_type):
        self.getItem().setType(item_type)

    def changeItemOrigin(self, item_origin):
        self.getItem().setOrigin(item_origin)

    def changeItemDamageType(self, item_damage_type):
        self.getItem().setDamageType(item_damage_type)

    def changeItemLevel(self):
        item = self.getItem()
        item_level = self.ItemLevel.text()
        if item.isPlayerCrafted():

            try:  # VALUE MIGHT BE INVALID ...
                item_level = int(item_level)
            except ValueError:
                item_level = int(51)

            if item_level < 1 or item_level > 51:
                item_level = 1 if item_level < 1 else 51

        self.getItem().setLevel(str(item_level))
        self.ItemLevel.setModified(False)
        self.restoreItem(self.getItem())

    def changeItemQuality(self):
        self.getItem().setQuality(self.ItemQuality.text())
        self.ItemQuality.setModified(False)

    def changeItemBonus(self):
        self.getItem().setBonus(self.ItemBonus.text())
        self.ItemBonus.setModified(False)

    def changeItemAFDPS(self):
        self.getItem().setAFDPS(self.ItemAFDPS.text())
        self.ItemAFDPS.setModified(False)

    def changeItemSpeed(self):
        self.getItem().setSpeed(self.ItemSpeed.text())
        self.ItemSpeed.setModified(False)

    def changeItemLeftHand(self, state):
        self.getItem().setLeftHand(state == 2)

    def changeItemRequirement(self):
        self.getItem().setRequirement(self.ItemRequirement.text())

    def changeItemNotes(self):
        self.getItem().setNotes(self.ItemNotes.toPlainText())

    # RECURSIVE METHOD ...
    def changeItemRestrictions(self, selection):
        item = self.getItem()
        if selection.checkState() == Qt.Checked:
            if selection.text() == 'All':
                for index in range(1, self.ItemRestrictionsList.count()):
                    self.ItemRestrictionsList.item(index).setCheckState(Qt.Unchecked)
                item.addClassRestriction(selection.text())
            else:
                self.ItemRestrictionsList.item(0).setCheckState(Qt.Unchecked)
                item.addClassRestriction(selection.text())
        else:
            item.removeClassRestriction(selection.text())

# =============================================== #
#     CHANGE ETYPE/EFFECT/AMOUNT/REQ METHODS      #
# =============================================== #

    def changeEffectType(self, etype, index = None):
        index = self.getSlotIndex() if index is None else index
        self.getItem().getSlot(index).setEffectType(etype)

        # CASCADE THE CHANGES ...
        self.updateEffectList(index)

    def changeEffect(self, effect, index = None):
        index = self.getSlotIndex() if index is None else index
        self.getItem().getSlot(index).setEffect(effect)

        # CASCADE THE CHANGES ...
        self.updateEffectAmountList(index)

    def changeEffectAmount(self, amount, index = None):
        index = self.getSlotIndex() if index is None else index
        self.getItem().getSlot(index).setEffectAmount(amount)

        # CASCADE THE CHANGES ...
        self.updateEffectRequirement(index)

    def changeEffectRequirement(self, requirement, index = None):
        index = self.getSlotIndex() if index is None else index
        self.getItem().getSlot(index).setEffectRequirement(requirement)

        # CASCADE THE CHANGES ...
        self.calculate()

# =============================================== #
#        METHODS SEPARATED FOR READABILITY        #
# =============================================== #
#         REVAMP AFTER DICTIONARY REWRITE         #
# =============================================== #

    def updateEffectTypeList(self, index):
        slot = self.getItem().getSlot(index)

        # CLEAR THE COMBOBOX ...
        self.EffectType[index].clear()

        # POPULATE THE COMBOBOX ...
        if slot.isCrafted():
            self.EffectType[index].insertItems(0, CraftedTypeList)
        elif slot.isEnhanced():
            self.EffectType[index].insertItems(0, EnhancedTypeList)
        elif slot.isDropped():
            self.EffectType[index].insertItems(0, DropTypeList)

        # REMOVE FOCUS FROM NON-STAFF LOCATIONS ...
        if self.getItem().getLocation() != 'Two-Handed':
            self.EffectType[index].removeItem(self.EffectType[index].findText('Focus'))

        # UPDATE THE COMBOBOX ...
        self.EffectType[index].setCurrentText(slot.getEffectType())

        # CASCADE THE CHANGES ...
        self.changeEffectType(slot.getEffectType(), index)

# =============================================== #

    def updateEffectList(self, index):
        slot = self.getItem().getSlot(index)

        # CLEAR THE COMBOBOX ...
        self.Effect[index].clear()

        # DETERMINE VALUES ...
        if slot.isUtilized():

            values = list()
            if slot.isCrafted():
                if not self.UnusableSkills.isChecked() and slot.getEffectType() == 'Skill':
                    values = AllBonusList['All'][self.getCharClass()]['All Skills']
                else:
                    values = CraftedEffectList[self.getCharRealm()][slot.getEffectType()]
            elif slot.isEnhanced():
                values = EnhancedEffectList['All'][slot.getEffectType()]
            elif slot.isDropped():
                values = DropEffectList[self.getCharRealm()][slot.getEffectType()]

            # POPULATE THE COMBOBOX ...
            self.Effect[index].insertItems(0, values)

        effect = slot.getEffect()
        if self.Effect[index].findText(effect) == -1:
            if slot.isCrafted() and slot.getEffectType() == 'Skill':
                effect = self.getFirstClassSkill()
            else:
                effect = self.Effect[index].currentText()

        # UPDATE THE COMBOBOX ...
        self.Effect[index].setCurrentText(effect)

        # CASCADE THE CHANGES ...
        self.changeEffect(effect, index)

# =============================================== #

    def updateEffectAmountList(self, index):
        slot = self.getItem().getSlot(index)

        # CLEAR THE COMBOBOX IF ...
        if slot.isCrafted() or slot.isEnhanced():
            self.AmountStatic[index].clear()

        # DETERMINE VALUES ...
        if slot.isUtilized():

            values = list()
            if slot.isCrafted() or slot.isEnhanced():
                if slot.isCrafted():
                    if slot.getEffect().split(None)[0] == 'All':
                        values = CraftedValuesList[slot.getEffectType()][:1]
                    else:
                        values = CraftedValuesList[slot.getEffectType()]
                elif slot.isEnhanced():
                    values = EnhancedValuesList[slot.getEffectType()]

                try:  # VALUES MIGHT HAVE SUB-VALUES ...
                    values = values[slot.getEffect()]
                except TypeError:
                    pass

                # POPULATE THE COMBOBOX ...
                self.AmountStatic[index].insertItems(0, values)

        amount = slot.getEffectAmount()
        if slot.isCrafted() or slot.isEnhanced():
            if self.AmountStatic[index].findText(amount) == -1:
                amount = self.AmountStatic[index].currentText()

            # UPDATE THE COMBOBOX ...
            self.AmountStatic[index].setCurrentText(amount)

        if slot.isDropped():
            amount = amount if slot.isUtilized() else ''

            # UPDATE THE LINE-EDIT ...
            self.AmountEdit[index].setText(amount)

        # CASCADE THE CHANGES ...
        self.changeEffectAmount(amount, index)

# =============================================== #

    def updateEffectRequirement(self, index):
        slot = self.getItem().getSlot(index)

        requirement = slot.getEffectRequirement()
        if slot.isDropped():
            requirement = requirement if slot.isUtilized() else ''

            # UPDATE THE LINE-EDIT ...
            self.Requirement[index].setText(requirement)

        # CASCADE THE CHANGES ...
        self.changeEffectRequirement(requirement, index)

# =============================================== #
#           NEW/SAVE/LOAD/DELETE METHODS          #
# =============================================== #

    def newTemplate(self):
        if self.templateWasModified():
            action = self.saveTemplatePrompt()
            if action == QMessageBox.Yes:
                self.saveTemplate()
                if self.templateWasModified():
                    return
            if action == QMessageBox.Cancel:
                return

        # RESET THE APPLICATION ...
        self.initialize()

    def openTemplate(self):
        options = QFileDialog.Options()
        path = self.Settings.get('PATHS', 'TemplatePath')
        filename, filters = QFileDialog.getOpenFileName(
            QFileDialog(), "Open Template", path, 'Templates (*.ktf);; All Files (*.*)', options = options)

        if filename in ('', None):
            return

        if self.templateWasModified():
            action = self.saveTemplatePrompt()
            if action == QMessageBox.Yes:
                self.saveTemplate()
                if self.templateWasModified():
                    return
            if action == QMessageBox.Cancel:
                return

        if self.importFromXML(filename) != -1:
            self.TemplateName = os.path.basename(filename)
            self.TemplatePath = os.path.dirname(filename)
        else:
            QMessageBox.warning(
                self, 'Error!',
                'The template you are attempting to import \n'
                'is using an unsupported XML format.',
                QMessageBox.Ok, QMessageBox.Ok
            )
            return

    def saveTemplate(self):
        if None in (self.TemplateName, self.TemplatePath):
            self.saveTemplateAs()
        else:
            self.exportAsXML(os.path.join(self.TemplatePath, self.TemplateName))
            self.InitialValues = self.exportAsXML(None, True, False)

    def saveTemplateAs(self):
        options = QFileDialog.Options()
        path = self.Settings.get('PATHS', 'TemplatePath')
        filename, filters = QFileDialog.getSaveFileName(
            QFileDialog(), 'Save Item', path, 'Templates (*.ktf);; All Files (*.*)', options = options)

        if filename in ('', None):
            return

        self.exportAsXML(filename)
        self.TemplateName = os.path.basename(filename)
        self.TemplatePath = os.path.dirname(filename)
        self.InitialValues = self.exportAsXML(None, True, False)

    def saveTemplatePrompt(self):
        prompt = QMessageBox.warning(
            self, 'Save Changes?',
            'This template has been modified.\n'
            'Do you want to save these changes?',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel
        ); return prompt

    def newItem(self, action):
        selection = action.text().split(None)[0]
        state = self.getItem().isEquipped()

        realm = 'All' if selection == 'Dropped' else self.getCharRealm()
        item = Item(selection, self.CurrentItemLabel, realm)
        item.setName(f'{selection} Item')
        item.setEquipped(state)

        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item

        if selection == 'Legendary':
            item.setLevel(51)
            if action.text().split(None)[1] == 'Staff':
                item.getSlot(4).setAll('Focus', 'All Spell Lines', '50')
                item.getSlot(5).setAll('ToA Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Magic Damage', '3')
            elif action.text().split(None)[1] == 'Bow':
                item.getSlot(4).setAll('ToA Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('ToA Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Magic Damage', '3')
            elif action.text().split(None)[1] == 'Weapon':
                item.getSlot(4).setAll('ToA Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('ToA Bonus', 'Melee Damage', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Style Damage', '3')

        # CASCADE THE CHANGES ...
        self.restoreItem(self.getItem())

    def loadItem(self):
        options = QFileDialog.Options()
        path = self.Settings.get('PATHS', 'ItemPath')
        filename, filters = QFileDialog.getOpenFileName(
            QFileDialog(), 'Load Item:', path, 'Items (*.xml);; All Files (*.*)', options = options)

        if filename in ('', None):
            return

        item = Item('Imported', self.CurrentItemLabel, self.getCharRealm())
        if item.importFromXML(filename) != -1:
            self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
            self.ItemAttributeList[self.CurrentItemLabel] = item
            self.restoreItem(self.getItem())
        else:
            QMessageBox.warning(
                self, 'Error!',
                'The item you are attempting to import \n'
                'is using an unsupported XML format.',
                QMessageBox.Ok, QMessageBox.Ok
            )
            return

    def convertItem(self, action):
        selection = action.text().split(None)[0]
        state = self.getItem().isEquipped()

        realm = 'All' if selection == 'Dropped' else self.getCharRealm()
        item = Item(selection, self.CurrentItemLabel, realm)
        item.setName(f'{selection} Item')
        item.setEquipped(state)

        del self.ItemDictionary[self.CurrentItemLabel][0]
        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item

        if selection == 'Legendary':
            item.setLevel(51)
            if action.text().split(None)[1] == 'Staff':
                item.getSlot(4).setAll('Focus', 'All Spell Lines', '50')
                item.getSlot(5).setAll('ToA Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Magic Damage', '3')
            elif action.text().split(None)[1] == 'Bow':
                item.getSlot(4).setAll('ToA Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('ToA Bonus', 'Casting Speed', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Magic Damage', '3')
            elif action.text().split(None)[1] == 'Weapon':
                item.getSlot(4).setAll('ToA Bonus', 'Armor Factor', '10')
                item.getSlot(5).setAll('ToA Bonus', 'Melee Damage', '3')
                item.getSlot(6).setAll('ToA Bonus', 'Style Damage', '3')

        # CASCADE THE CHANGES ...
        self.restoreItem(self.getItem())

    def saveItem(self):
        item = self.getItem(self.CurrentItemLabel)

        if item.getName() in ('', None):
            QMessageBox.warning(
                self, 'Error!',
                'You must specify a name before saving this item!',
                QMessageBox.Ok, QMessageBox.Ok
            )
            return

        if item.isPlayerCrafted():
            QMessageBox.warning(
                self, 'Error!',
                'You cannot export a craftable item.',
                QMessageBox.Ok, QMessageBox.Ok
            )
            return

        options = QFileDialog.Options()
        path = os.path.join(self.Settings.get('PATHS', 'ItemPath'), item.getName())
        filename, filters = QFileDialog.getSaveFileName(
            QFileDialog(), 'Save Item', path, 'Items (*.xml);; All Files (*.*)', options = options)

        if filename:
            item.exportAsXML(filename)

    def deleteItem(self):
        if len(self.ItemDictionary[self.CurrentItemLabel]) > 1:
            del self.ItemDictionary[self.CurrentItemLabel][0]
            item = self.ItemDictionary[self.CurrentItemLabel][0]
            self.ItemAttributeList[self.CurrentItemLabel] = item
            self.restoreItem(self.getItem())
        else:
            self.clearItem()

    def clearItem(self):
        state = self.getItem().isEquipped()
        self.ItemDictionary[self.CurrentItemLabel].remove(self.getItem())

        realm = 'All' if self.getItem().isDropped() else self.getCharRealm()
        item = Item(self.getItem().getState(), self.CurrentItemLabel, realm)
        item.setName(f'{item.getState()} Item')
        item.setEquipped(state)

        self.ItemDictionary[self.CurrentItemLabel].insert(0, item)
        self.ItemAttributeList[self.CurrentItemLabel] = item
        self.restoreItem(self.getItem())

    def clearItemSlots(self):
        self.getItem(self.CurrentItemLabel).clearSlots()
        self.restoreItem(self.getItem())

# =============================================== #
#              MISCELLANEOUS METHODS              #
# =============================================== #

    def templateWasModified(self):
        initial_values = etree.tostring(self.InitialValues, encoding = 'UTF-8')
        current_values = etree.tostring(self.exportAsXML(None, True, False), encoding = 'UTF-8')
        return initial_values != current_values

    def mousePressEvent(self, event):
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()' ...
            self.focusWidget().clearFocus()
        except AttributeError:
            pass

    def setToolbarOptions(self, selection):
        for action in self.ToolbarMenu.actions():
            action.setChecked(action.data() == selection.data())
        if selection.data() == 0:
            self.Toolbar.hide()
        else:
            self.setIconSize(QSize(selection.data(), selection.data()))
            self.Toolbar.show()

    def insertSkill(self, amount, bonus, group):
        self.SkillsView.model().insertRows(self.SkillsView.model().rowCount(), 1)
        width = 3 if (-10 < amount < 10) else 2
        bonus = "%*d %s" % (width, amount, bonus,)
        index = self.SkillsView.model().index(self.SkillsView.model().rowCount() - 1, 0, QModelIndex())
        self.SkillsView.model().setData(index, QVariant(bonus), Qt.DisplayRole)
        self.SkillsView.model().setData(index, QVariant(group), Qt.UserRole)

    def closeEvent(self, event):
        if self.templateWasModified():
            action = self.saveTemplatePrompt()
            if action == QMessageBox.Yes:
                self.saveTemplate()
                if self.templateWasModified():
                    event.ignore()
            if action == QMessageBox.No:
                self.Settings.save()
                event.accept()
            if action == QMessageBox.Cancel:
                event.ignore()

        # SAVE SETTINGS ...
        self.Settings.save()
