import json
import os
from this import d

from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QAction, Qt, QDesktopServices
from PySide6.QtWidgets import QWidget, QMenu, QFileDialog
from natsort import natsorted

from interface.ui_index import Ui_Index
from interface.ui_local import Ui_Local
from qt_owner import QtOwner
from server import Status, time
from task.qt_task import QtTaskBase
from task.task_local import LocalData
from tools.str import Str
from tools.tool import time_me
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
        self.action4 = QAction(Str.GetStr(Str.ImportDouble), self.toolMenu, triggered=self.CheckAction3)
        self.action3 = QAction(Str.GetStr(Str.SupportDrop), self.toolMenu)
        self.action3.setEnabled(False)
        # self.action3 = QAction(Str.GetStr(Str.ImportSimpleDir), self.toolMenu, triggered=self.CheckAction3)
        # self.action4 = QAction(Str.GetStr(Str.ImportChipDir), self.toolMenu, triggered=self.CheckAction4)

        self.toolMenu.addAction(self.action1)
        self.toolMenu.addAction(self.action2)
        self.toolMenu.addAction(self.action4)
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
        self.bookList.LoadCallBack = self.LoadNextPage
        self.lastPath = ""
        self.sortKeyCombox.setCurrentIndex(1)
        self.sortIdCombox.currentIndexChanged.connect(self.Init)
        self.sortKeyCombox.currentIndexChanged.connect(self.Init)

        self.setAcceptDrops(True)
        self.categoryBook = {}
        self.bookCategory = {}
        self.tagsList.clicked.connect(self.ClickTagsItem)
        self.curSelectCategory = ""
        self.isCurRead = False
        self.bookList.isMoveMenu = True
        self.bookList.MoveHandler = self.MoveCallBack
        self.bookList.openMenu = True
        self.bookList.OpenDirHandler = self.OpenDirCallBack
        self.lineEdit.textChanged.connect(self.SearchTextChange)
        self.delAll.clicked.connect(self.ShowDelAll)
        self.searchText = ""

        self.sortAllBookIds = []

    def SearchTextChange(self, text):
        self.searchText = text
        self.InitBook()

    def Init(self):
        self.categoryBook, self.bookCategory = self.db.LoadCategory()
        self.tagsList.clear()
        self.tagsList.AddItem(Str.GetStr(Str.All), True)
        item = self.tagsList.AddItem(Str.GetStr(Str.CurRead), True)
        if self.isCurRead:
            item.setSelected(True)

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
        self.ResetSortBookIds()
        self.ShowPages()

    def ResetSortBookIds(self):
        if self.curSelectCategory:
            allBookId = self.categoryBook.get(self.curSelectCategory, [])
        else:
            allBookId = self.allBookInfos.keys()
        allBookId2 = self.db.Search(self.searchText)
        showIds = list(set(allBookId) & set(allBookId2))
        self.sortAllBookIds = []
        allBookInfos = []
        for i in showIds:
            v = self.allBookInfos.get(i)
            if v:
                if self.isCurRead:
                    if v.lastReadTime > 0:
                        allBookInfos.append(v)
                else:
                    allBookInfos.append(v)

        for v in self.ToSortData(allBookInfos):
            if v.id in showIds:
                self.sortAllBookIds.append(v.id)

    @time_me
    def ShowPages(self, page=1):
        showLen = 30
        maxPage = len(self.sortAllBookIds) // showLen + 1
        showStart = (page - 1) * showLen
        showEnd = page * showLen

        self.spinBox.setValue(page)
        self.spinBox.setMaximum(maxPage)
        self.bookList.UpdatePage(page, maxPage)
        self.pages.setText(self.bookList.GetPageStr())
        self.nums.setText("{}：{} ".format(Str.GetStr(Str.FavoriteNum), len(self.sortAllBookIds)))

        showIds2 = self.sortAllBookIds[showStart:showEnd]
        for id in showIds2:
            v = self.allBookInfos.get(id)
            if v:
                categoryList = self.bookCategory.get(v.id, [])
                categoryStr = ",".join(categoryList)
                if not self.searchText or self.searchText in v.title:
                    self.bookList.AddBookByLocal(v, categoryStr)
        return

    def LoadNextPage(self):
        self.ShowPages(self.bookList.page + 1)

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.clear()
        self.ShowPages(page)
        return

    def ClickTagsItem(self, modelIndex):
        index = modelIndex.row()
        item = self.tagsList.item(index)
        if not item:
            return
        widget = self.tagsList.itemWidget(item)
        text = widget.text()
        # print(text)
        self.isCurRead = False
        if text == "+":
            self.OpenFavoriteFold()
        elif index == 0:
            self.curSelectCategory = ""
            self.Init()
            self.sortIdCombox.setCurrentIndex(0)
            self.sortKeyCombox.setCurrentIndex(1)
        elif index == 1:
            self.curSelectCategory = ""
            self.isCurRead = True
            self.Init()
            self.sortIdCombox.setCurrentIndex(0)
            self.sortKeyCombox.setCurrentIndex(0)
        else:
            self.curSelectCategory = text
            self.Init()

    def ShowDelAll(self):
        QtOwner().OpenLocalDelAll()

    def ToSortData(self, value):
        datas = list(value)
        sortId = self.sortIdCombox.currentIndex()
        sortKeyID = self.sortKeyCombox.currentIndex()
        isRevert = (sortId == 0)
        if sortKeyID == 0:
            datas.sort(key=lambda a: a.lastReadTime, reverse=isRevert)
        elif sortKeyID == 2:
            datas = natsorted(datas, key=lambda a: a.title, reverse=isRevert)
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
        # self.Init()
        self.bookList.DelBookID(bookId)

    def DelLocalReadAll(self, bookIds):
        for bookId in bookIds:
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
        if v.eps != []:
            type = LocalData.Type3
        elif v.isZipFile:
            type = LocalData.Type2
        else:
            type = LocalData.Type1

        QtOwner().ShowLoading()
        self.AddLocalTaskLoad(type, v.file, bookId, callBack=self.OpenLocalBookBack)
        return

    def OpenLocalBookBack(self, st, books, bookId):
        QtOwner().CloseLoading()
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
        self.db.AddLoadLocalBook(v)
        if v.eps != []:
            QtOwner().OpenLocalEpsView(v.id)
            return

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

    def UpdateLastTick(self, taskId):
        if taskId not in self.allBookInfos:
            return
        v = self.allBookInfos[taskId]
        v.lastReadTime = int(time.time())
        self.db.AddLoadLocalBook(v)
        return

    def AddEpsDataToDB(self, taskId, subId):
        if taskId not in self.allBookInfos:
            return
        for v in self.allBookInfos[taskId].eps:
            if v.id == subId:
                self.db.AddLoadLocalEpsBook(v)
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
                # 已存在则更新
                alreadyNum += 1
                self.allBookInfos[v.id].CopyData(v)
                self.db.AddLoadLocalBook(self.allBookInfos[v.id])
            else:
                self.allBookInfos[v.id] = v
                addNum += 1
                # 忽略
                if self.curSelectCategory:
                    category = self.curSelectCategory
                    self.db.AddCategory(self.curSelectCategory, v.id)
                else:
                    category = ""
                self.bookList.AddBookByLocal(v, category)
                self.AddDataToDB(v.id)
        QtOwner().ShowMsg("已添加{}本到书架, {}本存在已忽略".format(addNum, alreadyNum))
        self.lineEdit.setText("")
        self.isCurRead = False
        self.sortIdCombox.setCurrentIndex(0)
        self.sortKeyCombox.setCurrentIndex(1)
        self.Init()
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

    # 导入单本目录
    def CheckAction3(self):
        if self.lastPath:
            url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold), dir=self.lastPath)
        else:
            url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            QtOwner().ShowLoading()
            self.AddLocalTaskLoad(LocalData.Type3, url, os.path.dirname(url), self.CheckAction1LoadBack)
        return

    # 批量导入带章节的目录
    def CheckAction4(self):
        return

    # 批量导入下载目录
    def ImportDownloadDirs(self, dirs):
        self.curSelectCategory = ""
        self.AddLocalTaskLoad(LocalData.Type6, dirs, "", self.CheckAction1LoadBack)
        return

    def dragEnterEvent(self, event):
        if (event.mimeData().hasUrls()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, evemt):
        return

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if (mimeData.hasUrls()):
            urls = mimeData.urls()
            QtOwner().ShowLoading()
            fileNames = [str(i.toLocalFile()) for i in urls]
            self.AddLocalTaskLoad(LocalData.Type5, fileNames, "", self.CheckAction1LoadBack)

    def MoveCallBack(self, index):
        widget = self.bookList.indexWidget(index)
        if widget:
            self.OpenFavoriteFold(widget.id)

    def OpenDirCallBack(self, index):
        widget = self.bookList.indexWidget(index)
        if widget:
            info = self.allBookInfos.get(widget.id)
            if not info:
                return
            assert isinstance(info, LocalData)
            if info.isZipFile:
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(info.file)))
            else:
                QDesktopServices.openUrl(QUrl.fromLocalFile(info.file))

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