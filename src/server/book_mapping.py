BOOK_COLUMNS = (
    "id", "title", "title2", "author", "chineseTeam", "description", "epsCount",
    "pages", "finished", "likesCount", "categories", "tags", "created_at",
    "updated_at", "path", "fileServer", "creator", "totalLikes", "totalViews", "shareId",
)


class DbBook:
    def __init__(self):
        self.id = ""
        self.shareId = 0
        self.title = ""
        self.title2 = ""
        self.author = ""
        self.chineseTeam = ""
        self.description = ""
        self.epsCount = 0
        self.pages = 0
        self.finished = False
        self.categories = ""
        self.tags = ""
        self.likesCount = 0
        self.created_at = 0
        self.updated_at = 0
        self.path = ""
        self.fileServer = ""
        self.originalName = ""
        self.creator = ""
        self.totalLikes = 0
        self.totalViews = 0

    @property
    def pagesCount(self):
        return self.pages

    def CopyFromJson(self, data):
        for key, value in data.items():
            setattr(self, key, value)


def book_projection(has_share_id=True, alias=""):
    """旧库缺少分享编号时提供同名默认列，避免改变结果列的含义。"""
    prefix = alias + "." if alias else ""
    return ", ".join("0 AS shareId" if field == "shareId" and not has_share_id
                     else prefix + field for field in BOOK_COLUMNS)


def book_from_row(columns, row, factory=DbBook):
    """SQLite 和 Qt SQL 均先取列名，再使用同一套书籍映射。"""
    book = factory()
    for column, value in zip(columns, row):
        field = "id" if column == "bookId" else column
        if value is None and field not in ("totalLikes", "totalViews"):
            continue
        if hasattr(book, field) or field == "tick":
            setattr(book, field, value)
    book.finished = bool(book.finished)
    return book


def books_from_cursor(cursor):
    columns = [column[0] for column in cursor.description]
    return [book_from_row(columns, row) for row in cursor.fetchall()]
