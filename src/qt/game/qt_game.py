import json

from PySide2 import QtWidgets

from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req
from src.util import Log
from ui.game import Ui_Game


class QtGame(QtWidgets.QWidget, Ui_Game, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Game.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookList.InitBook(self.LoadNextPage)
        self.bookList.doubleClicked.connect(self.OpenGameInfo)
        self.bookList.InstallCategory()


    def OpenGameInfo(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList.item(index)
        if not item:
            return
        widget = self.bookList.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        QtOwner().owner.gameInfoForm.OpenBook(bookId)

    def SwitchCurrent(self):
        self.bookList.clear()
        self.bookList.page = 1
        self.bookList.pages = 1
        self.spinBox.setValue(1)
        self.spinBox.setMaximum(self.bookList.pages)
        self.bookList.UpdateState()
        self.UpdatePageLabel()
        QtOwner().owner.loadingForm.show()
        self.RefreshData()
        pass

    def RefreshData(self):
        self.AddHttpTask(req.GetGameReq(self.bookList.page), callBack=self.InitGameBack)

    def InitGameBack(self, data):
        QtOwner().owner.loadingForm.close()
        self.bookList.UpdateState()
        try:
            data = json.loads(data)
            page = data.get("data").get("games").get("page", 1)
            pages = data.get("data").get("games").get("pages", 1)
            self.bookList.UpdatePage(page, pages)
            self.spinBox.setMaximum(self.bookList.pages)
            self.UpdatePageLabel()
            for info in data.get("data").get("games").get("docs"):
                self.bookList.AddBookItem(info)
        except Exception as es:
            Log.Error(es)

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.UpdatePageLabel()
        self.RefreshData()

    def LoadNextPage(self):
        self.bookList.page += 1
        self.RefreshData()
        self.UpdatePageLabel()

    def UpdatePageLabel(self):
        self.pages.setText("页：{}/{}".format(str(self.bookList.page), str(self.bookList.pages)))