import os
import pickle
import sqlite3
import threading
import time
from queue import Queue

# 一本书
from config import config
from config.setting import Setting
from qt_owner import QtOwner
from task.task_sql import TaskSql
from tools.book import BookMgr
from tools.log import Log
from tools.singleton import Singleton
from tools.status import Status
from tools.tool import time_me
# 保留 DbBook 的旧导入路径和历史序列化兼容性。
from server.book_mapping import DbBook, book_projection, books_from_cursor
from server.book_query import BookQuery, SqlStatement, books_by_ids_statement, execute_statement
from tools.page_result import PageRequest, PageResult


class SqlServer(Singleton):
    DbInfos = dict()
    DbInfos["book"] = "book.db"

    TaskCheck = 0
    TaskTypeSql = 1
    TaskTypeSelectBook = 100
    TaskTypeSelectWord = 101
    TaskTypeSelectUpdate = 102
    TaskTypeSelectFavorite = 103
    TaskTypeCacheBook = 104          # 缓存
    TaskTypeCacheBookByShareId = 107          # 缓存
    TaskTypeCategoryBookNum = 105    # 查询分类数量
    TaskTypeSearchBookNum = 106      # 查询分页数量
    TaskTypeSelectBookPage = 108     # 查询书籍与分页总数
    TaskTypeUpdateBook = 2
    TaskTypeUpdateFavorite= 3
    TaskTypeClose = 4

    def __init__(self):
        self._inQueue = {}
        self.cacheWord = []
        self.data = []
        for i in self.DbInfos.keys():
            self._inQueue[i] = Queue()
            thread = threading.Thread(target=self._Run, args=(i, ))
            thread.setName("DB-"+str(i))
            # thread.setDaemon(True)
            thread.start()

    def AddSqlTask(self, table, taskType, data, taskId):
        self._inQueue[table].put((taskType, data, taskId))

    def SetCacheWord(self, data):
        self.cacheWord = data
        self.LoadCacheWord()

    def Stop(self):
        SqlServer.SaveCacheWord()
        for i in self.DbInfos.keys():
            self._inQueue[i].put((self.TaskTypeClose, "", ""))

    def _Run(self, bookName):
        bookPath = self.DbInfos.get(bookName)
        isInit = True
        conn = None
        try:
            path = os.path.join(Setting.GetDBPath(), bookPath)
            if not os.path.isfile(path):
                QtOwner().isUseDb = False
                isInit = False
            else:
                conn = sqlite3.connect(path, timeout=5)
                conn.execute("PRAGMA journal_mode=WAL")
                self.__DoCheckHavePicaID(conn)
        except Exception as es:
            Log.Error(es)
            QtOwner().isUseDb = False
            isInit = False

        inQueue = self._inQueue[bookName]
        while True:
            taskType, data, backId = inQueue.get(True)
            try:
                if taskType == self.TaskTypeClose:
                    break
                result = self._SqlFailureResult(taskType)
                try:
                    if isInit:
                        if taskType == self.TaskCheck:
                            conn.execute("select * from system")
                            result = "1"
                        elif taskType == self.TaskTypeSql:
                            with conn:
                                conn.execute(data)
                            result = ""
                        elif taskType == self.TaskTypeSelectBook:
                            result = self._SelectBook(conn, data, backId)
                        elif taskType == self.TaskTypeSelectBookPage:
                            result = self._SelectBookPage(conn, data, backId)
                        elif taskType == self.TaskTypeSelectWord:
                            result = self._SelectWord(conn, data, backId)
                        elif taskType == self.TaskTypeSelectUpdate:
                            result = self._SelectUpdateInfo(conn, data, backId)
                        elif taskType == self.TaskTypeSelectFavorite:
                            result = self._SelectFavoriteIds(conn, data, backId)
                        elif taskType == self.TaskTypeCacheBook:
                            result = self._SelectCacheBook(conn, data, backId)
                        elif taskType == self.TaskTypeCategoryBookNum:
                            result = self._SelectCategoryBookNum(conn, data, backId)
                        elif taskType == self.TaskTypeSearchBookNum:
                            result = self._SelectBookNum(conn, data, backId)
                        elif taskType == self.TaskTypeUpdateFavorite:
                            result = self._UpdateFavorite(conn, data, backId)
                        elif taskType == self.TaskTypeUpdateBook:
                            result = self._UpdateBookInfo(conn, data, backId)
                    response = pickle.dumps(result)
                except Exception as es:
                    Log.Error(es)
                    response = pickle.dumps(self._SqlFailureResult(taskType))
                # 每个 SQL 任务只有这一处终态通知，写操作在事务提交后才到达这里。
                if backId:
                    TaskSql().taskObj.sqlBack.emit(backId, response)
            finally:
                inQueue.task_done()
        if conn:
            conn.close()
        Log.Info("db: close conn:{}".format(bookName))
        return

    @classmethod
    def _SqlFailureResult(cls, taskType):
        if taskType == cls.TaskCheck:
            return ""
        if taskType == cls.TaskTypeCacheBook:
            return {"st": Status.Error, "bookList": []}
        if taskType in (cls.TaskTypeUpdateBook, cls.TaskTypeUpdateFavorite):
            return {"st": Status.Error}
        return None

    def __DoCheckHavePicaID(self, conn):
        cur = conn.cursor()
        sql = "PRAGMA table_info(book);"
        allName = []
        cur.execute(sql)
        for data in cur.fetchall():
            allName.append(data[1])
        if "shareId" in allName:
            QtOwner().isDbHavePicaID = True
        else:
            QtOwner().isDbHavePicaID = False

    @staticmethod
    def _HasShareId(conn):
        return any(column[1] == "shareId" for column in conn.execute("PRAGMA table_info(book)"))

    def _SelectBook(self, conn, sql, backId):
        return books_from_cursor(execute_statement(conn, sql))

    def _SelectBookPage(self, conn, data, backId):
        query, request = data
        hasShareId = self._HasShareId(conn)
        _, _, count = query.statements(has_share_id=hasShareId)
        total = execute_statement(conn, count).fetchone()[0]
        request = request.clamp(total)
        rows, _, _ = query.statements(request, hasShareId)
        books = books_from_cursor(execute_statement(conn, rows))
        return PageResult.from_total(books, request, total)

    def _SelectBookNum(self, conn, sql, backId):
        return execute_statement(conn, sql).fetchone()[0]

    def _SelectCategoryBookNum(self, conn, sql, backId):
        from tools.category import CateGoryMgr
        if isinstance(sql, SqlStatement):
            statement = SqlStatement("select category, count(*) from category where bookId in ({}) group by category".format(sql.sql), sql.params)
        else:
            statement = "select category, count(*) from category where bookId in ({}) group by category".format(sql)
        return {CateGoryMgr().indexCategories.get(category): count
                for category, count in execute_statement(conn, statement)}

    def _SelectWord(self, conn, sql, backId):
        cur = conn.cursor()
        cur.execute("select * from words")
        words = []
        for data in cur.fetchall():
            words.append(data[1])
        return words

    def _SelectUpdateInfo(self, conn, sql, backId):
        cur = conn.cursor()
        cur.execute("select id, size, time, sub_version from system where 1 order by id desc limit 1")
        nums = 0
        time = ""
        version = 0
        dbVer = ""
        for data in cur.fetchall():
            dbVer = data[0]
            nums = data[1]
            time = data[2]
            version = data[3]

        cur.execute("select count(*) from book")
        for data in cur.fetchall():
            nums = data[0]

        return dbVer, nums, time, version

    def _SelectFavoriteIds(self, conn, sql, backId):
        cur = conn.cursor()
        sql = "select id,sortId from favorite where user ='{}'".format(Setting.UserId.value)
        cur.execute(sql)
        allFavoriteIds = []
        for data in cur.fetchall():
            allFavoriteIds.append((data[0], data[1]))
        return allFavoriteIds

    def _SelectCacheBook(self, conn, bookId, backId):
        hasShareId = self._HasShareId(conn)
        if isinstance(bookId, int) and not hasShareId:
            return self._SqlFailureResult(self.TaskTypeCacheBook)
        field = "shareId" if isinstance(bookId, int) else "id"
        statement = SqlStatement("SELECT {} FROM book WHERE {} = ?".format(
            book_projection(hasShareId), field), (bookId,))
        books = self._SelectBook(conn, statement, backId)
        for book in books:
            BookMgr().AddBookByDb(book)
        return {"st": Status.Ok, "bookList": books}

    @time_me
    def _UpdateBookInfo(self, conn, data, backId):
        cur = conn.cursor()

        addData, tick, version = data
        with conn:

            for book in addData:
                if not book:
                    continue
                if QtOwner().isDbHavePicaID and book.shareId > 0:
                    sql = "replace INTO book(id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
                          "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews, shareId) " \
                          "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', {17}, {18}, {19}); " \
                        .format(book.id, book.title, book.title2, book.author, book.chineseTeam, book.description,
                                book.epsCount, book.pages, int(book.finished), book.likesCount,
                                book.categories, book.tags, book.created_at, book.updated_at, book.path, book.fileServer,
                                book.creator, book.totalLikes, book.totalViews, book.shareId)
                else:
                    sql = "replace INTO book(id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
                          "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews) " \
                          "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', {17}, {18}); " \
                        .format(book.id, book.title, book.title2, book.author, book.chineseTeam, book.description,
                                book.epsCount, book.pages, int(book.finished), book.likesCount,
                                book.categories, book.tags, book.created_at, book.updated_at, book.path,
                                book.fileServer,
                                book.creator, book.totalLikes, book.totalViews)

                sql = sql.replace("\0", "")
                cur.execute(sql)

                for name in book.categories.split(","):
                    from tools.category import CateGoryMgr
                    index = CateGoryMgr().categoriseIndex.get(name)
                    if not index:
                        continue
                    sql = "replace INTO category(bookId, category) VALUES ('{0}', {1}); ".format(book.id, index)
                    sql = sql.replace("\0", "")
                    cur.execute(sql)

            timeArray = time.localtime(tick)
            strTime = "{}-{}-{} {}:{}:{}".format(timeArray.tm_year, timeArray.tm_mon, timeArray.tm_mday, timeArray.tm_hour, timeArray.tm_min, timeArray.tm_sec)
            sql = "update system set sub_version={}, time='{}' where id='{}'".format(version, strTime, config.DbVersion)
            cur.execute(sql)

            Log.Info("db: update database, len:{}, version:{}, tick:{} ".format(len(addData), tick, version))
        return {"st": Status.Ok}

    def _UpdateFavorite(self, conn, addData, backId):
        cur = conn.cursor()
        with conn:
            for bookId, sortId in addData:
                if not bookId:
                    continue
                sql = "replace INTO favorite(id, user, sortId) VALUES ('{0}', '{1}', {2});".format(bookId, Setting.UserId.value, sortId)
                sql = sql.replace("\0", "")
                cur.execute(sql)
        return {"st": Status.Ok}

    @staticmethod
    def GetBookByIds(bookIds):
        return books_by_ids_statement(bookIds, QtOwner().isDbHavePicaID).legacy_sql()

    @staticmethod
    def GetBookMetrics(bookIds):
        return books_by_ids_statement(bookIds, metrics_only=True).legacy_sql()

    @staticmethod
    def Search2(wordList, isTitle, isAuthor, isDes, isTag, isCategory, isCreator,
                categorys, page, sortKey=0, sortId=0, isFinish=False, limitIds=None):
        """兼容原有三段字符串 SQL 接口，新分页调用直接传入查询条件。"""
        query = BookQuery.from_legacy(wordList, isTitle, isAuthor, isDes, isTag,
                                     isCategory, isCreator, categorys, sortKey,
                                     sortId, isFinish, limitIds)
        request = None if page < 0 else PageRequest(max(1, page))
        return tuple(statement.legacy_sql() for statement in query.statements(
            request, QtOwner().isDbHavePicaID))

    @staticmethod
    def SaveCacheWord():
        path = os.path.join(Setting.GetStatePath(), "cache_word")
        try:
            if not SqlServer().cacheWord:
                return
            f = open(path, "w+", encoding="utf-8")
            f.write("\n".join(SqlServer().cacheWord))
            f.close()
        except Exception as es:
            Log.Error(es)

    @staticmethod
    def LoadCacheWord():
        path = os.path.join(Setting.GetStatePath(), "cache_word")
        try:
            if not os.path.isfile(path):
                return
            f = open(path, "r", encoding="utf-8")
            data = f.read()
            f.close()
            for v in data.split("\n"):
                if v:
                    SqlServer().cacheWord.append(v)
        except Exception as es:
            Log.Error(es)
