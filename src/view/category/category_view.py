from PySide6 import QtWidgets
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

        if refresh or self.bookList.count() <= 0:
            QtOwner().ShowLoading()
            self.AddHttpTask(req.CategoryReq(), callBack=self.InitCateGoryBack)
        pass

    def InitCateGoryBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            self.bookList.clear()
            for index, info in enumerate(CateGoryMgr().idToCateGoryBase):
                self.bookList.AddBookItem(info.id, info.title, info.thumb.get("fileServer"), info.thumb.get("path"))
            # QtOwner().owner.searchForm.InitCheckBox()
        else:
            QtOwner().ShowError(Str.GetStr(st))
        return

    def SelectItem(self, item):
        assert isinstance(item, QListWidgetItem)
        widget = self.bookList.itemWidget(item)
        QtOwner().OpenSearchByCategory(widget.nameLable.text())
        return
