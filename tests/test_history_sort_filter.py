import os
from pathlib import Path
import sys
import types
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
# 测试源代码时无需编译图片资源，业务模块保持真实导入。
sys.modules.setdefault("images_rc", types.ModuleType("images_rc"))

from PySide6.QtWidgets import QApplication

from component.list.comic_list_widget import ComicListWidget
from tools.str import Str
from view.user.history_view import filter_and_sort_history, history_has_update, history_show_title, iso_to_tick


def tick(text):
    return int(datetime.strptime(text, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())


def history(bookId, name, readDay):
    return SimpleNamespace(bookId=bookId, name=name, tick=tick(readDay), epsId=0)


def info(bookId, title, updated, totalLikes=None, title2=""):
    return SimpleNamespace(id=bookId, title=title, title2=title2, totalLikes=totalLikes,
                           updated_at="{}T00:00:00.000Z".format(updated) if updated else 0)


class HistorySortFilterTests(unittest.TestCase):
    def setUp(self):
        self.histories = [history("a", "旧标题", "2026-01-03"), history("b", "漫畫乙", "2026-01-02"),
                          history("c", "丙", "2026-01-01"), history("d", "不在书库", "2026-01-04")]
        self.infos = {"a": info("a", "正确标题甲", "2026-02-01", 5),
                      "b": info("b", "漫畫乙", "2025-12-01", 9),
                      "c": info("c", "丙", "2026-01-05", None)}

    def ids(self, **kwargs):
        return [h.bookId for h in filter_and_sort_history(self.histories, self.infos, **kwargs)]

    def test_default_is_recent_reading_first(self):
        self.assertEqual(self.ids(), ["d", "a", "b", "c"])
        self.assertEqual(self.ids(descending=False), ["c", "b", "a", "d"])

    def test_sort_by_catalog_field_puts_missing_last(self):
        # 缺少字段的 d（不在书库）和 c（无爱心数）排最后，彼此仍按最近阅读
        self.assertEqual(self.ids(field="totalLikes"), ["b", "a", "d", "c"])
        self.assertEqual(self.ids(field="totalLikes", descending=False), ["a", "b", "d", "c"])
        self.assertEqual(self.ids(field="updated_at"), ["a", "c", "b", "d"])

    def test_search_matches_catalog_title_and_ignores_script(self):
        # 历史里存的是错误的“旧标题”，按书库的正确标题也能搜到；简繁体都能匹配
        self.assertEqual(self.ids(text="正确"), ["a"])
        self.assertEqual(self.ids(text="漫画"), ["b"])
        self.assertEqual(self.ids(text="不在"), ["d"])

    def test_only_update_keeps_books_updated_after_last_read(self):
        self.assertEqual(self.ids(onlyUpdate=True), ["a", "c"])
        self.assertTrue(history_has_update(self.histories[0], self.infos["a"]))
        self.assertFalse(history_has_update(self.histories[3], None))

    def test_show_title_keeps_original_script_and_fixes_wrong_title(self):
        # 书库标题是简体化的（日文汉字也被转换），同一本书时保留历史里的原标题
        same = history("e", "王女&女騎士 恥辱の見世物", "2026-01-01")
        self.assertEqual(history_show_title(same, info("e", "王女&女骑士 耻辱の见世物", None)), "王女&女騎士 恥辱の見世物")
        # 历史里写成了别的书的标题时，以书库为准
        self.assertEqual(history_show_title(self.histories[0], self.infos["a"]), "正确标题甲")
        self.assertEqual(history_show_title(self.histories[3], None), "不在书库")

    def test_iso_to_tick_accepts_catalog_formats(self):
        self.assertEqual(iso_to_tick("2026-01-02T00:00:00.000Z"), tick("2026-01-02"))
        self.assertEqual(iso_to_tick("2026-01-02T00:00:00Z"), tick("2026-01-02"))
        self.assertIsNone(iso_to_tick(0))


class HistoryItemTextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        Str.Reload()

    def test_progress_is_short_and_full_text_in_tooltip(self):
        # 进度与“NEW”标记共用一行，只有封面宽，必须用短格式
        books = ComicListWidget(None)
        self.addCleanup(books.close)
        record = SimpleNamespace(bookId="a", name="A", url="", path="", tick=tick("2026-01-01"), epsId=19)
        book = SimpleNamespace(epsCount=35, totalLikes=1, likesCount=0, fileServer="", path="",
                               updated_at="", pages=10, finished=False)
        books.AddBookItemByHistory(record, book, "A")
        label = books.itemWidget(books.item(0)).categoryLabel
        self.assertTrue(label.text().endswith(" 20/35章"), label.text())
        self.assertEqual(label.toolTip(), "上次看到第20章/35章")


if __name__ == "__main__":
    unittest.main()
