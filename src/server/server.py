import threading
import time
import weakref
import json
from queue import Queue

import requests
import src.server.req as req
import src.server.res as res
from src.util import ToolUtil, Singleton, Log
from conf import config
from src.util.status import Status
import urllib3
urllib3.disable_warnings()


def handler(request):
    def generator(handler):
        Server().handler[request] = handler()
        return handler
    return generator


class Task(object):
    def __init__(self, request, bakParam=""):
        self.req = request
        self.res = None
        self.timeout = 5
        self.bakParam = bakParam
        self.status = Status.Ok


class Server(Singleton, threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        threading.Thread.__init__(self)
        self.handler = {}
        self.session = requests.session()
        self.address = ""
        self.imageServer = ""

        self.token = ""
        self._inQueue = Queue()
        self._downloadQueue = Queue()
        self.threadHandler = 0
        self.threadNum = config.ThreadNum
        self.downloadNum = config.DownloadThreadNum

        for i in range(self.threadNum):
            thread = threading.Thread(target=self.Run)
            thread.setDaemon(True)
            thread.start()

        for i in range(self.downloadNum):
            thread = threading.Thread(target=self.RunDownload)
            thread.setDaemon(True)
            thread.start()

    def Run(self):
        while True:
            try:
                task = self._inQueue.get(True)
            except Exception as es:
                continue
                pass
            self._inQueue.task_done()
            try:
                self._Send(task)
            except Exception as es:
                import sys
                cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
                e = sys.exc_info()[1]
                Log.Error(cur_tb, e)
            time.sleep(1)
        pass

    def RunDownload(self):
        while True:
            task = self._downloadQueue.get(True)
            self._downloadQueue.task_done()
            try:
                self._Download(task)
            except Exception as es:
                import sys
                cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
                e = sys.exc_info()[1]
                Log.Error(cur_tb, e)
            time.sleep(1)
        pass

    def __DealHeaders(self, request, token):
        if self.token:
            request.headers["authorization"] = self.token
        if token:
            request.headers["authorization"] = token

        if self.address:
            host = ToolUtil.GetUrlHost(request.url)
            if host in config.Url:
                request.url = request.url.replace(host, self.address).replace("https://", "http://")
                request.headers["Host"] = host
            else:
                request.url = request.url.replace(host, self.imageServer)

        if request.method.lower() == "post":
            request.headers["Content-Type"] = "application/json; charset=UTF-8"

    def Send(self, request, token="", bakParam="", isASync=True):
        self.__DealHeaders(request, token)
        if isASync:
            self._inQueue.put(Task(request, bakParam))
        else:
            self._Send(Task(request, bakParam))

    def _Send(self, task):
        try:
            if task.req.method.lower() == "post":
                self.Post(task)
            elif task.req.method.lower() == "get":
                self.Get(task)
            else:
                return
        except Exception as es:
            task.status = Status.NetError
            import sys
            cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
            e = sys.exc_info()[1]
            Log.Error(cur_tb, e)
        try:
            self.handler.get(task.req.__class__)(task)
            if task.res.raw:
                task.res.raw.close()
        except Exception as es:
            import sys
            cur_tb = sys.exc_info()[2]  # return (exc_type, exc_value, traceback)
            e = sys.exc_info()[1]
            Log.Error(cur_tb, e)

    def Post(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}


        r = self.session.post(request.url, proxies=request.proxy, headers=request.headers, data=json.dumps(request.params), timeout=task.timeout, verify=False)
        task.res = res.BaseRes(r)
        return task

    def Get(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout, verify=False)
        task.res = res.BaseRes(r)
        return task

    def Download(self, request, token="", bakParams="", isASync=True):
        self.__DealHeaders(request, token)
        task = Task(request, bakParams)
        if isASync:
            self._downloadQueue.put(task)
        else:
            self._Download(task)

    def _Download(self, task):
        try:
            request = task.req
            if request.params == None:
                request.params = {}

            if request.headers == None:
                request.headers = {}

            r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, stream=True, timeout=task.timeout, verify=False)
            # task.res = res.BaseRes(r)
            task.res = r
        except Exception as es:
            task.status = Status.NetError
        self.handler.get(task.req.__class__)(task)
        if task.res:
            task.res.close()
