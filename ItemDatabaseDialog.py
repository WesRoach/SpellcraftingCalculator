# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import QIcon, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog

Ui_ItemDatabaseDialog = uic.loadUiType(r'interface/ItemDatabaseDialog.ui')[0]


class ItemDatabaseDialog(QDialog, Ui_ItemDatabaseDialog):
    def __init__(self, parent = None, flags = Qt.Dialog, items = None):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        font = QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(8)
        self.setFont(font)

        self.initLayout()
        self.initControls()

# =============================================== #
#       INTERFACE SETUP AND INITIALIZATION        #
# =============================================== #

    def initLayout(self):
        self.setWindowTitle('Item Database')
        self.setWindowIcon(QIcon(None))

    def initControls(self):
        self.CloseButton.clicked.connect(self.accept)

# =============================================== #
#                  GETTER METHODS                 #
# =============================================== #

# =============================================== #
#                  CHANGE METHODS                 #
# =============================================== #

# =============================================== #
#             EXPORT/RESTORE METHODS              #
# =============================================== #

# =============================================== #
#                METHOD OVERRIDES                 #
# =============================================== #

    def mousePressEvent(self, event):
        try:  # NOT ALL WIDGETS HAVE 'clearFocus()' ...
            self.focusWidget().clearFocus()
        except AttributeError:
            pass
