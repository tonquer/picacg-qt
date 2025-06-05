from PySide6 import QtWidgets
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QListWidgetItem

from interface.ui_category import Ui_Category
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.category import CateGoryMgr
from tools.str import Str


class CategoryView(QtWidgets.QWidget, Ui_Category, QtTaskBase):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        Ui_Category.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookList.itemClicked.connect(self.SelectItem)

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")

        if refresh and self.bookList.count() <= 0:
            QtOwner().ShowLoading()
            self.AddHttpTask(req.CategoryReq(), callBack=self.InitCateGoryBack)
        pass

    def InitCateGoryBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            self.bookList.clear()
            if len(CateGoryMgr().idToCateGoryBase) > 0:
                self.AddStaticCategory()
            for index, info in enumerate(CateGoryMgr().idToCateGoryBase):
                self.bookList.AddBookItem(info.id, info.title, info.thumb.get("fileServer"), info.thumb.get("path"))
            # QtOwner().owner.searchForm.InitCheckBox()
        else:
            QtOwner().ShowError(Str.GetStr(st))
        return

    def AddStaticCategory(self):
        self.bookList.AddBookItem("1", Str.GetStr(Str.Rank), "", "")
        self.bookList.LoadingPictureComplete(QtOwner().GetFileData(":/png/icon/cat_leaderboard.jpg"), Status.Ok, 0)
        self.bookList.AddBookItem("2", Str.GetStr(Str.LeaveMsg), "", "")
        self.bookList.LoadingPictureComplete(QtOwner().GetFileData(":/png/icon/cat_forum.jpg"), Status.Ok, 1)
        self.bookList.AddBookItem("3", Str.GetStr(Str.AgoUpdate), "", "")
        self.bookList.LoadingPictureComplete(QtOwner().GetFileData(":/png/icon/cat_latest.jpg"), Status.Ok, 2)
        self.bookList.AddBookItem("4", Str.GetStr(Str.RandomBook), "", "")
        self.bookList.LoadingPictureComplete(QtOwner().GetFileData(":/png/icon/cat_random.jpg"), Status.Ok, 3)

    def SelectItem(self, item):
        assert isinstance(item, QListWidgetItem)
        widget = self.bookList.itemWidget(item)
        if widget.id == "1":
            QtOwner().OpenRank()
        elif widget.id == "2":
            QtOwner().OpenComment("5822a6e3ad7ede654696e482")
        elif widget.id == "3":
            QtOwner().OpenSearchByText("")
        elif widget.id == "4":
            QtOwner().OpenIndex()
        else:
            QtOwner().OpenSearchByCategory(widget.nameLable.text())
        return
