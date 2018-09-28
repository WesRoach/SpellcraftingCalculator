# HEADER PLACE HOLDER

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication
import MainWindow
import sys

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class SpellcraftingCalculator(QApplication):

    def __init__(self):
        args = sys.argv
        QApplication.__init__(self, args)
        self.setWindowIcon(QIcon(r'images/Spellcraft.png'))
        self.application = MainWindow.MainWindow()

    def initializeApplication(self):
        font = QFont(self.font())
        font.setFamily("Trebuchet MS")
        font.setPointSize(8)
        self.setFont(font)
        self.application.show()


if __name__ == '__main__':
    app = SpellcraftingCalculator()
    app.initializeApplication()
    sys.exit(app.exec_())
