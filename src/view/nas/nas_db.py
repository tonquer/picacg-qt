import json
import os.path
import time

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from config.setting import Setting
from tools.log import Log
from view.download.download_item import DownloadItem, DownloadEpsItem
from view.nas.nas_item import NasUploadItem, NasInfoItem


class NasDb(object):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE", "nas")
        path = os.path.join(Setting.GetConfigPath(), "nas.db")
        self.db.setDatabaseName(path)
        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists nas_info(\
            nas_id int primary key,\
            title varchar ,\
            address varchar,\
            port int, \
            type int ,\
            user varchar ,\
            passwd varchar ,\
            compress_index int,\
            save_index int,\
            dir_index int,\
            is_waifu2x int,\
            path varchar ,\
            tick int \
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists nas_upload(\
            book_id varchar ,\
            title varchar,\
            nas_id int,\
            eps_ids varchar, \
            curPreUpIndex int,\
            tick int, \
            status int ,\
            status_msg int ,\
            primary key (book_id,nas_id)\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
        # self.LoadDownload()

    def DelUploadDB(self, nas_id, book_id):
        query = QSqlQuery(self.db)
        sql = "delete from nas_upload where nas_id='{}' and book_id='{}'".format(nas_id, book_id)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())

        return

    def AddUploadDB(self, task):
        assert isinstance(task, NasUploadItem)
        tick = int(time.time())
        query = QSqlQuery(self.db)
        sql = "INSERT INTO nas_upload(nas_id, book_id, eps_ids, title, " \
              "curPreUpIndex, tick, status, status_msg) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6}, {7}) " \
              "ON CONFLICT(nas_id, book_id) DO UPDATE SET eps_ids='{2}', title='{3}', curPreUpIndex={4}, " \
              "tick = {5}, status = {6}, status_msg= {7}".\
            format(task.nasId, task.bookId, json.dumps(task.epsIds), task.title.replace("'", "''"), task.curPreUpIndex, task.tick, task.status, task.statusMsg)

        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def LoadUpload(self, owner):
        query = QSqlQuery(self.db)
        suc = query.exec_(
            """
            select eps_ids,nas_id,book_id,title,curPreUpIndex,tick,status,status_msg  from nas_upload
            """
        )
        if not suc:
            Log.Warn(query.lastError().text())
        downloads = {}
        while query.next():
            # bookId, downloadEpsIds, curDownloadEpsId, curConvertEpsId, title, savePath, convertPath
            info = NasUploadItem()
            data = json.loads(query.value(0))
            info.epsIds = [int(i) for i in data]
            info.nasId = query.value(1)
            info.bookId = query.value(2)
            info.title = query.value(3)
            info.curPreUpIndex = query.value(4)
            info.tick = query.value(5)
            info.status = query.value(6)
            info.status_msg = query.value(7)
            downloads[info.key] = info

        return downloads

    def DelNasDB(self, nas_id):
        query = QSqlQuery(self.db)
        sql = "delete from nas_info where nas_id='{}'".format(nas_id)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())

        return

    def AddNasDB(self, task):
        assert isinstance(task, NasInfoItem)
        query = QSqlQuery(self.db)
        sql = "INSERT INTO nas_info(nas_id, title, " \
              "address, type, user, passwd, compress_index, save_index, dir_index, is_waifu2x, path, port) " \
              "VALUES ({0}, {1}'{2}', '{3}', {4}, '{5}', '{6}', {7}, {8}, {9}, {10}, '{11}', {12}) " \
              "ON CONFLICT(nas_id) DO UPDATE SET title='{2}', address='{3}', type={4}, user='{5}', passwd='{6}', " \
              "compress_index = {7}, save_index = {8}, dir_index= {9}, is_waifu2x={10}, path='{11}', port={12}".\
            format(task.nasId, "", task.title.replace("'", "''"), task.address, task.type, task.user, task.passwd, task.compress_index, task.save_index, task.dir_index, task.is_waifu2x, task.path, task.port)

        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def LoadNasInfo(self, owner):
        query = QSqlQuery(self.db)
        suc = query.exec_(
            """
            select nas_id,\
            title  ,\
            address ,\
            type  ,\
            user  ,\
            passwd ,\
            compress_index,\
            save_index ,\
            dir_index ,\
            is_waifu2x ,\
            tick, \
            path,\
            port
            from nas_info
            """
        )
        if not suc:
            Log.Warn(query.lastError().text())
        downloads = {}
        while query.next():
            # bookId, downloadEpsIds, curDownloadEpsId, curConvertEpsId, title, savePath, convertPath
            info = NasInfoItem()
            info.nasId = query.value(0)
            info.title = query.value(1)
            info.address = query.value(2)
            info.type = query.value(3)
            info.user = query.value(4)
            info.passwd = query.value(5)
            info.compress_index = query.value(6)
            info.save_index = query.value(7)
            info.dir_index = query.value(8)
            info.is_waifu2x = query.value(9)
            info.tick = query.value(10)
            info.path = query.value(11)
            info.port = query.value(12)

            downloads[info.nasId] = info

        return downloads
