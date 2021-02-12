from PyQt5 import QtWidgets, QtGui
import weakref

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QCheckBox, QGroupBox, QAbstractSlider

from src.index.category import CateGoryMgr
from src.qt.qtlistwidget import QtBookList, QtIntLimit
from src.server import Server, req, Log, json, Status
from ui.search import Ui_search


class QtSearch(QtWidgets.QWidget, Ui_search):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_search.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.index = 1
        self.data = ""
        self.bookList = QtBookList(self, self.__class__.__name__)
        self.bookList.InitBook(self.LoadNextPage)

        self.bookLayout.addWidget(self.bookList)
        self.bookList.doubleClicked.connect(self.OpenSearch)
        self.categories = ""
        self.jumpLine.setValidator(QtIntLimit(1, 1, self))

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
        data = self.searchEdit.text()
        self.data = data
        if not data:
            return
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

    def SendSearch(self, data, page):
        self.owner().loadingForm.show()
        self.index = 1
        sort = ["dd", "da", "ld", "vd"]
        sortId = sort[self.comboBox.currentIndex()]
        self.owner().qtTask.AddHttpTask(lambda x: Server().Send(req.AdvancedSearchReq(page, [], data, sortId), bakParam=x), self.SendSearchBack)

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
                    self.bookList.AddBookItem(_id, title, info2, url, path, originalName)

            else:
                # QtWidgets.QMessageBox.information(self, '未搜索到结果', "未搜索到结果", QtWidgets.QMessageBox.Yes)
                self.owner().msgForm.ShowError("未搜索到结果")
        except Exception as es:
            import sys
            cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
            e = sys.exc_info()[1]
            Log.Error(cur_tb, e)
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