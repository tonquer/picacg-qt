import json

from PySide6 import QtWidgets

from interface.ui_game import Ui_Game
from qt_owner import QtOwner
from server import req, Status, Log
from task.qt_task import QtTaskBase
from tools.str import Str


class GameView(QtWidgets.QWidget, Ui_Game, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Game.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        # self.bookList.InitBook(self.LoadNextPage)
        # self.bookList.InstallGame()
        self.bookList.isGame = True

    def SwitchCurrent(self, **kwargs):
        if self.bookList.count() > 0:
            return
        self.bookList.clear()
        self.bookList.page = 1
        self.bookList.pages = 1
        self.spinBox.setValue(1)
        self.spinBox.setMaximum(self.bookList.pages)
        self.bookList.UpdateState()
        self.UpdatePageLabel()
        QtOwner().ShowLoading()
        self.RefreshData()
        pass

    def RefreshData(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetGameReq(self.bookList.page), callBack=self.InitGameBack)

    def InitGameBack(self, raw):
        QtOwner().CloseLoading()
        self.bookList.UpdateState()
        try:
            st = raw["st"]
            if st == Status.Ok:
                data = json.loads(raw["data"])
                page = data.get("data").get("games").get("page", 1)
                pages = data.get("data").get("games").get("pages", 1)
                self.bookList.UpdatePage(page, pages)
                self.spinBox.setMaximum(self.bookList.pages)
                self.UpdatePageLabel()
                for info in data.get("data").get("games").get("docs"):
                    self.bookList.AddBookByDict(info)
            else:
                QtOwner().ShowError(Str.GetStr(st))
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
        self.pages.setText(Str.GetStr(Str.Page) + ": {}/{}".format(str(self.bookList.page), str(self.bookList.pages)))
