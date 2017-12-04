# HEADER PLACE HOLDER

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget


class ItemWidget(QWidget):

    def __init_(self, parent = None, name = None):
        self.WidgetList = []

        QWidget.__init__(self, parent, flags = None)
        if name:
            self.setObjectName(name)

    def addItemWidget(self, index, text):
        self.insertItemWidget(index, text)

    def insertItemWidget(self, index, text):
        self.WidgetList.append([])
        pass

    def removeItemWidget(self, index, text):
        pass