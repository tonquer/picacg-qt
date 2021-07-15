import json

from PySide2 import QtWidgets

from src.qt.qtmain import QtOwner
from src.server import req, Log, QtTask
from ui.rank import Ui_Rank


class QtRank(QtWidgets.QWidget, Ui_Rank):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Rank.__init__(self)
        self.setupUi(self)
        self.h24BookList.InitBook()

        self.d7BookList.InitBook()

        self.d30BookList.InitBook()
        self.isInit = False
        self.tabWidget.setCurrentIndex(0)

    def SwitchCurrent(self):
        self.Init()
        pass

    def Init(self):
        if self.isInit:
            return
        self.isInit = True
        QtOwner().owner.loadingForm.show()
        QtTask().AddHttpTask(req.RankReq("H24"), self.InitBack, backParam="H24")
        QtTask().AddHttpTask(req.RankReq("D7"), self.InitBack, backParam="D7")
        QtTask().AddHttpTask(req.RankReq("D30"), self.InitBack, backParam="D30")

    def InitBack(self, raw, backParam):
        QtOwner().owner.loadingForm.close()
        try:
            if backParam == "H24":
                bookList = self.h24BookList
            elif backParam == "D7":
                bookList = self.d7BookList
            elif backParam == "D30":
                bookList = self.d30BookList
            else:
                assert False

            data = json.loads(raw)
            if data.get("code") == 200:
                for v in data.get("data").get("comics"):
                    bookList.AddBookItem(v)
        except Exception as es:
            Log.Error(es)
            self.isInit = False