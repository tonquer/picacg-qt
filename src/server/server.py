import json
import pickle
import socket
import threading
from queue import Queue

import urllib

import server.req as req
import server.res as res
from config import config
from config.global_config import GlobalConfig
from qt_owner import QtOwner
from task.qt_task import TaskBase
from tools.log import Log
from tools.singleton import Singleton
from tools.status import Status
from tools.tool import ToolUtil
import httpx


host_table = {}
_orig_getaddrinfo = socket.getaddrinfo
# 如果使用代理，無法使用自定義dns
def getaddrinfo2(host, port, *args, **kwargs):
    if host in host_table:
        address = host_table[host]
        Log.Info("dns parse, host:{}->{}".format(host, address))
    else:
        address = host
    results = _orig_getaddrinfo(address, port, *args, **kwargs)
    return results
socket.getaddrinfo = getaddrinfo2


def handler(request):
    def generator(handler):
        Server().handler[request.__name__] = handler()
        return handler
    return generator


class Task(object):
    def __init__(self, request, bakParam=""):
        self.req = request
        self.res = None
        # self.timeout = 5
        self.bakParam = bakParam
        self.status = Status.Ok
        self.index = 0

    @property
    def timeout(self):
        return self.req.timeout

class Server(Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.handler = {}
        # self.session = httpx.Client(http2=True, verify=False, trust_env=False)

        self.address = ""
        self.imageServer = ""
        self.imageAddress = ""

        self.token = ""
        self._inQueue = Queue()
        self._downloadQueue = Queue()
        self.threadHandler = 0
        self.threadNum = config.ThreadNum
        self.downloadNum = config.DownloadThreadNum
        self.threadSession = []
        self.downloadSession = []

        for i in range(self.threadNum):
            self.threadSession.append(self.GetNewClient(None))
            thread = threading.Thread(target=self.Run, args=[i])
            thread.setName("HTTP-"+str(i))
            thread.setDaemon(True)
            thread.start()

        for i in range(self.downloadNum):
            self.downloadSession.append(self.GetNewClient(None))
            thread = threading.Thread(target=self.RunDownload, args=[i])
            thread.setName("Download-" + str(i))
            thread.setDaemon(True)
            thread.start()

    def Run(self, index):
        while True:
            task = self._inQueue.get(True)
            self._inQueue.task_done()
            try:
                if task == "":
                    break
                self._Send(task, index)
            except Exception as es:
                Log.Error(es)
        pass

    def Stop(self):
        for i in range(self.threadNum):
            self._inQueue.put("")
        for i in range(self.downloadNum):
            self._downloadQueue.put("")

    def RunDownload(self, index):
        while True:
            task = self._downloadQueue.get(True)
            self._downloadQueue.task_done()
            try:
                if task == "":
                    break
                self._Download(task, index)
            except Exception as es:
                Log.Error(es)
        pass

    def UpdateDns(self, address, imageUrl, imageAdress):
        self.imageServer = imageUrl
        self.address = address
        self.imageAddress = imageAdress

        AllDomain = config.ApiDomain[:]
        # AllDomain.append(config.ImageServer2)
        # AllDomain.append(config.ImageServer2Jump)
        # AllDomain.append(config.ImageServer3Jump)
        for domain in AllDomain:
            if ToolUtil.IsipAddress(address):
                host_table[domain] = address
            elif not address and domain in host_table:
                host_table.pop(domain)

        for domain in GlobalConfig.ImageServerList.value:
            if ToolUtil.IsipAddress(imageAdress):
                host_table[domain] = imageAdress
            elif not imageAdress and domain in host_table:
                host_table.pop(domain)

        for domain in GlobalConfig.ImageJumList.value:
            if ToolUtil.IsipAddress(imageAdress):
                host_table[domain] = imageAdress
            elif not imageAdress and domain in host_table:
                host_table.pop(domain)

    
        return

    def GetNewClient(self, proxy):
        try:
            ## proxy会报错
            return httpx.Client(http2=True, verify=False, trust_env=False, proxy=proxy)
        except Exception as es:
            Log.Error(es)
            return httpx.Client(http2=True, verify=False, trust_env=False)
    
    def UpdateProxy(self):
        from config.setting import Setting
        self.UpdateProxy2(Setting.IsHttpProxy.value, Setting.HttpProxy.value, Setting.Sock5Proxy.value)

    def UpdateProxy2(self, httpProxyIndex, httpProxy, sock5Proxy):
        from tools.str import Str
        # sock5代理
        if httpProxyIndex == 2 and sock5Proxy:
            data = sock5Proxy.replace("http://", "").replace("https://", "").replace("sock5://",
                                                                                                   "").replace(
                "socks5://", "")
            trustEnv = False
            data = data.split(":")
            if len(data) == 2:
                host = data[0]
                port = data[1]
                proxy = f"socks5://{host}:{port}"
            else:
                Log.Warn("sock5 error, sock5Proxy:{}".format(sock5Proxy))
                proxy = None
        # http代理
        elif httpProxyIndex == 1 and httpProxy:
            proxy = httpProxy
            if "http" not in httpProxy:
                httpProxy = "http://" + proxy
            trustEnv = False
        # 系统代理
        elif httpProxyIndex == 3:
            proxy = None
            proxyDict = urllib.request.getproxies()
            if isinstance(proxyDict, dict) and proxyDict.get("http"):
                proxy = proxyDict.get("http")
                if "http" not in httpProxy:
                    httpProxy = "http://" + proxy
            trustEnv = False
        # 其他
        else:
            trustEnv = False
            proxy = None
        Log.Warn(f"update proxy, index:{httpProxyIndex}, proxy:{proxy}, env:{trustEnv}")

        self.threadSession = []
        for i in range(self.threadNum):
            self.threadSession.append(self.GetNewClient(proxy))

        self.downloadSession = []
        for i in range(self.downloadNum):
            self.downloadSession.append(self.GetNewClient(proxy))
        return

    def __DealHeaders(self, request, token):
        if self.token:
            request.headers["authorization"] = self.token
        if token:
            request.headers["authorization"] = token

        host = ToolUtil.GetUrlHost(request.url)
        if self.imageServer and host in GlobalConfig.ImageServerList.value:
            if not ToolUtil.IsipAddress(self.imageServer):
                request.url = request.url.replace(host, self.imageServer)

        if not request.isUseHttps:
            request.url = request.url.replace("https://", "http://")

        if request.proxyUrl:
            host = ToolUtil.GetUrlHost(request.url)
            request.url = request.url.replace(host, request.proxyUrl+"/"+host)

        from config.setting import Setting
        if Setting.IsUseSniPretend.value:
            for name in  GlobalConfig.SniDomain.value:
                if name in host:
                    request.extend["sni_hostname"] = name

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
            return self._Send(Task(request, backParam), 0)

    def _Send(self, task, index):
        try:
            Log.Info("request-> backId:{}, {}".format(task.bakParam, task.req))
            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                data = {"st": Status.OfflineModel, "data": ""}
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
                return

            if task.req.method.lower() == "post":
                self.Post(task, index)
            elif task.req.method.lower() == "get":
                self.Get(task, index)
            elif task.req.method.lower() == "put":
                self.Put(task, index)
            else:
                return
        except Exception as es:
            if isinstance(es, httpx.ConnectError):
                task.status = Status.ConnectErr
            elif isinstance(es, httpx.ConnectTimeout):
                task.status = Status.TimeOut
            elif isinstance(es, ConnectionResetError):
                task.status = Status.ResetErr
            else:
                task.status = Status.NetError
            # Log.Error(es)
            Log.Error(task.req.url + " " + es.__repr__())
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

    def Post(self, task, index=0):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}
        session = self.threadSession[index]
        task.res = res.BaseRes("", False, task.req.__class__.__name__)
        if request.file:
            r = session.post(request.url, follow_redirects=True, headers=request.headers, files=request.file,
                                  timeout=task.timeout, extensions=request.extend)
        else:
            r = session.post(request.url, follow_redirects=True, headers=request.headers, json=request.params, timeout=task.timeout, extensions=request.extend)
        task.res = res.BaseRes(r, request.isParseRes, task.req.__class__.__name__)
        return task

    def Put(self, task, index=0):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}
        session = self.threadSession[index]
        task.res = res.BaseRes("", False, task.req.__class__.__name__)
        r = session.put(request.url, follow_redirects=True, headers=request.headers, json=request.params, timeout=15, extensions=request.extend)
        task.res = res.BaseRes(r, request.isParseRes, task.req.__class__.__name__)
        return task

    def Get(self, task, index=0):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}
        session = self.threadSession[index]
        task.res = res.BaseRes("", False, task.req.__class__.__name__)
        # print(f"index:{index}, token:{task.req.headers}")
        r = session.get(request.url, follow_redirects=True, headers=request.headers, timeout=task.timeout, extensions=request.extend)
        task.res = res.BaseRes(r, request.isParseRes, task.req.__class__.__name__)
        return task

    def Download(self, request, token="", backParams="", isASync=True):
        self.__DealHeaders(request, token)
        task = Task(request, backParams)
        if isASync:
            self._downloadQueue.put(task)
        else:
            self._Download(task, 0)

    def ReDownload(self, task):
        task.res = ""
        task.status = Status.Ok
        self._downloadQueue.put(task)

    def _Download(self, task, index):
        try:
            task.req.resetCnt -= 1
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
            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                self.handler.get(task.req.__class__.__name__)(task)
                return

            request = task.req
            if request.params is None:
                request.params = {}

            if request.headers is None:
                request.headers = {}
            if not request.isReset:
                Log.Info("request-> backId:{}, {}".format(task.bakParam, task.req))
            else:
                Log.Info("request reset:{} -> backId:{}, {}".format(task.req.resetCnt, task.bakParam, task.req))

            history = []
            # oldHost = ToolUtil.GetUrlHost(request.url)

            # task.res = res.BaseRes(r)
            # print(r.elapsed.total_seconds())
            task.res = None
            task.index = index
        except Exception as es:
            # if isinstance(es, requests.exceptions.ConnectTimeout):
            #     task.status = Status.ConnectErr
            # elif isinstance(es, requests.exceptions.ReadTimeout):
            #     task.status = Status.TimeOut
            # elif isinstance(es, requests.exceptions.SSLError):
            #     if "WSAECONNRESET" in es.__repr__():
            #         task.status = Status.ResetErr
            #     else:
            #         task.status = Status.SSLErr
            # elif isinstance(es, requests.exceptions.ProxyError):
            #     task.status = Status.ProxyError
            # elif isinstance(es, ConnectionResetError):
            #     task.status = Status.ResetErr
            # else:
            #     task.status = Status.NetError
            task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
            if (task.req.resetCnt > 0):
                task.req.isReset = True
                self.ReDownload(task)
                return
        self.handler.get(task.req.__class__.__name__)(task)
        # if task.res:
        #     task.res.close()

    def TestSpeed(self, request, bakParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, bakParams)

        self._downloadQueue.put(task)

    def TestSpeedPing(self, request, bakParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, bakParams)
        self._inQueue.put(task)
