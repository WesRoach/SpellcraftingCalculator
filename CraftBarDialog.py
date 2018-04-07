# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon
from PyQt5.QtWidgets import QDialog
from Item import Item
from os import getenv, listdir

Ui_ReportWindow = uic.loadUiType(r'interface/CraftBarDialog.ui')[0]


class CraftBarDialog(QDialog, Ui_ReportWindow):
    def __init__(self, parent = None, flags = Qt.Dialog, items = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.ItemGemCount = 0
        self.ItemAttributeList = items
        self.ExportItemList = {}

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
        self.getCrafterList()

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initLayout(self):
        self.setWindowTitle('Export Gems to Quickbar')
        self.setWindowIcon(QIcon(None))

        self.BarSpinBox.setValue(1)
        self.RowSpinBox.setValue(1)
        self.StartSpinBox.setValue(1)

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

    def getCrafterList(self):
        self.CharacterTable.model().removeRows(0, self.CharacterTable.model().rowCount())
        pass

    def exportGemsToQuickbar(self):
        pass

    def getGemExportCount(self):
        self.ItemGemCount = 0
        for location in self.ExportItemList.keys():
            if location in self.ItemAttributeList.keys():
                if self.ItemAttributeList[location].ActiveState != 'Dropped':
                    for slot in self.ItemAttributeList[location].getSlotList():
                        if slot.getSlotType() == 'Craftable' and slot.getEffectType() != 'Unused':
                            self.ItemGemCount += 1
        self.GemExportCount.setText(str(self.ItemGemCount))

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
