# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import QIcon, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from Settings import Settings
import json
import os

Ui_DatabaseDialog = uic.loadUiType(r'interface/DatabaseDialog.ui')[0]


class DatabaseDialog(QDialog, Ui_DatabaseDialog):
    def __init__(self, parent = None, flags = Qt.Dialog,  location = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        font = QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(8)
        self.setFont(font)

        self.Settings = Settings.getInstance()

        self.initLayout()
        self.initControls()
        self.initialize()

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initLayout(self):
        self.setWindowTitle('Item Database')
        self.setWindowIcon(QIcon(None))

    def initControls(self):
        self.CloseButton.clicked.connect(self.accept)

    def initialize(self):
        pass

# =============================================== #
#                  SETTER METHODS                 #
# =============================================== #

# =============================================== #
#                  GETTER METHODS                 #
# =============================================== #

# =============================================== #
#                  CHANGE METHODS                 #
# =============================================== #

# =============================================== #
#                METHOD OVERRIDES                 #
# =============================================== #

    def mousePressEvent(self, event):
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()' ...
            self.focusWidget().clearFocus()
        except AttributeError:
            pass
