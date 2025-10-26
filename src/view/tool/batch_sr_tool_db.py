import json
import os.path

from PySide6.QtSql import QSqlDatabase, QSqlQuery
import sqlite3
from config.setting import Setting
from task.task_local import LocalData
from tools.log import Log


class BatchSrToolDb(object):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE", "batch_sr_tool")
        path = os.path.join(Setting.GetConfigPath(), "batch_sr_tool.db")
        self.db.setDatabaseName(path)
        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists batch_sr_item(id int primary key,\
            filename varchar,\
            path varchar,\
            addTime int,\
            tick varchar,\
            status int,\
            msg varchar\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

    def GetSaveStr(self, name):
        return name.replace("'", "''")

    def ClearBatchSrItem(self):
        query = QSqlQuery(self.db)
        sql = "delete from batch_sr_item where 1"
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())

    def AddBatchSrItem(self, info2):
        info = info2
        from view.tool.batch_sr_tool_view import BatchSrItem
        assert isinstance(info, BatchSrItem)
        query = QSqlQuery(self.db)
        sql = "INSERT INTO batch_sr_item(id, filename, path, addTime, tick, status, msg) " \
              "VALUES ({0}, '{1}', '{2}', {3}, '{4}', {5}, '{6}') " \
              "ON CONFLICT(id) DO UPDATE SET filename='{1}', path='{2}', addTime={3}, tick='{4}', status={5}, msg='{6}' ". \
            format(info.index, self.GetSaveStr(info.fileName), self.GetSaveStr(info.path)
                   , info.addTime, info.tick, info.status, info.msg)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def LoadBatchSrItem(self):
        query = QSqlQuery(self.db)
        sql = """
            select id, filename, path, addTime, tick, status, msg from batch_sr_item
            """

        from view.tool.batch_sr_tool_view import BatchSrItem
        suc = query.exec_(
            sql
        )
        if not suc:
            Log.Warn(query.lastError().text())
        downloads = {}
        while query.next():
            # bookId, downloadEpsIds, curDownloadEpsId, curConvertEpsId, title, savePath, convertPath
            info = BatchSrItem()
            info.index = query.value(0)
            info.fileName = query.value(1)
            info.path = query.value(2)
            info.addTime = query.value(3)
            info.tick = query.value(4)
            info.status = query.value(5)
            info.msg = query.value(6)

            downloads[info.index] = info

        return downloads