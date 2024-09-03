import os
import pickle
import sqlite3
import sys
import threading
import time
from queue import Queue

# 一本书
from config import config
from config.setting import Setting
from task.task_sql import TaskSql
from tools.book import BookMgr
from tools.langconv import Converter
from tools.log import Log
from tools.singleton import Singleton
from tools.status import Status
from tools.tool import time_me
from tools.user import User


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

    def CopyFromJson(self, data):
        for k, v in data.items():
            setattr(self, k, v)


class SqlServer(Singleton):
    DbInfos = dict()
    DbInfos["book"] = "db/book.db"

    TaskCheck = 0
    TaskTypeSql = 1
    TaskTypeSelectBook = 100
    TaskTypeSelectWord = 101
    TaskTypeSelectUpdate = 102
    TaskTypeSelectFavorite = 103
    TaskTypeCacheBook = 104          # 缓存
    TaskTypeCategoryBookNum = 105    # 查询分类数量
    TaskTypeSearchBookNum = 106      # 查询分页数量
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
            if sys.platform == "linux":
                path = os.path.join(Setting.GetConfigPath(), bookPath)
                conn = sqlite3.connect(path)
            else:
                conn = sqlite3.connect(bookPath)
        except Exception as es:
            Log.Error(es)
            from qt_owner import QtOwner
            QtOwner().isUseDb = False
            isInit = False

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

                if taskType == self.TaskTypeClose:
                    break
                if not isInit:
                    TaskSql().taskObj.sqlBack.emit(backId, pickle.dumps(""))
                    continue
                if taskType == self.TaskCheck:
                    try:
                        cur = conn.cursor()
                        cur.execute("select * from system")
                        data2 = pickle.dumps(str(int(isInit)))
                    except Exception as es:
                        Log.Error(es)
                        data2 = pickle.dumps("")
                    TaskSql().taskObj.sqlBack.emit(backId, data2)
                elif taskType == self.TaskTypeSql:
                    cur = conn.cursor()
                    cur.execute(data)
                    cur.execute("COMMIT")
                    if backId:
                        data2 = pickle.dumps("")
                        TaskSql().taskObj.sqlBack.emit(backId, data2)
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
                elif taskType == self.TaskTypeCategoryBookNum:
                    self._SelectCategoryBookNum(conn, data, backId)
                elif taskType == self.TaskTypeSearchBookNum:
                    self._SelectBookNum(conn, data, backId)
                elif taskType == self.TaskTypeUpdateFavorite:
                    self._UpdateFavorite(conn, data, backId)
                elif taskType == self.TaskTypeUpdateBook:
                    self._UpdateBookInfo(conn, data, backId)

            except Exception as es:
                Log.Error(es)
        if conn:
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
            TaskSql().taskObj.sqlBack.emit(backId, data)

    def _SelectBookNum(self, conn, sql, backId):
        cur = conn.cursor()
        nums = 0
        cur.execute(sql)
        for data in cur.fetchall():
            nums = data[0]
        data = pickle.dumps(nums)
        if backId:
            TaskSql().taskObj.sqlBack.emit(backId, data)

    def _SelectCategoryBookNum(self, conn, sql, backId):
        cur = conn.cursor()
        from tools.category import CateGoryMgr
        nums = {}
        cur.execute("select category, count(*) from category where bookId in ({}) group by category".format(sql))
        for data in cur.fetchall():
            nums[CateGoryMgr().indexCategories.get(data[0])] = data[1]
        data = pickle.dumps(nums)
        if backId:
            TaskSql().taskObj.sqlBack.emit(backId, data)

    def _SelectWord(self, conn, sql, backId):
        cur = conn.cursor()
        cur.execute("select * from words")
        words = []
        for data in cur.fetchall():
            words.append(data[1])
        data = pickle.dumps(words)
        if backId:
            TaskSql().taskObj.sqlBack.emit(backId, data)

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

        data = pickle.dumps((dbVer, nums, time, version))
        if backId:
            TaskSql().taskObj.sqlBack.emit(backId, data)

    def _SelectFavoriteIds(self, conn, sql, backId):
        cur = conn.cursor()
        sql = "select id,sortId from favorite where user ='{}'".format(Setting.UserId.value)
        cur.execute(sql)
        allFavoriteIds = []
        for data in cur.fetchall():
            allFavoriteIds.append((data[0], data[1]))
        data = pickle.dumps(allFavoriteIds)
        if backId:
            TaskSql().taskObj.sqlBack.emit(backId, data)

    def _SelectCacheBook(self, conn, bookId, backId):
        v = {}
        try:
            cur = conn.cursor()
            cur.execute(
                "select id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
                "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews from book where id ='{}'".format(
                    bookId))
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
                BookMgr().AddBookByDb(info)
                allFavoriteIds.append(info)
            v["bookList"] = allFavoriteIds
            v["st"] = Status.Ok
        except Exception as es:
            Log.Error(es)
        data = pickle.dumps(v)
        if backId:
            TaskSql().taskObj.sqlBack.emit(backId, data)

    @time_me
    def _UpdateBookInfo(self, conn, data, backId):
        cur = conn.cursor()

        addData, tick, version = data
        timeArray = time.localtime(tick)
        strTime = "{}-{}-{} {}:{}:{}".format(timeArray.tm_year, timeArray.tm_mon, timeArray.tm_mday, timeArray.tm_hour, timeArray.tm_min, timeArray.tm_sec)
        sql = "update system set sub_version={}, time='{}' where id='{}'".format(version, strTime, config.DbVersion)
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

                try:
                    for name in book.categories.split(","):
                        from tools.category import CateGoryMgr
                        index = CateGoryMgr().categoriseIndex.get(name)
                        if not index:
                            continue
                        sql = "replace INTO category(bookId, category) VALUES ('{0}', {1}); ".format(book.id, index)
                        sql = sql.replace("\0", "")
                        cur.execute(sql)
                except Exception as es:
                    Log.Error(es)

            except Exception as ex:
                Log.Error(ex)

        cur.execute("COMMIT")
        Log.Info("db: update database, len:{}, version:{}, tick:{} ".format(len(addData), tick, version))

    def _UpdateFavorite(self, conn, addData, backId):
        cur = conn.cursor()
        for bookId, sortId in addData:
            try:
                if not bookId:
                    continue
                sql = "replace INTO favorite(id, user, sortId) VALUES ('{0}', '{1}', {2});".format(bookId, Setting.UserId.value, sortId)
                sql = sql.replace("\0", "")
                cur.execute(sql)
            except Exception as ex:
                Log.Error(ex)

        cur.execute("COMMIT")

    @staticmethod
    def SearchFavorite(page, sortKey=0, sortId=0, searchText=""):
        if not searchText:
            sql = "select book.id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
                  "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews from book, favorite  where book.id = favorite.id and favorite.user='{}' ".format(
                Setting.UserId.value)
        else:
            sql = "select book.id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
                  "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews from book, favorite  where book.id = favorite.id and favorite.user='{}' ".format(
                Setting.UserId.value)
            sql += " and (book.title like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.title2 like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.author like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.chineseTeam like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.description like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.tags like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.categories like '%{}%')  ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))

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
    def Search(wordList, isTitle, isAutor, isDes, isTag, isCategory, isCreator, categorys, page, sortKey=0, sortId=0):
        wordList = Converter('zh-hans').convert(wordList)
        data = ""
        sql2Data = ""
        wordList2 = wordList.split("|")
        for words in wordList2:
            data2 = ""
            for word in words.split("&"):
                data3 = ""
                if not word:
                    continue
                if isTitle:
                    data3 += " title like '%{}%' or ".format(Converter('zh-hans').convert(word).replace("'", "''"))
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

            data4 = ""
            if categorys:
                for category in categorys:
                    data4 += " categories like '%{}%' or ".format(Converter('zh-hans').convert(category).replace("'", "''"))
            data4 = data4.strip("or ")

            if data2:
                if data4:
                    data += " or ({} and ({}))".format(data2, data4)
                else:
                    data += " or ({})".format(data2)
                sql2Data += " or ({})".format(data2)

        if data:
            sql = "SELECT id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
              "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews FROM book WHERE 0 {}".format(data)
        else:
            sql = "SELECT id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
              "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews FROM book WHERE 1 "

        if sql2Data:
            sql2Data = "SELECT id FROM book WHERE 0 {}".format(sql2Data)
        else:
            sql2Data = "SELECT id FROM book WHERE 1 "

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
        return sql, sql2Data

    @staticmethod
    def _GetSearchWhere(word, isTitle, isAuthor, isDes, isTag, isCategory, isCreator, isLike):
        data3 = ""
        if isLike:
            likeStr = "like"
            linkStr = "or"
        else:
            likeStr = "not like"
            linkStr = "and"

        if isTitle:
            data3 += " title {} '%{}%' {} ".format(likeStr, word, linkStr)
            data3 += " title2 {} '%{}%' {} ".format(likeStr, word, linkStr)
        if isAuthor:
            data3 += " author {} '%{}%' {} ".format(likeStr, word, linkStr)
            data3 += " chineseTeam {} '%{}%' {} ".format(likeStr, word, linkStr)
        if isDes:
            data3 += " description {} '%{}%' {} ".format(likeStr, word, linkStr)
        if isTag:
            data3 += " tags {} '%{}%' {} ".format(likeStr, word, linkStr)
        if isCategory:
            data3 += " categories {} '%{}%' {} ".format(likeStr, word, linkStr)
        if isCreator:
            data3 += " creator {} '%{}%' {} ".format(likeStr, word, linkStr)
        data3 = data3.strip("{} ".format(linkStr))
        return "({})".format(data3)

    @staticmethod
    def Search2(wordList, isTitle, isAuthor, isDes, isTag, isCategory, isCreator, categorys, page, sortKey=0, sortId=0):
        wordList = Converter('zh-hans').convert(wordList)
        wordList2 = wordList.split(" ")
        exclude = []
        andWords = []
        orWords = []

        for words in wordList2:
            if len(words) <= 0:
                continue
            words = Converter('zh-hans').convert(words)
            if words[0] == "+":
                andWords.append(words[1:])
            elif words[0] == "-":
                exclude.append(words[1:])
            else:
                orWords.append(words)

        if not andWords and not exclude:
            orWords = []
            orWords.append(wordList)

        data = ""
        data2 = ""
        for word in orWords:
            whereSql = SqlServer._GetSearchWhere(word, isTitle, isAuthor, isDes, isTag, isCategory, isCreator, True)
            data2 += "{} or ".format(whereSql)
        if data2:
            data += "({})".format(data2.strip("or "))

        data2 = ""
        for word in andWords:
            whereSql = SqlServer._GetSearchWhere(word, isTitle, isAuthor, isDes, isTag, isCategory, isCreator, True)
            data2 += "{} or ".format(whereSql)
        if data2:
            data += "and ({})".format(data2.strip("or "))

        data2 = ""
        for word in exclude:
            whereSql = SqlServer._GetSearchWhere(word, isTitle, isAuthor, isDes, isTag, isCategory, isCreator, False)
            data2 += "{} or ".format(whereSql)
        if data2:
            data += "and ({})".format(data2.strip("or "))

        sql2Data = data

        data2 = ""
        if categorys:
            for category in categorys:
                data2 += " categories like '%{}%' or ".format(Converter('zh-hans').convert(category).replace("'", "''"))
        if data2:
            data += "and ({})".format(data2.strip("or "))

        data = data.strip("and ").strip("or ")

        selectNumSql = data
        if data:
            sql = "SELECT id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
              "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews FROM book WHERE {}".format(data)
        else:
            sql = "SELECT id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
              "created_at, updated_at, path, fileServer, creator, totalLikes, totalViews FROM book WHERE 1 "

        if selectNumSql:
            selectNumSql = "SELECT count(*) FROM book WHERE {}".format(selectNumSql)
        else:
            selectNumSql = "SELECT count(*) FROM book WHERE 1 "

        if sql2Data:
            sql2Data = "SELECT id FROM book WHERE {}".format(sql2Data)
        else:
            sql2Data = "SELECT id FROM book WHERE 1 "

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
        return sql, sql2Data, selectNumSql

    @staticmethod
    def SaveCacheWord():
        path = os.path.join(Setting.GetConfigPath(), "cache_word")
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
        path = os.path.join(Setting.GetConfigPath(), "cache_word")
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