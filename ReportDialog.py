# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon
from PyQt5.QtWidgets import QDialog, QFileDialog
from Constants import GemMaterialsOrder
from lxml import etree

Ui_ReportDialog = uic.loadUiType(r'interface/ReportDialog.ui')[0]


class ReportDialog(QDialog, Ui_ReportDialog):

    def __init__(self, parent = None, flags = Qt.Dialog):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.initLayout()
        self.initControls()
        self.RawHTMLReport = ''

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initLayout(self):
        self.setWindowTitle('Report Window')
        self.setWindowIcon(QIcon(None))

    def initControls(self):
        self.CloseButton.clicked.connect(self.accept)
        self.ExportHTMLButton.clicked.connect(self.exportToHTML)
        self.ExportPlainTextButton.clicked.connect(self.exportToPlainText)

# =============================================== #
#          REPORT METHODS AND FUNCTIONS           #
# =============================================== #

    def materialsReport(self, item_list, realm):
        self.setWindowTitle('Materials Report')
        self.ExportHTMLButton.hide()
        self.ExportPlainTextButton.hide()

        materials = {'Items': {}, 'Gems': {}, 'Dusts': {}, 'Liquids': {}}

        for item in [x for x in item_list.values() if x.isPlayerCrafted()]:
            for slot in [x for x in item.getSlotList() if x.isCrafted() and x.isUtilized()]:

                try:  # THE KEY MAY NOT EXIST ...
                    materials['Items'][item.Location] += [slot.getGemName(realm)]
                except KeyError:
                    materials['Items'][item.Location] = [slot.getGemName(realm)]

                for material_type, material_list in slot.getGemMaterials(realm).items():
                    for material, amount in material_list.items():

                        try:  # THE KEY MAY NOT EXIST ...
                            materials[material_type][material] += amount
                        except KeyError:
                            materials[material_type][material] = amount

        for material_type, material_list in materials.items():
            if material_type in GemMaterialsOrder.keys():
                keys = GemMaterialsOrder[material_type]
                material_list = [(x, material_list.get(x)) for x in keys if x in material_list]
                materials[material_type] = material_list

        report = etree.Element('Materials')
        for material_type, material_list in materials.items():
            if material_type == 'Items':
                parent = etree.SubElement(report, 'Items')
                for location, jewels in material_list.items():
                    element = etree.SubElement(parent, 'Item', Location = location)
                    for jewel in jewels:
                        etree.SubElement(element, 'Jewel').text = jewel
            else:
                parent = etree.SubElement(report, material_type)
                for material, amount in material_list:
                    etree.SubElement(parent, 'Material', Amount = str(amount), Material = material)

        xslt = etree.parse(r'reports/DefaultMaterialsReport.xsl')
        transform = etree.XSLT(xslt)
        report = str(transform(report))

        self.ReportTextBrowser.setHtml(report)

    def templateReport(self, report):
        self.setWindowTitle('Template Report')

        # TODO: IMPLEMENT PLAIN TEXT REPORTS
        self.ExportPlainTextButton.setDisabled(True)

        xslt = etree.parse(r'reports/DefaultTemplateReport.xsl')
        transform = etree.XSLT(xslt)
        report = str(transform(report))

        parser = etree.HTMLParser(remove_blank_text = True)
        self.RawHTMLReport = etree.HTML(report, parser)
        self.ReportTextBrowser.setHtml(report)

# =============================================== #
#                    EXPORT                       #
# =============================================== #

    def exportToPlainText(self):
        pass

    def exportToHTML(self):
        options = QFileDialog.Options()
        filename, filters = QFileDialog.getSaveFileName(
            QFileDialog(), 'Save HTML Report', '', 'HTML Report (*.htm *.html);; All Files (*.*)', options = options)

        if filename in ('', None):
            return

        with open(filename, 'wb') as document:
            document.write(etree.tostring(self.RawHTMLReport, pretty_print = True, method = 'html'))
