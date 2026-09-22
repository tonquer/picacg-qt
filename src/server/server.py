import copy
import json
import pickle
import threading
import time
from queue import Queue

import curl_cffi.requests.exceptions as exceptions
from curl_cffi import requests as requests2, CurlOpt, CurlHttpVersion, CurlSslVersion, Session

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
import socket
import urllib

host_table = {}


# _orig_getaddrinfo = socket.getaddrinfo
# # 如果使用代理，無法使用自定義dns
# def getaddrinfo2(host, port, *args, **kwargs):
#     if host in host_table:
#         address = host_table[host]
#         Log.Info("dns parse, host:{}->{}".format(host, address))
#     else:
#         address = host
#     results = _orig_getaddrinfo(address, port, *args, **kwargs)
#     return results
# socket.getaddrinfo = getaddrinfo2


def handler(request):
    def generator(handler):
        Server().handler[request.__name__] = handler()
        return handler

    return generator


# class NewSession(requests2.Session):
#     def __init__(self, **kwargs):
#         requests2.Session.__init__(self, **kwargs)

# def _set_curl_options(self, *args, **kwargs):
#     c = args[0]
#     if GlobalConfig.WebDnsList.value:
#         c.setopt(CurlOpt.RESOLVE, GlobalConfig.WebDnsList.value)
#     # c.setopt(CurlOpt.SSL_OPTIONS, CurlOpt.ALLO)
#     # c.setopt(CurlOpt.SSLVERSION, 6)
#     # c.setopt(CurlOpt.SSL_VERIFYHOST, False)
#     # c.setopt(CurlOpt.SSL_VERIFYPEER, False)
#     return requests2.Session._set_curl_options(self, *args, **kwargs)


class Task(object):
    def __init__(self, request, backParam="", cacheAndLoadPath="", loadPath=""):
        self.req = request
        self.session = None
        self.res = None
        self.timeout = request.timeout
        self.backParam = backParam
        self.status = Status.Ok
        self.cacheAndLoadPath = cacheAndLoadPath
        self.loadPath = loadPath
        self.index = 0

    @property
    def bakParam(self):
        return self.backParam

    def GetText(self):
        if not self.res:
            return ""
        if hasattr(self.res, "raw"):
            return getattr(self.res.raw, "text", "")
        return ""


