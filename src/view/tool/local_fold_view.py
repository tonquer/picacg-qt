import weakref

from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtWidgets import QWidget, QListWidgetItem, QHBoxLayout, QLineEdit, QPushButton, QLabel

from component.dialog.base_mask_dialog import BaseMaskDialog
from interface.ui_local_fold import Ui_LocalFold
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from PySide6.QtCore import Signal

from tools.str import Str


class FavoriteFoldItem(QWidget):
    itemDeleted = Signal(QListWidgetItem)

    def __init__(self, text, item, isDel, *args, **kwargs):
        super(FavoriteFoldItem, self).__init__(*args, **kwargs)
        self._item = item  # 保留list item的对象引用
        self.fid = ""
        self.text = text
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # self.lineEdit = QLineEdit(text, self)
        if isDel:
            self.lineEdit = QLabel(text, self)
            self.pushButton = QPushButton("x", self, clicked=self._DoDeleteItem)
            self.SetEditEnable(False)
        else:
            self.lineEdit = QLineEdit(text, self)
            self.lineEdit.setStyleSheet("border: 2px solid #ff4081")
            self.lineEdit.setMinimumSize(100, 40)
            self.pushButton = QPushButton(Str.GetStr(Str.Save), self, clicked=self._DoDeleteItem)
            self.SetEditEnable(True)

        layout.addWidget(self.lineEdit)
        layout.addWidget(self.pushButton)

    def SetEditEnable(self, isEnable):
        if isEnable:
            # self.lineEdit.setEnabled(True)
            # self.lineEdit.setFocusPolicy(Qt.ClickFocus)
            self.pushButton.setVisible(True)
        else:
            # self.lineEdit.setEnabled(False)
            # self.lineEdit.setFocusPolicy(Qt.NoFocus)
            self.pushButton.setVisible(False)

    def _DoDeleteItem(self):
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        # 决定item的高度
        return QSize(200, 40)


