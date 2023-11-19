import os
import time

from PySide6 import QtWidgets
from PySide6.QtSql import QSqlDatabase, QSqlQuery

from config.setting import Setting
from interface.ui_history import Ui_History
from tools.log import Log
from tools.str import Str


class QtHistoryData(object):
    def __init__(self):
        self.bookId = ""         # bookId
        self.name = ""           # name
        self.epsId = 0           # 章节Id
        self.picIndex = 0           # 图片Index
        self.url = ""
        self.path = ""
        self.tick = 0


class HistoryView(QtWidgets.QWidget, Ui_History):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_History.__init__(self)
        self.setupUi(self)

        # self.bookList.InitBook(self.LoadNextPage)
        self.pageNums = 20
        self.bookList.LoadCallBack = self.LoadNextPage
        self.history = {}
        self.db = QSqlDatabase.addDatabase("QSQLITE", "history")
        path = os.path.join(Setting.GetConfigPath(), "history.db")
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

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh:
            self.bookList.clear()
            self.bookList.page = 1
            self.bookList.pages = len(self.history) // self.pageNums + 1
            self.spinBox.setValue(1)
            self.spinBox.setMaximum(self.pageNums)
            self.bookList.UpdateState()
            self.UpdatePageLabel()
            self.RefreshData(self.bookList.page)

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
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData(page)
        self.UpdatePageLabel()

    def LoadNextPage(self):
        self.bookList.page += 1
        self.RefreshData(self.bookList.page)
        self.UpdatePageLabel()

    def RefreshData(self, page):
        sortedList = list(self.history.values())
        sortedList.sort(key=lambda a: a.tick, reverse=True)
        self.bookList.UpdateState()
        start = (page-1) * self.pageNums
        end = start + self.pageNums
        for info in sortedList[start:end]:
            self.bookList.AddBookItemByHistory(info)

    def UpdatePageLabel(self):
        self.pages.setText(Str.GetStr(Str.Page)+"：{}/{}".format(str(self.bookList.page), str(self.bookList.pages)))

    def DelCallBack(self, bookId):
        if bookId not in self.history:
            return
        self.history.pop(bookId)
        self.DelHistory(bookId)
        self.bookList.DelBookID(bookId)

        #
        # page = 1
        # self.bookList.page = page
        # self.bookList.clear()
        # self.RefreshData(page)
        # self.UpdatePageLabel()
        return
