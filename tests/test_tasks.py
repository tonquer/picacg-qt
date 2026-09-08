import os
import pickle
import sqlite3
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from pathlib import Path
from queue import Queue
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

from config import config
from config.setting import Setting
from server.sql_server import DbBook, SqlServer
from task.qt_task import QtTaskQObject, TaskBase
from task.task_download import QtDownloadTask, TaskDownload
from task.task_http import QtHttpTask, TaskHttp
from task.task_local import LocalData, QLocalTask, TaskLocal
from task.task_qimage import QtQImageTask, TaskQImage
from task.task_sql import QtSqlTask, TaskSql
from task.task_upload import QtUpTask, TaskUpload
from task.task_waifu2x import QConvertTask, TaskWaifu2x
from tools.status import Status
from tools.str import Str
from view.nas.nas_item import NasUploadItem
from view.nas.nas_status import NasStatus


def make_manager(cls):
    # 使用真实任务类，跳过单例构造中的后台线程启动。
    manager = object.__new__(cls)
    TaskBase.__init__(manager)
    manager.taskObj = QtTaskQObject()
    return manager


class TaskLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.log_patch = patch("tools.log.Log.Error")
        self.log_patch.start()
        self.addCleanup(self.log_patch.stop)

    def assert_empty(self, manager):
        self.assertEqual({}, manager.tasks)
        self.assertEqual({}, manager.flagToIds)

    def task_cases(self):
        return [
            (TaskHttp, QtHttpTask(0), "taskId", "HandlerTask", [pickle.dumps({"st": Status.Ok})]),
            (TaskSql, QtSqlTask(0), "taskId", "HandlerSqlTask", [pickle.dumps(("version", 1, "time", 2))]),
            (TaskDownload, QtDownloadTask(), "downloadId", "HandlerTask", [0, b"image"]),
            (TaskQImage, QtQImageTask(0), "taskId", "HandlerTask", [QImage()]),
            (TaskLocal, QLocalTask(), "taskId", "HandlerTask", [Str.Ok, []]),
            (TaskUpload, QtUpTask(0), "taskId", "HandlerTask", [Str.Ok, ""]),
            (TaskWaifu2x, QConvertTask(), "taskId", "HandlerTask", []),
        ]

    def test_terminal_callbacks_are_consumed_once_even_on_callback_error(self):
        for cls, info, id_attr, handler_name, args in self.task_cases():
            for raises in (False, True):
                with self.subTest(task=cls.__name__, raises=raises):
                    manager = make_manager(cls)
                    callback = Mock(side_effect=RuntimeError("回调失败") if raises else None)
                    if isinstance(info, QtDownloadTask):
                        info.downloadCompleteBack = callback
                    else:
                        info.callBack = callback
                    task_id = manager._RegisterTask(info, "owner", id_attr=id_attr)
                    handler = getattr(manager, handler_name)
                    handler(task_id, *args)
                    handler(task_id, *args)
                    callback.assert_called_once()
                    self.assert_empty(manager)

    def test_absent_callbacks_and_cancelled_results_do_not_leak(self):
        for cls, info, id_attr, handler_name, args in self.task_cases():
            with self.subTest(task=cls.__name__):
                manager = make_manager(cls)
                task_id = manager._RegisterTask(info, "owner", id_attr=id_attr)
                getattr(manager, handler_name)(task_id, *args)
                self.assert_empty(manager)
                task_id = manager._RegisterTask(info, "owner", id_attr=id_attr)
                with patch.object(config, "CanWaifu2x", False):
                    manager.Cancel("owner")
                    manager.Cancel("owner")
                getattr(manager, handler_name)(task_id, *args)
                self.assert_empty(manager)

    def test_callback_can_register_new_task_under_same_owner(self):
        manager = make_manager(TaskHttp)
        new_ids = []
        info = QtHttpTask(0)
        info.callBack = lambda data: new_ids.append(manager._RegisterTask(QtHttpTask(0), "owner"))
        task_id = manager._RegisterTask(info, "owner")
        manager.HandlerTask(task_id, pickle.dumps("ok"))
        self.assertEqual({new_ids[0]}, manager.flagToIds["owner"])
        manager.HandlerTask(task_id, pickle.dumps("duplicate"))
        self.assertEqual(1, len(manager.tasks))

    def test_concurrent_registration_and_flag_cancellation(self):
        manager = make_manager(TaskHttp)
        barrier = threading.Barrier(4)

        def register(owner):
            barrier.wait()
            return [manager._RegisterTask(QtHttpTask(0), owner) for _ in range(50)]

        with ThreadPoolExecutor(max_workers=4) as pool:
            ids = [task_id for group in pool.map(register, range(1, 5)) for task_id in group]
        self.assertEqual(200, len(set(ids)))
        manager.Cancel(1)
        self.assertEqual(150, len(manager.tasks))
        for owner in range(2, 5):
            manager.Cancel(owner)
        self.assert_empty(manager)

    def test_dispatch_errors_remove_new_registration(self):
        manager = make_manager(TaskHttp)

        def fail(task_id):
            raise RuntimeError("分发失败")

        with self.assertRaises(RuntimeError):
            manager.AddHttpTask(fail, cleanFlag="owner")
        self.assert_empty(manager)
        manager = make_manager(TaskSql)
        with patch("server.sql_server.SqlServer") as server:
            server.return_value.AddSqlTask.side_effect = RuntimeError("分发失败")
            with self.assertRaises(RuntimeError):
                manager.AddSqlTask("book", "sql", 1, cleanFlag="owner")
        self.assert_empty(manager)

    def test_invalid_pickle_does_not_keep_terminal_task(self):
        for cls, record, handler in (
            (TaskHttp, QtHttpTask(0), "HandlerTask"),
            (TaskSql, QtSqlTask(0), "HandlerSqlTask"),
        ):
            manager = make_manager(cls)
            task_id = manager._RegisterTask(record, "owner")
            getattr(manager, handler)(task_id, b"invalid pickle")
            self.assert_empty(manager)

    def test_sql_failure_none_and_success_payloads_keep_callback_signature(self):
        manager = make_manager(TaskSql)
        for payload in (None, 0, [], {}, ("version", 1, "time", 2), {"st": Status.Ok}):
            info = QtSqlTask(0)
            info.callBack = Mock()
            info.backParam = 0
            task_id = manager._RegisterTask(info, "owner")
            manager.HandlerSqlTask(task_id, pickle.dumps(payload))
            info.callBack.assert_called_once_with(payload, 0)
            self.assert_empty(manager)

    def test_local_progress_stays_registered_until_terminal(self):
        manager = make_manager(TaskLocal)
        info = QLocalTask()
        info.callBack = Mock()
        task_id = manager._RegisterTask(info, "owner")
        for name in ("1.jpg", "2.jpg"):
            manager.HandlerTask(task_id, Str.Waiting, [("", name)])
            self.assertIs(info, manager._GetTask(task_id))
        manager.HandlerTask(task_id, Str.Ok, [])
        manager.HandlerTask(task_id, Str.Ok, [])
        self.assertEqual(3, info.callBack.call_count)
        self.assert_empty(manager)

    def test_local_read_and_scan_error_emit_terminal(self):
        manager = make_manager(TaskLocal)
        manager.taskObj.localBack.connect(manager.HandlerTask)
        callback = Mock()
        task_id = manager.AddLoadRead(LocalData.TypeLoadPicFile, "folder", None, callback, "owner")
        with patch("task.task_local.os.path.isdir", return_value=True), patch("task.task_local.os.walk", side_effect=OSError("读取失败")):
            manager.ParseAllPicPath(task_id, "folder")
        callback.assert_called_once_with(Str.ErrorPath, [])
        self.assert_empty(manager)
        info = QLocalTask()
        info.callBack = Mock(side_effect=RuntimeError("回调失败"))
        task_id = manager._RegisterTask(info, "owner")
        manager.HandlerTask2(task_id, Str.Ok, b"image")
        self.assert_empty(manager)

    def test_download_progress_terminal_and_metadata_handoff(self):
        manager = make_manager(TaskDownload)
        info = QtDownloadTask()
        info.downloadCallBack = Mock()
        info.downloadCompleteBack = Mock()
        task_id = manager._RegisterTask(info, "owner", id_attr="downloadId")
        for remaining in (100, 50, 0):
            manager.HandlerTask(task_id, remaining, b"")
            self.assertIs(info, manager._GetTask(task_id))
        manager.HandlerTask(task_id, 0, b"image")
        info.downloadCompleteBack.assert_called_once_with(b"image", Status.Ok)
        self.assert_empty(manager)
        for status in (Str.Success, Str.Cache, Str.Error, Str.SpaceEps, Str.UnderReviewBook, Str.Downloading):
            info = QtDownloadTask()
            info.statusBack = Mock()
            task_id = manager._RegisterTask(info, "owner", id_attr="downloadId")
            child_id = manager._RegisterTask(QtDownloadTask(), "owner", id_attr="downloadId")
            manager.HandlerTaskSt(task_id, {"st": status})
            self.assertEqual({child_id}, manager.flagToIds["owner"])
            info.statusBack.assert_called_once_with({"st": status})
            manager.Cancel("owner")
        self.assert_empty(manager)

    def test_download_save_error_and_metadata_error_finish(self):
        manager = make_manager(TaskDownload)
        manager.taskObj.downloadStBack.connect(manager.HandlerTaskSt)
        info = QtDownloadTask()
        info.statusBack = Mock()
        task_id = manager._RegisterTask(info, "owner", id_attr="downloadId")
        manager.HandlerTask(task_id, -2, b"")
        info.statusBack.assert_called_once_with({"st": Status.SaveError})
        self.assert_empty(manager)
        task_id = manager.DownloadBook("book", 0, 0, statusBack=Mock(), cleanFlag="owner")
        # 制造元数据格式错误，验证异常出口仍发送终态。
        manager.HandlerDownload({"missing_status": True}, (task_id, Str.Waiting))
        self.assert_empty(manager)

    def test_qimage_empty_input_keeps_worker_available(self):
        manager = make_manager(TaskQImage)
        manager.taskObj.imageBack.connect(manager.HandlerTask)
        first, second = Mock(), Mock()
        manager.AddQImageTask(b"", 1, 0, 0, 0, first, cleanFlag="owner")
        manager.AddQImageTask(b"invalid image", 1, 0, 0, 0, second, cleanFlag="owner")
        manager.Stop()
        manager.Run()
        first.assert_called_once()
        second.assert_called_once()
        self.assertTrue(first.call_args.args[0].isNull())
        self.assertTrue(second.call_args.args[0].isNull())
        self.assert_empty(manager)

    def test_upload_unexpected_error_finishes_and_queue_continues(self):
        manager = make_manager(TaskUpload)
        manager.taskObj.uploadBack.connect(manager.HandlerTask)
        callback = Mock()
        manager.AddLoadReadPicture(None, QtUpTask.Check, "", "", "", "", 0, None, callback, "owner")
        manager.Stop()
        with patch.object(manager, "CheckLink", side_effect=RuntimeError("连接失败")):
            manager.Run()
        callback.assert_called_once_with(Str.Error, "")
        self.assert_empty(manager)

    def test_waifu_cancellation_preserves_backend_operations(self):
        manager = make_manager(TaskWaifu2x)
        native = SimpleNamespace(remove=Mock(), removeWaitProc=Mock())
        fake_module = ModuleType("sr_vulkan")
        fake_module.sr_vulkan = native
        first = manager._RegisterTask(QConvertTask(), "first")
        second = manager._RegisterTask(QConvertTask(), "second")
        with patch.object(config, "CanWaifu2x", True), patch.dict(sys.modules, {"sr_vulkan": fake_module}):
            manager.ClearWaitConvertIds([first])
            native.removeWaitProc.assert_called_once_with([first])
            self.assertIsNotNone(manager._GetTask(second))
            manager.Cancel("second")
            native.remove.assert_called_once_with([second])
        self.assert_empty(manager)

    def test_nas_pause_cancels_item_tasks_and_ignores_late_upload_result(self):
        upload, sql, http = (make_manager(cls) for cls in (TaskUpload, TaskSql, TaskHttp))
        status = NasStatus()
        status.UpdateTableItem = Mock()
        status.UpdateTaskDB = Mock()
        item = NasUploadItem()
        item.bookId, item.nasId = "book", 1
        item.UploadInit = Mock(return_value=item.Uploading)
        item.GetNextParams = Mock(return_value=(item.Uploading, (None, "source", "archive", "target")))
        status.downloadDict[item.key] = item
        other_id = upload._RegisterTask(QtUpTask(0), "another-owner")
        with patch("task.task_upload.TaskUpload", return_value=upload), patch("task.task_sql.TaskSql", return_value=sql), patch("task.task_http.TaskHttp", return_value=http):
            status.StartItemDownload(item)
            old_id = next(iter(upload.flagToIds[item.cleanFlag]))
            sql._RegisterTask(QtSqlTask(0), item.cleanFlag)
            http._RegisterTask(QtHttpTask(0), item.cleanFlag)
            status.SetNewStatus(item, item.Pause)
            self.assertIsNone(upload._GetTask(old_id))
            self.assert_empty(sql)
            self.assert_empty(http)
            self.assertIsNotNone(upload._GetTask(other_id))
            status.StartItemDownload(item)
            new_id = next(iter(upload.flagToIds[item.cleanFlag]))
            self.assertNotEqual(old_id, new_id)
            upload.HandlerTask(old_id, Str.Ok, "")
            self.assertEqual(QtUpTask.Check, item.type)
            self.assertEqual({new_id}, upload.flagToIds[item.cleanFlag])
            upload.HandlerTask(new_id, Str.Ok, "")
            self.assertEqual(QtUpTask.MakeZip, item.type)
            self.assertEqual(1, len(upload.flagToIds[item.cleanFlag]))


class SqlLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "book.db"
        self.connection = sqlite3.connect(self.path)
        self.addCleanup(self.connection.close)
        fields = vars(DbBook())
        self.connection.execute("CREATE TABLE book ({})".format(",".join(fields)))
        row = dict(fields)
        row.update(id="book", title="示例", categories="测试分类", shareId=1)
        self.connection.execute("INSERT INTO book VALUES ({})".format(",".join("?" for _ in fields)), tuple(row.values()))
        self.connection.execute("CREATE TABLE system (id, size, time, sub_version)")
        self.connection.execute("INSERT INTO system VALUES ('v1', 1, '2026-01-01 00:00:00', 0)")
        self.connection.execute("CREATE TABLE words (id, word)")
        self.connection.execute("INSERT INTO words VALUES (1, '词条')")
        self.connection.execute("CREATE TABLE category (bookId, category, PRIMARY KEY (bookId, category))")
        self.connection.execute("INSERT INTO category VALUES ('book', 1)")
        self.connection.execute("CREATE TABLE favorite (id, user, sortId, PRIMARY KEY (id, user))")
        self.connection.execute("INSERT INTO favorite VALUES ('book', 'tester', 1)")
        self.connection.commit()

    def run_requests(self, requests, on_result=None, missing=False):
        # 执行真实 SQL 工作循环和 Qt 信号，数据库位于测试专用临时目录。
        server = object.__new__(SqlServer)
        server._inQueue = {"book": Queue()}
        manager = make_manager(TaskSql)
        manager.taskObj.sqlBack.connect(manager.HandlerSqlTask)
        emitted, results = [], {}
        manager.taskObj.sqlBack.connect(lambda task_id, payload: emitted.append((task_id, pickle.loads(payload))))
        owner = SimpleNamespace(isUseDb=True, isDbHavePicaID=True)

        def receive(data, index):
            results[index] = data
            if on_result:
                on_result(data, index)

        with ExitStack() as stack:
            stack.enter_context(patch("server.sql_server.SqlServer", return_value=server))
            stack.enter_context(patch("server.sql_server.TaskSql", return_value=manager))
            stack.enter_context(patch("server.sql_server.QtOwner", return_value=owner))
            stack.enter_context(patch("server.sql_server.BookMgr"))
            stack.enter_context(patch("tools.category.CateGoryMgr", return_value=SimpleNamespace(
                indexCategories={1: "测试分类"}, categoriseIndex={"测试分类": 1})))
            stack.enter_context(patch.object(Setting, "UserId", SimpleNamespace(value="tester")))
            stack.enter_context(patch.object(Setting, "GetDBPath", return_value=str(Path(self.directory.name) / "missing") if missing else self.directory.name))
            stack.enter_context(patch.object(config, "DbVersion", "v1"))
            stack.enter_context(patch("tools.log.Log.Error"))
            for index, (task_type, data) in enumerate(requests):
                manager.AddSqlTask("book", data, task_type, receive, index, cleanFlag="owner")
            server._inQueue["book"].put((SqlServer.TaskTypeClose, "", ""))
            server._Run("book")
        self.assertEqual(len(requests), len(emitted))
        self.assertEqual(len(requests), len(results))
        self.assertEqual({}, manager.tasks)
        self.assertEqual({}, manager.flagToIds)
        self.assertEqual(0, server._inQueue["book"].unfinished_tasks)
        return results

    def test_sql_success_payloads_and_committed_write_acknowledgements(self):
        book = DbBook()
        book.id, book.title = "new-book", "新增"
        select_columns = ("id,title,title2,author,chineseTeam,description,epsCount,pages,finished,likesCount,"
                          "categories,tags,created_at,updated_at,path,fileServer,creator,totalLikes,totalViews,shareId")
        committed = []

        def receive(data, index):
            if index == 9:
                committed.append(self.connection.execute("SELECT count(*) FROM book WHERE id='new-book'").fetchone()[0])
            if index == 10:
                committed.append(self.connection.execute("SELECT sortId FROM favorite WHERE id='book'").fetchone()[0])

        results = self.run_requests([
            (SqlServer.TaskCheck, ""),
            (SqlServer.TaskTypeSelectBook, "SELECT " + select_columns + " FROM book"),
            (SqlServer.TaskTypeSelectWord, ""),
            (SqlServer.TaskTypeSelectUpdate, ""),
            (SqlServer.TaskTypeSelectFavorite, ""),
            (SqlServer.TaskTypeCacheBook, "book"),
            (SqlServer.TaskTypeCategoryBookNum, "SELECT id FROM book"),
            (SqlServer.TaskTypeSearchBookNum, "SELECT count(*) FROM book"),
            (SqlServer.TaskTypeSql, "INSERT INTO words VALUES (2, '新增词条')"),
            (SqlServer.TaskTypeUpdateBook, ([book], 1700000000, 1)),
            (SqlServer.TaskTypeUpdateFavorite, [("book", 2)]),
        ], receive)
        self.assertEqual("1", results[0])
        self.assertEqual(["book"], [book.id for book in results[1]])
        self.assertEqual(["词条"], results[2])
        self.assertEqual(("v1", 1, "2026-01-01 00:00:00", 0), results[3])
        self.assertEqual([("book", 1)], results[4])
        self.assertEqual(Status.Ok, results[5]["st"])
        self.assertEqual(["book"], [book.id for book in results[5]["bookList"]])
        self.assertEqual({"测试分类": 1}, results[6])
        self.assertEqual(1, results[7])
        self.assertEqual("", results[8])
        self.assertEqual({"st": Status.Ok}, results[9])
        self.assertEqual({"st": Status.Ok}, results[10])
        self.assertEqual([1, 2], committed)

    def test_sql_errors_notify_once_and_do_not_stop_following_tasks(self):
        results = self.run_requests([
            (SqlServer.TaskTypeSelectBook, "SELECT * FROM missing"),
            (SqlServer.TaskTypeSearchBookNum, "SELECT count(*) FROM missing"),
            (SqlServer.TaskTypeCategoryBookNum, "SELECT id FROM missing"),
            (SqlServer.TaskTypeSql, "SELECT * FROM missing"),
            (SqlServer.TaskTypeSql, "DROP TABLE book"),
            (SqlServer.TaskTypeCacheBook, "book"),
            (SqlServer.TaskTypeSelectUpdate, ""),
            (SqlServer.TaskTypeSelectWord, ""),
        ])
        for index in (0, 1, 2, 3, 6):
            self.assertIsNone(results[index])
        self.assertEqual("", results[4])
        self.assertEqual({"st": Status.Error, "bookList": []}, results[5])
        self.assertEqual(["词条"], results[7])

    def test_missing_database_uses_type_appropriate_failure_payloads(self):
        task_types = [SqlServer.TaskCheck, SqlServer.TaskTypeSelectBook, SqlServer.TaskTypeSelectWord,
                      SqlServer.TaskTypeSelectUpdate, SqlServer.TaskTypeSelectFavorite,
                      SqlServer.TaskTypeCacheBook, SqlServer.TaskTypeCategoryBookNum,
                      SqlServer.TaskTypeSearchBookNum, SqlServer.TaskTypeSql,
                      SqlServer.TaskTypeUpdateBook, SqlServer.TaskTypeUpdateFavorite]
        results = self.run_requests([(task_type, "") for task_type in task_types], missing=True)
        for index in (1, 2, 3, 4, 6, 7, 8):
            self.assertIsNone(results[index])
        self.assertEqual("", results[0])
        self.assertEqual({"st": Status.Error, "bookList": []}, results[5])
        self.assertEqual({"st": Status.Error}, results[9])
        self.assertEqual({"st": Status.Error}, results[10])

    def test_failed_writes_rollback_before_error_callback(self):
        self.connection.execute("CREATE TRIGGER reject_book BEFORE INSERT ON book BEGIN SELECT RAISE(ABORT, '测试失败'); END")
        self.connection.execute("CREATE TRIGGER reject_favorite BEFORE INSERT ON favorite BEGIN SELECT RAISE(ABORT, '测试失败'); END")
        self.connection.commit()
        book = DbBook()
        book.id = "rejected"
        results = self.run_requests([
            (SqlServer.TaskTypeUpdateBook, ([book], 1700000000, 9)),
            (SqlServer.TaskTypeUpdateFavorite, [("book", 9)]),
            (SqlServer.TaskTypeSearchBookNum, "SELECT count(*) FROM book"),
        ])
        self.assertEqual({"st": Status.Error}, results[0])
        self.assertEqual({"st": Status.Error}, results[1])
        self.assertEqual(1, results[2])
        self.assertEqual(0, self.connection.execute("SELECT sub_version FROM system").fetchone()[0])
        self.assertEqual(1, self.connection.execute("SELECT sortId FROM favorite").fetchone()[0])

    def test_failed_version_query_does_not_change_update_watermark(self):
        # 版本回调测试不依赖编译后的图片资源。
        with patch.dict(sys.modules, {"images_rc": sys.modules.get("images_rc", ModuleType("images_rc"))}):
            from view.help.help_view import HelpView

        view = SimpleNamespace(curSubVersion=7, curUpdateTick=123)
        owner = Mock()
        with patch("view.help.help_view.QtOwner", return_value=owner):
            HelpView.UpdateDbInfoBack(view, None)
        self.assertEqual((7, 123), (view.curSubVersion, view.curUpdateTick))
        owner.ShowError.assert_called_once()


if __name__ == "__main__":
    unittest.main()
