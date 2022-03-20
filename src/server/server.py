import json
import threading
from queue import Queue

import requests
import urllib3
from urllib3.util.ssl_ import is_ipaddress

import server.req as req
import server.res as res
from config import config
from task.qt_task import TaskBase
from tools.log import Log
from tools.singleton import Singleton
from tools.status import Status
from tools.tool import ToolUtil

urllib3.disable_warnings()


from urllib3.util import connection
_orig_create_connection = connection.create_connection

host_table = {}


def _dns_resolver(host):
    if host in host_table:
        address = host_table[host]
        Log.Info("dns parse, host:{}->{}".format(host, address))
        return address
    else:
        return host


def patched_create_connection(address, *args, **kwargs):
    host, port = address
    hostname = _dns_resolver(host)
    return _orig_create_connection((hostname, port), *args, **kwargs)


connection.create_connection = patched_create_connection


def handler(request):
    def generator(handler):
        Server().handler[request.__name__] = handler()
        return handler
    return generator


class Task(object):
    def __init__(self, request, bakParam=""):
        self.req = request
        self.res = None
        self.timeout = 5
        self.bakParam = bakParam
        self.status = Status.Ok


class Server(Singleton):
    def __init__(self) -> None:
        super().__init__()
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
            thread.setName("HTTP-"+str(i))
            thread.setDaemon(True)
            thread.start()

        for i in range(self.downloadNum):
            thread = threading.Thread(target=self.RunDownload)
            thread.setName("Download-" + str(i))
            thread.setDaemon(True)
            thread.start()

    def Run(self):
        while True:
            task = self._inQueue.get(True)
            self._inQueue.task_done()
            try:
                if task == "":
                    break
                self._Send(task)
            except Exception as es:
                Log.Error(es)
        pass

    def Stop(self):
        for i in range(self.threadNum):
            self._inQueue.put("")
        for i in range(self.downloadNum):
            self._downloadQueue.put("")

    def RunDownload(self):
        while True:
            task = self._downloadQueue.get(True)
            self._downloadQueue.task_done()
            try:
                if task == "":
                    break
                self._Download(task)
            except Exception as es:
                Log.Error(es)
        pass

    def UpdateDns(self, address, imageAddress):
        self.imageServer = imageAddress
        self.address = address

        AllDomain = config.ApiDomain[:]
        AllDomain.append(config.ImageServer2)
        AllDomain.append(config.ImageServer2Jump)
        for domain in AllDomain:
            if is_ipaddress(address):
                host_table[domain] = address
            elif not address and domain in host_table:
                host_table.pop(domain)

        for domain in config.ImageDomain:
            if is_ipaddress(imageAddress):
                host_table[domain] = imageAddress
            elif not imageAddress and domain in host_table:
                host_table.pop(domain)
        # 换一个，清空pool
        self.session = requests.session()
        return

    def __DealHeaders(self, request, token):
        if self.token:
            request.headers["authorization"] = self.token
        if token:
            request.headers["authorization"] = token
        host = ToolUtil.GetUrlHost(request.url)
        if self.imageServer and host in config.ImageDomain:
            if not is_ipaddress(self.imageServer):
                request.url = request.url.replace(host, self.imageServer)

        if not request.isUseHttps:
            request.url = request.url.replace("https://", "http://")

        # host = ToolUtil.GetUrlHost(request.url)
        # if self.address and host in config.ApiDomain:
        #     request.headers["Host"] = host
        #     request.url = request.url.replace(host, self.address)
        #     # TODO CloudFlare指定Ip目前不能用Https
        #     request.url = request.url.replace("https://", "http://")
        #
        # if self.imageServer and host in config.ImageDomain:
        #     if is_ipaddress(self.imageServer):
        #         request.headers["Host"] = host
        #
        #         # TODO CloudFlare指定Ip目前不能用Https
        #         request.url = request.url.replace("https://", "http://")
        #
        #         # TODO 访问封面，301跳转后会失败，临时手动跳转
        #         if "static/tobeimg/" in request.url:
        #             request.headers["Host"] = "img.tipatipa.xyz"
        #             request.url = request.url.replace("static/tobeimg/", "")
        #     else:
        #         request.headers["Host"] = self.imageServer
        #
        #     request.url = request.url.replace(host, self.imageServer)

    def Send(self, request, backParam="", isASync=True):
        self.__DealHeaders(request, request.token)
        if isASync:
            return self._inQueue.put(Task(request, backParam))
        else:
            return self._Send(Task(request, backParam))

    def _Send(self, task):
        try:
            Log.Info("request-> backId:{}, {}".format(task.bakParam, task.req))
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
            Log.Info("response-> backId:{}, {}, st:{}, {}".format(task.bakParam, task.req.__class__.__name__, task.status, task.res))
        try:
            self.handler.get(task.req.__class__.__name__)(task)
            if task.res.raw:
                task.res.raw.close()
        except Exception as es:
            Log.Warn("task: {}, error".format(task.req.__class__))
            Log.Error(es)
        finally:
            return task.res

    def Post(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        r = self.session.post(request.url, proxies=request.proxy, headers=request.headers, data=json.dumps(request.params), timeout=task.timeout, verify=False)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Put(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
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

    def Download(self, request, token="", backParams="", isASync=True):
        self.__DealHeaders(request, token)
        task = Task(request, backParams)
        if isASync:
            self._downloadQueue.put(task)
        else:
            self._Download(task)

    def _Download(self, task):
        try:
            if not task.req.isReload:
                if not isinstance(task.req, req.SpeedTestReq) and not task.req.savePath:
                    for cachePath in [task.req.loadPath, task.req.cachePath]:
                        if cachePath and task.bakParam:
                            data = ToolUtil.LoadCachePicture(cachePath)
                            if data:
                                TaskBase.taskObj.downloadBack.emit(task.bakParam, len(data), b"")
                                TaskBase.taskObj.downloadBack.emit(task.bakParam, 0, data)
                                Log.Info("request cache -> backId:{}, {}".format(task.bakParam, task.req))
                                return
            request = task.req
            if request.params is None:
                request.params = {}

            if request.headers is None:
                request.headers = {}
            Log.Info("request-> backId:{}, {}".format(task.bakParam, task.req))
            r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, stream=True, timeout=task.timeout, verify=False)
            # task.res = res.BaseRes(r)
            # print(r.elapsed.total_seconds())
            task.res = r
        except Exception as es:
            Log.Warn(task.req.url + " " + es.__repr__())
            task.status = Status.NetError
        self.handler.get(task.req.__class__.__name__)(task)
        if task.res:
            task.res.close()

    def TestSpeed(self, request, bakParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, bakParams)
        task.timeout = 2
        self._downloadQueue.put(task)

    def TestSpeedPing(self, request, bakParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, bakParams)
        task.timeout = 2
        self._inQueue.put(task)
