from PySide2 import QtWidgets
import weakref

from src.index.category import CateGoryMgr
from src.qt.com.qtlistwidget import QtBookList
from src.util.status import Status
from ui.category import Ui_category


class QtCategory(QtWidgets.QWidget, Ui_category):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_category.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.bookList = QtBookList(self, self.__class__.__name__, owner)
        self.bookList.InitBook()
        self.gridLayout_2.addWidget(self.bookList)
        self.bookList.doubleClicked.connect(self.OpenSearch)
        self.bookList.InstallCategory()

    def SwitchCurrent(self):
        if self.bookList.count() <= 0:
            self.owner().loadingForm.show()
            self.owner().qtTask.AddHttpTask(lambda x: CateGoryMgr().UpdateCateGory(x), callBack=self.InitCateGoryBack)
        pass

    def InitCateGoryBack(self, msg):
        self.owner().loadingForm.close()
        if msg == Status.Ok:
            for index, info in enumerate(CateGoryMgr().idToCateGoryBase):
                url = info.thumb.get("fileServer")
                path = info.thumb.get("path")
                originalName = info.thumb.get("originalName")
                _id = info.id
                self.bookList.AddBookItem(_id, info.title, "", url, path, originalName)
            self.owner().searchForm.InitCheckBox()
        return

    def OpenSearch(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList.item(index)
        widget = self.bookList.itemWidget(item)
        text = widget.label.text()
        self.owner().userForm.listWidget.setCurrentRow(1)
        self.owner().searchForm.searchEdit.setText("")
        self.owner().searchForm.OpenSearchCategories(text)
        pass
