import json
import pickle
import sqlite3
import threading
import time
from queue import Queue

from conf import config
from src.qt.com.langconv import Converter
from src.util import Singleton, Log


# 一本书
class DbBook(object):
    def __init__(self):
        self.id = ""             # 唯一标识
        self.title = ""           # 标题
        self.title2 = ""           # 标题
        self.author = ""          # 作者
        self.chineseTeam = ""     # 汉化组
        self.description = ""     # 描述
        self.epsCount = 0         # 章节数
        self.pages = 0            # 页数
        self.finished = False     # 是否完本
        self.categories = ""      # 分类
        self.tags = ""            # tag
        self.likesCount = 0       # 爱心数
        self.created_at = 0       # 创建时间
        self.updated_at = 0       # 更新时间
        self.path = ""            # 路径
        self.fileServer = ""             # 路径
        self.originalName = ""    # 封面名
        self.creator = ""          # 上传者
        self.totalLikes = 0        #
        self.totalViews = 0        #


class SqlServer(Singleton):
    DbInfos = dict()
    DbInfos["book"] = "data/book.db"

    TaskTypeSql = 1
    TaskTypeSelectBook = 100
    TaskTypeSelectWord = 101
    TaskTypeSelectUpdate = 102
    TaskTypeSelectFavorite = 103
    TaskTypeCacheBook = 104
    TaskTypeUpdateBook = 2
    TaskTypeUpdateFavorite= 3
    TaskTypeClose = 4

    def __init__(self):
        self._inQueue = {}
        for i in self.DbInfos.keys():
            self._inQueue[i] = Queue()
            thread = threading.Thread(target=self._Run, args=(i, ))
            # thread.setDaemon(True)
            thread.start()

    def AddSqlTask(self, table, taskType, data, taskId):
        self._inQueue[table].put((taskType, data, taskId))

    def Stop(self):
        for i in self.DbInfos.keys():
            self._inQueue[i].put((self.TaskTypeClose, "", ""))

    def _Run(self, bookName):
        bookPath = self.DbInfos.get(bookName)
        conn = sqlite3.connect(bookPath)
        inQueue = self._inQueue[bookName]
        while True:
            try:
                task = inQueue.get(True)
            except Exception as es:
                continue
                pass
            inQueue.task_done()
            try:
                (taskType, data, backId) = task
                if taskType == self.TaskTypeSql:
                    cur = conn.cursor()
                    cur.execute(data)
                    cur.execute("COMMIT")
                    if backId:
                        data2 = pickle.dumps("")
                        from src.qt.util.qttask import QtTask
                        QtTask().sqlBack.emit(backId, data2)
                elif taskType == self.TaskTypeSelectBook:
                    self._SelectBook(conn, data, backId)
                elif taskType == self.TaskTypeSelectWord:
                    self._SelectWord(conn, data, backId)
                elif taskType == self.TaskTypeSelectUpdate:
                    self._SelectUpdateInfo(conn, data, backId)
                elif taskType == self.TaskTypeSelectFavorite:
                    self._SelectFavoriteIds(conn, data, backId)
                elif taskType == self.TaskTypeCacheBook:
                    self._SelectCacheBook(conn, data, backId)
                elif taskType == self.TaskTypeUpdateFavorite:
                    self._UpdateFavorite(conn, data, backId)
                elif taskType == self.TaskTypeUpdateBook:
                    self._UpdateBookInfo(conn, data, backId)
                elif taskType == self.TaskTypeClose:
                    break
            except Exception as es:
                Log.Error(es)
        conn.close()
        Log.Info("db: close conn:{}".format(bookName))
        return

    def _SelectBook(self, conn, sql, backId):
        cur = conn.cursor()
        cur.execute(sql)
        books = []
        for data in cur.fetchall():
            info = DbBook()
            info.id = data[0]
            info.title = data[1]
            info.title2 = data[2]
            info.author = data[3]
            info.chineseTeam = data[4]
            info.description = data[5]
            info.epsCount = data[6]
            info.pages = data[7]
            info.finished = data[8]
            info.likesCount = data[9]
            info.categories = data[10]
            info.tags = data[11]
            info.created_at = data[12]
            info.updated_at = data[13]
            info.path = data[14]
            info.fileServer = data[15]
            info.creator = data[16]
            info.totalLikes = data[17]
            info.totalViews = data[18]
            books.append(info)
        data = pickle.dumps(books)
        if backId:
            from src.qt.util.qttask import QtTask
            QtTask().sqlBack.emit(backId, data)

    def _SelectWord(self, conn, sql, backId):
        cur = conn.cursor()
        cur.execute("select * from words")
        words = []
        for data in cur.fetchall():
            words.append(data[1])
        data = pickle.dumps(words)
        if backId:
            from src.qt.util.qttask import QtTask
            QtTask().sqlBack.emit(backId, data)

    def _SelectUpdateInfo(self, conn, sql, backId):
        cur = conn.cursor()
        cur.execute("select * from system")
        nums = 0
        time = ""
        version = 0
        for data in cur.fetchall():
            if config.UpdateVersion == data[0]:
                nums = data[1]
                time = data[2]
                version = data[3]

        cur.execute("select count(*) from book")
        for data in cur.fetchall():
            nums = data[0]

        data = pickle.dumps((nums, time, version))
        if backId:
            from src.qt.util.qttask import QtTask
            QtTask().sqlBack.emit(backId, data)

    def _SelectFavoriteIds(self, conn, sql, backId):
        cur = conn.cursor()
        from src.user.user import User
        cur.execute("select * from favorite where user ='{}'".format(User().userId))
        allFavoriteIds = []
        for data in cur.fetchall():
            allFavoriteIds.append(data[0])
        data = pickle.dumps(allFavoriteIds)
        if backId:
            from src.qt.util.qttask import QtTask
            QtTask().sqlBack.emit(backId, data)

    def _SelectCacheBook(self, conn, bookId, backId):
        cur = conn.cursor()
        cur.execute("select id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
              "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews from book where id ='{}'".format(bookId))
        allFavoriteIds = []
        for data in cur.fetchall():
            info = DbBook()
            info.id = data[0]
            info.title = data[1]
            info.title2 = data[2]
            info.author = data[3]
            info.chineseTeam = data[4]
            info.description = data[5]
            info.epsCount = data[6]
            info.pages = data[7]
            info.finished = data[8]
            info.likesCount = data[9]
            info.categories = data[10]
            info.tags = data[11]
            info.created_at = data[12]
            info.updated_at = data[13]
            info.path = data[14]
            info.fileServer = data[15]
            info.creator = data[16]
            info.totalLikes = data[17]
            info.totalViews = data[18]
            from src.index.book import BookMgr
            BookMgr().AddBookByDb(info)
            allFavoriteIds.append(info)
        data = pickle.dumps(allFavoriteIds)
        if backId:
            from src.qt.util.qttask import QtTask
            QtTask().sqlBack.emit(backId, data)

    def _UpdateBookInfo(self, conn, data, backId):
        cur = conn.cursor()

        addData, tick, version = data
        timeArray = time.localtime(tick)
        strTime = "{}-{}-{} {}:{}:{}".format(timeArray.tm_year, timeArray.tm_mon, timeArray.tm_mday, timeArray.tm_hour, timeArray.tm_min, timeArray.tm_sec)
        sql = "update system set sub_version={}, time='{}' where id='{}'".format(version, strTime, config.UpdateVersion)
        cur.execute(sql)

        for book in addData:
            try:
                if not book:
                    continue
                sql = "replace INTO book(id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
                      "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews) " \
                      "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', {17}, {18}); " \
                    .format(book.id, book.title, book.title2, book.author, book.chineseTeam, book.description,
                            book.epsCount, book.pages, int(book.finished), book.likesCount,
                            book.categories, book.tags, book.created_at, book.updated_at, book.path, book.fileServer,
                            book.creator, book.totalLikes, book.totalViews)
                sql = sql.replace("\0", "")
                cur.execute(sql)
            except Exception as ex:
                Log.Error(ex)

        cur.execute("COMMIT")
        Log.Info("db: update database, len:{}, version:{}, tick:{} ".format(len(addData), tick, version))

    def _UpdateFavorite(self, conn, addData, backId):
        cur = conn.cursor()
        from src.user.user import User
        for bookId, sortId in addData:
            try:
                if not bookId:
                    continue
                sql = "replace INTO favorite(id, user, sortId) VALUES ('{0}', '{1}', {2});".format(bookId, User().userId, sortId)
                sql = sql.replace("\0", "")
                cur.execute(sql)
            except Exception as ex:
                Log.Error(ex)

        cur.execute("COMMIT")

    @staticmethod
    def SearchFavorite(page, sortKey=0, sortId=0):
        from src.user.user import User
        sql = "select book.id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
              "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews from book, favorite  where book.id = favorite.id and favorite.user='{}' ".format(
            User().userId)
        if sortKey == 0:
            sql += "ORDER BY book.updated_at "

        elif sortKey == 1:
            sql += "ORDER BY favorite.sortId "
        elif sortKey == 2:
            sql += "ORDER BY book.created_at "
        elif sortKey == 3:
            sql += "ORDER BY book.totalLikes "
        elif sortKey == 4:
            sql += "ORDER BY book.totalViews "
        elif sortKey == 5:
            sql += "ORDER BY book.epsCount "
        elif sortKey == 6:
            sql += "ORDER BY book.pages "

        if sortId == 0:
            sql += "DESC"
        else:
            sql += "ASC"
        sql += "  limit {},{};".format((page - 1) * 20, 20)
        return sql

    @staticmethod
    def Search(wordList, isTitle, isAutor, isDes, isTag, isCategory, isCreator, page, sortKey=0, sortId=0):
        data = ""
        wordList2 = wordList.split("|")
        for words in wordList2:
            data2 = ""
            for word in words.split("&"):
                data3 = ""
                if isTitle:
                    data3 += " title2 like '%{}%' or ".format(Converter('zh-hans').convert(word).replace("'", "''"))
                if isAutor:
                    data3 += " author like '%{}%' or ".format(Converter('zh-hans').convert(word).replace("'", "''"))
                    data3 += " chineseTeam like '%{}%' or ".format(Converter('zh-hans').convert(word).replace("'", "''"))
                if isDes:
                    data3 += " description like '%{}%' or ".format(Converter('zh-hans').convert(word).replace("'", "''"))
                if isTag:
                    data3 += " tags like '%{}%' or ".format(Converter('zh-hans').convert(word).replace("'", "''"))
                if isCategory:
                    data3 += " categories like '%{}%' or ".format(Converter('zh-hans').convert(word).replace("'", "''"))
                if isCreator:
                    data3 += " creator = '{}' or".format(word)
                data3 = data3.strip("or ")
                data2 += "({}) and ".format(data3)
            data2 = data2.strip("and ")
            if data2:
                data += " or ({})".format(data2)
        if data:
            sql = "SELECT id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
              "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews FROM book WHERE 0 {}".format(data)
        else:
            sql = "SELECT id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
              "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews FROM book WHERE 1 "
        if sortKey == 0:
            sql += "ORDER BY updated_at "
        elif sortKey == 1:
            sql += "ORDER BY created_at "
        elif sortKey == 2:
            sql += "ORDER BY totalLikes "
        elif sortKey == 3:
            sql += "ORDER BY totalViews "
        elif sortKey == 4:
            sql += "ORDER BY epsCount "
        elif sortKey == 5:
            sql += "ORDER BY pages "

        if sortId == 0:
            sql += "DESC"
        else:
            sql += "ASC"
        sql += "  limit {},{};".format((page-1)*20, 20)
        return sql