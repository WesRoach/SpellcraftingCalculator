# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon, QModelIndex, QVariant
from PyQt5.QtWidgets import QDialog
from Constants import ServerCodes
from os import getenv, path, walk
from re import compile

Ui_ReportWindow = uic.loadUiType(r'interface/CraftBarDialog.ui')[0]


class CraftBarDialog(QDialog, Ui_ReportWindow):
    def __init__(self, parent = None, flags = Qt.Dialog, items = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.ItemGemCount = 0
        self.ItemAttributeList = items
        self.ExportItemList = {}

        self.reini = compile('(\w+)-(\d+)\.ini$')
        self.resec = compile('\[(\w+)\]')
        self.rectl = compile('[Hh]otkey_(\d+)=44,13,')

        self.CraftableItems = {
            'Chest': self.ChestCheckBox,
            'Arms': self.ArmsCheckBox,
            'Head': self.HeadCheckBox,
            'Legs': self.LegsCheckBox,
            'Hands': self.HandsCheckBox,
            'Feet': self.FeetCheckBox,
            'Right Hand': self.RightHandCheckBox,
            'Left Hand': self.LeftHandCheckBox,
            'Two-Handed': self.TwoHandedCheckBox,
            'Ranged': self.RangedCheckBox,
        }

        self.initLayout()
        self.initControls()

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initLayout(self):
        self.setWindowTitle('Export Gems to Quickbar')
        self.setWindowIcon(QIcon(None))

        self.BarSpinBox.setValue(1)
        self.BarSpinBox.setMaximum(3)
        self.RowSpinBox.setValue(1)
        self.RowSpinBox.setMaximum(10)
        self.StartSpinBox.setValue(1)
        self.StartSpinBox.setMaximum(10)

        for location, item in self.ItemAttributeList.items():
            if location not in self.CraftableItems:
                continue
            elif item.ActiveState == 'Dropped' or item.Equipped == 0:
                self.CraftableItems[location].setCheckState(Qt.Unchecked)
                self.CraftableItems[location].setDisabled(True)

        for location in self.CraftableItems.keys():
            if self.CraftableItems[location].isEnabled():
                for slot in self.ItemAttributeList[location].getSlotList():
                    if slot.getSlotType() == 'Craftable' and slot.getEffectType() != 'Unused':
                        self.CraftableItems[location].setCheckState(Qt.Checked)

        # TODO: LOAD PATH FROM SAVED SETTINGS ...
        path = getenv('APPDATA') + '\\Electronic Arts\\Dark Age of Camelot\\'
        self.CharacterPath.setText(path)
        self.CharacterPath.setCursorPosition(0)
        self.CloseButton.setFocus()
        self.getCrafterList(path)
        self.ItemSelectionChanged()

    def initControls(self):
        self.CloseButton.clicked.connect(self.accept)
        self.ChestCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.ArmsCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.HeadCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.LegsCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.HandsCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.FeetCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.RightHandCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.LeftHandCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.TwoHandedCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.RangedCheckBox.clicked.connect(self.ItemSelectionChanged)

# =============================================== #
#       MISCELLANEOUS METHODS AND FUNCTIONS       #
# =============================================== #

    def getCrafterList(self, rootdir):
        character_list = []
        for root, dirs, files in walk(rootdir):
            character_list += [x for x in files if self.reini.search(x)]

    def getGemExportCount(self):
        self.ItemGemCount = 0
        for location in self.ExportItemList.keys():
            if location in self.ItemAttributeList.keys():
                if self.ItemAttributeList[location].ActiveState != 'Dropped':
                    for slot in self.ItemAttributeList[location].getSlotList():
                        if slot.getSlotType() == 'Craftable' and slot.getEffectType() != 'Unused':
                            self.ItemGemCount += 1
        self.GemExportCount.setText(str(self.ItemGemCount))

    def exportGemsToQuickbar(self):
        pass

# =============================================== #
#        SLOT/SIGNAL METHODS AND FUNCTIONS        #
# =============================================== #

    def mousePressEvent(self, event):
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()' ...
            self.focusWidget().clearFocus()
        except AttributeError:
            pass

    def ItemSelectionChanged(self):
        for location, checkbox in self.CraftableItems.items():
            if checkbox.checkState() == Qt.Checked:
                self.ExportItemList[location] = self.ItemAttributeList[location]
            elif location in self.ExportItemList.keys():
                del self.ExportItemList[location]
        self.getGemExportCount()
