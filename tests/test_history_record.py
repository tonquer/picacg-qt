import os
from pathlib import Path
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import PropertyMock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
# 测试源代码时无需编译图片资源，业务模块保持真实导入。
sys.modules.setdefault("images_rc", types.ModuleType("images_rc"))

from PySide6.QtWidgets import QApplication

from qt_owner import QtOwner
from tools.book import Book, BookMgr
from view.read.read_new_view import ReadNewView


class HistoryRecordTests(unittest.TestCase):
    """历史记录必须写入正在阅读的那本书，不能取详情页残留的书名。"""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.history = {}
        historyView = SimpleNamespace(GetHistory=self.history.get)
        # 详情页1 停留在另一本书上，模拟从“漫画详情2”进入阅读
        bookInfoView = SimpleNamespace(bookName="别的书", GetBookUrl=lambda: "https://other",
                                       GetBookUrlPath=lambda: "other.jpg")
        for name, value in (("historyView", historyView), ("bookInfoView", bookInfoView)):
            item = patch.object(QtOwner, name, new_callable=PropertyMock, return_value=value)
            item.start()
            self.addCleanup(item.stop)

    def addBook(self, bookId, title, fileServer, path):
        book = Book()
        book._id = bookId
        book.title = title
        book.thumb = {"fileServer": fileServer, "path": path}
        BookMgr().books[bookId] = book
        self.addCleanup(BookMgr().books.pop, bookId, None)

    def test_uses_reading_book_instead_of_detail_page(self):
        self.addBook("b2", "正在读的书", "https://s", "b2.jpg")
        reader = SimpleNamespace(bookId="b2")
        self.assertEqual(ReadNewView.GetHistoryBookInfo(reader), ("正在读的书", "https://s", "b2.jpg"))

    def test_falls_back_to_existing_history_without_book_info(self):
        self.history["b3"] = SimpleNamespace(name="旧标题", url="https://old", path="b3.jpg")
        reader = SimpleNamespace(bookId="b3")
        self.assertEqual(ReadNewView.GetHistoryBookInfo(reader), ("旧标题", "https://old", "b3.jpg"))

    def test_unknown_book_never_borrows_detail_page_title(self):
        reader = SimpleNamespace(bookId="b4")
        self.assertEqual(ReadNewView.GetHistoryBookInfo(reader), ("", "", ""))


if __name__ == "__main__":
    unittest.main()
