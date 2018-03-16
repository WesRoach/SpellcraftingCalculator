# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon
from PyQt5.QtWidgets import QDialog
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

    def materialsReport(self):
        self.setWindowTitle('Materials Report')
        self.ReportTextBrowser.setHtml('Materials Report')

    def templateReport(self, report):
        self.setWindowTitle('Template Report')

        xslt = etree.parse(r'reports/DefaultTemplateReport.xsl')
        transform = etree.XSLT(xslt)
        report = transform(report)

        print(etree.tostring(report, pretty_print=True).decode('UTF-8'))

        self.ReportTextBrowser.setHtml(str(report))
