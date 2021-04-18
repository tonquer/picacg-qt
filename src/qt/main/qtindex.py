import json
import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QIcon

from resources.resources import DataMgr
from src.qt.com.qtlistwidget import QtBookList
from src.server import Server, req,  Log
from src.user.user import User
from ui.index import Ui_Index


class QtIndex(QtWidgets.QWidget, Ui_Index):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_Index.__init__(self)
        self.setupUi(self)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.owner = weakref.ref(owner)
        self.isInit = False
        self.bookList1 = QtBookList(self, "1", owner)
        self.bookList1.InitBook()
        self.horizontalLayout.addWidget(self.bookList1)
        self.bookList1.doubleClicked.connect(self.OpenSearch1)
        self.bookList2 = QtBookList(self, "2", owner)
        self.bookList2.InitBook()
        self.bookList2.doubleClicked.connect(self.OpenSearch2)
        self.horizontalLayout_2.addWidget(self.bookList2)

        self.bookList3 = QtBookList(self, "3", owner)
        self.bookList3.InitBook()
        self.bookList3.doubleClicked.connect(self.OpenSearch3)
        self.horizontalLayout_3.addWidget(self.bookList3)
        p = QPixmap()
        p.loadFromData(DataMgr().GetData("fold2"))
        q = QPixmap()
        q.loadFromData(DataMgr().GetData("fold1"))
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton.setIcon(QIcon(p))
        self.bookList1.setVisible(False)
        self.toolButton_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_2.setIcon(QIcon(p))
        self.bookList2.setVisible(False)
        self.toolButton_3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_3.setIcon(QIcon(q))
        self.bookList3.setVisible(True)

        self.toolButton.clicked.connect(self.SwitchButton1)
        self.toolButton_2.clicked.connect(self.SwitchButton2)
        self.toolButton_3.clicked.connect(self.SwitchButton3)

    def SwitchCurrent(self):
        if User().token:
            self.Init()
            if not self.bookList3.count():
                self.InitRandom()
        pass

    def Init(self):
        self.isInit = True
        self.owner().loadingForm.show()
        self.owner().qtTask.AddHttpTask(lambda x: Server().Send(req.GetCollectionsReq(), bakParam=x), self.InitBack)

    def InitRandom(self):
        self.owner().loadingForm.show()
        self.owner().qtTask.AddHttpTask(lambda x: Server().Send(req.GetRandomReq(), bakParam=x), self.InitRandomBack)

    def InitBack(self, data):
        try:
            self.owner().loadingForm.close()
            self.bookList1.clear()
            self.bookList2.clear()
            data = json.loads(data)
            for categroys in data.get("data").get("collections"):
                if categroys.get("title") == "本子神推薦":
                    bookList = self.bookList1
                else:
                    bookList = self.bookList2
                for v in categroys.get('comics'):
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

    def InitRandomBack(self, data):
        try:
            self.owner().loadingForm.close()
            data = json.loads(data)
            self.bookList3.clear()
            for v in data.get("data").get('comics'):
                bookList = self.bookList3
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

    def OpenSearch1(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList1.item(index)
        if not item:
            return
        widget = self.bookList1.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        self.owner().bookInfoForm.OpenBook(bookId)
        return

    def OpenSearch2(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList2.item(index)
        if not item:
            return
        widget = self.bookList2.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        self.owner().bookInfoForm.OpenBook(bookId)
        return

    def OpenSearch3(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList3.item(index)
        if not item:
            return
        widget = self.bookList3.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        self.owner().bookInfoForm.OpenBook(bookId)
        return

    def SwitchButton1(self):
        isVisible = self.bookList1.isVisible()
        self.bookList1.setVisible(not isVisible)
        p = QPixmap()
        if isVisible:
            p.loadFromData(DataMgr().GetData("fold2"))
        else:
            p.loadFromData(DataMgr().GetData("fold1"))
        self.toolButton.setIcon(QIcon(p))
        return

    def SwitchButton2(self):
        isVisible = self.bookList2.isVisible()
        self.bookList2.setVisible(not isVisible)
        p = QPixmap()
        if isVisible:
            p.loadFromData(DataMgr().GetData("fold2"))
        else:
            p.loadFromData(DataMgr().GetData("fold1"))
        self.toolButton_2.setIcon(QIcon(p))

        return

    def SwitchButton3(self):
        isVisible = self.bookList3.isVisible()
        self.bookList3.setVisible(not isVisible)
        p = QPixmap()
        if isVisible:
            p.loadFromData(DataMgr().GetData("fold2"))
        else:
            p.loadFromData(DataMgr().GetData("fold1"))
        self.toolButton_3.setIcon(QIcon(p))
        return
