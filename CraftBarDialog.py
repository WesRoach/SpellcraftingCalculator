# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon
from PyQt5.QtWidgets import QDialog
from os import getenv, listdir

Ui_ReportWindow = uic.loadUiType(r'interface/CraftBarDialog.ui')[0]


class CraftBarDialog(QDialog, Ui_ReportWindow):
    def __init__(self, parent = None, flags = Qt.Dialog, items = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.ItemGemCount = 0
        self.ItemAttributeList = items
        self.ItemCraftableList = {}

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
        self.RowSpinBox.setValue(1)
        self.StartSpinBox.setValue(1)

        for location, checkbox in self.CraftableItems.items():
            if self.ItemAttributeList[location].ActiveState == 'Dropped':
                checkbox.setDisabled(True)

        # TODO: LOAD PATH FROM SAVED SETTINGS ...
        path = getenv('APPDATA') + '\\Electronic Arts\\Dark Age of Camelot\\'
        self.CharacterPath.setText(path)
        self.CharacterPath.setCursorPosition(0)
        self.CloseButton.setFocus()

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
#        SLOT/SIGNAL METHODS AND FUNCTIONS        #
# =============================================== #

    def ItemSelectionChanged(self):
        pass
