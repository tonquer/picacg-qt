import json

from PySide6.QtWidgets import QWidget

from interface.ui_index import Ui_Index
from qt_owner import QtOwner
from server import req, Log, User, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class IndexView(QWidget, Ui_Index, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Index.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.toolButton.clicked.connect(self.InitRandom)
        self.tabWidget.setCurrentIndex(0)
        # self.randomList.InitBook()

        # self.godList.InitBook()

        # self.magicList.InitBook()

    def SwitchCurrent(self, **kwargs):
        if User().token:
            if not self.godList.count():
                self.Init()
            if not self.randomList.count():
                self.InitRandom()
        pass

    def Init(self):
        self.isInit = True
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetCollectionsReq(), self.InitBack)

    def InitRandom(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetRandomReq(), self.InitRandomBack)

    def InitBack(self, raw):
        try:
            QtOwner().CloseLoading()
            self.godList.clear()
            self.magicList.clear()
            st = raw["st"]
            if st == Status.Ok:
                data = json.loads(raw["data"])
                allData = [data.get("data").get("collections", [])]
                for i, categroys in enumerate(data.get("data").get("collections")):
                    if i == 0:
                        bookList = self.godList
                    else:
                        bookList = self.magicList
                    if i < 2:
                        self.tabWidget.setTabText(i+1, categroys.get("title"))
                    for v in categroys.get('comics'):
                        bookList.AddBookByDict(v)
            else:
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)
            self.isInit = False

    def InitRandomBack(self, raw):
        try:
            QtOwner().CloseLoading()
            data = json.loads(raw["data"])
            st = raw["st"]
            if st == Status.Ok:
                self.randomList.clear()
                for v in data.get("data").get('comics'):
                    bookList = self.randomList
                    # title = v.get("title", "")
                    # _id = v.get("_id")
                    # url = v.get("thumb", {}).get("fileServer")
                    # path = v.get("thumb", {}).get("path")
                    # info = Str.GetStr(Str.ComicFinished) if v.get("finished") else ""
                    # info += "{}E/{}P".format(str(v.get("epsCount")), str(v.get("pagesCount")))
                    # bookList.AddBookItem(_id, title, "", url, path)
                    bookList.AddBookByDict(v)
            else:
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)
