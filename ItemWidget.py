# HEADER PLACE HOLDER

from PyQt5.QtWidgets import QWidget


class Widget:

    def __init__(self):
        self.enabled = True
        self.text = None
        self.data = None


class ItemWidget(QWidget):

    def __init_(self, parent = None, name = None):
        self.WidgetList = []

        QWidget.__init__(self, parent, flags = None)
        if name:
            self.setObjectName(name)

    def addItemWidget(self, index, text):
        self.insertItemWidget(index, text)

    def insertItemWidget(self, index, text):
        widget = Widget()
        widget.text = text
        self.WidgetList.append([])
        self.WidgetList[index].append(widget)
        print(self.WidgetList)

    def removeItemWidget(self, index, text):
        pass


if __name__ == '__main__':
    pass
