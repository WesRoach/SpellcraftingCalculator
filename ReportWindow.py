# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QFontMetrics, QIcon, QSize
from PyQt5.QtWidgets import QDialog, QStyle, QStyleOptionComboBox

Ui_ReportWindow = uic.loadUiType(r'interface/ReportWindow.ui')[0]


class ReportWindow(QDialog, Ui_ReportWindow):
    def __init__(self, parent = None, flags = Qt.Dialog):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.initLayout()
        self.initControls()

    def initLayout(self):
        self.setWindowTitle('Report Window')
        self.setWindowIcon(QIcon(None))

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initControls(self):
        self.CloseButton.clicked.connect(self.accept)

# =============================================== #
#          REPORT METHODS AND FUNCTIONS           #
# =============================================== #

    def materialsReport(self):
        self.setWindowTitle('Materials Report')

    def templateReport(self):
        self.setWindowTitle('Template Report')
