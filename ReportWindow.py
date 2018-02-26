# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QFontMetrics, QIcon, QSize
from PyQt5.QtWidgets import QDialog, QStyle, QStyleOptionComboBox

Ui_ReportWindow = uic.loadUiType(r'interface/ReportWindow.ui')[0]


class ReportWindow(QDialog, Ui_ReportWindow):
    def __init__(self, parent = None, flags = Qt.Dialog):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.Materials = None
        self.Gems = None

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
        self.Materials = {'Gems': {}, 'Dusts': {}, 'Liquids': {},}
        self.Gems = {}

    def templateReport(self):
        self.setWindowTitle('Template Report')

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
