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

    def materialsReport(self, items, realm):
        self.setWindowTitle('Materials Report')
        self.ExportHTMLButton.hide()
        self.ExportPlainTextButton.hide()

        gems = {}
        materials = {'Gems': {}, 'Dusts': {}, 'Liquids': {}}

        for location, item in items.items():
            if item.ActiveState == 'Dropped' or item.Equipped != 2:
                continue
            for slot in item.getSlotList():
                if slot.getSlotType() != 'Craftable' or slot.getEffectType() == 'Unused':
                    continue
                for material_type, material_list in slot.getGemMaterials(realm).items():
                    for material, amount in material_list.items():
                        if material in materials[material_type]:
                            materials[material_type][material] += amount
                        else:
                            materials[material_type][material] = amount
                if slot.getGemName(realm) in gems:
                    gems[slot.getGemName(realm)] += 1
                else:
                    gems[slot.getGemName(realm)] = 1

        output = '<center><b>Jewels</b></center><hr><ul>\n'

        for gem_name, amount in gems.items():
            output += '<li>%d  %s</li>\n' % (amount, gem_name)

        output += '</ul>\n'

        self.ReportTextBrowser.setHtml(output)

        # DEBUGGING
        print('Gems:', gems.items())
        print('Materials', materials.items())

    def templateReport(self, report):
        self.setWindowTitle('Template Report')

        xslt = etree.parse(r'reports/DefaultTemplateReport.xsl')
        transform = etree.XSLT(xslt)
        report = transform(report)

        print(etree.tostring(report, pretty_print=True).decode('UTF-8'))

        self.ReportTextBrowser.setHtml(str(report))
