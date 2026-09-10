from dataclasses import dataclass, replace
from typing import Optional, Tuple

from server.book_mapping import book_projection
from tools.langconv import Converter
from tools.page_result import PageRequest


SEARCH_FIELDS = {
    "title": ("title", "title2"),
    "author": ("author", "chineseTeam"),
    "description": ("description",),
    "tags": ("tags",),
    "categories": ("categories",),
    "creator": ("creator",),
}
SORT_FIELDS = ("updated_at", "created_at", "totalLikes", "totalViews", "epsCount", "pages", "id")


@dataclass(frozen=True)
class SqlStatement:
    sql: str
    params: tuple = ()

    def legacy_sql(self):
        """仅供旧的字符串 SQL 调用入口使用，参数中的引号统一转义。"""
        parts = self.sql.split("?")
        if len(parts) != len(self.params) + 1:
            raise ValueError("SQL 占位符与参数数量不一致")
        result = parts[0]
        for value, part in zip(self.params, parts[1:]):
            if value is None:
                literal = "NULL"
            elif isinstance(value, (int, float)):
                literal = str(value)
            else:
                literal = "'{}'".format(str(value).replace("'", "''"))
            result += literal + part
        return result


def execute_statement(connection, statement):
    if isinstance(statement, SqlStatement):
        return connection.execute(statement.sql, statement.params)
    return connection.execute(statement)


@dataclass(frozen=True)
class BookQuery:
    text: str = ""
    fields: Tuple[str, ...] = tuple(SEARCH_FIELDS)
    categories: Tuple[str, ...] = ()
    finished_only: bool = False
    limit_ids: Optional[Tuple[str, ...]] = None
    sort_field: str = "updated_at"
    descending: bool = True

    def __post_init__(self):
        if any(field not in SEARCH_FIELDS for field in self.fields):
            raise ValueError("未知的搜索字段")
        if self.sort_field not in SORT_FIELDS:
            raise ValueError("未知的排序字段")

    @classmethod
    def from_legacy(cls, text, is_title, is_author, is_description, is_tag,
                    is_category, is_creator, categories, sort_key=0, sort_id=0,
                    finished_only=False, limit_ids=None):
        enabled = (is_title, is_author, is_description, is_tag, is_category, is_creator)
        fields = tuple(field for field, selected in zip(SEARCH_FIELDS, enabled) if selected)
        sort_field = SORT_FIELDS[sort_key] if 0 <= sort_key < 6 else "id"
        return cls(text, fields, tuple(categories), bool(finished_only),
                   tuple(limit_ids) if limit_ids is not None else None, sort_field, sort_id == 0)

    def for_facets(self):
        return replace(self, categories=(), sort_field="id", descending=False)

    def _where(self, include_categories=True):
        text = Converter("zh-hans").convert(self.text).strip(" ")
        optional, required, excluded = [], [], []
        for word in text.split(" "):
            if not word:
                continue
            if word.startswith("+"):
                required.append(word[1:])
            elif word.startswith("-"):
                excluded.append(word[1:])
            else:
                optional.append(word)
        if not required and not excluded:
            optional = [text]

        columns = [column for field in self.fields for column in SEARCH_FIELDS[field]]
        clauses, params = [], []

        def word_clause(word, exclude=False):
            if not columns:
                return "1" if exclude else "0"
            operator, joiner = ("NOT LIKE", " AND ") if exclude else ("LIKE", " OR ")
            params.extend(["%" + word + "%"] * len(columns))
            return "(" + joiner.join(column + " " + operator + " ?" for column in columns) + ")"

        if optional:
            clauses.append("(" + " OR ".join(word_clause(word) for word in optional) + ")")
        clauses.extend(word_clause(word) for word in required)
        clauses.extend(word_clause(word, True) for word in excluded)
        if self.finished_only:
            clauses.append("finished=1")
        if self.limit_ids is not None:
            clauses.append("id IN ({})".format(",".join("?" for _ in self.limit_ids)))
            params.extend(self.limit_ids)
        if include_categories and self.categories:
            clauses.append("(" + " OR ".join("categories LIKE ?" for _ in self.categories) + ")")
            params.extend("%" + Converter("zh-hans").convert(category) + "%" for category in self.categories)
        return " AND ".join(clauses) or "1", tuple(params)

    def statements(self, page: Optional[PageRequest] = None, has_share_id=True):
        """列表与总数共用条件，分类统计仅忽略已勾选分类。"""
        where, params = self._where()
        facet_where, facet_params = self._where(include_categories=False)
        order = self.sort_field + (" DESC" if self.descending else " ASC")
        if self.sort_field != "id":
            order += ", id ASC"
        sql = "SELECT {} FROM book WHERE {} ORDER BY {}".format(book_projection(has_share_id), where, order)
        row_params = params
        if page is not None:
            sql += " LIMIT ? OFFSET ?"
            row_params += (page.page_size, page.offset)
        return (SqlStatement(sql, row_params),
                SqlStatement("SELECT id FROM book WHERE " + facet_where, facet_params),
                SqlStatement("SELECT count(*) FROM book WHERE " + where, params))


def books_by_ids_statement(book_ids, has_share_id=True, metrics_only=False):
    ids = tuple(book_ids)
    projection = "id, created_at, updated_at, epsCount, pages, totalLikes, totalViews" if metrics_only else book_projection(has_share_id)
    return SqlStatement("SELECT {} FROM book WHERE id IN ({})".format(
        projection, ",".join("?" for _ in ids)), ids)


FAVORITE_SORT_FIELDS = ("tick", "updated_at", "created_at", "totalLikes", "totalViews", "epsCount", "pages")
FAVORITE_COLUMNS = ("bookId AS id", "title", "author", "chineseTeam", "description",
                    "epsCount", "pages", "finished", "categories", "tags", "created_at",
                    "updated_at", "path", "fileServer", "tick")


@dataclass(frozen=True)
class FavoriteQuery:
    text: str = ""
    folder_id: int = 0
    sort_field: str = "tick"
    descending: bool = True

    def __post_init__(self):
        if self.sort_field not in FAVORITE_SORT_FIELDS:
            raise ValueError("未知的收藏排序字段")

    @classmethod
    def from_legacy(cls, text="", folder_id=0, sort_key=0, sort_id=0):
        return cls(text, folder_id, FAVORITE_SORT_FIELDS[sort_key], sort_id == 0)

    def statement(self, page: Optional[PageRequest] = None):
        clauses, params = [], []
        if self.folder_id:
            clauses.append("bookId IN (SELECT bookId FROM favorite_fid WHERE fid=?)")
            params.append(self.folder_id)
        if self.text:
            columns = ("title", "author", "description", "tags", "bookId", "categories")
            clauses.append("(" + " OR ".join(column + " LIKE ?" for column in columns) + ")")
            params.extend(["%" + Converter("zh-hans").convert(self.text) + "%"] * len(columns))
        direction = " DESC" if self.descending else " ASC"
        order = []
        if self.sort_field not in ("totalLikes", "totalViews"):
            order.append(self.sort_field + direction)
        if self.sort_field == "updated_at":
            order.append("tick" + direction)
        order.append("bookId ASC")
        sql = "SELECT {} FROM favorite WHERE {} ORDER BY {}".format(
            ", ".join(FAVORITE_COLUMNS), " AND ".join(clauses) or "1", ", ".join(order))
        if page is not None:
            sql += " LIMIT ? OFFSET ?"
            params.extend((page.page_size, page.offset))
        return SqlStatement(sql, tuple(params))
