# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon
from PyQt5.QtWidgets import QDialog

Ui_ReportWindow = uic.loadUiType(r'interface/CraftBarWindow.ui')[0]


class CraftBarWindow(QDialog, Ui_ReportWindow):
    def __init__(self, parent = None, flags = Qt.Dialog):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.initLayout()
        self.initControls()

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initLayout(self):
        self.setWindowTitle('Export Gems to QuickBar\'s')
        self.setWindowIcon(QIcon(None))

    def initControls(self):
        pass