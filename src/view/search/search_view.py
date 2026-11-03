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
from tools.category import CateGoryMgr
from tools.langconv import Converter
from tools.str import Str
from server.book_mapping import book_from_comic
from server.book_query import BookQuery, SORT_FIELDS, RECOMMEND_SORT_FIELDS, order_books_by_ids, sort_books
from tools.page_result import PageRequest, PageResult
from tools.pagination import SEARCH_PAGE_SIZE


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
        self.isCanJump = True
        # 当前显示的推荐列表 (类型, bookId)，切换列表后丢弃旧请求的回包
        self.recommendSource = None
        # 推荐列表一次取完，按推荐顺序保存，本地分页和排序
        self.recommendIds = []
        self.recommendFound = {}
        self.recommendPending = 0
        self.recommendBooks = None
        self.recommendSortKey.hide()
        self.recommendSortKey.currentIndexChanged.connect(self.ChangeRecommendSort)

    def ResetSearch(self):
        self.recommendSource = None
        self.recommendBooks = None
        self.bookList.UpdatePage(1, 1)
        self.bookList.clear()
        self.spinBox.setMaximum(1)
        self.spinBox.setValue(1)
        self.label.setText(self.bookList.GetPageStr())

    def SetRecommendShow(self):
        # 推荐列表不走搜索接口，只显示本地分页和推荐排序
        self.label.show()
        self.spinBox.show()
        self.jumpPage.show()
        self.recommendSortKey.show()
        self.sortId.show()
        self.sortKey.hide()
        self.comboBox.hide()
        self.isCanJump = True

    def SetJumpShow(self, isShow):
        self.recommendSortKey.hide()
        if isShow:
            self.label.show()
            self.spinBox.show()
            self.jumpPage.show()
            if self.isLocal:
                self.sortId.show()
                self.sortKey.show()
                self.comboBox.hide()
            else:
                self.sortId.hide()
                self.sortKey.hide()
                self.comboBox.show()
            self.isCanJump = True
        else:
            self.label.hide()
            self.spinBox.hide()
            self.jumpPage.hide()
            self.sortId.hide()
            self.sortKey.hide()
            self.comboBox.hide()
            self.isCanJump = False

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

        if not QtOwner().IsCanUseDb():
            self.isLocal = False
            self.SetEnable(self.isLocal)

        isRecomend =  kwargs.get("recoment")
        if isRecomend == 1:
            bookId = kwargs.get("bookId")
            self.StartRecommend((1, bookId))
            self.AddHttpTask(req.GetComicsRecommendation(bookId), self.OpenRecommendationBack, bookId)
            return
        if isRecomend == 2:
            bookId = kwargs.get("bookId")
            self.StartRecommend((2, bookId))
            if bookId in self.cacheRecommend:
                self.OpenRecommendationBack2({"data": self.cacheRecommend[bookId]}, bookId)
                return
            # 有本地书库时一次取服务上限 100 个，本地分页；没有书库时每本都要单独请求，只取一页
            limit = 100 if QtOwner().IsCanUseDb() else SEARCH_PAGE_SIZE
            self.AddHttpTask(req.GetRecommendByIdReq(bookId, limit), self.OpenRecommendationBack2, bookId)
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
            if not QtOwner().IsCanUseDb():
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

    def OpenRecommendationBack(self, raw, bookId):
        source = (1, bookId)
        if self.recommendSource != source:
            return
        fallback = {}
        try:
            commentsData = json.loads(raw.get("data"))
            for v in commentsData.get("data").get("comics"):
                book = book_from_comic(v)
                fallback[book.id] = book
        except Exception as es:
            Log.Error(es)
        # 官方接口固定返回约 10 个；优先用本地书库的完整字段排序，没收录的直接用接口数据
        self.LoadRecommendBooks(source, list(fallback), fallback)

    def OpenRecommendationBack2(self, raw, bookId):
        source = (2, bookId)
        if self.recommendSource != source:
            return
        allBookIds = []
        try:
            commentsData = json.loads(raw.get("data"))
            allBookIds = list(commentsData.get("recommendations", []))
            # self.cacheRecommend[bookId] = data
        except Exception as es:
            Log.Error(es)
        self.LoadRecommendBooks(source, allBookIds, {})

    def StartRecommend(self, source):
        self.bookList.clear()
        self.recommendSource = source
        self.recommendIds = []
        self.recommendFound = {}
        self.recommendPending = 0
        self.recommendBooks = None
        self.recommendSortKey.blockSignals(True)
        self.recommendSortKey.setCurrentIndex(0)
        self.recommendSortKey.blockSignals(False)
        self.bookList.UpdatePage(1, 1)
        self.spinBox.setValue(1)
        self.spinBox.setMaximum(1)
        self.label.setText(self.bookList.GetPageStr())
        QtOwner().ShowLoading()

    def LoadRecommendBooks(self, source, bookIds, fallback):
        """bookIds 为推荐顺序；先查本地书库，缺的用 fallback 或网络补上，全部到齐后再显示。"""
        self.recommendIds = list(dict.fromkeys(bookIds))
        if self.recommendIds and QtOwner().IsCanUseDb():
            sql = SqlServer.GetBookByIds(self.recommendIds)
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, callBack=self.OpenLocalRecommendationBack, backParam=(source, fallback))
        else:
            self.FillRecommendBooks(source, self.recommendIds, fallback)

    def OpenLocalRecommendationBack(self, books, backParam):
        source, fallback = backParam
        if self.recommendSource != source:
            return
        # IN 查询不保证顺序；本地书库还没收录的新书单独补上，查询失败时全部补
        found, missing = order_books_by_ids(books or [], self.recommendIds)
        self.recommendFound = {book.id: book for book in found}
        self.FillRecommendBooks(source, missing, fallback)

    def FillRecommendBooks(self, source, bookIds, fallback):
        netIds = []
        for bookId in bookIds:
            if bookId in fallback:
                self.recommendFound[bookId] = fallback[bookId]
            else:
                netIds.append(bookId)
        self.recommendPending = len(netIds)
        for bookId in netIds:
            self.AddHttpTask(req.GetComicsBookReq(bookId), self.OpenRecommendationBack3, (source, bookId))
        if not netIds:
            self.FinishRecommendBooks()

    def OpenRecommendationBack3(self, raw, backParam):
        source, bookId = backParam
        if self.recommendSource != source:
            return
        try:
            if raw.get("st") == Str.Ok:
                data = json.loads(raw.get("data"))
                self.recommendFound[bookId] = book_from_comic(data.get('data').get("comic"))
        except Exception as es:
            Log.Error(es)
        self.recommendPending -= 1
        if self.recommendPending <= 0:
            self.FinishRecommendBooks()

    def FinishRecommendBooks(self):
        self.recommendBooks = [self.recommendFound[i] for i in self.recommendIds if i in self.recommendFound]
        self.bookList.clear()
        self.ShowRecommendPage(1)

    def ShowRecommendPage(self, page):
        if self.recommendBooks is None:
            return
        field = RECOMMEND_SORT_FIELDS[self.recommendSortKey.currentIndex()]
        books = sort_books(self.recommendBooks, field, self.sortId.currentIndex() == 0)
        request = PageRequest(page, SEARCH_PAGE_SIZE).clamp(len(books))
        items = books[request.offset:request.offset + request.page_size]
        self.ApplyPageResult(PageResult.from_total(items, request, len(books)), self.bookList.AddBookItemByDbBook)

    def ChangeRecommendSort(self, pos):
        if self.recommendBooks is None:
            return
        self.bookList.clear()
        self.ShowRecommendPage(1)

    def SendSearchCategories(self, page):
        sort = ["dd", "da", "ld", "vd"]
        self.SetPageLoading(True)
        QtOwner().ShowLoading()
        if QtOwner().IsCanUseDb() and self.categories in CateGoryMgr().allCategorise:
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
        if self.recommendBooks is not None:
            self.ShowRecommendPage(page)
            return
        if not self.categories:
            self.SendSearch(page)
        else:
            self.SendSearchCategories(page)
        return

    def LoadNextPage(self):
        if not self.isCanJump:
            return
        if self.bookList.page >= self.bookList.pages:
            self.SetPageLoading(False)
            return
        if self.recommendBooks is not None:
            self.ShowRecommendPage(self.bookList.page + 1)
            return
        if not self.categories:
            self.SendSearch(self.bookList.page + 1)
        else:
            self.SendSearchCategories(self.bookList.page + 1)
        return

    def ChangeSort(self, pos):
        if self.recommendSource is not None:
            # 推荐列表只在本地重排，不能触发搜索
            self.ChangeRecommendSort(pos)
            return
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
