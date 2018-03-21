# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon
from PyQt5.QtWidgets import QDialog
from Constants import GemMaterialsOrder
from lxml import etree

Ui_ReportWindow = uic.loadUiType(r'interface/ReportWindow.ui')[0]


class ReportWindow(QDialog, Ui_ReportWindow):
    def __init__(self, parent = None, flags = Qt.Dialog):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.initLayout()
        self.initControls()

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initLayout(self):
        self.setWindowTitle('Report Window')
        self.setWindowIcon(QIcon(None))

    def initControls(self):
        self.CloseButton.clicked.connect(self.accept)

# =============================================== #
#          REPORT METHODS AND FUNCTIONS           #
# =============================================== #

    def materialsReport(self, item_list, realm):
        self.setWindowTitle('Materials Report')
        self.ExportHTMLButton.hide()
        self.ExportPlainTextButton.hide()

        materials = {'Items': {}, 'Gems': {}, 'Liquids': {}, 'Dusts': {}}

        # GATHER CRAFTABLE AND EQUIPPED ITEMS ...
        for location, item in item_list.items():
            if item.ActiveState != 'Dropped' and item.Equipped != 0:
                pass

        for key, value in materials.items():
            print(key, value)

        self.ReportTextBrowser.setHtml('This shit is broken ...')

    def templateReport(self, report):
        self.setWindowTitle('Template Report')

        xslt = etree.parse(r'reports/DefaultTemplateReport.xsl')
        transform = etree.XSLT(xslt)
        report = transform(report)

        self.ReportTextBrowser.setHtml(str(report))

# =============================================== #
#              XML IMPORT AND EXPORT              #
# =============================================== #
