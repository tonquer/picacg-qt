from PySide6 import QtWidgets

from src.index.category import CateGoryMgr
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req
from src.util.status import Status
from ui.category import Ui_category


class QtCategory(QtWidgets.QWidget, Ui_category, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_category.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookList.InitBook()
        self.bookList.InstallCategory()

    def SwitchCurrent(self):
        if self.bookList.count() <= 0:
            QtOwner().owner.loadingForm.show()
            self.AddHttpTask(req.CategoryReq(), callBack=self.InitCateGoryBack)
        pass

    def InitCateGoryBack(self, msg):
        QtOwner().owner.loadingForm.close()
        if msg == Status.Ok:
            for index, info in enumerate(CateGoryMgr().idToCateGoryBase):
                self.bookList.AddBookItem(info)
            QtOwner().owner.searchForm.InitCheckBox()
        return
