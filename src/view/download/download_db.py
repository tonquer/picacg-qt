import json
import os.path
import time

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from config.setting import Setting
from tools.log import Log
from view.download.download_item import DownloadItem, DownloadEpsItem


class DownloadDb(object):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE", "download")
        path = os.path.join(Setting.GetConfigPath(), "download.db")
        self.db.setDatabaseName(path)
        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists download(\
            bookId varchar primary key,\
            downloadEpsIds varchar,\
            curDownloadEpsId int,\
            curConvertEpsId int,\
            tick int,\
            title varchar,\
            savePath varchar,\
            convertPath varchar,\
            status varchar,\
            convertStatus varchar\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

        query = QSqlQuery(self.db)
        sql = """ALTER TABLE 'download' ADD 'tick' int DEFAULT 1683388800;"""
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists download_eps(\
            bookId varchar,\
            epsId int,\
            epsTitle varchar,\
            picCnt int,\
            curPreDownloadIndex int,\
            curPreConvertId int,\
            primary key (bookId,epsId)\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
        # self.LoadDownload()

    def DelDownloadDB(self, bookId):
        query = QSqlQuery(self.db)
        sql = "delete from download where bookId='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())

        sql = "delete from download_eps where bookId='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def AddDownloadDB(self, task):
        assert isinstance(task, DownloadItem)
        tick = int(time.time())
        query = QSqlQuery(self.db)
        sql = "INSERT INTO download(bookId, downloadEpsIds, curDownloadEpsId, curConvertEpsId, title, " \
              "savePath, convertPath, status, convertStatus, tick) " \
              "VALUES ('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}', '{7}', '{8}', {9}) " \
              "ON CONFLICT(bookId) DO UPDATE SET downloadEpsIds='{1}', curDownloadEpsId={2}, curConvertEpsId={3}, " \
              "title = '{4}', savePath = '{5}', convertPath= '{6}', status = '{7}', convertStatus = '{8}'".\
            format(task.bookId, json.dumps(task.epsIds), task.curDownloadEpsId, task.curConvertEpsId, task.title.replace("'", "''"),
                   task.savePath.replace("'", "''"), task.convertPath.replace("'", "''"), task.status, task.convertStatus, tick)

        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def AddDownloadEpsDB(self, info):
        assert isinstance(info, DownloadEpsItem)
        query = QSqlQuery(self.db)
        sql = "INSERT INTO download_eps(bookId, epsId, epsTitle, picCnt, curPreDownloadIndex, curPreConvertId) " \
              "VALUES ('{0}', {1}, '{2}', {3}, {4}, {5}) " \
              "ON CONFLICT(bookId, epsId) DO UPDATE SET epsTitle='{2}', picCnt={3}, curPreDownloadIndex={4}, " \
              "curPreConvertId = {5}".\
            format(info.bookId, info.epsId, info.epsTitle.replace("'", "''"), info.picCnt, info.curPreDownloadIndex,
                   info.curPreConvertId)

        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def LoadDownload(self, owner):
        query = QSqlQuery(self.db)
        suc = query.exec_(
            """
            select bookId,downloadEpsIds,curDownloadEpsId,curConvertEpsId,title,savePath,convertPath,status,convertStatus,tick  from download
            """
        )
        if not suc:
            Log.Warn(query.lastError().text())
        downloads = {}
        while query.next():
            # bookId, downloadEpsIds, curDownloadEpsId, curConvertEpsId, title, savePath, convertPath
            info = DownloadItem()
            info.bookId = query.value(0)
            data = json.loads(query.value(1))
            info.epsIds = [int(i) for i in data]
            info.curDownloadEpsId = query.value(2)
            info.curConvertEpsId = query.value(3)
            info.title = query.value(4)
            info.savePath = query.value(5)
            info.convertPath = query.value(6)
            info.status = query.value(7)
            info.convertStatus = query.value(8)
            info.tick = query.value(9)
            downloads[info.bookId] = info

        query = QSqlQuery(self.db)
        suc = query.exec_(
            """
            select * from download_eps
            """
        )
        if not suc:
            Log.Warn(query.lastError().text())
        while query.next():
            # bookId, epsId, epsTitle, picCnt, curPreDownloadIndex, curPreConvertId

            bookId = query.value(0)
            task = downloads.get(bookId)
            if not task:
                continue
            info = DownloadEpsItem()
            info.bookId = bookId
            info.epsId = query.value(1)
            info.epsTitle = query.value(2)
            info.picCnt = query.value(3)
            info.curPreDownloadIndex = query.value(4)
            info.curPreConvertId = query.value(5)
            task.epsInfo[info.epsId] = info

        return downloads