class LocalFoldView(BaseMaskDialog, Ui_LocalFold, QtTaskBase):
    MoveOkBack = Signal(str, list)
    FoldChange = Signal()
    AddFold = Signal(str)
    DelFold = Signal(str)
    InitBack = Signal()

    def __init__(self, parent, owner, bookId=""):
        BaseMaskDialog.__init__(self, parent)
        QtTaskBase.__init__(self)
        self.owner = weakref.ref(owner)
        self.setupUi(self.widget)
        self.setMinimumSize(400, 500)
        # self.listWidget.setFlow(self.listWidget.LeftToRight)
        self.listWidget.setSelectionMode(self.listWidget.SelectionMode.MultiSelection)
        self.listWidget.itemClicked.connect(self.SelectItem)
        self.widget.adjustSize()
        self.closeButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self._MoveBookToFold)
        self.editButton.clicked.connect(self.SwitchEdit)
        self.InitBack.connect(self.Init)
        self.isEditMode = False
        self.bookId = bookId
        self.isFoldChange = False
        if not self.bookId:
            self.saveButton.hide()

        self.Init()
        self.listWidget.setFocus()

    @property
    def categoryBook(self):
        return self.owner().categoryBook

    @property
    def bookCategory(self):
        return self.owner().bookCategory

    def Init(self):
        self.listWidget.clear()
        # self.AddAllItem()
        for name in self.categoryBook.keys():
            self.AddItem(name)
        return

    def SelectItem(self, item):
        assert isinstance(item, QListWidgetItem)
        # widget = self.bookList.itemWidget(item)
        if item.isSelected():
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        return

    def SwitchEdit(self):
        self.isEditMode = not self.isEditMode
        self._SwitchEdit()

    def _SwitchEdit(self):
        if self.isEditMode:
            self.saveButton.hide()
            self.AddEditItem("")
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                w = self.listWidget.itemWidget(item)
                if i <= 0:
                    continue
                w.SetEditEnable(True)
                # item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        else:
            if self.bookId:
                self.saveButton.setVisible(True)

            # 删除最后一个
            row = self.listWidget.count() - 1
            item = self.listWidget.takeItem(row)
            # 删除widget
            self.listWidget.removeItemWidget(item)
            del item
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                w = self.listWidget.itemWidget(item)
                w.SetEditEnable(False)
                # item.setFlags(item.flags() & Qt.ItemIsSelectable)

                # if w.fid == self.fid:
                #     item.setSelected(True)

        return

    def AddItem(self, name):
        item = QListWidgetItem(self.listWidget)
        widget = FavoriteFoldItem(name, item, True, self.listWidget)
        # 绑定删除信号
        widget.itemDeleted.connect(self._DoDeleteItem)
        # item.setCheckState(Qt.Checked)

        # item.setData(Qt.DisplayRole, "text")
        # item.setData(Qt.CheckStateRole, Qt.Checked)
        # item.setCheckable(True)
        item.setCheckState(Qt.Unchecked)
        if self.bookId:
            allCategory = self.bookCategory.get(self.bookId, [])
            if name in allCategory:
                item.setCheckState(Qt.Checked)
                item.setSelected(True)

        item.setSizeHint(widget.sizeHint())
        self.listWidget.setItemWidget(item, widget)
        # if widget.fid == self.fid:
        #     item.setSelected(True)
        return

    def AddEditItem(self, name):

        item = QListWidgetItem(self.listWidget)
        widget = FavoriteFoldItem(name, item, False, self.listWidget)
        # 绑定删除信号
        item.setSizeHint(widget.sizeHint()+QSize(0, 20))
        widget.itemDeleted.connect(self._DoAddItem)
        self.listWidget.setItemWidget(item, widget)
        return

    def AddAllItem(self):
        item = QListWidgetItem(self.listWidget)
        widget = FavoriteFoldItem(Str.GetStr(Str.All), item, True, self.listWidget)
        item.setSizeHint(widget.sizeHint())
        self.listWidget.setItemWidget(item, widget)
        # if widget.fid == self.fid:
        #     item.setSelected(True)

    def _DoAddItem(self, item):

        # 根据item得到它对应的行数
        row = self.listWidget.indexFromItem(item).row()
        w = self.listWidget.itemWidget(item)
        name = w.lineEdit.text()
        if not name:
            return
        if name == Str.GetStr(Str.All):
            QtOwner().ShowError(Str.GetStr(Str.AlreadyHave))
            return
        if name == Str.GetStr(Str.CurRead):
            QtOwner().ShowError(Str.GetStr(Str.AlreadyHave))
            return

        if name in self.categoryBook:
            QtOwner().ShowError(Str.GetStr(Str.AlreadyHave))
            return
        self.isEditMode = False
        self.AddFold.emit(w.lineEdit.text())
        self.InitBack.emit()
        # QtOwner().ShowLoading()
        # self.AddHttpTask(req.AddFavoritesFoldReq2(w.lineEdit.text()), self._DoAddItemBack, row)

    def _DoAddItemBack(self, raw, row):
        QtOwner().CloseLoading()
        if raw["st"] == Status.Ok:
            self.Init()
            self.isFoldChange = True
        QtOwner().CheckShowMsg(raw)

    def _DoDeleteItem(self, item):
        # 根据item得到它对应的行数
        row = self.listWidget.indexFromItem(item).row()
        w = self.listWidget.itemWidget(item)
        item = self.listWidget.takeItem(row)
        self.listWidget.removeItemWidget(item)
        self.DelFold.emit(w.lineEdit.text())
        del item
        self.isEditMode = False
        self.InitBack.emit()

    def _MoveBookToFold(self):
        fid = ""
        allcategory = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            w = self.listWidget.itemWidget(item)
            if item.isSelected():
                allcategory.append(w.lineEdit.text())
        self.MoveOkBack.emit(self.bookId, allcategory)

    def _MoveBookToFoldBack(self, raw):
        QtOwner().CloseLoading()
        QtOwner().CheckShowMsg(raw)
        if raw["st"] == Status.Ok:
            self.close()
            self.MoveOkBack.emit()

    def closeEvent(self, arg__1) -> None:
        self.closed.emit()
        self.Close()
        arg__1.accept()

    def Close(self):
        if self.isFoldChange:
            self.FoldChange.emit()
