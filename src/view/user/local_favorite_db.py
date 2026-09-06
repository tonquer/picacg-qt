import json
import os.path
import time

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from config.setting import Setting
from server.sql_server import DbBook
from tools.book import Book
from tools.langconv import Converter
from tools.log import Log
from view.download.download_item import DownloadItem, DownloadEpsItem
from tools.pagination import FAVORITE_PAGE_SIZE

class LocalFavoriteItem(DbBook):
    def __init__(self):
        DbBook.__init__(self)
        self.add_tick = 0


class LocalFavoriteDb(object):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE", "favorite")
        path = os.path.join(Setting.GetStatePath(), "favorite.db")
        self.db.setDatabaseName(path)
        if not self.db.open():
            Log.Warn(self.db.lastError().text())
        query = QSqlQuery(self.db)
        sqlList = [ """\
            create table if not exists favorite(\
            bookId varchar primary key,\
            title varchar,\
            author varchar,\
            chineseTeam varchar,\
            epsCount int,\
            pages int,\
            finished int,\
            created_at varchar,\
            updated_at varchar,\
            fileServer varchar,\
            path varchar,\
            categories varchar,\
            tags varchar,\
            description varchar, \
            tick int  DEFAULT 0
            )\
            """,
            """\
                        create table if not exists favorite_fold(\
                        fid INTEGER primary key autoincrement,\
                        name varchar,\
                        tick int,\
                        UNIQUE(name)
                        )\
                        """,
            """\
                        create table if not exists favorite_fid(\
                        fid int,\
                        bookId varchar\
                        )\
                        """
        ]
        for sql in sqlList:
            query = QSqlQuery(self.db)
            suc = query.exec_(sql)
            if not suc:
                a = query.lastError().text()
                Log.Warn(a)
        # self.LoadDownload()

    def DelFavoriteDB(self, bookId):
        query = QSqlQuery(self.db)
        sql = "delete from favorite where bookId='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        sql = "delete from favorite_fid where bookId='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def AddBookToDB(self, book):
        if isinstance(book, DbBook):
            url = book.fileServer
            path = book.path
        elif isinstance(book, Book):
            url = book.thumb.get('fileServer', "")
            path = book.thumb.get('path', "")
        else:
            raise
        tick = int(time.time())
        query = QSqlQuery(self.db)
        sql = "replace INTO favorite(bookId, title, author, chineseTeam, description, epsCount, pages, finished, categories, tags," \
        "created_at, updated_at, path, fileServer, tick) " \
        "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6}, {7}, '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', {14}); ". \
            format(book.id,
                   Converter('zh-hans').convert(book.title).replace("'", "''"),
                   Converter('zh-hans').convert(book.author).replace("'", "''"),
                   Converter('zh-hans').convert(book.chineseTeam).replace("'", "''"),
                   Converter('zh-hans').convert(book.description).replace("'", "''"),
                   book.epsCount, book.pagesCount,
                   int(book.finished),
                   Converter('zh-hans').convert(",".join(book.categories)).replace("'", "''"),
                   Converter('zh-hans').convert(",".join(book.tags).replace("'", "''")),
                   book.created_at, book.updated_at,
                   path, url,
                   tick)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        # self.UpdateBookEpsNum(book.baseInfo.bookId, book.epsCount, int(time.time()))
        return

    def AddFavoriteFid(self, name):
        query = QSqlQuery(self.db)
        sql = "INSERT INTO favorite_fold(name, tick) " \
              "VALUES ('{0}', {1})". \
            format(name, str(int(time.time())))

        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
            return False
        return True

    def DelFavoriteFid(self, fid):
        query = QSqlQuery(self.db)
        sql = "delete from favorite_fold where fid={}".format(fid)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return True

    def AddBookFavoriteFid(self, bookId, fid):
        query = QSqlQuery(self.db)
        self.DelBookFavoriteFid(bookId)
        if fid == 0:
            return True
        sql = "INSERT INTO favorite_fid(fid, bookId) " \
              "VALUES ({0}, '{1}')". \
            format(fid, bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
            return False
        return True

    def UpdateBookFavoriteFid(self, bookId, fids):
        query = QSqlQuery(self.db)
        self.DelBookFavoriteFid(bookId)
        if fids == [0]:
            return True
        for fid in fids:
            if fid == 0:
                continue

            sql = "INSERT INTO favorite_fid(fid, bookId) " \
                  "VALUES ({0}, '{1}')". \
                format(fid, bookId)
            suc = query.exec_(sql)
            if not suc:
                Log.Warn(query.lastError().text())
                return False
        return True

    # def UpdateBookEpsNum(self, bookId, epsNum, updateTick):
    #     query = QSqlQuery(self.db)
    #     sql = f"UPDATE favorite SET max_eps_num={epsNum}, last_uptick={updateTick} WHERE bookId='{bookId}' and max_eps_num!={epsNum}"
    #     suc = query.exec_(sql)
    #     if not suc:
    #         Log.Warn(query.lastError().text())
    #         return False
    #     return True

    # def UpdateBookInfo(self, book):
    #     query = QSqlQuery(self.db)
    #     tagStr = Converter('zh-hans').convert(",".join(book.baseInfo.tagList).replace("'", "''"))
    #     author = Converter('zh-hans').convert(",".join(book.baseInfo.authorList).replace("'", "''"))
    #     coverUrl = book.baseInfo.coverUrl
    #     des = Converter('zh-hans').convert(book.pageInfo.des).replace("'", "''")
    #     title = Converter('zh-hans').convert(book.baseInfo.title).replace("'", "''")
    #     sql = f"UPDATE favorite SET description='{des}', title='{title}', coverUrl='{coverUrl}', author='{author}', tagList='{tagStr}' WHERE bookId='{book.baseInfo.bookId}'"
    #     suc = query.exec_(sql)
    #     if not suc:
    #         Log.Warn(query.lastError().text())
    #         return False
    #     return True

    def DelBookFavoriteFid(self, book_id):
        query = QSqlQuery(self.db)
        sql = "delete from favorite_fid where bookId='{}'".format(book_id)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
            return False
        return True

    def LoadFold(self):
        sql = "select fid, name from favorite_fold where 1"
        self.db.exec()
        query = QSqlQuery(self.db)
        suc = query.exec_(sql)
        data = {}
        if not suc:
            Log.Warn(query.lastError().text())
            return data
        while query.next():
            fid = query.value(0)
            name = query.value(1)
            data[int(fid)] = name
        return data

    def LoadBookFold(self):
        sql = "select fid, bookId from favorite_fid where 1"
        self.db.exec()
        query = QSqlQuery(self.db)
        suc = query.exec_(sql)
        data = {}
        if not suc:
            Log.Warn(query.lastError().text())
            return data
        while query.next():
            fid = query.value(0)
            bookId = query.value(1)
            data.setdefault(int(fid), set())
            data[int(fid)].add(bookId)
        return data

    def SearchFavorite(self, page, sortKey=0, sortId=0, fid=0, searchText=""):
        if not searchText:
            sql = "select bookId, title, author, chineseTeam, description, epsCount, pages, finished, categories, tags, created_at, updated_at, path, fileServer, tick  " \
                  "from favorite as book  where 1 "
            if fid != 0:
                sql += f" and bookId in (select bookId from favorite_fid where fid={fid}) "
        else:
            sql = "select bookId, title, author, chineseTeam, description, epsCount, pages, finished, categories, tags, created_at, updated_at, path, fileServer, tick  " \
                  "from favorite as book where 1 "
            if fid != 0:
                sql += f" and bookId in (select bookId from favorite_fid where fid={fid}) "
            sql += " and (book.title like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.author like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.description like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.tags like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.bookId like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.categories like '%{}%')  ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))

        if sortKey == 1:
            if sortId == 0:
                sql += "ORDER BY book.updated_at DESC, book.tick DESC, book.bookId ASC"
            else:
                sql += "ORDER BY book.updated_at ASC, book.tick ASC, book.bookId ASC"
        elif sortKey == 0:
            if sortId == 0:
                sql += "ORDER BY book.tick DESC, book.bookId ASC"
            else:
                sql += "ORDER BY book.tick ASC, book.bookId ASC"
        elif sortKey in (2, 5, 6):
            column = {2: "created_at", 5: "epsCount", 6: "pages"}[sortKey]
            direction = "DESC" if sortId == 0 else "ASC"
            sql += "ORDER BY book.{} {}, book.bookId ASC".format(column, direction)
        else:
            sql += "ORDER BY book.bookId ASC"


        if page >= 0:
            sql += "  limit {},{};".format((max(1, page) - 1) * FAVORITE_PAGE_SIZE, FAVORITE_PAGE_SIZE)

        self.db.exec()
        query = QSqlQuery(self.db)
        suc = query.exec_(sql)
        data = []
        if not suc:
            Log.Warn(query.lastError().text())
        while query.next():
            # select bookId, title, author, chineseTeam, description, epsCount, pages, finished, categories, tags, created_at, updated_at, path, fileServer, tick
            info = LocalFavoriteItem()
            bookId = query.value(0)
            info.id = bookId
            info.title = query.value(1)
            info.author = query.value(2)
            info.chineseTeam = query.value(3)
            info.description = query.value(4)
            info.epsCount = query.value(5)
            info.pages = query.value(6)
            info.finished = bool(query.value(7))
            info.categories = query.value(8)
            info.tags = query.value(9)
            info.created_at = query.value(10)
            info.updated_at = query.value(11)
            info.path = query.value(12)
            info.fileServer = query.value(13)
            info.tick = query.value(14)
            data.append(info)
        return data
