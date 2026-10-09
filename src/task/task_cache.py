import hashlib
import os
import sqlite3
import time
from datetime import datetime, timedelta

from config.setting import Setting
from task.qt_task import TaskBase, QtTaskBase
from tools.log import Log
from cachetools import LRUCache, TLRUCache

from tools.tool import ToolUtil, time_me


class LRUDiskCache(TLRUCache):
    def popitem(self):
        key, value = super().popitem()
        TaskCache().RemoveCacheDiskPath(value.key, value.path)
        return key, value

    def expire(self, time=None):
        items = super().expire(time)
        for item in items:
            key, val = item
            assert isinstance(val, FilePicCache)
            TaskCache().RemoveCacheDiskPath(val.key, val.path)
        return items

class FilePicCache(object):
    def __init__(self):
        # self.downloadTaskId = 0
        self.data = ""
        self.key = ""
        self.path = ""
        self.size = 0
        self.tick = 0
        self.ttl = 0

    @staticmethod
    def GetSize(self):
        return self.size

    @staticmethod
    def GetTTU(key, value, now):
        isinstance(value, FilePicCache)
        return now + timedelta(seconds=value.ttl)


class DiskCacheDB(object):
    def __init__(self):
        self.db = None
        self.cur = None

    def Init(self):
        self.db = sqlite3.connect(os.path.join(Setting.GetStatePath(), "disk_cache.db"),
                                  check_same_thread=False)
        self.cur = self.db.cursor()
        sql = """\
            create table if not exists cache_path(\
            key varchar primary key,\
            path varchar, \
            tick INTEGER, \
            size INTEGER
            )\
            """
        try:
            suc = self.db.execute(sql)
        except Exception as es:
            Log.Error(es)

        sql = """\
            create table if not exists cache_sys(\
            key varchar primary key,\
            cache_path varchar, \
            last_tick INTEGER
            )\
            """
        try:
            suc = self.db.execute(sql)
        except Exception as es:
            Log.Error(es)

    def GetLastTick(self):
        if not self.db:
            return 0
        try:
            suc = self.cur.execute(
                """
                select last_tick from cache_sys where key='sys'
                """
            )
            for query in self.cur.fetchall():
                return int(query[0])
        except Exception as es:
            Log.Error(es)
        return 0

    def LoadAll(self):
        if not self.db:
            return []
        suc = self.cur.execute(
            """
            select key, path, tick, size from cache_path
            """
        )
        allFile = []
        now = int(time.time())
        for query in self.cur.fetchall():
            file = FilePicCache()
            file.size = int(query[3])
            file.key = query[0]
            file.path = query[1]
            file.tick = int(query[2])
            allFile.append(file)
        return allFile

    def DelAll(self):
        if not self.db:
            return
        try:
            sql = "delete from cache_path where 1"
            suc = self.cur.execute(sql)
            self.cur.execute("COMMIT")
        except Exception as es:
            Log.Error(es)

    def DelByKey(self, key):
        if not self.db:
            return
        try:
            sql = "delete from cache_path where key='{}'".format(key)
            suc = self.cur.execute(sql)
            self.cur.execute("COMMIT")
        except Exception as es:
            Log.Error(es)

    def Add(self, file):
        self.__Add(file)
        self.cur.execute("COMMIT")

    def AddAll(self, files):
        if not files:
            return
        for file in files:
            self.__Add(file)
        self.cur.execute("COMMIT")

    def __Add(self, file):
        assert isinstance(file, FilePicCache)
        if not self.db:
            return
        sql = "INSERT INTO cache_path(key, path, size, tick) " \
              "VALUES ('{0}', '{1}', {2}, {3}) " \
              "ON CONFLICT(key) DO UPDATE SET size={2}, tick={2}". \
            format(file.key, file.path, file.size, file.tick)
        suc = self.cur.execute(sql)
        return

    def UpdateInfo(self):
        if not self.db:
            return
        sql = "INSERT INTO cache_sys(key, last_tick) " \
              "VALUES ('{0}', {1}) " \
              "ON CONFLICT(key) DO UPDATE SET last_tick={1}". \
            format("sys", int(time.time()))
        suc = self.cur.execute(sql)
        return

