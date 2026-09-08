import json
import re
from functools import partial

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QHelpEvent
from PySide6.QtWidgets import QWidget, QCheckBox

from component.layout.flow_layout import FlowLayout
from interface.ui_search import Ui_Search
from qt_owner import QtOwner
from server import req, Log, Status
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.category import CateGoryMgr
from tools.langconv import Converter
from tools.str import Str
from server.book_query import BookQuery, SORT_FIELDS
from tools.page_result import PageRequest, PageResult


class SearchView(QWidget, Ui_Search, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Search.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.categories = ""
        self.text = ""
        self.isLocal = True
        self.isTitle = True
        self.isDes = True
        self.isCategory = True
        self.isTag = True
        self.isAuthor = True
        self.isUpLoad = True
        self.isFinish = False
        self.bookList.LoadCallBack = self.LoadNextPage
        # self.categoryList.itemClicked.connect(self.ClickCategoryListItem)
        # self.InitCategoryList()
        # self.categoryList.setSelectionMode(QListView.MultiSelection)
        # self.categoryList.setSpacing(1)
        self.comboBox.currentIndexChanged.connect(self.ChangeSort)
        self.sortKey.currentIndexChanged.connect(self.ChangeSort)
        self.sortId.currentIndexChanged.connect(self.ChangeSort)
        self.searchButton.clicked.connect(self.lineEdit.Search)

        self.widget.hide()
        self.selectAllButton.hide()
        self.saveButton.hide()
        self.unfoldButton.clicked.connect(partial(self.CheckShowWidget))
        self.saveButton.clicked.connect(self.ClearAndSendSearch)
        self.selectAllButton.clicked.connect(partial(self.CheckSelectAll))
        self.jumpPage.clicked.connect(self.JumpPage)
        self.flowLayout = FlowLayout(self.widget)
        self.allBox = {}
        self.isSelectAll = False
        self.InitCategory()
        self.lastText = "--1"
        self.hiddenNum = 0
        self.searchLabel.installEventFilter(self)
        # self.someDownButton.clicked.connect(self.bookList.OpenBookDownloadAll)

        self.cacheRecommend = {}
        self.isSearch2 = False

    def ResetSearch(self):
        self.bookList.UpdatePage(1, 1)
        self.bookList.clear()
        self.spinBox.setMaximum(1)
        self.spinBox.setValue(1)
        self.label.setText(self.bookList.GetPageStr())

    def SetPageLoading(self, loading):
        self.bookList.UpdateState(loading)
        self.spinBox.setEnabled(not loading)
        self.jumpPage.setEnabled(not loading)

    def BuildBookQuery(self, categories):
        if self.categories:
            text, fields = self.categories, ("categories",)
        else:
            text = self.text
            enabled = {"title": self.isTitle, "author": self.isAuthor,
                       "description": self.isDes, "tags": self.isTag,
                       "categories": self.isCategory, "creator": self.isUpLoad}
            fields = tuple(field for field, selected in enabled.items() if selected)
        return BookQuery(text=text, fields=fields, categories=tuple(categories),
                         finished_only=self.isFinish if not self.categories else False,
                         sort_field=SORT_FIELDS[self.sortKey.currentIndex()],
                         descending=self.sortId.currentIndex() == 0)

    def QueueLocalPage(self, query, page):
        self.AddSqlTask("book", (query, PageRequest(page)), SqlServer.TaskTypeSelectBookPage,
                        self.ReceiveLocalPage, page)
        self.UpdateFacetCounts(query)

    def ReceiveLocalPage(self, result, requestedPage):
        if result is None:
            self.SetPageLoading(False)
            QtOwner().CloseLoading()
            QtOwner().ShowError(Str.GetStr(Str.Error))
            return
        if result.page != requestedPage:
            self.bookList.clear()
        self.ApplyPageResult(result, self.bookList.AddBookItemByDbBook)

    def ApplyPageResult(self, result, addItem):
        QtOwner().CloseLoading()
        self.bookList.UpdatePage(result.page, result.pages)
        self.SetPageLoading(True)
        self.spinBox.setMaximum(result.pages)
        self.spinBox.setValue(result.page)
        self.label.setText(self.bookList.GetPageStr())
        try:
            for item in result.items:
                addItem(item)
        finally:
            self.SetPageLoading(False)

    def UpdateFacetCounts(self, query):
        key = query.for_facets()
        if key != self.lastText:
            self.lastText = key
            self.ClearLocalNum()
            _, statement, _ = key.statements()
            self.AddSqlTask("book", statement, SqlServer.TaskTypeCategoryBookNum,
                            self.SendLocalCategoryNumBack, key)

    def InitCategory(self):
        for categorory in CateGoryMgr().allCategorise:
            text = Converter('zh-hans').convert(categorory)
            box = QCheckBox(text)
            box.setMinimumWidth(160)

            self.allBox[text] = box
            self.flowLayout.addWidget(box)

    def UpdateTime(self, text):
        self.lineEdit.UpdateTime(text)

    def GetSelectCategory(self):
        if self.isSelectAll:
            return []
        else:
            category = []
            for k, box in self.allBox.items():
                if box.isChecked():
                    if self.isLocal:
                        category.append(Converter('zh-hans').convert(k))
                    else:
                        category.append(Converter('zh-hant').convert(k))
            return category

    def CheckSelectAll(self):
        self.isSelectAll = not self.isSelectAll
        if self.isSelectAll:
            self.selectAllButton.setText(Str.GetStr(Str.NotSelectAll))
            for v in self.allBox.values():
                v.setChecked(True)
        else:
            self.selectAllButton.setText(Str.GetStr(Str.SelectAll))
            for v in self.allBox.values():
                v.setChecked(False)
        return

    def CheckShowWidget(self):
        if self.widget.isHidden():
            self.widget.setVisible(True)
            self.saveButton.setVisible(True)
            self.selectAllButton.setVisible(True)
        else:
            self.widget.setVisible(False)
            self.saveButton.setVisible(False)
            self.selectAllButton.setVisible(False)
        return

    def InitWord(self):
        self.AddSqlTask("book", "", SqlServer.TaskTypeSelectWord, self.InitWordBack)
        self.lineEdit.SetCacheWord()
        return

    def InitWordBack(self, data):
        if not data:
            return
        self.lineEdit.SetWordData(data)

    # def InitCategoryList(self):
    #     self.categoryList.clear()
    #     for name in ["耽美", "伪娘", "禁书", "扶她", "重口", "生肉", "纯爱", "SM", "NTR", "WEBTOON"]:
    #         self.categoryList.AddItem(name, True)

    def SwitchCurrent(self, **kwargs):
        text = kwargs.get("text")
        categories = kwargs.get("categories")
        if text and re.match('^[0-9a-zA-Z]+$',text) and len(text) == len("5d5d760774184679c1e63f4c"):
            QtOwner().OpenBookInfo(text)
            return
        if text and "pica" in text.lower() and text.lower().replace("pica", "").isdigit():
            QtOwner().OpenBookInfoByShareId(int(text.lower().replace("pica", "")))
            self.lineEdit.AddCacheWord(text)
            return

        if not QtOwner().isUseDb:
            self.isLocal = False

        isRecomend =  kwargs.get("recoment")
        if isRecomend == 1:
            self.bookList.clear()
            bookId = kwargs.get("bookId")
            self.bookList.UpdatePage(1, 1)
            self.spinBox.setValue(1)
            self.spinBox.setMaximum(1)
            self.label.setText(self.bookList.GetPageStr())
            QtOwner().ShowLoading()
            self.AddHttpTask(req.GetComicsRecommendation(bookId), self.OpenRecommendationBack)
            return
        if isRecomend == 2:
            self.bookList.clear()
            bookId = kwargs.get("bookId")
            self.bookList.UpdatePage(1, 1)
            self.spinBox.setValue(1)
            self.spinBox.setMaximum(1)
            self.label.setText(self.bookList.GetPageStr())
            if bookId in self.cacheRecommend:
                self.OpenRecommendationBack2({"data": self.cacheRecommend[bookId]}, bookId)
                return
            QtOwner().ShowLoading()
            self.AddHttpTask(req.GetRecommendByIdReq(bookId), self.OpenRecommendationBack2, bookId)
            return

        if categories is not None:
            self.categories = categories
        self.bookList.setFocus()
        if categories is not None:
            self.isLocal = False
            self.text = ""
            self.lineEdit.setText(self.categories)
            self.ResetSearch()
            if self.categories in CateGoryMgr().allCategorise:
                self.SetEnable(True)
            else:
                self.SetEnable(False)
            self.SendSearchCategories(1)
        elif text is not None:
            self.text = text
            self.categories = ""
            self.lineEdit.setText(self.text)
            self.ResetSearch()
            isLocal = kwargs.get("isLocal")

            if isLocal is not None:
                self.isLocal = isLocal
            if not QtOwner().canUseDb:
                self.isLocal = False
            self.SetEnable(self.isLocal)
            self.isTitle = kwargs.get("isTitle")
            self.isDes = kwargs.get("isDes")
            self.isCategory = kwargs.get("isCategory")
            self.isTag = kwargs.get("isTag")
            self.isAuthor = kwargs.get("isAuthor")
            self.isUpLoad = kwargs.get("isUpLoad")
            self.isFinish = kwargs.get("isFinish", False)
            self.lineEdit.AddCacheWord(self.text)
            self.SendSearch(1)
        pass

    def SetDbError(self):
        self.isLocal = False
        self.SetEnable(False)
        self.lineEdit.SetDbError()

    def SetEnable(self, isLocal):
        if self.isSearch2:
            return
        self.sortId.setVisible(isLocal)
        self.sortKey.setVisible(isLocal)
        self.comboBox.setVisible(not isLocal)

    def OpenRecommendationBack(self, raw):
        QtOwner().CloseLoading()
        data = raw.get("data")
        try:
            commentsData = json.loads(data)
            for v in commentsData.get("data").get("comics"):
                self.bookList.AddBookByDict(v)
        except Exception as es:
            Log.Error(es)

    def OpenRecommendationBack2(self, raw, bookId):
        QtOwner().CloseLoading()
        data = raw.get("data")
        try:
            commentsData = json.loads(data)
            allBookIds = []
            for v in commentsData.get("recommendations", []):
                allBookIds.append(v)
            if QtOwner().canUseDb:
                sql = SqlServer.GetBookByIds(allBookIds)
                self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, callBack=self.OpenLocalRecommendationBack, backParam=1)
            else:
                for bookId in allBookIds:
                    self.AddHttpTask(req.GetComicsBookReq(bookId), self.OpenRecommendationBack3, bookId)
                    # if v.get('pic'):
                    #     v['thumb'] = {}
                    #     host = ToolUtil.GetUrlHost(v.get('pic'))
                    #     v['thumb']['fileServer'] = "https://" + host
                    #     v['thumb']['path'] = v.get('pic').replace("http://", "").replace("https://", "").replace(host, "").replace("/static", "")
                    #     self.bookList.AddBookByDict(v)
            # self.cacheRecommend[bookId] = data
        except Exception as es:
            Log.Error(es)

    def OpenRecommendationBack3(self, raw, bookId):
        book = BookMgr().GetBook(bookId)
        if not book:
            return
        if raw.get("st") == Str.Ok:
            data = json.loads(raw.get("data"))
            self.bookList.AddBookByDict(data.get('data').get("comic"))
        return

    def OpenLocalRecommendationBack(self, books, page):
        self.SendLocalBack(books, page)
        if books is None:
            return
        self.bookList.pages = 1
        self.spinBox.setMaximum(1)
        self.spinBox.setValue(1)
        self.bookList.UpdatePage(1, self.bookList.pages)

    def SendSearchCategories(self, page):
        sort = ["dd", "da", "ld", "vd"]
        self.SetPageLoading(True)
        QtOwner().ShowLoading()
        if QtOwner().canUseDb and self.categories in CateGoryMgr().allCategorise:
            categorys = self.GetSelectCategory()
            if len(categorys) > 0:
                self.categoryNum.setText("已选择{}个分类".format(len(categorys)))
            else:
                self.categoryNum.setText("")
            self.QueueLocalPage(self.BuildBookQuery(categorys), page)
        else:
            self.ClearLocalNum()
            sortId = sort[self.comboBox.currentIndex()]
            self.AddHttpTask(req.CategoriesSearchReq(page, self.categories, sortId), self.SendSearchBack)

    def SendSearchBack(self, raw):
        QtOwner().CloseLoading()
        try:
            data = json.loads(raw["data"])
            st = raw["st"]
            if st == Status.Ok:
                info = data.get("data").get("comics")
                self.ApplyPageResult(PageResult.from_remote(info), self.bookList.AddBookByDict)
                self.bookList.setFocus()
            else:
                # QtWidgets.QMessageBox.information(self, '未搜索到结果', "未搜索到结果", QtWidgets.QMessageBox.Yes)
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)
        finally:
            self.SetPageLoading(False)
        pass

    def ClearAndSendSearch(self):
        for k, box in self.allBox.items():
            if not box.isChecked():
                self.isSelectAll = False

        self.ResetSearch()
        if not self.categories:
            self.SendSearch(1)
        else:
            self.SendSearchCategories(1)

    def SendSearch(self, page):
        self.SetPageLoading(True)
        QtOwner().ShowLoading()
        categorys = self.GetSelectCategory()
        if len(categorys) > 0:
            self.categoryNum.setText("已选择{}个分类".format(len(categorys)))
        else:
            self.categoryNum.setText("")

        if self.isLocal:
            self.QueueLocalPage(self.BuildBookQuery(categorys), page)
        else:
            self.ClearLocalNum()
            self.lastText = "--1"
            sort = ["dd", "da", "ld", "vd"]
            sortId = sort[self.comboBox.currentIndex()]
            self.AddHttpTask(req.AdvancedSearchReq(page, categorys, self.text, sortId), self.SendSearchBack)

    def ClearLocalNum(self):
        for k, v in self.allBox.items():
            v.setText(k)
        return

    def SendLocalCategoryNumBack(self, nums, text):
        if text != self.lastText or not isinstance(nums, dict):
            return
        for k, v in nums.items():
            box = self.allBox.get(k)
            if not box:
                continue
            if not k:
                continue
            if int(v) > 0:
                box.setText("{}({})".format(k, v))
            else:
                box.setText("{}".format(k))
        return

    def SendLocalBack(self, books, page):
        if books is None:
            self.SetPageLoading(False)
            QtOwner().CloseLoading()
            QtOwner().ShowError(Str.GetStr(Str.Error))
            return
        self.ApplyPageResult(PageResult(books, page, self.bookList.pages), self.bookList.AddBookItemByDbBook)

    # def ClickCategoryListItem(self, item):
        # isClick = self.categoryList.ClickItem(item)
        # item = self.categoryList.itemFromIndex(index)
        # data = item.text()
        # if item.isSelected():
        #     QtOwner().ShowMsg(Str.GetStr(Str.Hidden) + data)
        # else:
        #     QtOwner().ShowMsg(Str.GetStr(Str.NotHidden) + data)
        # self.CheckCategoryShowItem()

    # def CheckCategoryShowItem(self):
    #     data = []
    #     for i in range(self.categoryList.count()):
    #         item = self.categoryList.item(i)
    #         if item.isSelected():
    #             widget = self.categoryList.itemWidget(item)
    #             data.append(widget.text())
    #     # data = self.categoryList.GetAllSelectItem()
    #     self.hiddenNum = 0
    #     for i in range(self.bookList.count()):
    #         item = self.bookList.item(i)
    #         widget = self.bookList.itemWidget(item)
    #         isHidden = False
    #         text = widget.categoryLabel.text()
    #         text2 = Converter('zh-hans').convert(text)
    #         for name in data:
    #             if name in text2:
    #                 self.hiddenNum += 1
    #                 item.setHidden(True)
    #                 isHidden = True
    #                 break
    #         if not isHidden:
    #             item.setHidden(False)
    #     if self.hiddenNum > 0:
    #         self.hideLabel.setText("已屏蔽{}个本子".format(self.hiddenNum))
    #     else:
    #         self.hideLabel.setText("")

    def JumpPage(self):
        page = self.spinBox.value()
        if self.bookList.isLoadingPage or not 1 <= page <= self.bookList.pages:
            return
        self.bookList.clear()
        if not self.categories:
            self.SendSearch(page)
        else:
            self.SendSearchCategories(page)
        return

    def LoadNextPage(self):
        if self.bookList.page >= self.bookList.pages:
            self.SetPageLoading(False)
            return
        if not self.categories:
            self.SendSearch(self.bookList.page + 1)
        else:
            self.SendSearchCategories(self.bookList.page + 1)
        return

    def ChangeSort(self, pos):
        self.ResetSearch()
        if not self.categories:
            self.SendSearch(1)
        else:
            self.SendSearchCategories(1)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                help = QHelpEvent(QEvent.Type.ToolTip, event.pos(), event.globalPos())
                QtOwner().app.postEvent(self.searchLabel, help)
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    # def OpenSearchCategories(self, categories):
    #     # self.setFocus()
    #     # self.bookList.clear()
    #     self.categories = categories
    #     self.searchEdit.setPlaceholderText(categories)
    #     self.bookList.UpdatePage(1, 1)
    #     self.bookList.UpdateState()
    #     self.SendSearchCategories(1)