class Server(Singleton):
    def __init__(self) -> None:
        Singleton.__init__(self)
        self.handler = {}
        # self.session = NewSession()
        # self.session2 = NewSession()
        # self.session2 = cloudscraper.session()
        self.address = ""
        self.imageServer = ""

        self.token = ""
        self._inQueue = Queue()
        self._downloadQueue = Queue()
        # self._oldQueue = Queue()
        self._speedQueue = Queue()
        self.threadHandler = 0
        self.threadNum = config.ThreadNum

        # from config.setting import Setting
        # self.downloadNum = Setting.MultiNum.value
        self.speedThreadNum = 8
        self.downloadNum = config.DownloadThreadNum
        self.allWaitThread = []
        # self.threadSession = []
        # self.downloadSession = []
        # self.oldSession = []

    def Init(self):
        # self.UpdateProxy()
        # for i in range(1):
        # self.oldSession.append(requests2.Session())
        # thread = threading.Thread(target=self.RunOld, args=[i])
        # thread.setName("HTTP-Old-"+str(i))
        # thread.setDaemon(True)
        # thread.start()

        for i in range(self.threadNum):
            # self.threadSession.append(self.GetNewSession())
            thread = threading.Thread(target=self.Run, args=[i])
            thread.setName("HTTP-" + str(i))
            thread.setDaemon(True)
            thread.start()
            self.allWaitThread.append(thread)

        for i in range(self.downloadNum):
            # self.downloadSession.append(self.GetNewSession())
            thread = threading.Thread(target=self.RunDownload, args=[i])
            thread.setName("Download-" + str(i))
            thread.setDaemon(True)
            thread.start()
            self.allWaitThread.append(thread)

        for i in range(self.speedThreadNum):
            # self.threadSession.append(self.GetNewSession())
            thread = threading.Thread(target=self.RunSpeed, args=[i])
            thread.setName("Speed-" + str(i))
            thread.setDaemon(True)
            thread.start()
            self.allWaitThread.append(thread)

    # def GetNewSession(self, isOpenHttp3=False, isOpenEch=False, isOpenDoh=False, dohUrl=""):
    #     curlDict = {}
    #
    #     if host_table:
    #         resolve_list = []
    #         for k, v in host_table.items():
    #             resolve_list.append(f"{k}:443:{v}")
    #
    #         curlDict[CurlOpt.RESOLVE] = resolve_list
    #
    #     if isOpenEch:
    #         curlDict[CurlOpt.ECH] = "true"
    #     if isOpenDoh and dohUrl:
    #         curlDict[CurlOpt.DOH_URL] = dohUrl
    #
    #     curlDict[CurlOpt.DNS_CACHE_TIMEOUT] = 300
    #     if isOpenHttp3:
    #         ver = CurlHttpVersion.V3
    #     else:
    #         ver = CurlHttpVersion.V2_0
    #     curlDict[CurlOpt.SSLVERSION] = CurlSslVersion.TLSv1_3
    #
    #     return requests2.Session(curl_options=curlDict, http_version=ver, impersonate="chrome110")
    # try:
    #     return httpx.Client(http2=True, verify=False, trust_env=False, proxy=proxy)
    # except Exception as es:
    #     Log.Error(es)
    #     return httpx.Client(http2=True, verify=False, trust_env=False)

    def Run(self, index):
        time.sleep(2)
        while True:
            task = self._inQueue.get(True)
            self._inQueue.task_done()
            try:
                with requests2.Session() as session:
                    if task == "":
                        break
                    self._Send(task, index, session)
            except Exception as es:
                Log.Error(es)
        pass

    def RunSpeed(self, index):
        time.sleep(2)
        while True:
            task = self._speedQueue.get(True)
            self._speedQueue.task_done()
            try:
                with requests2.Session() as session:
                    if task == "":
                        break
                    self._Send(task, index, session)
            except Exception as es:
                Log.Error(es)
        pass

    # def RunOld(self, index):
    #     while True:
    #         task = self._oldQueue.get(True)
    #         self._oldQueue.task_done()
    #         try:
    #             if task == "":
    #                 break
    #             self._Send(task, index, isOld=True)
    #         except Exception as es:
    #             Log.Error(es)
    #     pass

    def Stop(self):
        for q in [self._inQueue, self._downloadQueue, self._speedQueue]:
            while not q.empty():
                q.get(False)
                q.task_done()

        for i in range(self.threadNum):
            self._inQueue.put("")
        for i in range(self.downloadNum):
            self._downloadQueue.put("")
        for i in range(self.speedThreadNum):
            self._speedQueue.put("")

        for thread in self.allWaitThread:
            Log.Info(f"wait {thread.name} end")
            thread.join()
        Log.Info("all thread end")

    def RunDownload(self, index):
        time.sleep(2)
        while True:
            task = self._downloadQueue.get(True)
            self._downloadQueue.task_done()
            try:
                with requests2.Session(impersonate="chrome110") as session:
                    if task == "":
                        break
                    self._Download(task, index, session)
            except Exception as es:
                Log.Error(es)
        pass

    def __DealHeaders(self, request, token):
        # if not request.isUseHttps:
        #     request.url = request.url.replace("https://", "http://")
        ## 图片域名
        # request.resetUrlHost = GlobalConfig.PicUrlList.value[:]
        if request.proxyUrl:
            host = ToolUtil.GetUrlHost(request.url)
            request.url = request.url.replace(host, request.proxyUrl + "/" + host)

    def Send(self, request, token="", backParam="", isASync=True, index=0):
        self.__DealHeaders(request, token)
        if isinstance(request, req.SpeedTestReq):
            if isASync:
                return self._downloadQueue.put(Task(request, backParam))
            else:
                with requests2.Session() as session:
                    return self._Download(Task(request, backParam), index, session)
        else:
            if isinstance(request, (req.SpeedTestPingReq, req.SpeedTestPing2Req)):
                if isASync:
                    return self._speedQueue.put(Task(request, backParam))
                else:
                    with requests2.Session() as session:
                        return self._Send(Task(request, backParam), index, session)

            if isASync:
                return self._inQueue.put(Task(request, backParam))
            else:
                with requests2.Session() as session:
                    return self._Send(Task(request, backParam), index, session)

    def _Send(self, task, index, session):
        while True:
            # 每次尝试独立记录结果，避免成功重试仍携带上次失败状态。
            task.status = Status.Ok
            task.res = res.BaseRes("", False)# 复制curl_opts
            session.curl_options = copy.deepcopy(task.req.curl_opt)
            task.session = session

            self._SendAttempt(task, index)
            if task.status == Status.OfflineModel:
                return task.res
            if task.status == Status.Ok or task.req.resetCnt < 0:
                break
            task.req.ResetToSwitchNextUrl()

        try:
            self.handler.get(task.req.__class__.__name__)(task)
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            respose = task.res
            task.res = None
            task.session = None
            return respose

    def _SendAttempt(self, task, index):
        try:
            task.req.resetCnt -= 1
            Log.Info("request{}-> backId:{}, {}".format(index, task.bakParam, task.req))
            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                data = {"st": Status.OfflineModel, "data": ""}
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
                return

            if task.req.method.lower() == "post":
                self.Post(task, index)
            elif task.req.method.lower() == "post2":
                self.Post(task)
            elif task.req.method.lower() == "get":
                self.Get(task, index)
            elif task.req.method.lower() == "get2":
                self.Get(task)
            elif task.req.method.lower() == "put":
                self.Put(task, index)
            else:
                return
        except exceptions.DNSError as es:
            task.status = Status.DnsError
            Log.Warn(f"error:{task.req.GetPri()}")
            Log.Error(es)
        except exceptions.Timeout as es:
            if "Connection was reset" in str(es):
                task.status = Status.ResetErr
            elif "ECH_REJECTED" in str(es):
                task.status = Status.EchError
            elif "TLSV1_ALERT_UNRECOGNIZED_NAME" in str(es):
                task.status = Status.SNIError
            else:
                task.status = Status.TimeOut
            Log.Warn(f"error:{task.req.GetPri()}")
            Log.Error(es)
        except exceptions.SSLError as es:
            if "Connection was reset" in str(es):
                task.status = Status.ResetErr
            elif "ECH_REJECTED" in str(es):
                task.status = Status.EchError
            elif "TLSV1_ALERT_UNRECOGNIZED_NAME" in str(es):
                task.status = Status.SNIError
            else:
                task.status = Status.NetError
            Log.Warn(f"error:{task.req.GetPri()}")
            Log.Error(es)
        except exceptions.ConnectionError as es:
            task.status = Status.ConnectErr
            Log.Warn(f"error:{task.req.GetPri()}")
            Log.Error(es)
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(f"error:{task.req.GetPri()}")
            Log.Error(es)
        except:
            Log.Error(f"error:{task.req.GetPri()}")
        finally:
            Log.Info("response{}-> backId:{}, {}, st:{}, {}".format(index, task.backParam, task.req.__class__.__name__,
                                                                    task.status, task.res))

    def Post(self, task, index=0):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}
        # if isOld:
        #     session = self.oldSession[index]
        # else:
        #     session = self.threadSession[index]
        task.res = res.BaseRes("", False)

        if task.req.cookies:
            r = task.session.post(request.url, proxies=request.proxy, headers=request.headers, data=request.params,
                                  timeout=task.timeout, cookies=task.req.cookies, json=task.req.json)
        else:
            r = task.session.post(request.url, proxies=request.proxy, headers=request.headers, data=request.params,
                                  timeout=task.timeout, json=task.req.json)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    # def Post2(self, task):
    #     request = task.req
    #     if request.params == None:
    #         request.params = {}
    #
    #     if request.headers == None:
    #         request.headers = {}
    #
    #     task.res = res.BaseRes("", False)
    #     if task.req.cookies:
    #         r = self.session2.post(request.url, proxies=request.proxy, impersonate="chrome110", headers=request.headers, data=request.params,
    #                               timeout=task.timeout, verify=False, cookies=task.req.cookies)
    #     else:
    #         r = self.session2.post(request.url, proxies=request.proxy, impersonate="chrome110", headers=request.headers, data=request.params,
    #                               timeout=task.timeout, verify=False)
    #     task.res = res.BaseRes(r, request.isParseRes)
    #     return task

    def Put(self, task, index=0):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        # if isOld:
        #     session = self.oldSession[index]
        # else:
        #     session = self.threadSession[index]

        r = task.session.put(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout, json=task.req.json)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Get(self, task, index=0):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        # if isOld:
        #     session = self.oldSession[index]
        # else:
        #     session = self.threadSession[index]
        if task.req.cookies:
            r = task.session.get(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout,
                                 cookies=task.req.cookies, json=task.req.json)
        else:
            r = task.session.get(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout, json=task.req.json)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    # def Get2(self, task):
    #     request = task.req
    #     if request.params == None:
    #         request.params = {}
    #
    #     if request.headers == None:
    #         request.headers = {}
    #     task.res = res.BaseRes("", False)
    #
    #     if task.req.cookies:
    #         r = self.session2.get(request.url, proxies=request.proxy, impersonate="chrome110", headers=request.headers, timeout=task.timeout, cookies=task.req.cookies)
    #     else:
    #         r = self.session2.get(request.url, proxies=request.proxy, impersonate="chrome110", headers=request.headers, timeout=task.timeout)
    #     task.res = res.BaseRes(r, request.isParseRes)
    #     return task

    def Download(self, request, token="", backParams="", cacheAndLoadPath="", loadPath="", isASync=True):
        self.__DealHeaders(request, token)
        task = Task(request, backParams, cacheAndLoadPath, loadPath)
        if isASync:
            self._downloadQueue.put(task)
        else:
            with requests2.Session() as session:
                self._Download(task, 0, session)

    def ReDownload(self, task):
        task.res = ""
        task.status = Status.Ok
        self._downloadQueue.put(task)

    def _Download(self, task, index, session):
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
                                Log.Info("request{} cache -> backId:{}, {}".format(index, task.bakParam, task.req))
                                return

            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                self.handler.get(task.req.__class__.__name__)(task)
                return

            # 复制curl_opts
            session.curl_options = copy.deepcopy(task.req.curl_opt)
            task.session = session

            request = task.req
            if request.params == None:
                request.params = {}

            if request.headers == None:
                request.headers = {}
            if not request.isReset:
                Log.Info("request{}-> backId:{}, {}".format(index, task.bakParam, task.req))
            else:
                Log.Info(
                    "request{} reset:{} -> backId:{}, {}".format(index, task.req.resetCnt, task.bakParam, task.req))
            # task.res = res.BaseRes(r)
            # print(r.elapsed.total_seconds())
            task.res = None
            task.index = index
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
            # if (task.req.resetCnt > 0):
            #     task.req.isReset = True
            #     self.ReDownload(task)
            #     return
        try:
            self.handler.get(task.req.__class__.__name__)(task)
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            task.res = None
            task.session = None

    def TestSpeed(self, request, bakParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, bakParams)
        self._downloadQueue.put(task)

    def TestSpeedPing(self, request, bakParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, bakParams)
        self._inQueue.put(task)