class TaskCache(TaskBase, QtTaskBase):
    MB = 1024 * 1024
    DAY = 24 * 3600

    DefaultMem = 128         # 内存cache默认128M
    DefaultDisk = 1024       # 磁盘cache默认1024M
    DefaultTick = DAY

    TypeInitDiskDB = 0  # 初始化磁盘缓存
    TypeInitDiskCache = 1  # 初始化磁盘缓存
    TypeAddDiskCache = 2  # 添加磁盘缓存
    TypeRemoveDiskCache = 3  # 删除磁盘缓存

    def __init__(self):
        TaskBase.__init__(self)
        QtTaskBase.__init__(self)
        self.isOpenMem = False
        self.isOpenDisk = False
        self.isInitDisk = False
        self.__diskDB = DiskCacheDB()
        self.diskSaveSecond = self.DAY * 30
        self.memeryCache = LRUCache(maxsize=self.DefaultMem * self.MB, getsizeof=FilePicCache.GetSize)

        # 该结构只有本线程修改，只做统计大小用，无实际存储img数据
        self.diskCache = LRUDiskCache(maxsize=self.DefaultDisk * self.MB, ttu=FilePicCache.GetTTU,
                                      getsizeof=FilePicCache.GetSize, timer=datetime.now)

        self.thread.start()

    def Init(self):
        self._inQueue.put((self.TypeInitDiskDB, ()))

        from qt_owner import QtOwner
        self.taskObj.diskCacheRefresh.connect(QtOwner().settingView.UpdateCacheLabe)

        if not Setting.SavePath.value or not Setting.IsInitSave.value:
            return
        self.isOpenMem = bool(Setting.IsOpenMemCache.value)
        self.isOpenDisk = bool(Setting.IsOpenDiskCache.value)
        if Setting.MemCacheSize.value > 0:
            self.memeryCache = LRUCache(maxsize=Setting.MemCacheSize.value * self.MB, getsizeof=FilePicCache.GetSize)
        if Setting.DiskCacheSize.value > 0:
            self.diskCache = LRUDiskCache(maxsize=Setting.DiskCacheSize.value * self.MB, ttu=FilePicCache.GetTTU,
                                          getsizeof=FilePicCache.GetSize, timer=datetime.now)
        if Setting.DiskCacheDay.value > 0:
            self.diskSaveSecond = Setting.DiskCacheDay.value * self.DAY
        if self.isOpenDisk:
            self._inQueue.put((self.TypeInitDiskDB, ()))
        return

    ## 需要在download前初始化
    def InitDownload(self):
        self.taskObj.downloadBack.connect(self.DownloadSuc)

    ## 需要在waifu2x前初始化
    def InitWaifu2x(self):
        self.taskObj.convertBack.connect(self.ConvertSuc)

    def GetMemSize(self):
        return round(self.memeryCache.currsize / 1024 / 1024, 2)

    def GetDiskSize(self):
        if not self.isInitDisk:
            return -1
        return round(self.diskCache.currsize / 1024 / 1024, 2)

    def Run(self):
        while True:
            try:
                v = self._inQueue.get(True)
                if v == "":
                    break
                cacheType, params = v
                if cacheType == self.TypeInitDiskDB:
                    self.__InitDiskDB()
                if cacheType == self.TypeInitDiskCache:
                    self.__InitDiskCache()
                elif cacheType == self.TypeAddDiskCache:
                    self.__AddCacheDiskPath(*params)
                elif cacheType == self.TypeRemoveDiskCache:
                    self.__RemoveCacheDiskPath(params)
            except Exception as es:
                Log.Error(es)
            self._inQueue.task_done()

    def GetMemDataByKey(self, key):
        with self._taskLock:
            file = self.memeryCache.get(key)
            if file:
                return file.data
        return None

    def AddDownloadFromCache(self, data, resetCnt):
        from task.task_download import QtDownloadTask
        assert isinstance(data, QtDownloadTask)
        taskId = data.downloadId
        from server.server import Server
        from server import req
        if data.memCacheKey and not data.isReload and self.isOpenMem:
            key = data.memCacheKey
            with self._taskLock:
                file = self.memeryCache.get(key)
            if file:
                data.isCacheFetch = True
                TaskBase.taskObj.downloadBack.emit(data.downloadId, file.size, b"")
                TaskBase.taskObj.downloadBack.emit(data.downloadId, 0, file.data)
                Log.Debug("fetch cache info, taskId:{}, key:{}, path:{}, size:{}".format(taskId, key, data.path, len(file.data)))
                return

        Server().Download(req.DownloadBookReq(data.url, data.loadPath, data.cachePath, data.savePath, data.isReload,
                                              resetCnt=resetCnt), backParams=taskId)

    @time_me
    def AddConvertFromCache(self, data):
        from task.task_waifu2x import QConvertTask
        assert isinstance(data, QConvertTask)
        taskId = data.taskId
        if data.path and self.isOpenMem:
            key = self.GetPathCacheKey(self.GetModelCahcehPath(data.path, data.model))
            with self._taskLock:
                file = self.memeryCache.get(key)
            if file:
                data.saveData = file.data
                data.isCacheFetch = True
                TaskBase.taskObj.convertBack.emit(taskId)
                Log.Debug("fetch cache waifu2x info, taskId:{}, key:{}, path:{}, size:{}".format(taskId, key, data.path, len(file.data)))
                return True
        return False

    def ConvertSuc(self, taskId):
        from task.task_waifu2x import QConvertTask, TaskWaifu2x
        task = TaskWaifu2x()._GetTask(taskId)
        if not task or not task.path:
            return
        if task.isCacheFetch:
            return
        if not task.saveData:
            return
        assert isinstance(task, QConvertTask)
        file = FilePicCache()
        file.data = task.saveData
        file.path = self.GetModelCahcehPath(task.path, task.model)
        file.key = self.GetPathCacheKey(file.path)
        file.size = len(file.data)
        Log.Debug("add cache waifu2x info, taskId:{}, key:{}, path:{}, size:{}".format(taskId, file.key, file.path, len(file.data)))
        with self._taskLock:
            self.memeryCache[file.key] = file
        return

    def DownloadSuc(self, downloadId, size, data):
        if not self.isOpenMem:
            return
        if size < 0 or not data:
            return
        from task.task_download import TaskDownload
        task = TaskDownload()._GetTask(downloadId)
        if not task or not task.memCacheKey:
            return
        if task.isCacheFetch:
            return

        file = FilePicCache()
        file.data = data
        file.key = task.memCacheKey
        file.path = task.path
        file.size = len(data)
        Log.Debug("add cache info, taskId:{}, key:{}, path:{}, size:{}".format(downloadId, file.key, file.path, len(data)))
        with self._taskLock:
            self.memeryCache[file.key] = file

    def LoadDataSuc(self, path, data):
        if not path or not data:
            return
        if not self.isOpenMem:
            return
        file = FilePicCache()
        file.data = data
        file.path = path
        file.key = self.GetPathCacheKey(file.path)
        file.size = len(file.data)
        Log.Debug("add cache data info, key:{}, path:{}, size:{}".format(file.key, file.path, len(file.data)))
        with self._taskLock:
            self.memeryCache[file.key] = file
        return

    def __InitDiskDB(self):
        self.__diskDB.Init()
        lastTick = self.__diskDB.GetLastTick()
        Log.Info(f"init disk db, last_tick:{lastTick}")
        if not Setting.SavePath.value or not Setting.IsInitSave.value:
            return
        if not self.isOpenDisk:
            return
        if lastTick > 0:
            now = int(time.time())
            files = self.__diskDB.LoadAll()
            for file in files:
                file.ttl = (file.tick + self.diskSaveSecond) - now
                if file.ttl <= 0 :
                    self.RemoveCacheDiskPath(file.key, file.path)
                    continue
                self.diskCache[file.key] = file

            self.isInitDisk = True
            return
        self.InitDiskCache()
        return

    def InitDiskCache(self):
        self.isInitDisk = False
        self._inQueue.put((self.TypeInitDiskCache, ()))

    # init
    def __InitDiskCache(self):
        self.isInitDisk = True
        # 遍历cache目录文件，计算缓存时长
        if not Setting.SavePath.value:
            return
        cachePath = Setting.GetCachePath()
        if not cachePath:
            return
        self.diskCache.clear()
        self.__diskDB.DelAll()
        now = int(time.time())
        formatList = ToolUtil.AllUseFormat
        pathList = ["book", "category", "cover", "game", "user", "waifu2x"]
        allFiles = []
        for path in pathList:
            for root, dirs, files in os.walk(os.path.join(cachePath, path)):
                for file in files:
                    if file[-4:] in formatList or file[-5:] in formatList:
                        full_path = os.path.join(root, file)
                        key = self.GetPathCacheKey(full_path)
                        mtime = int(os.path.getmtime(full_path))
                        file = FilePicCache()
                        # 不需要存data
                        file.size = os.path.getsize(full_path)
                        file.key = key
                        file.path = full_path
                        file.tick = mtime
                        file.ttl = (file.tick + self.diskSaveSecond) - now
                        if file.ttl <= 0:
                            self.RemoveCacheDiskPath(file.key, file.path)
                            continue
                        self.diskCache[file.key] = file
                        allFiles.append(file)
        self.__diskDB.AddAll(allFiles)
        self.__diskDB.UpdateInfo()
        totalSize = sum([v.size for v in allFiles])
        Log.Debug(f"init disk cache info, len:{len(allFiles)}, size:{totalSize}")
        TaskBase.taskObj.diskCacheRefresh.emit()
        return

    def AddCacheDiskPath(self, path, data):
        if not self.isOpenDisk:
            return
        self._inQueue.put((self.TypeAddDiskCache, (path, data)))

    def __AddCacheDiskPath(self, path, data):
        if not self.isOpenDisk:
            return
        if not path or not data:
            return
        file = FilePicCache()
        # 不需要存data
        file.size = len(data)
        file.key = self.GetPathCacheKey(path)
        file.path = path
        file.tick = int(time.time())
        file.ttl = self.diskSaveSecond
        self.diskCache[file.key] = file
        self.__diskDB.Add(file)
        Log.Debug("add cache disk, key:{}, size:{}".format(file.key, len(data)))
        ToolUtil.SavePicture(data, path, "jpg")
        return

    def RemoveCacheDiskPath(self, key, path):
        self._inQueue.put((self.TypeRemoveDiskCache, (key, path)))
        return

    def __RemoveCacheDiskPath(self, v):
        key, path = v
        self.__diskDB.DelByKey(key)
        if os.path.isfile(path):
            os.remove(path)
            Log.Debug(f"remove cache disk, path: {path}")
        return

    def GetPathCacheKey(self, path):
        path = path.replace("//", "/").replace("/", "\\")
        return hashlib.md5(path.encode("utf-8")).hexdigest()

    def GetModelCahcehPath(self, path, model: dict):
        return path + "/" + f"model/{model.get('model', 0)}/scale/{model.get('scale', 0)}"

    def GetUrlCacheKey(self, url):
        return hashlib.md5(url.encode("utf-8")).hexdigest()