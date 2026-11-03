import os
import time
from datetime import datetime

from PySide6 import QtWidgets
from PySide6.QtSql import QSqlDatabase, QSqlQuery

from config.setting import Setting
from interface.ui_history import Ui_History
from qt_owner import QtOwner
from server.book_query import SORT_FIELDS
from server.sql_server import SqlServer
from task.qt_task import QtTaskBase
from tools.langconv import Converter
from tools.log import Log
from tools.str import Str
from tools.pagination import HISTORY_PAGE_SIZE, page_count
from tools.page_result import PageRequest, PageResult


class QtHistoryData(object):
    def __init__(self):
        self.bookId = ""         # bookId
        self.name = ""           # name
        self.epsId = 0           # 章节Id
        self.picIndex = 0           # 图片Index
        self.url = ""
        self.path = ""
        self.tick = 0


# 最近阅读 + 与本地搜索相同的书库字段
HISTORY_SORT_FIELDS = ("tick",) + SORT_FIELDS[:6]
DATE_SORT_FIELDS = ("updated_at", "created_at")
_toSimple = None


def iso_to_tick(text):
    """书库时间形如 2026-11-01T16:15:06.796Z。"""
    if not text or not isinstance(text, str):
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return int(datetime.strptime(text, fmt).timestamp())
        except ValueError:
            continue
    return None


def history_has_update(history, info):
    """上次阅读之后，书库中这本书又更新过。"""
    tick = iso_to_tick(info.updated_at) if info else None
    return tick is not None and tick > (history.tick or 0)


def normalize_title(text):
    global _toSimple
    if _toSimple is None:
        _toSimple = Converter('zh-hans')
    return _toSimple.convert(text or "").replace(" ", "").lower()


def history_show_title(history, info):
    """书库标题经过简体化（日文汉字也被转换），与历史标题是同一本书时保留原标题；
    不一致（历史写错了标题，或已改名）时以书库为准。"""
    if not info or not info.title or normalize_title(history.name) == normalize_title(info.title):
        return history.name
    return info.title


def filter_and_sort_history(histories, infos, field="tick", descending=True, text="", onlyUpdate=False):
    """infos 为 bookId -> 本地书库中的书；书库中缺少排序字段的书排在最后。"""
    items = sorted(histories, key=lambda h: h.bookId)
    items.sort(key=lambda h: h.tick or 0, reverse=True)
    if text:
        key = normalize_title(text)

        def match(h):
            info = infos.get(h.bookId)
            titles = [h.name] + ([info.title, info.title2] if info else [])
            return any(key in normalize_title(title) for title in titles)

        items = [h for h in items if match(h)]
    if onlyUpdate:
        items = [h for h in items if history_has_update(h, infos.get(h.bookId))]
    if field == "tick":
        return items if descending else items[::-1]

    def value(h):
        v = getattr(infos.get(h.bookId), field, None)
        if field in DATE_SORT_FIELDS:
            return str(v)[:19] if v else None
        try:
            return int(v)
        except (TypeError, ValueError):
            return None

    present = [h for h in items if value(h) is not None]
    absent = [h for h in items if value(h) is None]
    return sorted(present, key=value, reverse=descending) + absent


