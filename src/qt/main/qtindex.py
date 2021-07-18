import json

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QIcon

from resources.resources import DataMgr
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req, Log
from src.user.user import User
from ui.index import Ui_Index


class QtIndex(QtWidgets.QWidget, Ui_Index, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Index.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False

        self.randomList.InitBook()

        self.godList.InitBook()

        self.magicList.InitBook()

    def SwitchCurrent(self):
        if User().token:
            self.Init()
            if not self.randomList.count():
                self.InitRandom()
        pass

    def Init(self):
        self.isInit = True
        QtOwner().owner.loadingForm.show()
        self.AddHttpTask(req.GetCollectionsReq(), self.InitBack)

    def InitRandom(self):
        QtOwner().owner.loadingForm.show()
        self.AddHttpTask(req.GetRandomReq(), self.InitRandomBack)

    def InitBack(self, data):
        try:
            QtOwner().owner.loadingForm.close()
            self.godList.clear()
            self.magicList.clear()
            data = json.loads(data)
            for categroys in data.get("data").get("collections"):
                if categroys.get("title") == "本子神推薦":
                    bookList = self.godList
                else:
                    bookList = self.magicList
                for v in categroys.get('comics'):
                    bookList.AddBookItem(v)
        except Exception as es:
            Log.Error(es)
            self.isInit = False

    def InitRandomBack(self, data):
        try:
            QtOwner().owner.loadingForm.close()
            data = json.loads(data)
            self.randomList.clear()
            for v in data.get("data").get('comics'):
                bookList = self.randomList
                title = v.get("title", "")
                _id = v.get("_id")
                url = v.get("thumb", {}).get("fileServer")
                path = v.get("thumb", {}).get("path")
                originalName = v.get("thumb", {}).get("originalName")
                info = "完本," if v.get("finished") else ""
                info += "{}E/{}P".format(str(v.get("epsCount")), str(v.get("pagesCount")))
                bookList.AddBookItem(v)
        except Exception as es:
            Log.Error(es)
