# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt, QIcon, QModelIndex, QVariant
from PyQt5.QtWidgets import QDialog, QMessageBox
from Constants import GemHotkeyValues, ServerCodes
from configparser import DEFAULTSECT, RawConfigParser
from os import getenv, path, remove, walk
from re import compile

Ui_ReportWindow = uic.loadUiType(r'interface/CraftBarDialog.ui')[0]


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


class CraftBarDialog(QDialog, Ui_ReportWindow):
    def __init__(self, parent = None, flags = Qt.Dialog, items = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

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

        self.TableModel = self.CharacterTable.model()

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
            elif not item.isCraftable():
                self.CraftableItems[location].setCheckState(Qt.Unchecked)
                self.CraftableItems[location].setDisabled(True)

        for location in self.CraftableItems.keys():
            if self.CraftableItems[location].isEnabled():
                for slot in self.ItemAttributeList[location].getSlotList():
                    if slot.isCraftable():
                        self.CraftableItems[location].setCheckState(Qt.Checked)

        # TODO: LOAD PATH FROM SAVED SETTINGS ...
        ini_path = getenv('APPDATA') + '\\Electronic Arts\\Dark Age of Camelot\\'
        self.CharacterPath.setText(ini_path)
        self.CharacterPath.setCursorPosition(0)
        self.CloseButton.setFocus()
        self.getCrafterList(ini_path)
        self.ItemSelectionChanged()

    def initControls(self):
        self.ChestCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.ArmsCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.HeadCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.LegsCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.HandsCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.FeetCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.RightHandCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.LeftHandCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.TwoHandedCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.RangedCheckBox.clicked.connect(self.ItemSelectionChanged)
        self.CharacterTable.selectionModel().selectionChanged.connect(self.CharacterSelectionChanged)
        self.ExportButton.clicked.connect(self.exportGemsToQuickbar)
        self.RestoreButton.clicked.connect(self.restoreQuickbar)
        self.CloseButton.clicked.connect(self.accept)

# =============================================== #
#       MISCELLANEOUS METHODS AND FUNCTIONS       #
# =============================================== #

    def getCrafterList(self, rootdir):
        for root, dirs, files in walk(rootdir):
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
        self.CharacterTable.resizeRowsToContents()

        if self.TableModel.rowCount() == 1:
            self.CharacterTable.selectRow(0)

    def getGemCount(self):
        self.GemCount = 0
        for item in self.ItemExportList.values():
            self.GemCount += sum(1 for x in item.getSlotList() if x.isCraftable())
        self.GemExportCount.setText(str(self.GemCount))

    def exportGemsToQuickbar(self):
        if len(self.Selection) == 0 or self.GemCount == 0: return
        bar = (self.QuickbarNum.value() - 1) if (self.QuickbarNum.value() != 1) else ''
        file = self.TableModel.data(self.TableModel.index(self.Selection[0].row(), 0), Qt.UserRole)
        index = ((self.QuickbarRow.value() - 1) * 10) + (self.QuickbarStart.value() - 1)

        with open(file, 'r') as document:
            with open(file + '.bak', 'w') as backup:
                backup.write(document.read())

        if (100 - index) < self.GemCount:
            QMessageBox.warning(
                self, 'Error!', 'There is insufficient space on the selected \n Quickbar to export the gems.')
            return

        button_strings = []
        for location, item in self.ItemExportList.items():
            for slot in [x for x in item.getSlotList() if x.isCraftable()]:

                try:  # HOTKEY MIGHT NOT EXIST ...
                    gem_tier = slot.getGemIndex()
                    gem_name = slot.getGemName(item.Realm).split(' ', 1)[1]
                    gem_hotkey = GemHotkeyValues[item.Realm][gem_name]
                    button_strings.append('45,13%03d%02d,,-1' % (gem_hotkey, gem_tier))
                except ValueError:
                    continue

        config = IniConfigParser()
        config.read([file])

        with open(file, 'w') as document:
            for string in button_strings:
                config.set(f'Quickbar{bar}', f'Hotkey_{index}', string)
                index += 1
            config.write(document)

        QMessageBox.information(
            self, 'Success!', 'Successfully exported gems to Quickbar!', QMessageBox.Ok)

    def restoreQuickbar(self):
        if len(self.Selection) == 0: return
        index = self.TableModel.index(self.Selection[0].row(), 0)
        file = self.TableModel.data(index, Qt.UserRole)

        if path.exists(file + '.bak') and path.isfile(file + '.bak'):
            with open(file, 'w') as document:
                with open(file + '.bak', 'r') as backup:
                    document.write(backup.read())
            remove(file + '.bak')

# =============================================== #
#        SLOT/SIGNAL METHODS AND FUNCTIONS        #
# =============================================== #

    def mousePressEvent(self, event):
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()' ...
            self.focusWidget().clearFocus()
        except AttributeError:
            pass

    def ItemSelectionChanged(self):
        self.ItemExportList.clear()
        for location, checkbox in self.CraftableItems.items():
            if checkbox.checkState() == Qt.Checked:
                self.ItemExportList[location] = self.ItemAttributeList[location]

        # CASCADE THE CHANGES ...
        self.getGemCount()

    def CharacterSelectionChanged(self):
        self.Selection = self.CharacterTable.selectedIndexes()
