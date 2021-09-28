from PySide2 import QtWidgets
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QCheckBox

from src.index.category import CateGoryMgr
from src.qt.com.langconv import Converter
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req, Log, json
from src.server.sql_server import SqlServer
from ui.search import Ui_search


class QtSearch(QtWidgets.QWidget, Ui_search, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_search.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.index = 1
        self.data = ""
        self.bookList.InitBook(self.LoadNextPage)

        ## self.bookList.doubleClicked.connect(self.OpenSearch)
        self.categories = ""
        self.searchEdit.words = []
        self.InitWord()

        self.UpdateDbInfo()
        self.categoryList.itemClicked.connect(self.ClickCategoryListItem)

        self.keywordList.itemClicked.connect(self.ClickKeywordListItem)
        self.SetSearch()
        # self.sucLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.allCategorise = [
                    "嗶咔漢化",
                    "全彩",
                    "長篇",
                    "同人",
                    "短篇",
                    "圓神領域",
                    "碧藍幻想",
                    "CG雜圖",
                    "英語 ENG",
                    "生肉",
                    "純愛",
                    "百合花園",
                    "耽美花園",
                    "偽娘哲學",
                    "後宮閃光",
                    "扶他樂園",
                    "單行本",
                    "姐姐系",
                    "妹妹系",
                    "SM",
                    "性轉換",
                    "足の恋",
                    "人妻",
                    "NTR",
                    "強暴",
                    "非人類",
                    "艦隊收藏",
                    "Love Live",
                    "SAO 刀劍神域",
                    "Fate",
                    "東方",
                    "WEBTOON",
                    "禁書目錄",
                    "歐美",
                    "Cosplay",
                    "重口地帶",
        ]

    def UpdateDbInfo(self):
        self.AddSqlTask("book", "", SqlServer.TaskTypeSelectUpdate, self.UpdateDbInfoBack)

    def UpdateDbInfoBack(self, data):
        nums, times, _ = data
        self.numsLabel.setText(str(nums))
        self.timesLabel.setText(times)
        return

    def InitWord(self):
        self.AddSqlTask("book", "", SqlServer.TaskTypeSelectWord, self.InitWordBack)
        return

    def InitWordBack(self, data):
        self.searchEdit.words = data

    def InitCategoryList(self):
        self.categoryList.clear()
        if not self.localBox.isChecked():
            for name in ["耽美", "偽娘", "禁書", "扶她", "重口", "生肉", "純愛", "WEBTOON"]:
                self.categoryList.AddItem(name)
        else:
            for name in ["耽美", "伪娘", "禁书", "扶她", "重口", "生肉", "纯爱", "WEBTOON"]:
                self.categoryList.AddItem(name)

    def InitKeywordTranslate(self):
        if not self.localBox.isChecked():
            self.InitKeyWord()
        else:
            for i in range(self.keywordList.count()):
                item = self.keywordList.item(i)
                item.setText(Converter('zh-hans').convert(item.text()).replace("'", "\""))

    def SwitchCurrent(self):
        self.InitKeywordTranslate()
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

    def Search2(self, text):
        self.setFocus()
        QtOwner().owner.userForm.toolButton1.click()

        if self.localBox.isChecked():
            self.searchEdit.setText(text)
        else:
            self.searchEdit.setText(text)
        self.searchEdit.listView.hide()
        self.Search()
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
            QtOwner().owner.bookInfoForm.OpenBook(data)
            return
        # if not data:
        #     return
        if not categories:
            self.categories = []
        else:
            pass
        self.categories = ""
        self.bookList.clear()
        self.bookList.update()
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.searchEdit.setPlaceholderText("")
        self.SendSearch(self.data, 1)

    def SetSearch(self):
        # self.localBox.setChecked(not self.localBox.isChecked())
        self.InitCategoryList()
        self.InitKeywordTranslate()
        if self.localBox.isChecked():
            self.authorBox.setEnabled(True)
            self.desBox.setEnabled(True)
            self.tagsBox.setEnabled(True)
            self.categoryBox.setEnabled(True)
            self.titleBox.setEnabled(True)
            self.sortKey.setEnabled(True)
            self.sortId.setEnabled(True)
            self.comboBox.setEnabled(False)
            self.creatorBox.setEnabled(True)
        else:
            self.authorBox.setEnabled(False)
            self.desBox.setEnabled(False)
            self.tagsBox.setEnabled(False)
            self.categoryBox.setEnabled(False)
            self.titleBox.setEnabled(False)
            self.sortKey.setEnabled(False)
            self.sortId.setEnabled(False)
            self.comboBox.setEnabled(True)
            self.creatorBox.setEnabled(False)

    def SendSearch(self, data, page):
        self.index = 1
        self.searchEdit.listView.hide()
        if self.localBox.isChecked():
            QtOwner().owner.loadingForm.show()
            sql = SqlServer.Search(data, self.titleBox.isChecked(), self.authorBox.isChecked(), self.desBox.isChecked(), self.tagsBox.isChecked(), self.categoryBox.isChecked(), self.creatorBox.isChecked(), page, self.sortKey.currentIndex(), self.sortId.currentIndex())
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, callBack=self.SendLocalBack, backParam=page)
        else:
            QtOwner().owner.loadingForm.show()
            sort = ["dd", "da", "ld", "vd"]
            sortId = sort[self.comboBox.currentIndex()]
            self.AddHttpTask(req.AdvancedSearchReq(page, [], data, sortId), self.SendSearchBack)

    def SendLocalBack(self, books, page):
        QtOwner().owner.loadingForm.close()
        self.bookList.UpdateState()
        pages = 100
        self.bookList.UpdatePage(page, pages)
        # self.jumpLine.setValidator(QtIntLimit(1, pages, self))
        self.spinBox.setValue(page)
        self.spinBox.setMaximum(pages)
        pageText = "页：" + str(self.bookList.page) + "/" + str(self.bookList.pages)
        self.label.setText(pageText)
        for v in books:
            self.bookList.AddBookItem(v)
        self.CheckCategoryShowItem()
        self.bookList.update()

    def OpenSearchCategories(self, categories):
        self.setFocus()
        self.bookList.clear()
        self.categories = categories
        self.searchEdit.setPlaceholderText(categories)
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.SendSearchCategories(1)

    def SendSearchCategories(self, page):
        QtOwner().owner.loadingForm.show()
        # TODO 搜索和分类检索不太一样，切页时会有点问题
        sort = ["dd", "da", "ld", "vd"]
        sortId = sort[self.comboBox.currentIndex()]
        if self.localBox.isChecked() and self.categories in self.allCategorise:
            QtOwner().owner.loadingForm.show()
            sql = SqlServer.Search(self.categories, False, False, False, False, True, False, page, self.sortKey.currentIndex(), self.sortId.currentIndex())
            self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, callBack=self.SendLocalBack, backParam=page)
        else:
            self.AddHttpTask(req.CategoriesSearchReq(page, self.categories, sortId), self.SendSearchBack)

    def SearchAutor(self, text):
        self.titleBox.setChecked(False)
        self.authorBox.setChecked(True)
        self.desBox.setChecked(False)
        self.tagsBox.setChecked(False)
        self.categoryBox.setChecked(False)
        self.creatorBox.setChecked(False)
        self.Search2(text)

    def SearchTags(self, text):
        self.titleBox.setChecked(False)
        self.authorBox.setChecked(False)
        self.desBox.setChecked(False)
        self.tagsBox.setChecked(True)
        self.categoryBox.setChecked(False)
        self.creatorBox.setChecked(False)
        self.Search2(text)

    def SearchCategories(self, text):
        self.titleBox.setChecked(True)
        self.authorBox.setChecked(True)
        self.desBox.setChecked(True)
        self.tagsBox.setChecked(True)
        self.categoryBox.setChecked(True)
        self.creatorBox.setChecked(False)
        self.searchEdit.setText("")
        self.OpenSearchCategories(text)

    def SearchCreator(self, creator):
        self.titleBox.setChecked(False)
        self.authorBox.setChecked(False)
        self.desBox.setChecked(False)
        self.tagsBox.setChecked(False)
        self.categoryBox.setChecked(False)
        self.creatorBox.setChecked(True)
        self.Search2(creator)

    def InitKeyWord(self):
        self.AddHttpTask(req.GetKeywords(), self.SendKeywordBack)

    def SendSearchBack(self, raw):
        QtOwner().owner.loadingForm.close()
        try:
            self.bookList.UpdateState()
            data = json.loads(raw)
            if data.get("code") == 200:
                info = data.get("data").get("comics")
                page = int(info.get("page"))
                pages = int(info.get("pages"))
                self.bookList.UpdatePage(page, pages)
                # self.jumpLine.setValidator(QtIntLimit(1, pages, self))
                self.spinBox.setValue(page)
                self.spinBox.setMaximum(pages)
                pageText = "页：" + str(self.bookList.page) + "/" + str(self.bookList.pages)
                self.label.setText(pageText)
                for v in info.get("docs", []):
                    self.bookList.AddBookItem(v)
                self.CheckCategoryShowItem()
            else:
                # QtWidgets.QMessageBox.information(self, '未搜索到结果', "未搜索到结果", QtWidgets.QMessageBox.Yes)
                QtOwner().owner.msgForm.ShowError(self.tr("未搜索到结果"))
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
        QtOwner().owner.bookInfoForm.OpenBook(bookId)

    def JumpPage(self):
        page = int(self.spinBox.text())
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
            QtOwner().owner.msgForm.ShowMsg(self.tr("屏蔽") + data)
        else:
            QtOwner().owner.msgForm.ShowMsg(self.tr("取消屏蔽") + data)
        self.CheckCategoryShowItem()

    def CheckCategoryShowItem(self):
        data = self.categoryList.GetAllSelectItem()
        for i in range(self.bookList.count()):
            item = self.bookList.item(i)
            widget = self.bookList.itemWidget(item)
            isHidden = False
            for name in data:
                if name in widget.leftLabel1.text():
                    item.setHidden(True)
                    isHidden = True
                    break
            if not isHidden:
                item.setHidden(False)

    def ClickKeywordListItem(self, item):
        self.titleBox.setChecked(True)
        self.authorBox.setChecked(True)
        self.desBox.setChecked(True)
        self.tagsBox.setChecked(True)
        self.categoryBox.setChecked(True)
        self.creatorBox.setChecked(False)
        self.Search2(item.text())

    def focusOutEvent(self, ev):
        self.searchEdit.listView.hide()
        return super(self.__class__, self).focusOutEvent(ev)

    def Update(self):
        QtOwner().owner.InitUpdateDatabase()

    def SetUpdateText(self, text, color, enable):
        self.sucLabel.setText(text)
        self.sucLabel.setStyleSheet("background-color:transparent;color:{}".format(color))
        self.sucLabel.setEnabled(enable)
        if enable:
            self.sucLabel.setCursor(Qt.PointingHandCursor)
        else:
            self.sucLabel.setCursor(Qt.ArrowCursor)