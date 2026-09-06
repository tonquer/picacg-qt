import os
from pathlib import Path
import sqlite3
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
# 测试源代码时无需编译图片资源，业务模块保持真实导入。
sys.modules.setdefault("images_rc", types.ModuleType("images_rc"))

from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QApplication, QLabel, QSpinBox

from component.list.base_list_widget import BaseListWidget
from qt_owner import QtOwner
from server.sql_server import DbBook, SqlServer
from tools.pagination import page_count
from view.search.search_view import SearchView, _WAITING_PAGE_RESULT
from view.tool.local_read_view import LocalReadView
from view.user.history_view import HistoryView
from view.user.local_favorite_db import LocalFavoriteDb
from view.user.local_favorite_view import LocalFavoriteView


class PaginationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.patches = [patch.object(QtOwner, name) for name in ("ShowLoading", "CloseLoading", "ShowError", "ShowMsg")]
        self.patches.append(patch.object(BaseListWidget, "ClearTask"))
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)
        self.owner = QtOwner()
        self.addCleanup(setattr, self.owner, "canUseDb", self.owner.canUseDb)
        self.addCleanup(setattr, self.owner, "isDbHavePicaID", self.owner.isDbHavePicaID)
        self.owner.canUseDb = True
        self.owner.isDbHavePicaID = True
        self.main = sqlite3.connect(":memory:")
        self.addCleanup(self.main.close)
        fields = vars(DbBook())
        self.main.execute("CREATE TABLE book ({})".format(",".join(fields)))
        for index in range(225):
            values = dict(fields)
            values.update(id=f"{index:03}", title="示例", finished=index % 2,
                          categories="全彩" if index < 120 else "长篇", updated_at=1,
                          totalLikes=index, totalViews=225 - index)
            self.main.execute("INSERT INTO book VALUES ({})".format(",".join("?" for _ in fields)), tuple(values.values()))

    def main_books(self, sql):
        cursor = self.main.execute(sql)
        books = []
        for row in cursor:
            book = DbBook()
            for column, value in zip(cursor.description, row):
                if hasattr(book, column[0]):
                    setattr(book, column[0], value)
            books.append(book)
        return books

    def favorite_db(self, count=225):
        database = LocalFavoriteDb.__new__(LocalFavoriteDb)
        name = "pagination-" + uuid4().hex
        database.db = QSqlDatabase.addDatabase("QSQLITE", name)
        database.db.setDatabaseName(":memory:")
        self.assertTrue(database.db.open())
        self.addCleanup(database.db.close)
        query = QSqlQuery(database.db)
        self.assertTrue(query.exec_("CREATE TABLE favorite (bookId TEXT, title TEXT, author TEXT, chineseTeam TEXT, description TEXT, epsCount INTEGER, pages INTEGER, finished INTEGER, categories TEXT, tags TEXT, created_at INTEGER, updated_at INTEGER, path TEXT, fileServer TEXT, tick INTEGER)"))
        self.assertTrue(query.exec_("CREATE TABLE favorite_fid (fid INTEGER, bookId TEXT)"))
        self.assertTrue(query.exec_("CREATE TABLE favorite_fold (fid INTEGER, name TEXT)"))
        self.assertTrue(query.exec_("INSERT INTO favorite_fold VALUES (1, '文件夹')"))
        for index in range(count):
            self.assertTrue(query.prepare("INSERT INTO favorite VALUES (?, ?, '', '', '', ?, ?, 0, '全彩', '', ?, ?, '', '', ?)"))
            for value in (f"{index:03}", "匹配" if index < 15 else "其他", index, index * 2, index, index % 2, index):
                query.addBindValue(value)
            self.assertTrue(query.exec_())
            if index < 12:
                self.assertTrue(query.exec_(f"INSERT INTO favorite_fid VALUES (1, '{index:03}')"))
        return database

    def favorite_view(self, count=225):
        database = self.favorite_db(count)
        with patch("view.user.local_favorite_view.LocalFavoriteDb", return_value=database):
            view = LocalFavoriteView()
        view._shown = []
        view.bookList.AddBookItemByDbBook = lambda book, **kwargs: view._shown.append(book.id)
        original_clear = view.bookList.clear
        def clear():
            view._shown.clear()
            original_clear()
        view.bookList.clear = clear
        view._queries = []
        def query(table, sql, task_type, callback=None, pending=None, **kwargs):
            view._queries.append(sql)
            callback(self.main_books(sql), pending)
        view.AddSqlTask = query
        self.addCleanup(view.close)
        return view

    def test_page_count_boundaries(self):
        for size in (20, 100, 30):
            for total, expected in ((0, 1), (1, 1), (size - 1, 1), (size, 1), (size + 1, 2), (size * 2, 2)):
                with self.subTest(size=size, total=total):
                    self.assertEqual(page_count(total, size), expected)

    def test_search_count_and_facets_share_base_conditions(self):
        ids = [f"{i:03}" for i in range(150)]
        sql, facets, count = SqlServer.Search2("示例", True, False, False, False, False, False,
                                             ["全彩"], 1, isFinish=True, limitIds=ids)
        self.assertEqual(len(self.main.execute(sql).fetchall()), 20)
        self.assertEqual(self.main.execute(count).fetchone()[0], 60)
        self.assertEqual(len(self.main.execute(facets).fetchall()), 75)
        sql, facets, count = SqlServer.Search2("示例", True, False, False, False, False, False,
                                             [], 1, isFinish=True, limitIds=[])
        self.assertEqual(self.main.execute(sql).fetchall(), [])
        self.assertEqual(self.main.execute(count).fetchone()[0], 0)
        self.assertEqual(self.main.execute(facets).fetchall(), [])

    def test_search_stable_pages_and_old_schema(self):
        result = []
        for page in (1, 2):
            sql, _, _ = SqlServer.Search2("示例", True, False, False, False, False, False, [], page)
            result.extend(row[0] for row in self.main.execute(sql))
        self.assertEqual(result, [f"{i:03}" for i in range(40)])
        self.main.execute("ALTER TABLE book DROP COLUMN shareId")
        self.owner.isDbHavePicaID = False
        sql, _, _ = SqlServer.Search2("示例", True, False, False, False, False, False, [], 1)
        self.assertEqual(len(self.main.execute(sql).fetchall()), 20)

    def test_search_waits_for_rows_and_count_in_both_orders(self):
        view = SearchView()
        self.addCleanup(view.close)
        view.bookList.AddBookItemByDbBook = lambda book: None
        for count_first in (False, True):
            view.SetPageLoading(True)
            pending = {"page": 1, "books": _WAITING_PAGE_RESULT, "total": _WAITING_PAGE_RESULT}
            first, second = ((view.ReceiveLocalTotal, 40), (view.ReceiveLocalBooks, [])) if count_first else ((view.ReceiveLocalBooks, []), (view.ReceiveLocalTotal, 40))
            first[0](first[1], pending)
            self.assertTrue(view.bookList.isLoadingPage)
            second[0](second[1], pending)
            self.assertFalse(view.bookList.isLoadingPage)
            self.assertEqual(view.bookList.pages, 2)
            self.assertEqual(view.spinBox.maximum(), 2)
        view.bookList.UpdatePage(3, 5)
        view.ResetSearch()
        self.assertEqual(view.bookList.page, 1)
        view.bookList.UpdatePage(1, 5)
        view.spinBox.setMaximum(5)
        view.spinBox.setValue(3)
        sent = []
        view.SendSearch = sent.append
        view.JumpPage()
        self.assertEqual(sent, [3])

    def test_search_failure_releases_page_lock_and_facets_use_full_query(self):
        view = SearchView()
        self.addCleanup(view.close)
        view.bookList.UpdatePage(1, 3)
        view.SetPageLoading(True)
        pending = {"page": 2, "books": _WAITING_PAGE_RESULT, "total": _WAITING_PAGE_RESULT}
        view.ReceiveLocalBooks(None, pending)
        self.assertFalse(view.bookList.isLoadingPage)
        view.ReceiveLocalTotal(60, pending)
        self.assertFalse(view.bookList.isLoadingPage)
        self.assertEqual(view.bookList.page, 1)
        queries = []
        view.AddSqlTask = lambda *args: queries.append(args)
        view.UpdateFacetCounts("SELECT 1", ("category", "全彩"))
        view.UpdateFacetCounts("SELECT 1", ("category", "全彩"))
        view.UpdateFacetCounts("SELECT 1", ("category", "长篇"))
        self.assertEqual(len(queries), 2)

    def test_search_does_not_request_more_pages_while_inserting_rows(self):
        view = SearchView()
        self.addCleanup(view.close)
        requests = []
        view.bookList.LoadCallBack = lambda: requests.append(True)
        view.bookList.pages = 3
        view.bookList.AddBookItemByDbBook = lambda book: view.bookList.ValueChange(view.bookList.verticalScrollBar().maximum())
        view.SendLocalBack([DbBook(), DbBook()], 1)
        self.assertEqual(requests, [])
        self.assertFalse(view.bookList.isLoadingPage)

    def test_both_scroll_inputs_guard_loading_last_page_and_retry(self):
        view = BaseListWidget(None)
        self.addCleanup(view.close)
        requests = []
        view.LoadCallBack = lambda: requests.append(view.page + 1)
        view.UpdatePage(1, 2)
        view.ValueChange(view.verticalScrollBar().maximum())
        view.OnActionTriggered()
        self.assertEqual(requests, [2])
        view.UpdateState(False)
        view.OnActionTriggered()
        self.assertEqual(requests, [2, 2])
        view.UpdatePage(2, 2)
        view.ValueChange(view.verticalScrollBar().maximum())
        self.assertEqual(requests, [2, 2])

    def test_favorite_filter_count_page_size_and_query_reset(self):
        view = self.favorite_view()
        view.RefreshDataFocus()
        self.assertEqual((len(view._shown), view.bookList.pages), (100, 3))
        view.LoadNextPage()
        self.assertEqual((len(view._shown), view.bookList.page), (200, 2))
        view.SearchTextChange("匹配")
        self.assertEqual((len(view._shown), view.bookList.page, view.bookList.pages), (15, 1, 1))
        view.InitFolder()
        view.folderBox.setCurrentIndex(1)
        self.assertEqual((len(view._shown), view.bookList.pages), (12, 1))
        self.assertEqual(view.spinBox.maximum(), 1)

    def test_favorite_global_metric_sort_snapshot_and_missing_rows(self):
        view = self.favorite_view()
        self.main.execute("DELETE FROM book WHERE id='224'")
        view.sortKeyCombox.setCurrentIndex(3)
        self.assertEqual(view._shown, [f"{i:03}" for i in range(223, 123, -1)])
        metric_queries = sum("totalLikes, totalViews" in sql and "'', ''" in sql for sql in view._queries)
        view.LoadNextPage()
        view.LoadNextPage()
        self.assertEqual(len(view._shown), 225)
        self.assertEqual(view._shown[-1], "224")
        self.assertEqual(sum("totalLikes, totalViews" in sql and "'', ''" in sql for sql in view._queries), metric_queries)
        self.assertEqual(len(set(view._shown)), 225)
        view.sortIdCombox.setCurrentIndex(1)
        self.assertEqual(view._shown[:3], ["000", "001", "002"])
        self.owner.canUseDb = False
        view.RefreshDataFocus()
        self.assertEqual(view.sortKeyCombox.currentIndex(), 0)
        self.assertFalse(view.sortKeyCombox.model().item(3).isEnabled())
        self.assertFalse(view.sortKeyCombox.model().item(4).isEnabled())

    def test_favorite_all_local_sorts_are_global_before_limit(self):
        database = self.favorite_db()
        for key in (0, 2, 5, 6):
            books = database.SearchFavorite(1, key, 0)
            self.assertEqual([book.id for book in books], [f"{i:03}" for i in range(224, 124, -1)])
        books = database.SearchFavorite(1, 1, 0)
        self.assertEqual([book.id for book in books[:3]], ["223", "221", "219"])

    def test_history_and_local_book_exact_pages_and_shrink(self):
        listed = []
        book_list = BaseListWidget(None)
        self.addCleanup(book_list.close)
        book_list.AddBookItemByHistory = lambda book: listed.append(book.bookId)
        history = SimpleNamespace(history={str(i): SimpleNamespace(bookId=str(i), tick=i) for i in range(40)},
                                  pageNums=20, bookList=book_list, spinBox=QSpinBox(), UpdatePageLabel=lambda: None)
        HistoryView.RefreshData(history, 2)
        self.assertEqual((book_list.page, book_list.pages, history.spinBox.maximum(), len(listed)), (2, 2, 2, 20))
        history.history = {}
        HistoryView.RefreshData(history, 2)
        self.assertEqual((book_list.page, book_list.pages, history.spinBox.maximum()), (1, 1, 1))
        shown = []
        book_list.AddBookByLocal = lambda book, category: shown.append(book.id)
        local = SimpleNamespace(sortAllBookIds=list(range(60)), allBookInfos={i: SimpleNamespace(id=i, title="书") for i in range(60)},
                                bookCategory={}, bookList=book_list, spinBox=QSpinBox(), pages=QLabel(), nums=QLabel(), searchText="")
        LocalReadView.ShowPages(local, 2)
        self.assertEqual((book_list.page, book_list.pages, local.spinBox.maximum(), len(shown)), (2, 2, 2, 30))


if __name__ == "__main__":
    unittest.main()
