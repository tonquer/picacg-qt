import hashlib
import os
import time

from config.setting import Setting
from task.qt_task import TaskBase, QtTaskBase
from tools.log import Log
from cachetools import LRUCache, TLRUCache

from tools.tool import ToolUtil


class LRUDiskCache(TLRUCache):
    def popitem(self):
        key, value = super().popitem()
        print('Key "%s" evicted with value "%s"' % (key, value))
        TaskCache().RemoveCacheDiskPath(value.path)
        return key, value


class FilePicCache(object):
    def __init__(self):
        # self.downloadTaskId = 0
        self.data = ""
        self.key = ""
        self.path = ""
        self.size = 0
        self.ttl = 0

    @staticmethod
    def GetSize(self):
        return self.size

    @staticmethod
    def GetTTU(key, value, now):
        isinstance(value, FilePicCache)
        return now + value.ttl


class TaskCache(TaskBase, QtTaskBase):
    MB = 1024 * 1024
    DAY = 24 * 3600

    DefaultMem = 128         # 内存cache默认128M
    DefaultDisk = 1024       # 磁盘cache默认1024M
    DefaultTick = DAY

    TypeInitDiskCache = 1  # 初始化磁盘缓存
    TypeAddDiskCache = 2  # 添加磁盘缓存
    TypeRemoveDiskCache = 3  # 删除磁盘缓存

    def __init__(self):
        TaskBase.__init__(self)
        QtTaskBase.__init__(self)
        self.isOpenMem = False
        self.isOpenDisk = False
        self.isInitDisk = False
        self.diskSaveSecond = self.DAY * 30
        self.memeryCache = LRUCache(maxsize=self.DefaultMem * self.MB, getsizeof=FilePicCache.GetSize)

        # 该结构只有本线程修改，只做统计大小用，无实际存储img数据
        self.diskCache = LRUDiskCache(maxsize=self.DefaultDisk * self.MB, ttu=FilePicCache.GetTTU,
                                      getsizeof=FilePicCache.GetSize)

        self.thread.start()

    def Init(self):
        if not Setting.SavePath.value or not Setting.IsInitSave.value:
            return
        self.isOpenMem = bool(Setting.IsOpenMemCache.value)
        self.isOpenDisk = bool(Setting.IsOpenDiskCache.value)
        if Setting.MemCacheSize.value > 0:
            self.memeryCache = LRUCache(maxsize=Setting.MemCacheSize.value * self.MB, getsizeof=FilePicCache.GetSize)
        if Setting.DiskCacheSize.value > 0:
            self.diskCache = LRUDiskCache(maxsize=Setting.DiskCacheSize.value * self.MB, ttu=FilePicCache.GetTTU,
                                          getsizeof=FilePicCache.GetSize)
        if Setting.DiskCacheDay.value > 0:
            self.diskSaveSecond = Setting.DiskCacheDay.value * self.DAY
        if self.isOpenDisk:
            self._inQueue.put((self.TypeInitDiskCache, ()))
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
        time.sleep(10)
        while True:
            try:
                v = self._inQueue.get(True)
                if v == "":
                    break
                cacheType, params = v
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

    # init
    def __InitDiskCache(self):
        self.isInitDisk = True
        # 遍历cache目录文件，计算缓存时长
        if not Setting.SavePath.value:
            return
        cachePath = Setting.GetCachePath()
        if not cachePath:
            return
        now = int(time.time())
        formatList = [".jpg", ".png", ".gif", ".webp", ".bmp", ".apng", ".jpeg"]
        pathList = ["book", "category", "cover", "game", "user", "waifu2x"]
        for path in pathList:
            for root, dirs, files in os.walk(os.path.join(cachePath, path)):
                for file in files:
                    if file[-4:] in formatList or file[-5:] in formatList:
                        full_path = os.path.join(root, file)
                        mtime = int(os.path.getmtime(full_path))
                        if now - mtime >= self.diskSaveSecond:
                            self.RemoveCacheDiskPath(full_path)
                            continue
                        file = FilePicCache()
                        # 不需要存data
                        file.size = os.path.getsize(full_path)
                        file.key = self.GetPathCacheKey(full_path)
                        file.path = full_path
                        file.ttl = now - mtime
                        self.diskCache[file.key] = file
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
        file.ttl = self.diskSaveSecond
        self.diskCache[file.key] = file
        Log.Debug("add cache disk, key:{}, size:{}".format(file.key, len(data)))
        ToolUtil.SavePicture(data, path, "jpg")
        return

    def RemoveCacheDiskPath(self, path):
        self._inQueue.put((self.TypeRemoveDiskCache, path))
        return

    def __RemoveCacheDiskPath(self, path):
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