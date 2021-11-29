import json

from PySide6 import QtWidgets

from interface.ui_rank import Ui_Rank
from qt_owner import QtOwner
from server import req, Log, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class RankView(QtWidgets.QWidget, Ui_Rank, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Rank.__init__(self)
        QtTaskBase.__init__(self)

        self.isInitKind = False
        self.setupUi(self)

        self.isInit = False
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.SwitchPage)

    def SwitchCurrent(self, **kwargs):
        self.Init()
        pass

    def SwitchPage(self, index):
        if index == 0 and self.h24BookList.count() <= 0:
            self.AddHttpTask(req.RankReq("H24"), self.InitBack, backParam="H24")
        elif index == 1 and self.d7BookList.count() <= 0:
            self.AddHttpTask(req.RankReq("D7"), self.InitBack, backParam="D7")
        elif index == 2 and self.d30BookList.count() <= 0:
            self.AddHttpTask(req.RankReq("D30"), self.InitBack, backParam="D30")
        elif index == 3 and not self.isInitKind:
            QtOwner().ShowLoading()
            self.AddHttpTask(req.KnightRankReq(), self.InitKindBack)
        return

    def Init(self):
        if self.isInit:
            return
        self.isInit = True
        QtOwner().ShowLoading()
        self.AddHttpTask(req.RankReq("H24"), self.InitBack, backParam="H24")
        # self.AddHttpTask(req.RankReq("D7"), self.InitBack, backParam="D7")
        # self.AddHttpTask(req.RankReq("D30"), self.InitBack, backParam="D30")

    def InitBack(self, raw, backParam):
        QtOwner().CloseLoading()
        try:
            if backParam == "H24":
                bookList = self.h24BookList
            elif backParam == "D7":
                bookList = self.d7BookList
            elif backParam == "D30":
                bookList = self.d30BookList
            else:
                assert False

            st = raw["st"]
            if st == Status.Ok:
                data = json.loads(raw["data"])
                for v in data.get("data").get("comics"):
                    bookList.AddBookByDict(v)
            else:
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)
            self.isInit = False

    def InitKindBack(self, raw):
        QtOwner().CloseLoading()
        try:
            data = json.loads(raw["data"])
            if data.get("code") == 200:
                self.isInitKind = True
                for index, v in enumerate(data.get("data").get("users")):
                    self.kindList.AddUserKindItem(v, index+1)
            else:
                QtOwner().ShowError(raw["st"])
        except Exception as es:
            Log.Error(es)
            self.isInit = False
