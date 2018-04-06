# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon
from PyQt5.QtWidgets import QDialog

Ui_ReportWindow = uic.loadUiType(r'interface/CraftBarDialog.ui')[0]


class CraftBarDialog(QDialog, Ui_ReportWindow):
    def __init__(self, parent = None, flags = Qt.Dialog, items = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.ItemAttributeList = items

        self.CraftableItems = [
            'Chest', 'Arms', 'Head', 'Legs', 'Hands', 'Feet',
            'Right Hand', 'Left Hand', 'Two-Handed', 'Ranged']

        self.ItemCheckBoxes = [
            self.ChestCheckBox,
            self.ArmsCheckBox,
            self.HeadCheckBox,
            self.LegsCheckBox,
            self.HandsCheckBox,
            self.FeetCheckBox,
            self.RightHandCheckBox,
            self.LeftHandCheckBox,
            self.TwoHandedCheckBox,
            self.RangedCheckBox,
        ]

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
