import os
from pathlib import Path
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, PropertyMock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
# 测试源代码时无需编译图片资源，业务模块保持真实导入。
sys.modules.setdefault("images_rc", types.ModuleType("images_rc"))

from qt_owner import QtOwner


class DetailHistoryRefreshTests(unittest.TestCase):
    def test_both_detail_pages_reload_reading_progress(self):
        views = {}
        for name in ("bookInfoView", "bookInfoView2"):
            views[name] = SimpleNamespace(ReloadHistory=SimpleNamespace(emit=Mock()))
            item = patch.object(QtOwner, name, new_callable=PropertyMock, return_value=views[name])
            item.start()
            self.addCleanup(item.stop)
        QtOwner().ReloadBookInfoHistory()
        for view in views.values():
            view.ReloadHistory.emit.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
