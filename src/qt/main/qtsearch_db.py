import time

from PySide2.QtSql import QSqlQuery, QSqlDatabase

from conf import config
from src.util import Log


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
        self.totalLikes = 0        #
        self.totalViews = 0        #


class QtSearchDb(object):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.db = QSqlDatabase.addDatabase("QSQLITE", "book")
        self.db.setDatabaseName("data/book.db")
        if not self.db.open():
            Log.Warn(self.db.lastError().text())

    def InitWord(self):
        query = QSqlQuery(self.db)
        suc = query.exec_(
            """
            select * from words
            """
        )
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
        words = []
        while query.next():
            word = query.value(1)
            words.append(word)
        return words

    def InitUpdateInfo(self):
        query = QSqlQuery(self.db)
        suc = query.exec_(
            """
            select * from system
            """
        )
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
        nums = 0
        time = ""
        version = 0
        while query.next():
            if config.UpdateVersion == query.value(0):
                nums = query.value(1)
                time = query.value(2)
                version = query.value(3)
        return nums, time, version

    def Search(self, wordList, isTitle, isAutor, isDes, isTag, isCategory, page, sortKey=0, sortId=0):
        query = QSqlQuery(self.db)
        data = ""
        wordList2 = wordList.split("|")
        for words in wordList2:
            data2 = ""
            for word in words.split("&"):
                if not word:
                    continue
                data3 = ""
                if isTitle:
                    data3 += " title2 like '%{}%' or ".format(word)
                if isAutor:
                    data3 += " author like '%{}%' or ".format(word)
                    data3 += " chineseTeam like '%{}%' or ".format(word)
                if isDes:
                    data3 += " description like '%{}%' or ".format(word)
                if isTag:
                    data3 += " tags like '%{}%' or ".format(word)
                if isCategory:
                    data3 += " categories like '%{}%' or ".format(word)
                data3 = data3.strip("or ")
                data2 += "({}) and ".format(data3)
            data2 = data2.strip("and ")
            if data2:
                data += " or ({})".format(data2)
        if data:
            sql = "SELECT * FROM book WHERE 0 {}".format(data)
        else:
            sql = "SELECT * FROM book WHERE 1 "
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
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
        books = []
        while query.next():
            info = DbBook()
            info.id = query.value(0)
            info.title = query.value(1)
            info.title2 = query.value(2)
            info.author = query.value(3)
            info.chineseTeam = query.value(4)
            info.description = query.value(5)
            info.epsCount = query.value(6)
            info.pages = query.value(7)
            info.finished = query.value(8)
            info.likesCount = query.value(9)
            info.categories = query.value(10)
            info.tags = query.value(11)
            info.created_at = query.value(12)
            info.updated_at = query.value(13)
            info.path = query.value(14)
            info.fileServer = query.value(15)
            info.originalName = query.value(16)
            info.totalLikes = query.value(17)
            info.totalViews = query.value(18)
            books.append(info)
        return books

    def Select(self, bookId):
        query = QSqlQuery(self.db)
        sql = "select * from book where id='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
            return None
        while query.next():
            info = DbBook()
            info.id = query.value(0)
            info.title = query.value(1)
            info.title2 = query.value(2)
            info.author = query.value(3)
            info.chineseTeam = query.value(4)
            info.description = query.value(5)
            info.epsCount = query.value(6)
            info.pages = query.value(7)
            info.finished = query.value(8)
            info.likesCount = query.value(9)
            info.categories = query.value(10)
            info.tags = query.value(11)
            info.created_at = query.value(12)
            info.updated_at = query.value(13)
            info.path = query.value(14)
            info.fileServer = query.value(15)
            info.originalName = query.value(16)
            return info
        return None

    def Update(self, addData, tick, version):
        timeArray = time.localtime(tick)
        strTime = "{}-{}-{} {}:{}:{}".format(timeArray.tm_year, timeArray.tm_mon, timeArray.tm_mday, timeArray.tm_hour, timeArray.tm_min, timeArray.tm_sec)
        sql = "update system set sub_version={}, time='{}' where id='{}'".format(version, strTime, config.UpdateVersion)

        self.db.transaction()
        query = QSqlQuery(self.db)
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
        for book in addData:
            try:
                if not book:
                    continue
                sql = "replace INTO book(id, title, title2, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
                      "created_at, updated_at, path, fileServer, originalName, totalLikes, totalViews) " \
                      "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', {17}, {18}); " \
                    .format(book.id, book.title, book.title2, book.author, book.chineseTeam, book.description,
                            book.epsCount, book.pages, int(book.finished), book.likesCount,
                            book.categories, book.tags, book.created_at, book.updated_at, book.path, book.fileServer,
                            book.originalName, book.totalLikes, book.totalViews)
                sql = sql.replace("\0", "")
                suc = query.exec_(sql)
                if not suc:
                    a = query.lastError().text()
                    Log.Warn(a)
            except Exception as ex:
                Log.Error(ex)

        self.db.commit()
        Log.Info("db: update database, len:{}, version:{}, tick:{} ".format(len(addData), tick, version))