class HistoryView(QtWidgets.QWidget, Ui_History, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_History.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)

        # self.bookList.InitBook(self.LoadNextPage)
        self.pageNums = HISTORY_PAGE_SIZE
        self.bookList.isHistory = True
        self.bookList.LoadCallBack = self.LoadNextPage
        self.bookList.BatchDelCallBack = self.BatchDelCallBack
        self.history = {}
        self.db = QSqlDatabase.addDatabase("QSQLITE", "history")
        path = os.path.join(Setting.GetStatePath(), "history.db")
        self.db.setDatabaseName(path)
        # self.bookList.InstallDel()

        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists history(\
            bookId varchar primary key,\
            name varchar,\
            epsId int, \
            picIndex int,\
            url varchar,\
            path varchar,\
            tick int\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
        self.LoadHistory()
        self.bookList.isDelMenu = True
        self.bookList.DelCallBack = self.DelCallBack

        # bookId -> 本地书库中的书，用于排序、筛选，并以书库为准显示标题和封面
        self.bookInfos = {}
        self.updateCheckText = self.updateCheck.text()
        self.sortKey.currentIndexChanged.connect(self.ChangeFilter)
        self.sortId.currentIndexChanged.connect(self.ChangeFilter)
        self.updateCheck.toggled.connect(self.ChangeFilter)
        self.searchEdit.textChanged.connect(self.ChangeFilter)

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh:
            self.bookList.clear()
            self.bookList.page = 1
            self.bookList.pages = page_count(len(self.history), self.pageNums)
            self.spinBox.setMaximum(self.bookList.pages)
            self.spinBox.setValue(1)
            self.bookList.UpdateState()
            self.UpdatePageLabel()
            if self.history and QtOwner().IsCanUseDb():
                sql = SqlServer.GetBookByIds(list(self.history))
                self.AddSqlTask("book", sql, SqlServer.TaskTypeSelectBook, callBack=self.LoadBookInfosBack)
                return
            self.RefreshData(self.bookList.page)

    def LoadBookInfosBack(self, books):
        self.bookInfos = {book.id: book for book in books or []}
        num = sum(1 for h in self.history.values() if history_has_update(h, self.bookInfos.get(h.bookId)))
        self.updateCheck.setText("{}({})".format(self.updateCheckText, num))
        self.bookList.clear()
        self.RefreshData(1)

    def ChangeFilter(self, *args):
        self.bookList.clear()
        self.RefreshData(1)

    def GetShowList(self):
        return filter_and_sort_history(self.history.values(), self.bookInfos,
                                       HISTORY_SORT_FIELDS[self.sortKey.currentIndex()],
                                       self.sortId.currentIndex() == 0,
                                       self.searchEdit.text().strip(), self.updateCheck.isChecked())

    def GetHistory(self, bookId):
        return self.history.get(bookId)

    def DelHistory(self, bookId):
        query = QSqlQuery(self.db)
        sql = "delete from history where bookId='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def AddHistory(self, bookId, name, epsId, index, url, path):
        tick = int(time.time())
        info = self.history.get(bookId)
        if not info:
            info = QtHistoryData()
            self.history[bookId] = info
        info.bookId = bookId
        info.name = name
        info.epsId = epsId
        info.picIndex = index
        info.url = url
        info.path = path
        info.tick = tick

        query = QSqlQuery(self.db)

        sql = "INSERT INTO history(bookId, name, epsId, picIndex, url, path, tick) " \
              "VALUES ('{0}', '{1}', {2}, {3}, '{4}', '{5}', {6}) " \
              "ON CONFLICT(bookId) DO UPDATE SET name='{1}', epsId={2}, picIndex={3}, url = '{4}', path='{5}', tick={6}".\
            format(bookId, name.replace("'", "''"), epsId, index, url, path, tick)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def LoadHistory(self):
        query = QSqlQuery(self.db)
        query.exec_(
            """
            select * from history
            """
        )
        while query.next():
            # bookId, name, epsId, index, url, path
            info = QtHistoryData()
            info.bookId = query.value(0)
            info.name = query.value(1)
            info.epsId = query.value(2)
            info.picIndex = query.value(3)
            info.url = query.value(4)
            info.path = query.value(5)
            info.tick = query.value(6)
            self.history[info.bookId] = info
        pass

    def JumpPage(self):
        page = self.spinBox.value()
        if not 1 <= page <= self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData(page)
        self.UpdatePageLabel()

    def LoadNextPage(self):
        if self.bookList.page >= self.bookList.pages:
            self.bookList.UpdateState()
            return
        self.RefreshData(self.bookList.page + 1)
        self.UpdatePageLabel()

    def RefreshData(self, page):
        sortedList = self.GetShowList()
        request = PageRequest(page, self.pageNums).clamp(len(sortedList))
        items = sortedList[request.offset:request.offset + request.page_size]
        result = PageResult.from_total(items, request, len(sortedList))
        self.bookList.UpdatePage(result.page, result.pages)
        self.bookList.UpdateState(True)
        self.spinBox.setMaximum(result.pages)
        self.spinBox.setValue(result.page)
        self.nums.setText("{}：{} ".format(Str.GetStr(Str.HistoryNum), result.total))
        for info in result.items:
            book = self.bookInfos.get(info.bookId)
            self.bookList.AddBookItemByHistory(info, book, history_show_title(info, book))
        self.bookList.UpdateState()
        self.UpdatePageLabel()

    def UpdatePageLabel(self):
        self.pages.setText(Str.GetStr(Str.Page)+"：{}/{}".format(str(self.bookList.page), str(self.bookList.pages)))

    def BatchDelCallBack(self, bookIds):
        for bookId in bookIds:
            self.history.pop(bookId, None)
            self.DelHistory(bookId)
        self.ReloadCurrentPage()

    def DelCallBack(self, bookId):
        if bookId not in self.history:
            return
        self.history.pop(bookId)
        self.DelHistory(bookId)
        self.ReloadCurrentPage()

        #
        # page = 1
        # self.bookList.page = page
        # self.bookList.clear()
        # self.RefreshData(page)
        # self.UpdatePageLabel()
        return

    def ReloadCurrentPage(self):
        page = self.bookList.page
        self.bookList.clear()
        self.RefreshData(page)
