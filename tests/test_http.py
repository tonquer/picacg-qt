import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from server.server import Server, Task
from server.user_handler import DownloadBookHandler, SpeedTestHandler
from server import user_handler
from server import server as server_module
from tools.status import Status


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.server = object.__new__(Server)
        self.handler = Mock()
        self.server.handler = {"SimpleNamespace": self.handler}
        self.request = SimpleNamespace(
            timeout=10, resetCnt=1, method="get", url="https://example.invalid/",
            params={}, headers={}, cookies={}, proxy={}, curl_opt={}, json=None,
            isParseRes=False, ResetToSwitchNextUrl=Mock(), GetPri=lambda: "测试请求",
        )
        self.task = Task(self.request, backParam=1)
        self.owner = patch.object(server_module, "QtOwner", return_value=SimpleNamespace(isOfflineModel=False))
        self.owner.start()
        self.addCleanup(self.owner.stop)
        self.log = patch.object(server_module, "Log")
        self.log.start()
        self.addCleanup(self.log.stop)

    def test_retry_success_replaces_error_and_returns_response(self):
        response = object()

        def attempt(task, *args):
            if transport.call_count == 1:
                raise server_module.exceptions.Timeout("测试超时")
            task.res = response

        transport = Mock(side_effect=attempt)
        self.server.Get = transport
        self.assertIs(self.server._Send(self.task, 0), response)
        self.assertEqual(self.task.status, Status.Ok)
        self.assertEqual(transport.call_count, 2)
        self.request.ResetToSwitchNextUrl.assert_called_once()
        self.handler.assert_called_once_with(self.task)

    def test_failure_exhausts_budget_and_notifies_once(self):
        self.request.resetCnt = 2
        self.server.Get = Mock(side_effect=server_module.exceptions.Timeout("测试超时"))
        self.server._Send(self.task, 0)
        self.assertEqual(self.server.Get.call_count, 3)
        self.assertEqual(self.request.ResetToSwitchNextUrl.call_count, 2)
        self.assertEqual(self.task.status, Status.TimeOut)
        self.handler.assert_called_once_with(self.task)

    def test_zero_retries_attempts_once(self):
        self.request.resetCnt = 0
        self.server.Get = Mock(side_effect=server_module.exceptions.Timeout("测试超时"))
        self.server._Send(self.task, 0)
        self.server.Get.assert_called_once()
        self.request.ResetToSwitchNextUrl.assert_not_called()

    def test_first_success_does_not_retry(self):
        self.server.Get = Mock()
        self.server._Send(self.task, 0)
        self.server.Get.assert_called_once()
        self.request.ResetToSwitchNextUrl.assert_not_called()
        self.handler.assert_called_once()

    def test_http_methods_forward_request_timeout(self):
        for method in ("Get", "Post", "Put"):
            for timeout in (2, 3, 7, 10):
                with self.subTest(method=method, timeout=timeout):
                    self.request.timeout = timeout
                    task = Task(self.request)
                    with patch.object(server_module.requests2, method.lower(), return_value=SimpleNamespace()) as send:
                        getattr(self.server, method)(task)
                    self.assertEqual(send.call_args.kwargs["timeout"], timeout)

    def test_timeout_is_preserved_for_download_and_speed_tasks(self):
        for handler in (DownloadBookHandler(), SpeedTestHandler()):
            for timeout in (2, 3, 7, 10):
                with self.subTest(handler=type(handler).__name__, timeout=timeout):
                    self.request.timeout = timeout
                    # 返回非成功状态，验证下载入口而不产生缓存文件。
                    response = Mock(headers={}, status_code=500)
                    response.iter_content.return_value = []
                    with patch.object(user_handler.requests2, "get", return_value=response) as send:
                        handler(Task(self.request))
                    self.assertEqual(send.call_args.kwargs["timeout"], timeout)

    def test_offline_notifies_once_without_transport(self):
        server_module.QtOwner.return_value.isOfflineModel = True
        self.server.Get = Mock()
        with patch.object(server_module, "TaskBase") as base:
            self.server._Send(self.task, 0)
        base.taskObj.taskBack.emit.assert_called_once()
        self.handler.assert_not_called()
        self.server.Get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
