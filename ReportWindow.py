# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon
from PyQt5.QtWidgets import QDialog
from Constants import GemMaterialsOrder
from lxml import etree, html
from xml.etree import ElementTree

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

        materials = {'Items': {}, 'Jewels': {}, 'Gems': {}, 'Liquids': {}, 'Dusts': {}}

        # GATHER CRAFTABLE AND EQUIPPED ITEMS ...
        for location, item in item_list.items():
            if item.ActiveState != 'Dropped' and item.Equipped != 0:
                materials['Items'][location] = item

        # GATHER JEWELS FOR EACH LOCATION ...
        for location, item in materials['Items'].items():
            for slot in item.getSlotList():
                if slot.getSlotType() == 'Craftable' and slot.getEffectType() != 'Unused':
                    if location not in materials['Jewels']:
                        materials['Jewels'][location] = {}
                    if slot.getGemName(realm) in materials['Jewels'][location]:
                        materials['Jewels'][location][slot.getGemName(realm)] += 1
                    else:
                        materials['Jewels'][location][slot.getGemName(realm)] = 1

        # GATHER ALL THE MATERIALS ...
        for location, item in materials['Items'].items():
            for slot in item.getSlotList():
                if slot.getSlotType() == 'Craftable' and slot.getEffectType() != 'Unused':
                    for material_type, material_list in slot.getGemMaterials(realm).items():
                        for material, amount in material_list.items():
                            if material in materials[material_type]:
                                materials[material_type][material] += amount
                            else:
                                materials[material_type][material] = amount

        # SORT ALL THE LISTS ...
        for material_type, material_list in materials.items():
            if material_type in GemMaterialsOrder.keys():
                keys = GemMaterialsOrder[material_type]
                material_list = [[x, material_list.get(x)] for x in keys if x in material_list]
            materials[material_type] = material_list

        # GENERATE THE MATERIALS REPORT ...
        for key, value in materials.items():
            print(key, value)

        output = etree.Element('html')
        etree.SubElement(output, 'body').text = 'Hello World'

        self.ReportTextBrowser.setHtml(etree.tounicode(output, method = 'html'))

    def templateReport(self, report):
        self.setWindowTitle('Template Report')

        xslt = etree.parse(r'reports/DefaultTemplateReport.xsl')
        transform = etree.XSLT(xslt)
        report = transform(report)

        self.ReportTextBrowser.setHtml(str(report))
