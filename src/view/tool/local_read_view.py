import json
import os
from this import d

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QWidget, QMenu, QFileDialog
from natsort import natsorted

from interface.ui_index import Ui_Index
from interface.ui_local import Ui_Local
from qt_owner import QtOwner
from server import req, Log, User, Status
from task.qt_task import QtTaskBase
from task.task_local import LocalData
from tools.str import Str
from view.tool.local_read_db import LocalReadDb


class LocalReadView(QWidget, Ui_Local, QtTaskBase):
    ReloadHistory = Signal(int)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Index.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        # self.tabWidget.setCurrentIndex(0)
        # self.toolButton.clicked.connect(self.AddBookByDir)
        self.toolMenu = QMenu(self.toolButton)

        self.action1 = QAction(Str.GetStr(Str.ImportSimple), self.toolMenu, triggered=self.CheckAction1)
        self.action2 = QAction(Str.GetStr(Str.ImportSimpleZip), self.toolMenu, triggered=self.CheckAction2)
        self.action3 = QAction(Str.GetStr(Str.SupportDrop), self.toolMenu)
        self.action3.setEnabled(False)
        # self.action3 = QAction(Str.GetStr(Str.ImportSimpleDir), self.toolMenu, triggered=self.CheckAction3)
        # self.action4 = QAction(Str.GetStr(Str.ImportChipDir), self.toolMenu, triggered=self.CheckAction4)

        self.toolMenu.addAction(self.action1)
        self.toolMenu.addAction(self.action2)
        self.toolMenu.addAction(self.action3)
        # self.toolMenu.addAction(self.action3)
        # self.toolMenu.addAction(self.action4)

        self.toolButton.setMenu(self.toolMenu)
        self.db = LocalReadDb()
        self.bookList.isLocal = True
        # self.randomList.InitBook()

        # self.godList.InitBook()

        # self.magicList.InitBook()
        self.allBookInfos = {}
        self.isInit = False

        self.bookList.isDelMenu = True
        self.bookList.DelCallBack = self.DelLocalRead
        self.bookList.LoadingPicture = self.LoadingPicture
        self.bookList.ReDownloadPicture = self.LoadingPicture
        self.lastPath = ""

        self.sortIdCombox.currentIndexChanged.connect(self.Init)
        self.sortKeyCombox.currentIndexChanged.connect(self.Init)
        self.setAcceptDrops(True)
        self.categoryBook = {}
        self.bookCategory = {}
        self.tagsList.clicked.connect(self.ClickTagsItem)
        self.curSelectCategory = ""
        self.bookList.isMoveMenu = True
        self.bookList.MoveHandler = self.MoveCallBack

    def Init(self):
        self.categoryBook, self.bookCategory = self.db.LoadCategory()
        self.tagsList.clear()
        self.tagsList.AddItem(Str.GetStr(Str.All), True)

        for category in self.categoryBook.keys():
            item = self.tagsList.AddItem(category, True)

            if category == self.curSelectCategory:
                item.setSelected(True)
        self.tagsList.AddItem("+")
        self.InitBook()

    def InitBook(self):
        self.bookList.clear()
        books = self.db.LoadLocalBook()
        oldDict = dict(self.allBookInfos)
        self.allBookInfos.clear()

        for v in books.values():
            self.allBookInfos[v.id] = v
            oldV = oldDict.get(v.id)
            if oldV:
                v.CopyData(oldV)

        if self.curSelectCategory:
            allBookId = self.categoryBook.get(self.curSelectCategory, [])
        else:
            allBookId = self.allBookInfos.keys()
        for v in self.ToSortData(list(self.allBookInfos.values())):
            if v.id in allBookId:
                categoryList = self.bookCategory.get(v.id, [])
                categoryStr = ",".join(categoryList)
                self.bookList.AddBookByLocal(v, categoryStr)
        return

    def ClickTagsItem(self, modelIndex):
        index = modelIndex.row()
        item = self.tagsList.item(index)
        if not item:
            return
        widget = self.tagsList.itemWidget(item)
        text = widget.text()
        # print(text)
        if text == "+":
            self.OpenFavoriteFold()
        elif text == Str.GetStr(Str.All):
            self.curSelectCategory = ""
            self.Init()
        else:
            self.curSelectCategory = text
            self.Init()

    def ToSortData(self, value):
        datas = list(value)
        sortId = self.sortIdCombox.currentIndex()
        sortKeyID = self.sortKeyCombox.currentIndex()
        isRevert = (sortId != 0)
        if sortKeyID == 0:
            datas.sort(key=lambda a: a.lastReadTime, reverse=isRevert)
        elif sortKeyID == 1:
            datas = natsorted(datas, key=lambda a:a.title, reverse=isRevert)
        else:
            datas.sort(key=lambda a: a.addTime, reverse=isRevert)
        return datas

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh:
            self.Init()
        return

    def InitData(self):
        return

    def HandlerTask(self, st, books, url):
        alreadyNum = 0
        addNum = 0
        for v in books:
            if v.id in self.allBookInfos:
                alreadyNum += 1
            else:
                self.allBookInfos[v.id] = v
                addNum += 1
                self.bookList.AddBookByLocal(v)
        QtOwner().ShowMsg("已添加{}本到书架, {}本存在已忽略".format(addNum, alreadyNum))
        return

    def LoadingPicture(self, index):
        if isinstance(index, int):
            item = self.bookList.item(index)
            widget = self.bookList.itemWidget(item)
        else:
            widget = self.bookList.indexWidget(index)
        bookId = widget.id
        if bookId not in self.allBookInfos:
            return
        v = self.allBookInfos[bookId]
        self.AddLocalTaskLoadPicture(v, -1, index, self.bookList.LoadingPictureComplete)

    def DelLocalRead(self, bookId):
        if bookId not in self.allBookInfos:
            return
        del self.allBookInfos[bookId]
        self.db.DelDownloadDB(bookId)
        self.Init()

    def OpenLocalBook(self, bookId):
        if bookId not in self.allBookInfos:
            return
        v = self.allBookInfos[bookId]
        assert isinstance(v, LocalData)
        type = LocalData.Type1 if not v.isZipFile else LocalData.Type2
        self.AddLocalTaskLoad(type, v.file, bookId, callBack=self.OpenLocalBookBack)
        return

    def OpenLocalBookBack(self, st, books, bookId):
        if st != Status.Ok:
            QtOwner().ShowError(Str.GetStr(st))
            return
        if books == []:
            QtOwner().ShowError(Str.GetStr(Str.NotPictureFile))
            return
        if bookId not in self.allBookInfos:
            return
        v = self.allBookInfos[bookId]
        assert isinstance(v, LocalData)
        newV = books[0]
        v.CopyData(newV)
        if v.picCnt <= 0:
            QtOwner().ShowError(Str.GetStr(Str.NotPictureFile))
            return
        self.AddDataToDB(bookId)
        QtOwner().OpenLocalReadView(v)
        return

    def AddDataToDB(self, taskId):
        if taskId not in self.allBookInfos:
            return
        v = self.allBookInfos[taskId]
        self.db.AddLoadLocalBook(v)
        return

    def AddBookByDir(self):
        return

    # 导入单本目录
    def CheckAction1(self):
        if self.lastPath:
            url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold), dir=self.lastPath)
        else:
            url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            QtOwner().ShowLoading()
            self.AddLocalTaskLoad(LocalData.Type1, url, os.path.dirname(url), self.CheckAction1LoadBack)
        return

    def CheckAction1LoadBack(self, st, books, url):
        QtOwner().CloseLoading()
        if st != Status.Ok:
            QtOwner().ShowError(Str.GetStr(st))
            return
        alreadyNum = 0
        addNum = 0
        if url:
            self.lastPath = url
        for v in books:
            if v.id in self.allBookInfos:
                alreadyNum += 1
            else:
                self.allBookInfos[v.id] = v
                addNum += 1
                if self.curSelectCategory:
                    category = self.curSelectCategory
                    self.db.AddCategory(self.curSelectCategory, v.id)
                else:
                    category = ""
                self.bookList.AddBookByLocal(v, category)
                self.AddDataToDB(v.id)
        QtOwner().ShowMsg("已添加{}本到书架, {}本存在已忽略".format(addNum, alreadyNum))
        return

    # 导入单本Zip
    def CheckAction2(self):
        if self.lastPath:
            filename = QFileDialog.getOpenFileName(self, "Open Zip", self.lastPath, "Image Files(*.zip)")
        else:
            filename = QFileDialog.getOpenFileName(self, "Open Zip", ".", "Image Files(*.zip)")
        if filename and len(filename) >= 1:
            name = filename[0]
            if os.path.isfile(name):
                QtOwner().ShowLoading()
                path = os.path.dirname(name)
                self.AddLocalTaskLoad(LocalData.Type2, name, path, self.CheckAction1LoadBack)
        return

    # 批量导入目录
    def CheckAction3(self):
        return

    # 批量导入带章节的目录
    def CheckAction4(self):
        return

    def JumpPage(self):
        return

    def dragEnterEvent(self, event):
        if(event.mimeData().hasUrls()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, evemt):
        return

    def dropEvent(self, event):
        mimeData  = event.mimeData()
        if(mimeData.hasUrls()):
            urls = mimeData.urls()
            QtOwner().ShowLoading()
            fileNames = [str(i.toLocalFile()) for i in urls]
            self.AddLocalTaskLoad(LocalData.Type5, fileNames, "", self.CheckAction1LoadBack)

    def MoveCallBack(self, index):
        widget = self.bookList.indexWidget(index)
        if widget:
            self.OpenFavoriteFold(widget.id)

    def OpenFavoriteFold(self, bookId=""):
        from view.tool.local_fold_view import LocalFoldView
        w = LocalFoldView(QtOwner().owner, self, bookId)
        w.show()
        w.AddFold.connect(self.AddCategory)
        w.DelFold.connect(self.DelCategory)
        w.MoveOkBack.connect(self.MoveCategory)

    def AddCategory(self, name):
        if name in self.categoryBook:
            return
        self.categoryBook[name] = []
        self.db.AddCategory(name)
        self.Init()

    def DelCategory(self, name):
        if name not in self.categoryBook:
            return
        self.db.DelCategory(name)
        self.curSelectCategory = ""
        self.Init()

    def MoveCategory(self, bookId, categoryList):
        self.db.DelBookCategory(bookId)
        for v in categoryList:
            self.db.AddCategory(v, bookId)
        self.Init()