import re

from PySide6.QtCore import QStringListModel, QPoint
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLineEdit, QLabel, QWidget, \
    QHBoxLayout

from interface.ui_line_edit_help_widget import Ui_LineEditHelp
from qt_owner import QtOwner
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
        self.widget.setFocusPolicy(Qt.NoFocus)
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

    @property
    def listView(self):
        return self.help.listView

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

    def SetText(self, index):
        item = self.model.itemData(index)
        self.setText(item.get(0))
        self.Search()
        return

    def setCompleter(self, strings):
        if not strings:
            # self.widget.hide()
            self.model.setStringList([])
            return
        if self.isNotReload:
            return
        datas = []
        strings = strings.upper()

        strings2 = re.split('&|\|', strings)
        strings = strings2.pop() if len(strings2) > 0 else ""
        isSelf = False
        strings = Converter('zh-hans').convert(strings)
        for data in self.words:
            assert isinstance(data, str)
            # if fuzz.token_sort_ratio(strings, data) >= 80:
            if strings == data:
                isSelf = True
            elif strings in data:
                datas.append(data)
        datas.sort()
        if isSelf:
            datas.insert(0, strings)
        # if not datas:
            # self.listView.hide()
            # return
        self.model.setStringList(datas)
        # index = self.listView.model().index(0, 0)
        # self.listView.setCurrentIndex(index)
        # self.listView.setMinimumHeight(self.height())
        # self.listView.setMinimumWidth(self.width())
        # p = QPoint(0, self.height())
        # x = self.mapToGlobal(p).x()
        # y = self.mapToGlobal(p).y() + 1
        # self.listView.move(x, y)
        # self.listView.show()

    def keyReleaseEvent(self, ev):
        # print(ev.key())
        if ev.key() == Qt.Key_Enter or ev.key() == Qt.Key_Return:
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
        QtOwner().OpenSearch(text, isLocal, isTitle, isDes, isCategory, isTag, isAuthor)
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