import json
import re

from PySide2.QtCore import Qt, QStringListModel, QPoint, QEvent
from PySide2.QtWidgets import QApplication, QLineEdit, QListView, QCompleter, QWidget, QHBoxLayout


class CompleteLineEdit(QLineEdit):
    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        self.listView = QListView()
        origPolicy = self.focusPolicy()
        self.listView.setParent(self, Qt.Popup)
        self.listView.setFocusPolicy(Qt.NoFocus)
        self.listView.setFocusProxy(self)
        self.setFocusPolicy(origPolicy)
        self.model = QStringListModel(self)
        self.textChanged.connect(self.setCompleter)
        self.listView.clicked.connect(self.completeText)
        self.listView.setWindowFlags(Qt.ToolTip)
        self.listView.setModel(self.model)
        self.words = []
        self.isNotReload = False

    def keyPressEvent(self, ev):
        if not self.listView.isHidden():
            key = ev.key()
            count = self.listView.model().rowCount()
            currentIndex = self.listView.currentIndex()
            if Qt.Key_Down == key:
                curText = re.split('&|\|', self.text())
                curText = curText.pop() if len(curText) > 0 else ""
                if currentIndex.row() <= 0 and curText != currentIndex.data():
                    row = 0
                else:
                    row = currentIndex.row() + 1 if currentIndex.row() + 1 < count else 0
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)
                if self.listView.currentIndex().isValid():
                    self.completeText2(self.listView.currentIndex(), False)
                return
            elif Qt.Key_Up == key:
                row = currentIndex.row() - 1 if currentIndex.row() > 0 else 0
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)
                if self.listView.currentIndex().isValid():
                    self.completeText2(self.listView.currentIndex(), False)
                return
            elif Qt.Key_Escape == key:
                self.listView.hide()
            elif Qt.Key_Enter == key or Qt.Key_Return == key:
                if currentIndex.isValid():
                    self.completeText(self.listView.currentIndex())
                self.listView.hide()
        return QLineEdit.keyPressEvent(self, ev)

    def setCompleter(self, strings):
        if not strings:
            self.listView.hide()
            return
        if self.isNotReload:
            return
        datas = []
        strings = strings.upper()

        strings2 = re.split('&|\|', strings)
        strings = strings2.pop() if len(strings2) > 0 else ""
        isSelf = False
        from src.qt.com.langconv import Converter
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
        if not datas:
            self.listView.hide()
            return
        self.model.setStringList(datas)
        index = self.listView.model().index(0, 0)
        # self.listView.setCurrentIndex(index)
        self.listView.setMinimumHeight(self.height())
        self.listView.setMinimumWidth(self.width())
        p = QPoint(0, self.height())
        x = self.mapToGlobal(p).x()
        y = self.mapToGlobal(p).y() + 1
        self.listView.move(x, y)
        self.listView.show()

    def completeText(self, modelIndex):
        self.completeText2(modelIndex)
        self.listView.hide()

    def completeText2(self, modelIndex, isNext=True):
        text = modelIndex.data()
        data = text.split("|")
        self.isNotReload = True
        oldData = re.split('&|\|', self.text())
        # print(self.text())
        if len(oldData) > 0:
            text = self.text().replace(oldData[len(oldData)-1], data[0])
        if data[0] and isNext:
            text = text + "|"
        self.setText(text)
        self.isNotReload = False

    def focusOutEvent(self, ev):
        self.listView.hide()
        return QLineEdit.focusOutEvent(self, ev)
