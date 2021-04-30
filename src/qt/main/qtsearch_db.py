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
        self.categories = []      # 分类
        self.tags = []            # tag
        self.likesCount = 0       # 爱心数
        self.created_at = 0       # 创建时间
        self.updated_at = 0       # 更新时间
        self.path = ""            # 路径
        self.fileServer = ""             # 路径
        self.originalName = ""    # 封面名


class QtSearchDb(object):
    def __init__(self, owner):
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
        while query.next():
            if config.UpdateVersion == query.value(0):
                nums = query.value(1)
                time = query.value(2)
        return nums, time

    def Search(self, word, isTitle, isAutor, isDes, isTag, isCategory, page, sortKey=0, sortId=0):
        query = QSqlQuery(self.db)
        data = ""
        if isTitle:
            data += " or title2 like '%{}%' ".format(word)
        if isAutor:
            data += " or author like '%{}%' ".format(word)
        if isDes:
            data += " or description like '%{}%' ".format(word)
        if isTag:
            data += " or tags like '%{}%' ".format(word)
        if isCategory:
            data += " or categories like '%{}%' ".format(word)
        sql = "SELECT * FROM book WHERE 0 {}".format(data)
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
            info.created_at = query.value(12)
            info.updated_at = query.value(13)
            info.path = query.value(14)
            info.fileServer = query.value(15)
            info.originalName = query.value(16)
            books.append(info)
        return books
