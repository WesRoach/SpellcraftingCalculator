# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import QIcon, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QMessageBox
from Constants import GemHotkeyValues, ServerCodes
from configparser import DEFAULTSECT, RawConfigParser
from re import compile
import os

Ui_QuickbarDialog = uic.loadUiType(r'interface/QuickbarDialog.ui')[0]


class IniConfigParser(RawConfigParser):

    def __init__(self, defaults = None):
        RawConfigParser.__init__(self, defaults, strict = False)

    def write(self, file, **kwargs):
        if self._defaults:
            file.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in list(self._defaults.items()):
                file.write("%s=%s\n" % (key, str(value).replace('\n', '\n\t')))
            file.write("\n")

        for section in self._sections:
            file.write("[%s]\n" % section)
            for (key, value) in list(self._sections[section].items()):
                if key != "__name__":
                    file.write("%s=%s\n" % (key, str(value).replace('\n', '\n\t')))
            file.write("\n")


class QuickbarDialog(QDialog, Ui_QuickbarDialog):
    def __init__(self, parent = None, flags = Qt.Dialog, items = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        font = QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(8)
        self.setFont(font)

        self.Selection = []
        self.GemCount = 0
        self.ItemExportList = {}
        self.ItemAttributeList = items

        self.CraftableItems = {
            'Chest': self.ChestCheckBox,
            'Arms': self.ArmsCheckBox,
            'Head': self.HeadCheckBox,
            'Legs': self.LegsCheckBox,
            'Hands': self.HandsCheckBox,
            'Feet': self.FeetCheckBox,
            'Right Hand': self.RightHandCheckBox,
            'Left Hand': self.LeftHandCheckBox,
            'Two-Handed': self.TwoHandedCheckBox,
            'Ranged': self.RangedCheckBox,
        }

        self.reini = compile('(\w+)-(\d+)\.ini$')
        self.resec = compile('\[(\w+)\]')
        self.rectl = compile('[Hh]otkey_(\d+)=44,13,')

        self.TableModel = self.CrafterTable.model()

        self.initLayout()
        self.initControls()

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initLayout(self):
        self.setWindowTitle('Export Gems to Quickbar')
        self.setWindowIcon(QIcon(None))

        self.QuickbarNum.setValue(1)
        self.QuickbarNum.setMinimum(1)
        self.QuickbarNum.setMaximum(3)
        self.QuickbarRow.setValue(1)
        self.QuickbarRow.setMinimum(1)
        self.QuickbarRow.setMaximum(10)
        self.QuickbarStart.setValue(1)
        self.QuickbarStart.setMinimum(1)
        self.QuickbarStart.setMaximum(10)

        for location, item in self.ItemAttributeList.items():
            if location not in self.CraftableItems.keys():
                continue
            elif not item.isPlayerCrafted():
                self.CraftableItems[location].setCheckState(Qt.Unchecked)
                self.CraftableItems[location].setDisabled(True)

        for location in self.CraftableItems.keys():
            if self.CraftableItems[location].isEnabled():
                for slot in self.ItemAttributeList[location].getSlotList():
                    if slot.isCrafted() and slot.isUtilized():
                        self.CraftableItems[location].setCheckState(Qt.Checked)

        self.getCrafterList()
        self.changeItemSelection()
        self.CloseButton.setFocus()

    def initControls(self):
        self.ChestCheckBox.clicked.connect(self.changeItemSelection)
        self.ArmsCheckBox.clicked.connect(self.changeItemSelection)
        self.HeadCheckBox.clicked.connect(self.changeItemSelection)
        self.LegsCheckBox.clicked.connect(self.changeItemSelection)
        self.HandsCheckBox.clicked.connect(self.changeItemSelection)
        self.FeetCheckBox.clicked.connect(self.changeItemSelection)
        self.RightHandCheckBox.clicked.connect(self.changeItemSelection)
        self.LeftHandCheckBox.clicked.connect(self.changeItemSelection)
        self.TwoHandedCheckBox.clicked.connect(self.changeItemSelection)
        self.RangedCheckBox.clicked.connect(self.changeItemSelection)
        self.CrafterTable.selectionModel().selectionChanged.connect(self.changeCrafterSelection)
        self.ExportButton.clicked.connect(self.exportGemsToQuickbar)
        self.RestoreButton.clicked.connect(self.restoreQuickbar)
        self.CloseButton.clicked.connect(self.accept)

# =============================================== #
#                  GETTER METHODS                 #
# =============================================== #

    @staticmethod
    def getCrafterPath():
        path = os.getenv('APPDATA')
        path += '\\Electronic Arts'
        path += '\\Dark Age of Camelot'
        return path

    def getCrafterList(self):
        self.CrafterTable.setRowCount(0)
        for root, dirs, files in os.walk(self.getCrafterPath()):
            for file in (x for x in files if self.reini.search(x)):
                with open(root + '\\' + file, 'r') as document:
                    if self.rectl.search(document.read()) is not None:
                        character = self.reini.search(file).group(1)
                        server_code = self.reini.search(file).group(2)
                        server = ServerCodes[server_code] if server_code in ServerCodes else 'Unknown'
                        self.TableModel.insertRows(self.TableModel.rowCount(), 1)
                        index = self.TableModel.index(self.TableModel.rowCount() - 1, 0, QModelIndex())
                        self.TableModel.setData(index, QVariant(' ' + server), Qt.DisplayRole)
                        self.TableModel.setData(index, QVariant(root + '\\' + file), Qt.UserRole)
                        index = self.TableModel.index(self.TableModel.rowCount() - 1, 1, QModelIndex())
                        self.TableModel.setData(index, QVariant(' ' + character), Qt.DisplayRole)
        self.CrafterTable.resizeRowsToContents()

        if self.TableModel.rowCount() == 1:
            self.CrafterTable.selectRow(0)

    def getQuickbarNumber(self):
        return self.QuickbarNum.value()

    def getQuickbarRow(self):
        return self.QuickbarRow.value() - 1

    def getQuickbarStart(self):
        return self.QuickbarStart.value() - 1

    def getGemCount(self):
        self.GemCount = 0
        for item in self.ItemExportList.values():
            self.GemCount += sum(1 for x in item.getSlotList() if x.isCrafted() and x.isUtilized())
        self.GemExportCount.setText(str(self.GemCount))

# =============================================== #
#                  CHANGE METHODS                 #
# =============================================== #

    def changeCrafterSelection(self):
        self.Selection = self.CrafterTable.selectedIndexes()

    def changeItemSelection(self):
        self.ItemExportList.clear()
        for location, checkbox in self.CraftableItems.items():
            if checkbox.checkState() == Qt.Checked:
                self.ItemExportList[location] = self.ItemAttributeList[location]

        # CASCADE THE CHANGES ...
        self.getGemCount()

# =============================================== #
#             EXPORT/RESTORE METHODS              #
# =============================================== #

    def exportGemsToQuickbar(self):
        if len(self.Selection) == 0 or self.GemCount == 0:
            return

        index = (self.getQuickbarRow() * 10) + self.getQuickbarStart()
        number = self.getQuickbarNumber() if self.getQuickbarNumber() != 1 else ''
        file = self.TableModel.data(self.TableModel.index(self.Selection[0].row(), 0), Qt.UserRole)

        if (100 - index) < self.GemCount:
            QMessageBox.warning(
                self, 'Error!',
                'There is insufficient space on the selected \n'
                'Quickbar to export the item\'s gems.',
                QMessageBox.Ok, QMessageBox.Ok
            )
            return

        with open(file, 'r') as document:
            with open(file + '.bak', 'w') as backup:
                backup.write(document.read())

        button_strings = []
        for location, item in self.ItemExportList.items():
            for slot in [x for x in item.getSlotList() if x.isCrafted() and x.isUtilized()]:

                try:  # HOTKEY MIGHT NOT EXIST ...
                    gem_tier = slot.getGemIndex()
                    gem_name = slot.getGemName(item.Realm).split(None, 1)[1]
                    gem_hotkey = GemHotkeyValues[item.Realm][gem_name]
                    button_strings.append('45,13%03d%02d,,-1' % (gem_hotkey, gem_tier))
                except ValueError:
                    continue

        config = IniConfigParser()
        config.read([file])

        with open(file, 'w') as document:
            for string in button_strings:
                config.set(f'Quickbar{number}', f'Hotkey_{index}', string)
                index += 1
            config.write(document)

        QMessageBox.information(
            self, 'Success!',
            'Successfully exported gems to Quickbar!',
            QMessageBox.Ok, QMessageBox.Ok
        )

    def restoreQuickbar(self):
        if len(self.Selection) == 0: return
        index = self.TableModel.index(self.Selection[0].row(), 0)
        file = self.TableModel.data(index, Qt.UserRole)

        if os.path.exists(file + '.bak') and os.path.isfile(file + '.bak'):
            with open(file, 'w') as document:
                with open(file + '.bak', 'r') as backup:
                    document.write(backup.read())
            os.remove(file + '.bak')

# =============================================== #
#                METHOD OVERRIDES                 #
# =============================================== #

    def mousePressEvent(self, event):
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()' ...
            self.focusWidget().clearFocus()
        except AttributeError:
            pass
