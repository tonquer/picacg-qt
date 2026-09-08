import json
import os
from pathlib import Path
import pickle
import sqlite3
import sys
from types import ModuleType
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.modules.setdefault("images_rc", ModuleType("images_rc"))

from PySide6.QtWidgets import QApplication

from component.list.base_list_widget import BaseListWidget
from qt_owner import QtOwner
from server.book_mapping import DbBook, book_from_row, books_from_cursor
from server.book_query import BookQuery, FavoriteQuery, books_by_ids_statement, execute_statement
from server.sql_server import DbBook as CompatibilityDbBook, SqlServer
from tools.page_result import PageRequest, PageResult
from tools.status import Status
from view.user.favorite_view import FavoriteView
from view.user.local_favorite_db import LocalFavoriteItem
from tests import test_tasks


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.addCleanup(self.conn.close)
        fields = vars(DbBook())
        self.conn.execute("CREATE TABLE book ({})".format(",".join(fields)))
        rows = [
            ("a", "alpha beta", "全彩", 1),
            ("b", "alpha gamma", "全彩", 0),
            ("c", "beta gamma", "长篇", 1),
            ("d", "alpha beta gamma", "长篇", 1),
            ("e", '作者 "A"? 读本', "全彩", 1),
        ]
        for identity, title, category, finished in rows:
            values = dict(fields)
            values.update(id=identity, title=title, categories=category, finished=finished,
                          updated_at=1, totalLikes=10, totalViews=20)
            self.conn.execute("INSERT INTO book VALUES ({})".format(",".join("?" for _ in values)), tuple(values.values()))

    def rows(self, query):
        statement, _, _ = query.statements()
        return [book.id for book in books_from_cursor(execute_statement(self.conn, statement))]

    def test_query_keeps_phrase_required_and_excluded_word_semantics(self):
        self.assertEqual(self.rows(BookQuery("alpha beta", ("title",))), ["a", "d"])
        self.assertEqual(self.rows(BookQuery("alpha +beta -gamma", ("title",))), ["a"])
        self.assertEqual(self.rows(BookQuery("+beta -gamma", ("title",))), ["a"])
        self.assertEqual(self.rows(BookQuery("-gamma", ("title",))), ["a", "e"])
        self.assertEqual(self.rows(BookQuery("alpha", ())), [])

    def test_parameterized_and_legacy_queries_round_trip_quotes_and_question_marks(self):
        for text, expected in [('作者 "A"? 读本', ["e"]), ("' OR 1=1 --", [])]:
            query = BookQuery(text, ("title",))
            rows, _, count = query.statements(PageRequest(1))
            self.assertEqual([row[0] for row in execute_statement(self.conn, rows)], expected)
            self.assertEqual([row[0] for row in self.conn.execute(rows.legacy_sql())], expected)
            self.assertEqual(execute_statement(self.conn, count).fetchone()[0], len(expected))
        self.assertEqual(self.conn.execute("SELECT count(*) FROM book").fetchone()[0], 5)

    def test_count_facets_and_rows_keep_one_base_filter(self):
        query = BookQuery("", ("title",), ("全彩",), True, ("a", "b", "c", "d"))
        rows, facets, count = query.statements()
        self.assertEqual([row[0] for row in execute_statement(self.conn, rows)], ["a"])
        self.assertEqual(execute_statement(self.conn, count).fetchone()[0], 1)
        self.assertEqual({row[0] for row in execute_statement(self.conn, facets)}, {"a", "c", "d"})
        empty = BookQuery(limit_ids=())
        self.assertEqual(self.rows(empty), [])
        self.assertEqual(query.for_facets().categories, ())
        self.assertTrue(query.for_facets().finished_only)

    def test_projection_and_named_mapping_support_old_database_and_metrics(self):
        self.conn.execute("ALTER TABLE book DROP COLUMN shareId")
        statement, _, _ = BookQuery("alpha", ("title",)).statements(has_share_id=False)
        books = books_from_cursor(execute_statement(self.conn, statement))
        self.assertEqual([book.id for book in books], ["a", "b", "d"])
        self.assertTrue(all(book.shareId == 0 for book in books))
        metrics = books_by_ids_statement(["a"], metrics_only=True)
        self.assertEqual([column[0] for column in execute_statement(self.conn, metrics).description],
                         ["id", "totalLikes", "totalViews"])
        book = books_from_cursor(self.conn.execute("SELECT totalViews, id, totalLikes FROM book WHERE id='a'"))[0]
        self.assertEqual((book.id, book.totalLikes, book.totalViews), ("a", 10, 20))

    def test_mapping_retains_unknown_metrics_and_defaults_other_nulls(self):
        book = book_from_row(["bookId", "title", "finished", "pages", "totalLikes", "totalViews", "tick"],
                             ["id", None, None, None, None, 0, 123], LocalFavoriteItem)
        self.assertEqual((book.id, book.title, book.finished, book.pagesCount, book.tick), ("id", "", False, 0, 123))
        self.assertIsNone(book.totalLikes)
        self.assertEqual(book.totalViews, 0)
        self.assertEqual(book.shareId, 0)

    def test_legacy_import_and_pickle_still_resolve_db_book(self):
        self.assertIs(CompatibilityDbBook, DbBook)
        book = DbBook()
        book.id = "saved"
        with patch.object(DbBook, "__module__", "server.sql_server"):
            legacy_pickle = pickle.dumps(book)
        restored = pickle.loads(legacy_pickle)
        self.assertIsInstance(restored, DbBook)
        self.assertEqual(restored.id, "saved")

    def test_favorite_statement_preserves_folder_and_search_columns(self):
        self.conn.execute("CREATE TABLE favorite (bookId, title, author, chineseTeam, description, epsCount, pages, finished, categories, tags, created_at, updated_at, path, fileServer, tick)")
        self.conn.execute("CREATE TABLE favorite_fid (fid, bookId)")
        self.conn.execute("INSERT INTO favorite VALUES ('x', 'abc?', '', '', '', 1, 2, 0, '全彩', '', 1, 2, '', '', 3)")
        self.conn.execute("INSERT INTO favorite VALUES ('y', 'abc?', '', '', '', 1, 2, 0, '全彩', '', 1, 2, '', '', 4)")
        self.conn.execute("INSERT INTO favorite_fid VALUES (7, 'x')")
        criteria = FavoriteQuery(text="abc?", folder_id=7)
        statement = criteria.statement(PageRequest(1, 100))
        result = books_from_cursor(execute_statement(self.conn, statement))
        self.assertEqual([book.id for book in result], ["x"])
        self.assertEqual(result[0].tick, 3)

    def test_page_result_preserves_local_size_and_remote_page_metadata(self):
        for size in (20, 100, 30):
            result = PageResult.from_total([], PageRequest(9, size), size * 2)
            self.assertEqual((result.page, result.pages, result.total, result.page_size), (2, 2, size * 2, size))
        result = PageResult.from_remote({"docs": [1, 2], "page": 3, "pages": 7, "total": 50})
        self.assertEqual((result.page, result.pages, result.total, result.page_size), (3, 7, 50, None))
        result = PageResult.from_remote({"docs": [], "page": 1, "pages": 0, "total": 0, "limit": 12})
        self.assertEqual((result.page, result.pages, result.page_size), (1, 1, 12))


class QueryWorkerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.worker_tests = test_tasks.SqlLifecycleTests()
        self.worker_tests.setUp()
        self.addCleanup(self.worker_tests.doCleanups)

    def test_real_worker_emits_one_serializable_page_result(self):
        result = self.worker_tests.run_requests([
            (SqlServer.TaskTypeSelectBookPage, (BookQuery("示例", ("title",)), PageRequest(5, 20))),
            (SqlServer.TaskTypeCategoryBookNum, BookQuery("示例", ("title",)).statements()[1]),
        ])
        page = result[0]
        self.assertIsInstance(page, PageResult)
        self.assertEqual((page.page, page.pages, page.total, page.page_size), (1, 1, 1, 20))
        self.assertEqual([book.id for book in page.items], ["book"])
        self.assertEqual(result[1], {"测试分类": 1})

    def test_real_worker_page_error_notifies_once_and_continues(self):
        result = self.worker_tests.run_requests([
            (SqlServer.TaskTypeSql, "DROP TABLE book"),
            (SqlServer.TaskTypeSelectBookPage, (BookQuery(), PageRequest())),
            (SqlServer.TaskTypeSelectWord, ""),
        ])
        self.assertIsNone(result[1])
        self.assertEqual(result[2], ["词条"])
        result = self.worker_tests.run_requests([
            (SqlServer.TaskTypeSelectBookPage, (BookQuery(), PageRequest()))
        ], missing=True)
        self.assertIsNone(result[0])

    def test_real_worker_page_mapping_without_share_id(self):
        self.worker_tests.connection.execute("ALTER TABLE book DROP COLUMN shareId")
        self.worker_tests.connection.commit()
        result = self.worker_tests.run_requests([
            (SqlServer.TaskTypeSelectBookPage, (BookQuery(), PageRequest())),
            (SqlServer.TaskTypeCacheBook, "book"),
        ])
        self.assertEqual(result[0].items[0].shareId, 0)
        self.assertEqual(result[1]["bookList"][0].shareId, 0)


class OnlineFavoritePaginationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_failure_and_malformed_response_retry_same_page(self):
        with patch.object(QtOwner, "ShowLoading"), patch.object(QtOwner, "CloseLoading"), \
                patch.object(QtOwner, "ShowError"), patch.object(BaseListWidget, "ClearTask"), \
                patch("view.user.favorite_view.req.FavoritesReq", side_effect=lambda page, sort: page), \
                patch("view.user.favorite_view.Log.Error"):
            view = FavoriteView()
            self.addCleanup(view.close)
            requests = []
            view.AddHttpTask = lambda request, callback, pending: requests.append((request, callback, pending))
            view.bookList.AddBookByDict = lambda book: view.bookList.ValueChange(view.bookList.verticalScrollBar().maximum())
            view.bookList.UpdatePage(1, 3)
            for payload in ({"st": Status.Error}, {"st": Status.Ok, "data": "invalid"}):
                view.bookList.RequestNextPage()
                self.assertEqual(requests[-1][0], 2)
                self.assertEqual(view.bookList.page, 1)
                self.assertTrue(view.bookList.isLoadingPage)
                _, callback, pending = requests[-1]
                callback(payload, pending)
                self.assertFalse(view.bookList.isLoadingPage)
                self.assertEqual(view.bookList.page, 1)
            view.bookList.RequestNextPage()
            _, callback, pending = requests[-1]
            callback({"st": Status.Ok, "data": json.dumps({"data": {"comics": {
                "docs": [{"_id": "book"}], "page": 2, "pages": 3, "total": 30}}})}, pending)
            self.assertEqual([request[0] for request in requests], [2, 2, 2])
            self.assertEqual(view.bookList.page, 2)
            self.assertFalse(view.bookList.isLoadingPage)
            view.bookList.RequestNextPage()
            self.assertEqual(requests[-1][0], 3)


if __name__ == "__main__":
    unittest.main()
