import json

from PySide2 import QtWidgets
import weakref

from src.qt.com.qtlistwidget import QtBookList
from src.server import req, Server, Log
from ui.rank import Ui_Rank


class QtRank(QtWidgets.QWidget, Ui_Rank):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_Rank.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)

        self.h24BookList = QtBookList(self, "h24BookList", owner)
        self.h24BookList.InitBook()
        self.h24Layout.addWidget(self.h24BookList)
        self.h24BookList.doubleClicked.connect(self.OpenSearch)

        self.d7BookList = QtBookList(self, "d7BookList", owner)
        self.d7BookList.InitBook()
        self.d7Layout.addWidget(self.d7BookList)
        self.d7BookList.doubleClicked.connect(self.OpenSearch)

        self.d30BookList = QtBookList(self, "d30BookList", owner)
        self.d30BookList.InitBook()
        self.d30Layout.addWidget(self.d30BookList)
        self.d30BookList.doubleClicked.connect(self.OpenSearch)
        self.isInit = False

    def SwitchCurrent(self):
        self.Init()
        pass

    def Init(self):
        if self.isInit:
            return
        self.isInit = True
        self.owner().loadingForm.show()
        self.owner().qtTask.AddHttpTask(lambda x: Server().Send(req.RankReq("H24"), bakParam=x), self.InitBack, backParam="H24")
        self.owner().qtTask.AddHttpTask(lambda x: Server().Send(req.RankReq("D7"), bakParam=x), self.InitBack, backParam="D7")
        self.owner().qtTask.AddHttpTask(lambda x: Server().Send(req.RankReq("D30"), bakParam=x), self.InitBack, backParam="D30")

    def InitBack(self, raw, backParam):
        self.owner().loadingForm.close()
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
                    title = v.get("title", "")
                    _id = v.get("_id")
                    url = v.get("thumb", {}).get("fileServer")
                    path = v.get("thumb", {}).get("path")
                    originalName = v.get("thumb", {}).get("originalName")
                    info = "完本," if v.get("finished") else ""
                    info += "{}E/{}P".format(str(v.get("epsCount")), str(v.get("pagesCount")))
                    bookList.AddBookItem(_id, title, info, url, path, originalName)
        except Exception as es:
            Log.Error(es)
            self.isInit = False

    def OpenSearch(self, modelIndex):
        index = modelIndex.row()
        bookIndex = self.tabWidget.currentIndex()
        bookList = [self.h24BookList, self.d7BookList, self.d30BookList][bookIndex]
        item = bookList.item(index)
        if not item:
            return
        widget = bookList.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        self.owner().bookInfoForm.OpenBook(bookId)