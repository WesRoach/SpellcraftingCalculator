# HEADER PLACE HOLDER

from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QMainWindow, QMenu, QToolBar, QTreeWidgetItem, QWidget
from Character import AllBonusList, ClassList, Races, Realms
from Constants import Cap, DropLists, MythicalCap
from Item import Item, SlotList


class ItemWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent = parent)
        uic.loadUi(r'interface/ItemWidget.ui', self)
        self.enabled = True
        self.text = None
        self.data = None


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self, None, Qt.Window)
        uic.loadUi(r'interface/MainWindow.ui', self)

        self.FileMenu = QMenu('&File', self)
        self.EditMenu = QMenu('&Edit', self)
        self.ViewMenu = QMenu('&View', self)
        self.ErrorMenu = QMenu('&Errors', self)
        self.HelpMenu = QMenu('&Help', self)
        self.ToolBar = QToolBar("Crafting")

        self.StatLabel = {}
        self.StatValue = {}
        self.StatCap = {}
        self.StatMythicalCap = {}
        self.StatBonus = {}

        self.ItemIndex = 0
        self.ItemIndexList = {}
        self.ItemNumbering = 1
        self.ItemAttributeList = {}

        self.CurrentRealm = ''
        self.CurrentItemIndex = 0

        self.initMenuBar()
        self.initToolBar()
        self.initLayout()
        self.initControls()
        self.initialize(False)

    def initMenuBar(self):
        self.FileMenu.addAction('E&xit', self.close)

        self.menuBar().addMenu(self.FileMenu)
        self.menuBar().addMenu(self.EditMenu)
        self.menuBar().addMenu(self.ViewMenu)
        self.menuBar().addMenu(self.ErrorMenu)
        self.menuBar().addMenu(self.HelpMenu)

    def initToolBar(self):
        self.ToolBar.setObjectName("Crafting")
        self.ToolBar.setFloatable(False)
        self.ToolBar.addAction('New')

        self.addToolBar(self.ToolBar)

    def initLayout(self):
        font = QFont(self.font())
        font.setFamily("Trebuchet MS")
        font.setPointSize(8)
        self.setFont(font)

        # TODO: DYNAMICALLY ASSIGN SIZE
        self.setMinimumSize(780, 520)
        self.setWindowTitle('Spellcrafting Calculator')

        # MAKE SURE WE ARE TESTING WIDTH AND HEIGHT
        # VALUES BASED ON THE FONT BEING USED ...
        testFont = QFontMetrics(self.font())

        # TODO: DYNAMICALLY ASSIGN SIZE
        width = 100
        height = 20

        self.CharacterName.setFixedSize(QSize(width, height))
        self.CharacterRealm.setFixedSize(QSize(width, height))
        self.CharacterClass.setFixedSize(QSize(width, height))
        self.CharacterRace.setFixedSize(QSize(width, height))
        self.CharacterLevel.setFixedSize(QSize(width, height))
        self.CharacterRealmRank.setFixedSize(QSize(width, height))
        self.OutfitName.setFixedSize(QSize(width, height))

        for stat in (DropLists['All']['Stat'] + ('ArmorFactor', 'Fatigue', 'PowerPool',)):
            self.StatLabel[stat] = getattr(self, stat + 'Label')
            self.StatValue[stat] = getattr(self, stat)
            self.StatCap[stat] = getattr(self, stat + 'Cap')

            try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
                self.StatMythicalCap[stat] = getattr(self, stat + 'MythicalCap')
            except AttributeError:
                pass

        width = testFont.size(Qt.TextSingleLine, "CON: ", tabArray = None).width()
        self.StatsGroup.layout().setColumnMinimumWidth(0, width)
        width = testFont.size(Qt.TextSingleLine, "400", tabArray = None).width()
        self.StatsGroup.layout().setColumnMinimumWidth(1, width)
        width = testFont.size(Qt.TextSingleLine, "(400)", tabArray = None).width()
        self.StatsGroup.layout().setColumnMinimumWidth(2, width)
        width = testFont.size(Qt.TextSingleLine, "(26)", tabArray = None).width()
        self.StatsGroup.layout().setColumnMinimumWidth(3, width)

        for resist in (DropLists['All']['Resist']):
            self.StatLabel[resist] = getattr(self, resist + 'Label')
            self.StatValue[resist] = getattr(self, resist)
            self.StatBonus[resist] = getattr(self, resist + 'Cap')

            try:  # NOT ALL RESISTS HAVE MYTHICAL CAP ...
                self.StatMythicalCap[resist] = getattr(self, resist + 'MythicalCap')
            except AttributeError:
                pass

        width = testFont.size(Qt.TextSingleLine, "Essence: ", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(0, width)
        width = testFont.size(Qt.TextSingleLine, "26", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(1, width)
        width = testFont.size(Qt.TextSingleLine, "(15)", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(2, width)
        width = testFont.size(Qt.TextSingleLine, "+5", tabArray = None).width()
        self.ResistGroup.layout().setColumnMinimumWidth(3, width)

        for key, value in SlotList.items():
            root = QTreeWidgetItem(self.SlotListTreeView, [key])
            for val in value:
                root.addChild(QTreeWidgetItem([val]))

        self.CharacterRealm.insertItems(0, list(Realms))

    def initControls(self):
        self.SlotListTreeView.itemClicked.connect(self.ItemSelected)
        self.CharacterRealm.activated[int].connect(self.RealmChanged)
        self.CharacterClass.activated[int].connect(self.ClassChanged)
        self.CharacterRace.activated[int].connect(self.RaceChanged)

    def ItemSelected(self, selection):
        for index in self.SlotListTreeView.selectedIndexes():
            selection = index.data()

        print(self.ItemIndexList)

        for key, value in self.ItemIndexList.items():
            if selection == key:

                # DEBUGGING ...
                print('Selection: ' + str(value))
                print('Widget: ' + str(self.ItemStackedWidget.widget(value)))

                self.ItemStackedWidget.setCurrentIndex(value)

    def RealmChanged(self, value):
        Realm = str(self.CharacterRealm.currentText())
        self.CharacterClass.clear()
        self.CharacterClass.insertItems(0, list(ClassList[Realm]))
        self.ClassChanged(self.CharacterClass.currentIndex())
        self.CurrentRealm = Realm

    def ClassChanged(self, value):
        Realm = str(self.CharacterRealm.currentText())
        Class = str(self.CharacterClass.currentText())
        self.CharacterRace.clear()
        self.CharacterRace.insertItems(0, AllBonusList[Realm][Class]['Races'])
        self.RaceChanged(self.CharacterRace.currentIndex())
        self.calculate()

    def RaceChanged(self, value):
        Race = str(self.CharacterRace.currentText())
        for Resist in DropLists['All']['Resist']:
            if Resist in Races['All'][Race]['Resists']:
                self.StatBonus[Resist].setText('+ ' + str(Races['All'][Race]['Resists'][Resist]))
            else:
                self.StatBonus[Resist].setText('-')

    def LoadOptions(self):
        pass

    def SaveOptions(self):
        pass

    def initialize(self, boolean):
        self.CharacterName.setText('')
        self.CharacterLevel.setText('50')
        self.CharacterRealmRank.setText('10')

        # SETUP THE INITIAL CHARACTER ...
        self.CharacterRealm.setCurrentIndex(2)
        self.RealmChanged(self.CharacterRealm.currentIndex())
        self.CharacterClass.setCurrentIndex(7)
        self.ClassChanged(self.CharacterClass.currentIndex())
        self.CharacterRace.setCurrentIndex(2)
        self.RaceChanged(self.CharacterRace.currentIndex())

        self.ItemStackedWidget.setCurrentIndex(0)

        for key, value in SlotList.items():
            for val in value:
                self.ItemIndexList[val] = self.ItemIndex
                if key == 'Armor':
                    item = Item('crafted', val, self.CurrentRealm, self.ItemIndex)
                    item.ItemName = "Crafted Item #" + str(self.ItemNumbering)
                    self.ItemIndex += 1
                    self.ItemNumbering += 1
                    self.ItemAttributeList[val] = item
                else:
                    item = Item('drop', val, self.CurrentRealm, self.ItemIndex)
                    item.ItemName = "Drop Item #" + str(self.ItemNumbering)
                    self.ItemIndex += 1
                    self.ItemNumbering += 1
                    self.ItemAttributeList[val] = item

        # AttributeError: 'QStackedWidget' object has no ...
        for key, value in self.ItemIndexList.items():
            widget = ItemWidget()
            widget.Requirement1.setPlaceholderText(str(key))
            self.ItemStackedWidget.insertWidget(value, widget)

    def showStat(self, stat, show):
        if self.StatLabel[stat].isHidden() != show:
            return
        self.StatLabel[stat].setVisible(show)
        self.StatValue[stat].setVisible(show)
        self.StatCap[stat].setVisible(show)

        try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
            self.StatMythicalCap[stat].setVisible(show)
        except KeyError:
            pass

    def summarize(self):
        Level = int(self.CharacterLevel.text())
        Total = {
            'Utility': 0.0,
            'Stats': {},
            'Resists': {},
            'Skills': {},
            'Focus': {},
            'MythicalBonuses': {},
            'OtherBonuses': {},
            'PvEBonuses': {}
        }

        for effect in DropLists['All']['Resist']:
            Total['Resists'][effect] = {}
            Total['Resists'][effect]['Bonus'] = 0
            Total['Resists'][effect]['TotalBonus'] = 0
            Total['Resists'][effect]['MythicalCapBonus'] = 0
            Total['Resists'][effect]['TotalMythicalCapBonus'] = 0
            Race = str(self.CharacterRace.currentText())

            if effect in Races['All'][Race]['Resists']:
                Total['Resists'][effect]['RacialBonus'] = Races['All'][Race]['Resists'][effect]

            Base = Cap['Resist']
            BaseMythicalCap = MythicalCap['Resist Cap']
            Total['Resists'][effect]['Base'] = int(Level * Base[0]) + Base[1]
            Total['Resists'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        for effect in DropLists['All']['Stat'] + ('Armor Factor', 'Fatigue', '% Power Pool'):
            Total['Stats'][effect] = {}
            Total['Stats'][effect]['Bonus'] = 0
            Total['Stats'][effect]['TotalBonus'] = 0
            Total['Stats'][effect]['CapBonus'] = 0
            Total['Stats'][effect]['TotalCapBonus'] = 0
            Total['Stats'][effect]['MythicalCapBonus'] = 0
            Total['Stats'][effect]['TotalMythicalCapBonus'] = 0

            if effect in Cap:
                Base = Cap[effect]
                BaseCap = Cap[effect + ' Cap']

            else:
                Base = Cap['Stat']
                BaseCap = Cap['Stat Cap']

            Total['Stats'][effect]['Base'] = int(Level * Base[0]) + Base[1]
            Total['Stats'][effect]['BaseCap'] = int(Level * BaseCap[0]) + BaseCap[1]

            if effect in DropLists['All']['Mythical Cap Increase']:
                BaseMythicalCap = MythicalCap['Stat Cap']
                Total['Stats'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

            if effect in MythicalCap:
                BaseMythicalCap = MythicalCap[effect]
                Total['Stats'][effect]['BaseMythicalCap'] = int(Level * BaseMythicalCap[0]) + BaseMythicalCap[1]

        return Total

    def calculate(self):
        Realm = str(self.CharacterRealm.currentText())
        Class = str(self.CharacterClass.currentText())
        Total = self.summarize()

        for key, amounts in list(Total['Resists'].items()):
            Base = amounts['Base']
            TotalBonus = amounts['TotalBonus']
            BaseMythicalCap = amounts['BaseMythicalCap']
            TotalMythicalCapBonus = amounts['TotalMythicalCapBonus']
            self.StatValue[key].setText(str(int(Base - TotalBonus)))
            self.StatMythicalCap[key].setText('(' + str(int(BaseMythicalCap - TotalMythicalCapBonus)) + ')')

        for (key, datum) in list(Total['Stats'].items()):
            Acuity = AllBonusList[Realm][Class]["Acuity"]
            TotalBonus = datum['TotalBonus']

            if key == "Armor Factor":
                key = "ArmorFactor"

            if key == "% Power Pool":
                key = "PowerPool"

            if key[:5] == "Power":
                Skills = AllBonusList[Realm][Class]["All Magic Skills"]
                self.showStat(key, (datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0)
                              or (len(Skills) > 0))

            elif key == "Fatigue":
                Skills = AllBonusList[Realm][Class]["All Melee Weapon Skills"]
                self.showStat(key, (datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0)
                              or (len(Skills) > 0))

            elif key == "Acuity":
                self.showStat(key, ((datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0))
                              and (len(Acuity) == 0))

            elif key in ("Charisma", "Empathy", "Intelligence", "Piety"):
                self.showStat(key, (datum['TotalCapBonus'] > 0)
                              or (datum['TotalMythicalCapBonus'] > 0)
                              or (TotalBonus > 0)
                              or (key in Acuity))

            Base = datum['Base']
            BaseCap = datum['BaseCap']

            try:  # NOT ALL STATS HAVE MYTHICAL CAP ...
                BaseMythicalCap = datum['BaseMythicalCap']
            except KeyError:
                BaseMythicalCap = 0

            if datum['TotalCapBonus'] > 0:
                TotalCapBonus = datum['TotalCapBonus']

            if datum['TotalMythicalCapBonus'] > 0:
                TotalMythicalCapBonus = datum['TotalMythicalCapBonus']

            else:
                TotalCapBonus = 0
                TotalMythicalCapBonus = 0

            if TotalCapBonus > BaseCap:
                TotalCapBonus = BaseCap

            if TotalMythicalCapBonus > BaseMythicalCap:
                TotalMythicalCapBonus = BaseMythicalCap

            self.StatValue[key].setText(str(int(Base + TotalCapBonus) - TotalBonus))
            self.StatCap[key].setText('(' + str(int(BaseCap - TotalCapBonus)) + ')')
            self.StatMythicalCap[key].setText('(' + str(int(BaseMythicalCap - TotalMythicalCapBonus)) + ')')

            if BaseMythicalCap == 0:
                self.StatMythicalCap[key].setText('--  ')
