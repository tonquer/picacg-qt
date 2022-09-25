import re

from PySide6.QtCore import QStringListModel, QPoint
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLineEdit, QLabel, QWidget, \
    QHBoxLayout

from interface.ui_line_edit_help_widget import Ui_LineEditHelp
from qt_owner import QtOwner
from server.sql_server import SqlServer
from tools.langconv import Converter


class SearchLineEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        # self.action = QAction()
        # self.action.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogResetButton))
        # self.addAction(self.action, self.TrailingPosition)
        # self.action.triggered.connect(self.Search)
        proxy = self.focusPolicy()
        # self.listView = BaseListWidget(self)
        # self.listView.setParent(self, Qt.Popup)
        # self.listView.setFocusPolicy(Qt.NoFocus)
        # self.listView.setFocusProxy(self)
        # self.setFocusPolicy(proxy)

        self.widget = QWidget()
        self.help = Ui_LineEditHelp()
        self.help.setupUi(self.widget)

        self.widget.setParent(self, Qt.Popup)
        # self.widget.setFocusPolicy(Qt.NoFocus)
        self.widget.setFocusProxy(self)
        # self.setFocusPolicy(proxy)
        # self.widget.setFocusPolicy(Qt.NoFocus)
        self.widget.setWindowFlags(Qt.ToolTip)
        self.qLabel = QLabel("asdasdasdasd")
        self.hLayout = QHBoxLayout(self.widget)
        self.hLayout.addWidget(self.qLabel)

        # self.model = QWidgetListModel(self)
        # self.listView.setWindowFlags(Qt.ToolTip)
        self.words = []
        self.cacheWords = []
        self.model = QStringListModel(self)
        self.listView.setModel(self.model)
        self.textChanged.connect(self.setCompleter)
        self.listView.clicked.connect(self.SetText)
        self.help.localWidget.Switch.connect(self.SetEnable)
        # self.listView.setModel(self.model)
        self.isNotReload = False
        # self.help.authorWidget.SetState(False)
        # self.help.tagWidget.SetState(False)
        self.help.categoryWidget.SetState(False)
        self.isShowSearch = True

        self.searchTag1 = "<font color=#232629>"
        self.searchTag2 = "</font>"

    @property
    def listView(self):
        return self.help.listView

    def SetWordData(self, data):
        self.words = data

    def UpdateTime(self, text):
        self.help.updateTime.setText(text)
        return

    def SetCacheWord(self):
        SqlServer().SetCacheWord(self.cacheWords)
        self.model.setStringList(self.cacheWords)
        return

    def AddCacheWord(self, word):
        if not word:
            return
        if word in self.cacheWords:
            self.cacheWords.remove(word)
        self.cacheWords.insert(0, word)
        del self.cacheWords[200:]

    def SetDbError(self):
        self.isShowSearch = False
        self.help.localWidget.SetState(False)
        self.SetEnable(False)
        return

    def SetEnable(self, isLocal):
        self.help.titleLabel.setVisible(isLocal)
        self.help.titleWidget.setVisible(isLocal)
        self.help.tagLabel.setVisible(isLocal)
        self.help.tagWidget.setVisible(isLocal)
        self.help.desLabel.setVisible(isLocal)
        self.help.desWidget.setVisible(isLocal)
        self.help.categoryLabel.setVisible(isLocal)
        self.help.categoryWidget.setVisible(isLocal)
        self.help.authorLabel.setVisible(isLocal)
        self.help.authorWidget.setVisible(isLocal)
        self.help.uploadLabel.setVisible(isLocal)
        self.help.uploadWidget.setVisible(isLocal)

    def SetText(self, index):
        item = self.model.itemData(index)
        text = item.get(0)
        # self.setText(text.replace(self.searchTag1, "").replace(self.searchTag2, ""))
        self.setText(text)
        self.Search()
        return

    def setCompleter(self, strings):
        if not strings:
            # 显示搜索历史
            self.model.setStringList(self.cacheWords)
            return

        if self.isNotReload:
            return
        strings = strings.upper()

        strings2 = re.split('&|\|', strings)
        strings = strings2.pop() if len(strings2) > 0 else ""
        isSelf = False
        strings = Converter('zh-hans').convert(strings)
        matchIndex = {}
        for data in self.words:
            assert isinstance(data, str)
            if strings == data:
                isSelf = True

            else:
                index = data.find(strings)
                if index < 0:
                    continue
                matchIndex[data] = index
        datas = list(matchIndex.keys())
        datas.sort(key=matchIndex.get)

        if isSelf:
            datas.insert(0, strings)
        self.model.setStringList(datas)

    def keyReleaseEvent(self, ev):
        # print(ev.key())
        count = self.listView.model().rowCount()
        currentIndex = self.listView.currentIndex()
        if ev.key() == Qt.Key_Up:
            if count > 0:
                if currentIndex.row() < 0:
                    row = 0
                elif currentIndex.row() == 0:
                    row = count - 1
                else:
                    row = currentIndex.row() - 1 if currentIndex.row() > 0 else 0
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)

        elif ev.key() == Qt.Key_Down:
            if count > 0:
                if currentIndex.row() < 0:
                    row = 0
                else:
                    row = currentIndex.row() + 1 if currentIndex.row() + 1 < count else 0
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)

        if ev.key() == Qt.Key_Enter or ev.key() == Qt.Key_Return:
            currentIndex = self.listView.currentIndex()
            if currentIndex.row() >= 0:
                text = currentIndex.data()
                self.setText(text)
            self.Search()
        return QLineEdit.keyReleaseEvent(self, ev)

    def Search(self):
        text = self.text()
        isLocal = self.help.localWidget.state
        isTitle = self.help.titleWidget.state
        isDes = self.help.desWidget.state
        isCategory = self.help.categoryWidget.state
        isTag = self.help.tagWidget.state
        isAuthor = self.help.authorWidget.state
        isUpLoad = self.help.uploadWidget.state
        QtOwner().OpenSearch(text, isLocal, isTitle, isDes, isCategory, isTag, isAuthor, isUpLoad)
        self.clearFocus()
        return

    def clearFocus(self) -> None:
        return QLineEdit.clearFocus(self)

    def focusInEvent(self, ev):
        # print("in")
        self.ShowListView()
        return QLineEdit.focusInEvent(self, ev)

    def focusOutEvent(self, ev):
        self.widget.hide()
        # print("out")
        return QLineEdit.focusOutEvent(self, ev)

    def HideListView(self):
        if self.widget.isHidden():
            return
        self.widget.hide()
        # self.widget.clear()

    def ShowListView(self):
        if not self.widget.isHidden():
            return
        if not self.isShowSearch:
            return
        self.widget.show()
        pos = self.mapToGlobal(self.pos())
        # print(pos, self.pos(), self.size())
        self.widget.move(pos-self.pos()+QPoint(0, self.height()))
        self.widget.resize(max(500, self.width()), QtOwner().owner.height() // 2)
        # self.ShowInit()

    def CheckClick(self, pos):
        if self.widget.isHidden():
            return
        self.clearFocus()
        return