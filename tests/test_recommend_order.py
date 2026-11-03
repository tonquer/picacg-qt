import json
import os
from pathlib import Path
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
# 测试源代码时无需编译图片资源，业务模块保持真实导入。
sys.modules.setdefault("images_rc", types.ModuleType("images_rc"))

from PySide6.QtWidgets import QApplication

from server.book_mapping import book_from_comic
from server.book_query import RECOMMEND_SORT_FIELDS, order_books_by_ids, sort_books
from tools.str import Str
from view.search.search_view import SearchView


def books(*ids, **fields):
    return [SimpleNamespace(id=i, **{k: v[n] for k, v in fields.items()}) for n, i in enumerate(ids)]


class RecommendOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_keeps_recommend_order_and_reports_missing(self):
        # IN 查询按主键顺序返回，推荐顺序是 c, a, d, b
        ordered, missing = order_books_by_ids(books("a", "b", "c"), ["c", "a", "d", "b", "a"])
        self.assertEqual([v.id for v in ordered], ["c", "a", "b"])
        self.assertEqual(missing, ["d"])

    def test_sort_books_by_field_keeps_rank_and_puts_missing_last(self):
        items = books("a", "b", "c", "d", totalLikes=[5, None, 9, 5],
                      updated_at=["2024-01-01T00:00:00.000Z", 0, "2026-01-01T00:00:00.000Z", "2025-01-01T00:00:00.000Z"])
        self.assertEqual([v.id for v in sort_books(items, "")], ["a", "b", "c", "d"])
        self.assertEqual([v.id for v in sort_books(items, "totalLikes")], ["c", "a", "d", "b"])
        self.assertEqual([v.id for v in sort_books(items, "totalLikes", False)], ["a", "d", "c", "b"])
        self.assertEqual([v.id for v in sort_books(items, "updated_at")], ["c", "d", "a", "b"])

    def test_book_from_comic_maps_server_fields(self):
        book = book_from_comic({"_id": "x", "title": "标题", "pagesCount": 30, "epsCount": 2, "totalLikes": 7,
                                "categories": ["全彩", "长篇"], "updated_at": "2026-01-01T00:00:00.000Z",
                                "thumb": {"fileServer": "https://s", "path": "x.jpg"}})
        self.assertEqual((book.id, book.title, book.pages, book.epsCount, book.totalLikes, book.likesCount),
                         ("x", "标题", 30, 2, 7, 7))
        self.assertEqual((book.categories, book.fileServer, book.path), ("全彩,长篇", "https://s", "x.jpg"))

    def view(self, source=(2, "src"), ids=()):
        view = SimpleNamespace(recommendSource=source, recommendIds=list(ids), recommendFound={},
                               recommendPending=0, AddHttpTask=Mock(), FinishRecommendBooks=Mock(),
                               OpenRecommendationBack3=Mock())
        view.FillRecommendBooks = lambda source, ids, fallback: SearchView.FillRecommendBooks(view, source, ids, fallback)
        return view

    def test_local_result_is_reordered_and_missing_books_fetched(self):
        view = self.view(ids=["b", "new", "a"])
        SearchView.OpenLocalRecommendationBack(view, books("a", "b"), ((2, "src"), {}))
        self.assertEqual(list(view.recommendFound), ["b", "a"])
        self.assertEqual(view.recommendPending, 1)
        self.assertEqual(view.AddHttpTask.call_args[0][2], ((2, "src"), "new"))
        view.FinishRecommendBooks.assert_not_called()

    def test_fallback_and_network_results_finish_once(self):
        view = self.view(ids=["x", "y"])
        fallbackBook = SimpleNamespace(id="x")
        SearchView.FillRecommendBooks(view, (2, "src"), ["x", "y"], {"x": fallbackBook})
        self.assertIs(view.recommendFound["x"], fallbackBook)
        raw = {"st": Str.Ok, "data": json.dumps({"data": {"comic": {"_id": "y", "title": "Y"}}})}
        SearchView.OpenRecommendationBack3(view, raw, ((2, "src"), "y"))
        self.assertEqual(view.recommendFound["y"].title, "Y")
        view.FinishRecommendBooks.assert_called_once_with()

    def test_stale_result_from_previous_list_is_ignored(self):
        view = self.view(source=(2, "other"), ids=["a", "new"])
        SearchView.OpenLocalRecommendationBack(view, books("a"), ((2, "src"), {}))
        SearchView.OpenRecommendationBack3(view, {"st": Str.Ok, "data": "{}"}, ((2, "src"), "new"))
        self.assertEqual((view.recommendFound, view.AddHttpTask.called), ({}, False))
        view.FinishRecommendBooks.assert_not_called()

    def test_also_viewed_uses_api_books_as_fallback_in_order(self):
        calls = []
        view = SimpleNamespace(recommendSource=(1, "src"), LoadRecommendBooks=lambda *args: calls.append(args))
        raw = {"data": json.dumps({"data": {"comics": [{"_id": "b", "title": "B"}, {"_id": "a", "title": "A"}]}})}
        SearchView.OpenRecommendationBack(view, raw, "src")
        source, ids, fallback = calls[0]
        self.assertEqual((source, ids, fallback["a"].title), ((1, "src"), ["b", "a"], "A"))
        SearchView.OpenRecommendationBack(view, raw, "other")
        self.assertEqual(len(calls), 1)

    def test_recommend_page_is_sorted_and_paged_locally(self):
        pages = []
        items = books(*["b{}".format(i) for i in range(25)], totalLikes=list(range(25)))
        view = SimpleNamespace(recommendBooks=items,
                               recommendSortKey=SimpleNamespace(currentIndex=lambda: RECOMMEND_SORT_FIELDS.index("totalLikes")),
                               sortId=SimpleNamespace(currentIndex=lambda: 0),
                               bookList=SimpleNamespace(AddBookItemByDbBook=Mock()),
                               ApplyPageResult=lambda result, add: pages.append(result))
        SearchView.ShowRecommendPage(view, 1)
        SearchView.ShowRecommendPage(view, 2)
        self.assertEqual([(r.page, r.pages, len(r.items)) for r in pages], [(1, 2, 20), (2, 2, 5)])
        self.assertEqual((pages[0].items[0].id, pages[1].items[-1].id), ("b24", "b0"))


if __name__ == "__main__":
    unittest.main()
