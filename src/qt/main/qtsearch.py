from PySide2 import QtWidgets
import weakref

from PySide2.QtWidgets import QCheckBox, QLabel

from src.index.category import CateGoryMgr
from src.qt.com.qtlistwidget import QtBookList, QtIntLimit, QtCategoryList
from src.qt.main.qtsearch_db import QtSearchDb
from src.server import Server, req, Log, json
from ui.search import Ui_search


class QtSearch(QtWidgets.QWidget, Ui_search):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_search.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.index = 1
        self.data = ""
        self.bookList = QtBookList(self, self.__class__.__name__, owner)
        self.bookList.InitBook(self.LoadNextPage)

        self.bookLayout.addWidget(self.bookList)
        self.bookList.doubleClicked.connect(self.OpenSearch)
        self.categories = ""
        self.jumpLine.setValidator(QtIntLimit(1, 1, self))
        self.searchDb = QtSearchDb(owner)
        self.searchEdit.words = self.searchDb.InitWord()
        nums, times = self.searchDb.InitUpdateInfo()
        self.numsLabel.setText(str(nums))
        self.timesLabel.setText(times)
        self.categoryList = QtCategoryList(self)
        layouy = QtWidgets.QHBoxLayout()
        layouy.addWidget(QLabel("屏蔽："))
        layouy.addWidget(self.categoryList)
        self.bookLayout.addLayout(layouy, 1, 0)
        for name in ["耽美", "偽娘", "禁書", "扶她", "重口", "生肉", "純愛", "WEBTOON"]:
            self.categoryList.AddItem(name)
        self.categoryList.itemClicked.connect(self.ClickCategoryListItem)

        self.keywordList = QtCategoryList(self)
        layouy = QtWidgets.QHBoxLayout()
        layouy.addWidget(QLabel("大家都在搜："))
        layouy.addWidget(self.keywordList)
        self.bookLayout.addLayout(layouy, 2, 0)
        self.keywordList.itemClicked.connect(self.ClickKeywordListItem)

    def SwitchCurrent(self):
        pass

    def InitCheckBox(self):
        # TODO 分类标签有点问题 暂时不显示
        return
        size = len(CateGoryMgr().idToCateGoryBase)
        hBoxLayout = QtWidgets.QHBoxLayout(self)
        a = QCheckBox("全部分类", self.groupBox)
        hBoxLayout.addWidget(a)

        for index, info in enumerate(CateGoryMgr().idToCateGoryBase, 2):
            if index % 9 == 0:
                self.comboBoxLayout.addLayout(hBoxLayout)
                hBoxLayout = QtWidgets.QHBoxLayout(self)
            a = QCheckBox(info.title, self.groupBox)
            hBoxLayout.addWidget(a)
        self.comboBoxLayout.addLayout(hBoxLayout)
        return

    def Search(self, categories=None):
        if not self.searchEdit.listView.isHidden():
            currentIndex = self.searchEdit.listView.currentIndex()
            if currentIndex.isValid():
                self.searchEdit.completeText(currentIndex)
            self.searchEdit.listView.hide()
            return

        data = self.searchEdit.text()
        self.data = data
        if len(data) == len("5822a6e3ad7ede654696e482"):
            self.owner().bookInfoForm.OpenBook(data)
            return
        # if not data:
        #     return
        if not categories:
            self.categories = []
        else:
            pass
        self.categories = ""
        self.bookList.clear()
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.searchEdit.setPlaceholderText("")
        self.SendSearch(self.data, 1)

    def SetSearch(self):
        # self.localBox.setChecked(not self.localBox.isChecked())
        if self.localBox.isChecked():
            self.authorBox.setEnabled(True)
            self.desBox.setEnabled(True)
            self.tagsBox.setEnabled(True)
            self.categoryBox.setEnabled(True)
            self.titleBox.setEnabled(True)
            self.sortKey.setEnabled(True)
            self.sortId.setEnabled(True)
        else:
            self.authorBox.setEnabled(False)
            self.desBox.setEnabled(False)
            self.tagsBox.setEnabled(False)
            self.categoryBox.setEnabled(False)
            self.titleBox.setEnabled(False)
            self.sortKey.setEnabled(False)
            self.sortId.setEnabled(False)

    def SendSearch(self, data, page):
        self.index = 1
        self.searchEdit.listView.hide()
        if self.localBox.isChecked():
            books = self.searchDb.Search(data, self.titleBox.isChecked(), self.authorBox.isChecked(), self.desBox.isChecked(), self.tagsBox.isChecked(), self.categoryBox.isChecked(), page, self.sortKey.currentIndex(), self.sortId.currentIndex())
            self.SendLocalBack(books, page)
        else:
            self.owner().loadingForm.show()
            sort = ["dd", "da", "ld", "vd"]
            sortId = sort[self.comboBox.currentIndex()]
            self.owner().qtTask.AddHttpTask(lambda x: Server().Send(req.AdvancedSearchReq(page, [], data, sortId), bakParam=x), self.SendSearchBack)

    def SendLocalBack(self, books, page):
        self.owner().loadingForm.close()
        self.bookList.UpdateState()
        pages = 100
        self.bookList.UpdatePage(page, pages)
        self.jumpLine.setValidator(QtIntLimit(1, pages, self))
        pageText = "页：" + str(self.bookList.page) + "/" + str(self.bookList.pages)
        self.label.setText(pageText)
        for v in books:
            title = v.title2
            _id = v.id
            url = v.fileServer
            path = v.path
            originalName = v.originalName
            info2 = "完本," if v.finished else ""
            info2 += "{}E/{}P".format(str(v.epsCount), str(v.pages))
            param = v.categories
            self.bookList.AddBookItem(_id, title, info2, url, path, param)
        self.CheckCategoryShowItem()

    def OpenSearchCategories(self, categories):
        self.bookList.clear()
        self.categories = categories
        self.searchEdit.setPlaceholderText(categories)
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.SendSearchCategories(1)

    def SendSearchCategories(self, page):
        self.owner().loadingForm.show()
        # TODO 搜索和分类检索不太一样，切页时会有点问题
        sort = ["dd", "da", "ld", "vd"]
        sortId = sort[self.comboBox.currentIndex()]
        self.owner().qtTask.AddHttpTask(
            lambda x: Server().Send(req.CategoriesSearchReq(page, self.categories, sortId), bakParam=x),
            self.SendSearchBack)

    def InitKeyWord(self):
        self.owner().qtTask.AddHttpTask(
            lambda x: Server().Send(req.GetKeywords(), bakParam=x), self.SendKeywordBack)

    def SendSearchBack(self, raw):
        self.owner().loadingForm.close()
        try:
            self.bookList.UpdateState()
            data = json.loads(raw)
            if data.get("code") == 200:
                info = data.get("data").get("comics")
                page = int(info.get("page"))
                pages = int(info.get("pages"))
                self.bookList.UpdatePage(page, pages)
                self.jumpLine.setValidator(QtIntLimit(1, pages, self))
                pageText = "页：" + str(self.bookList.page) + "/" + str(self.bookList.pages)
                self.label.setText(pageText)
                for v in info.get("docs", []):
                    title = v.get("title", "")
                    _id = v.get("_id")
                    url = v.get("thumb", {}).get("fileServer")
                    path = v.get("thumb", {}).get("path")
                    originalName = v.get("thumb", {}).get("originalName")
                    info2 = "完本," if v.get("finished") else ""
                    info2 += "{}E/{}P".format(str(v.get("epsCount")), str(v.get("pagesCount")))
                    param = ",".join(v.get("categories"))
                    self.bookList.AddBookItem(_id, title, info2, url, path, param)
                self.CheckCategoryShowItem()
            else:
                # QtWidgets.QMessageBox.information(self, '未搜索到结果', "未搜索到结果", QtWidgets.QMessageBox.Yes)
                self.owner().msgForm.ShowError("未搜索到结果")
        except Exception as es:
            Log.Error(es)
        pass

    def SendKeywordBack(self, raw):
        try:
            data = json.loads(raw)
            if data.get("code") == 200:
                self.keywordList.clear()
                for keyword in data.get('data', {}).get("keywords", []):
                    self.keywordList.AddItem(keyword)
                pass
            else:
                pass
        except Exception as es:
            Log.Error(es)
        pass

    def OpenSearch(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList.item(index)
        if not item:
            return
        widget = self.bookList.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        self.owner().bookInfoForm.OpenBook(bookId)

    def JumpPage(self):
        page = int(self.jumpLine.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        if not self.categories:
            self.SendSearch(self.data, page)
        else:
            self.SendSearchCategories(page)
        return

    def LoadNextPage(self):
        if not self.categories:
            self.SendSearch(self.data, self.bookList.page + 1)
        else:
            self.SendSearchCategories(self.bookList.page + 1)
        return

    def ChangeSort(self, pos):
        self.bookList.page = 1
        self.bookList.clear()
        if not self.categories:
            self.SendSearch(self.data, 1)
        else:
            self.SendSearchCategories(1)

    def ClickCategoryListItem(self, item):
        isClick = self.categoryList.ClickItem(item)
        data = item.text()
        if isClick:
            self.owner().msgForm.ShowMsg("屏蔽" + data)
        else:
            self.owner().msgForm.ShowMsg("取消屏蔽" + data)
        self.CheckCategoryShowItem()

    def CheckCategoryShowItem(self):
        data = self.categoryList.GetAllSelectItem()
        for i in range(self.bookList.count()):
            item = self.bookList.item(i)
            widget = self.bookList.itemWidget(item)
            isHidden = False
            for name in data:
                if name in widget.param:
                    item.setHidden(True)
                    isHidden = True
                    break
            if not isHidden:
                item.setHidden(False)

    def ClickKeywordListItem(self, item):
        data = item.text()
        self.searchEdit.setText(data)
        self.Search()

    def focusOutEvent(self, ev):
        self.searchEdit.listView.hide()
        return super(self.__class__, self).focusOutEvent(ev)