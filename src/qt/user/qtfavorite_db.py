import time

from PySide2.QtSql import QSqlQuery, QSqlDatabase

from src.user.user import User
from src.util import Log


# 一本书
class DbFavorite(object):
    def __init__(self):
        self.id = ""              # 唯一标识
        self.title = ""           # 标题
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
        self.totalLikes = 0
        self.totalViews = 0
        self.lastUpdateTick = 0   # 上次更新时间
        self.sortId = 0           # 排序使用


class QtFavoriteDb(object):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        self.db = QSqlDatabase.addDatabase("QSQLITE", "favorite")
        self.db.setDatabaseName("data/favorite.db")
        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists favorite(\
            id varchar,\
            user varchar,\
            title varchar,\
            author varchar,\
            chineseTeam varchar,\
            description varchar,\
            epsCount int, \
            pages int, \
            finished int,\
            likesCount int,\
            categories varchar,\
            tags varchar,\
            created_at varchar,\
            updated_at varchar,\
            path varchar,\
            fileServer varchar,\
            originalName varchar,\
            totalLikes int,\
            totalViews int,\
            lastUpdateTick int,\
            sortId int
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

        sql = """\
            CREATE UNIQUE INDEX id_user ON favorite (\
            id, \
            user\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

        self.allFavoriteIds = dict()
        self.needUpdatefavorite = []
        self.maxSortId = 0

    def LoadAllFavorite(self):
        query = QSqlQuery(self.db)
        sql = "select * from favorite where user ='{}'".format(User().userId)
        suc = query.exec_(sql)
        now = int(time.time())
        while query.next():
            # bookId, name, epsId, index, url, path
            bookId = query.value(0)
            lastUpdateTick = query.value(19)
            # sortId = query.value(20)
            # self.maxSortId = min(sortId, self.maxSortId)
            if now - lastUpdateTick >= 3600:
                self.needUpdatefavorite.append(bookId)
            self.allFavoriteIds[bookId] = 0
        return

    def UpdateSortId(self, bookId):
        self.maxSortId += 1
        self.allFavoriteIds[bookId] = self.maxSortId
        return self.maxSortId

    def UpdateFavorite(self, book):
        assert isinstance(book, DbFavorite)
        self.allFavoriteIds[book.id] = book.sortId
        query = QSqlQuery(self.db)
        sql = "replace INTO favorite(id, user, title, author, chineseTeam, description, epsCount, pages, finished, likesCount, categories, tags," \
              "created_at, updated_at, path, fileServer, originalName, totalLikes, totalViews, lastUpdateTick, sortId) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', {17}, {18}, {19}, {20}) " \
            .format(book.id, User().userId, book.title, book.author, book.chineseTeam, book.description, book.epsCount, book.pages, int(book.finished), book.likesCount,
                   book.categories, book.tags, book.created_at, book.updated_at, book.path, book.fileServer, book.originalName, book.totalLikes, book.totalViews, book.lastUpdateTick, book.sortId)
        sql = sql.replace("\0", "")
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def DelFavorite(self, bookId):
        query = QSqlQuery(self.db)
        sql = "delete from favorite where id='{}' and user='{}'".format(bookId, User().userId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())

        if bookId in self.allFavoriteIds:
            sortId = self.allFavoriteIds[bookId]
            self.allFavoriteIds.pop(bookId)
            if (sortId, bookId) in self.needUpdatefavorite:
                self.needUpdatefavorite.remove((sortId, bookId))
        return

    def Search(self, page, sortKey=0, sortId=0):
        query = QSqlQuery(self.db)

        sql = "SELECT * FROM favorite WHERE user='{}' ".format(User().userId)
        if sortKey == 0:
            sql += "ORDER BY updated_at "

        elif sortKey == 1:
            sql += "ORDER BY sortId "
        elif sortKey == 2:
            sql += "ORDER BY created_at "
        elif sortKey == 3:
            sql += "ORDER BY totalLikes "
        elif sortKey == 4:
            sql += "ORDER BY totalViews "
        elif sortKey == 5:
            sql += "ORDER BY epsCount "
        elif sortKey == 6:
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
            info = DbFavorite()
            info.id = query.value(0)
            info.title = query.value(2)
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
            books.append(info)
        return books

    def Update(self, addData):
        self.db.transaction()
        query = QSqlQuery(self.db)
        for book in addData:
            try:
                if not book:
                    continue
                sql = "update favorite set title='{0}', author='{2}', chineseTeam='{3}', description='{4}', epsCount={5}, pages={6}, finished='{7}', likesCount={8}, categories='{9}', tags='{10}'," \
                      "created_at='{11}', updated_at='{12}', path='{13}', fileServer='{14}', originalName='{15}', totalLikes={16}, totalViews={17} where id='{18}';" \
                    .format(book.title, book.title2, book.author, book.chineseTeam, book.description,
                            book.epsCount, book.pages, int(book.finished), book.likesCount,
                            book.categories, book.tags, book.created_at, book.updated_at, book.path, book.fileServer,
                            book.originalName, book.totalLikes, book.totalViews, book.id)
                sql = sql.replace("\0", "")
                suc = query.exec_(sql)
                if not suc:
                    a = query.lastError().text()
                    Log.Warn(a)
            except Exception as ex:
                Log.Error(ex)

        self.db.commit()
        Log.Info("db: update favorite database, len:{} ".format(len(addData)))