import json
import threading
from queue import Queue

import requests
import urllib3
from requests import ConnectTimeout
from requests.exceptions import ProxyError, RequestException
from urllib3.exceptions import ConnectTimeoutError
from urllib3.util.ssl_ import is_ipaddress

import src.server.req as req
import src.server.res as res
from conf import config
from src.util import ToolUtil, Singleton, Log
from src.util.status import Status

urllib3.disable_warnings()


def handler(request):
    def generator(handler):
        Server().handler[request] = handler()
        return handler
    return generator


class Task(object):
    def __init__(self, request, bakParam="", cacheAndLoadPath="", loadPath=""):
        self.req = request
        self.res = None
        self.timeout = 5
        self.bakParam = bakParam
        self.status = Status.Ok
        self.cacheAndLoadPath = cacheAndLoadPath
        self.loadPath = loadPath


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
                Log.Error(es)
        pass

    def RunDownload(self):
        while True:
            task = self._downloadQueue.get(True)
            self._downloadQueue.task_done()
            try:
                self._Download(task)
            except Exception as es:
                Log.Error(es)
        pass

    def __DealHeaders(self, request, token):
        if self.token:
            request.headers["authorization"] = self.token
        if token:
            request.headers["authorization"] = token

        host = ToolUtil.GetUrlHost(request.url)
        if self.address and host in config.ApiDomain:
            request.headers["Host"] = host
            request.url = request.url.replace(host, self.address)
            # TODO CloudFlare指定Ip目前不能用Https
            request.url = request.url.replace("https://", "http://")

        if self.imageServer and host in config.ImageDomain:
            if is_ipaddress(self.imageServer):
                request.headers["Host"] = host

                # TODO CloudFlare指定Ip目前不能用Https
                request.url = request.url.replace("https://", "http://")

                # TODO 访问封面，301跳转后会失败，临时手动跳转
                if "static/tobeimg/" in request.url:
                    request.headers["Host"] = "img.tipatipa.xyz"
                    request.url = request.url.replace("static/tobeimg/", "")
            else:
                request.headers["Host"] = self.imageServer

            request.url = request.url.replace(host, self.imageServer)

    def Send(self, request, token="", backParam="", isASync=True):
        self.__DealHeaders(request, token)
        if isASync:
            self._inQueue.put(Task(request, backParam))
        else:
            self._Send(Task(request, backParam))

    def _Send(self, task):
        try:
            Log.Info("request-> backId:{} {}".format(task.bakParam, task.req))
            if task.req.method.lower() == "post":
                self.Post(task)
            elif task.req.method.lower() == "get":
                self.Get(task)
            elif task.req.method.lower() == "put":
                self.Put(task)
            else:
                return
        except Exception as es:
            task.status = Status.NetError
            # Log.Error(es)
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            Log.Info("response-> backId:{}, {}".format(task.bakParam, task.res))
        try:
            self.handler.get(task.req.__class__)(task)
            if task.res.raw:
                task.res.raw.close()
        except Exception as es:
            Log.Warn("task: {}, error".format(task.req.__class__))
            Log.Error(es)

    def Post(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        r = self.session.post(request.url, proxies=request.proxy, headers=request.headers, data=json.dumps(request.params), timeout=task.timeout, verify=False)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Put(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        r = self.session.put(request.url, proxies=request.proxy, headers=request.headers, data=json.dumps(request.params), timeout=60, verify=False)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Get(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout, verify=False)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Download(self, request, token="", bakParams="", cacheAndLoadPath="", loadPath= "", isASync=True):
        self.__DealHeaders(request, token)
        task = Task(request, bakParams, cacheAndLoadPath, loadPath)
        if isASync:
            self._downloadQueue.put(task)
        else:
            self._Download(task)

    def _Download(self, task):
        try:
            if not isinstance(task.req, req.SpeedTestReq):
                for cachePath in [task.cacheAndLoadPath, task.loadPath]:
                    if cachePath and task.bakParam:
                        data = ToolUtil.LoadCachePicture(cachePath)
                        if data:
                            from src.qt.util.qttask import QtTask
                            QtTask().downloadBack.emit(task.bakParam, len(data), data)
                            QtTask().downloadBack.emit(task.bakParam, 0, b"")
                            return
            request = task.req
            if request.params == None:
                request.params = {}

            if request.headers == None:
                request.headers = {}
            Log.Info("request-> backId:{}, {}".format(task.bakParam, task.req))
            r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, stream=True, timeout=task.timeout, verify=False)
            # task.res = res.BaseRes(r)
            # print(r.elapsed.total_seconds())
            task.res = r
        except Exception as es:
            Log.Warn(task.req.url + " " + es.__repr__())
            task.status = Status.NetError
        self.handler.get(task.req.__class__)(task)
        if task.res:
            task.res.close()

    def TestSpeed(self, request, bakParams="", testAddress="", testImageServer=""):
        bakAddress = self.address
        self.address = testAddress
        backImageServer = self.imageServer
        self.imageServer = testImageServer
        self.__DealHeaders(request, "")
        self.address = bakAddress
        self.imageServer = backImageServer
        self.address = bakAddress
        task = Task(request, bakParams)
        task.timeout = 2
        self._downloadQueue.put(task)

    def TestSpeedPing(self, request, bakParams="", testAddress="", testImageServer=""):
        bakAddress = self.address
        self.address = testAddress
        backImageServer = self.imageServer
        self.imageServer = testImageServer
        self.__DealHeaders(request, "")
        self.address = bakAddress
        self.imageServer = backImageServer
        task = Task(request, bakParams)
        task.timeout = 2
        self._inQueue.put(task)
