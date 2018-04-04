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

        materials = {'Items': {}, 'Gems': {}, 'Dusts': {}, 'Liquids': {}}

        for location, item in item_list.items():
            if item.ActiveState == 'Crafted' and item.Equipped != 0:
                for slot in item.getSlotList():
                    if slot.getSlotType() == 'Craftable' and slot.getEffectType() != 'Unused':
                        if item.Location in materials['Items']:
                            materials['Items'][item.Location] += [slot.getGemName(realm)]
                        else:
                            materials['Items'][item.Location] = [slot.getGemName(realm)]
                        for material_type, material_list in slot.getGemMaterials(realm).items():
                            for material, amount in material_list.items():
                                if material in materials[material_type]:
                                    materials[material_type][material] += amount
                                else:
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
        report = transform(report)

        self.ReportTextBrowser.setHtml(str(report))

    def templateReport(self, report):
        self.setWindowTitle('Template Report')

        xslt = etree.parse(r'reports/DefaultTemplateReport.xsl')
        transform = etree.XSLT(xslt)
        report = transform(report)

        self.ReportTextBrowser.setHtml(str(report))

# =============================================== #
#                       XML                       #
# =============================================== #

    def exportToXML(self, item_list, materials):
        pass
