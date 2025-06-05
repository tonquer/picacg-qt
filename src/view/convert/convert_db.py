import json
import os.path
import time

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from config.setting import Setting
from tools.log import Log
from view.convert.convert_item import ConvertItem
from view.download.download_item import DownloadItem, DownloadEpsItem


class ConvertDb(object):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE", "convert")
        path = os.path.join(Setting.GetConfigPath(), "convert.db")
        self.db.setDatabaseName(path)
        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)

        sql = """\
            create table if not exists convert(\
            id varchar primary key,\
            title varchar,\
            file varchar,\
            path varchar,\
            cur_eps_id int, \
            cur_index int, \
            status int,\
            eps_list varchar,\
            params varchar \
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

    def DelConvertDB(self, bookId):
        query = QSqlQuery(self.db)
        sql = "delete from convert where id='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def AddConvertDB(self, task):
        assert isinstance(task, ConvertItem)
        tick = int(time.time())
        query = QSqlQuery(self.db)
        sql = "INSERT INTO convert(id,title,file,path,cur_eps_id,cur_index,status,eps_list,params) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', {4}, {5}, {6}, '{7}', '{8)' " \
              "ON CONFLICT(id) DO UPDATE SET downloadEpsIds='{1}', curDownloadEpsId={2}, curConvertEpsId={3}, " \
              "title = '{4}', savePath = '{5}', convertPath= '{6}', status = '{7}', convertStatus = '{8}'".\
            format(task.bookId, json.dumps(task.epsIds), task.curDownloadEpsId, task.curConvertEpsId, task.title.replace("'", "''"),
                   task.savePath.replace("'", "''"), task.convertPath.replace("'", "''"), task.status, task.convertStatus, tick)

        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def LoadConvert(self, owner):
        query = QSqlQuery(self.db)
        suc = query.exec_(
            """
            select id,title,file,path,cur_eps_id,cur_index,status,eps_list,params from download
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

        return downloads
