import json
import os
import threading
import time
from zlib import crc32

from config import config
from config.setting import Setting
from task.qt_task import TaskBase, QtDownloadTask
from tools.log import Log
from tools.tool import CTime, ToolUtil


class TaskWaifu2x(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.taskObj.convertBack.connect(self.HandlerTask)
        self.thread.start()

        self.thread2 = threading.Thread(target=self.RunLoad2)
        self.thread2.setName("Task-" + str("Waifu2x"))
        self.thread2.setDaemon(True)

    def Start(self):
        self.thread2.start()
        return

    def Run(self):
        while True:
            try:
                taskId = self._inQueue.get(True)
                self._inQueue.task_done()
                if taskId == "":
                    break

                if taskId not in self.tasks:
                    continue
                task = self.tasks.get(taskId)
                isFind = False
                for cachePath in [task.cacheAndLoadPath, task.loadPath]:
                    data = ToolUtil.LoadCachePicture(cachePath)
                    if data:
                        task.saveData = data
                        self.taskObj.convertBack.emit(taskId)
                        isFind = True
                        continue
                if isFind:
                    continue
                if config.CanWaifu2x:
                    from waifu2x_vulkan import waifu2x_vulkan
                    scale = task.model.get("scale", 0)
                    mat = task.model.get("format", "jpg")
                    if scale <= 0:
                        sts = waifu2x_vulkan.add(task.imgData, task.model.get('model', 0), task.downloadId, task.model.get("width", 0),
                                          task.model.get("high", 0), mat)
                    else:
                        sts = waifu2x_vulkan.add(task.imgData, task.model.get('model', 0), task.downloadId, scale, mat)

                    Log.Info("Add convert info, taskId: {}, model:{}, sts:{}".format(str(task.downloadId), task.model,
                                                                                             str(sts)))
                else:
                    sts = -1
                if sts <= 0:
                    self.taskObj.convertBack.emit(taskId)
                    continue
            except Exception as es:
                Log.Error(es)
                continue

    def LoadData(self):
        if not config.CanWaifu2x:
            time.sleep(100)
            return None
        from waifu2x_vulkan import waifu2x_vulkan
        return waifu2x_vulkan.load(0)

    def RunLoad2(self):
        while True:
            info = self.LoadData()
            if not info:
                break
            t1 = CTime()
            data, convertId, taskId, tick = info
            info = self.tasks.get(taskId)
            if not info:
                continue
            if not data:
                lenData = 0
            else:
                lenData = len(data)

            Log.Warn("convert suc, taskId: {}, dataLen:{}, sts:{} tick:{}".format(str(taskId), lenData,
                                                                                          str(convertId),
                                                                                          str(tick)))
            assert isinstance(info, QtDownloadTask)
            info.saveData = data
            info.tick = tick
            if info.cacheAndLoadPath and not os.path.isdir(os.path.dirname(info.cacheAndLoadPath)):
                os.makedirs(os.path.dirname(info.cacheAndLoadPath))
            if info.cacheAndLoadPath and data:
                with open(info.cacheAndLoadPath, "wb+") as f:
                    f.write(data)
                Log.Debug("add convert cache, cachePath:{}".format(info.cacheAndLoadPath))
            else:
                pass
            self.taskObj.convertBack.emit(taskId)
            t1.Refresh("RunLoad")

    def AddConvertTask(self, path, imgData, model, completeCallBack, backParam=None, cleanFlag=None, filePath=""):
        info = QtDownloadTask()
        info.downloadCompleteBack = completeCallBack
        info.backParam = backParam
        self.taskId += 1
        self.tasks[self.taskId] = info
        info.downloadId = self.taskId
        info.imgData = imgData
        info.model = model
        if path:
            a = crc32(json.dumps(model).encode("utf-8"))
            if Setting.SavePath.value:
                path2 = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), config.Waifu2xPath)
                path = os.path.join(path2, path)
                info.cacheAndLoadPath = path + "-{}".format(a)
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        Log.Debug("add convert info, cachePath:{}, loadPath:{}".format(info.cacheAndLoadPath, info.loadPath))
        self._inQueue.put(self.taskId)
        return self.taskId

    def HandlerTask(self, taskId, isCallBack=True):
        if taskId not in self.tasks:
            return
        t1 = CTime()
        info = self.tasks[taskId]
        assert isinstance(info, QtDownloadTask)

        if info.cleanFlag:
            taskIds = self.flagToIds.get(info.cleanFlag, set())
            taskIds.discard(info.downloadId)
        info.downloadCompleteBack(info.saveData, taskId, info.backParam, info.tick)
        if info.cleanFlag:
            taskIds = self.flagToIds.get(info.cleanFlag, set())
            taskIds.discard(info.downloadId)
        del self.tasks[taskId]
        t1.Refresh("RunLoad")

    def ClearWaitConvertIds(self, taskIds):
        if not taskIds:
            return
        for taskId in taskIds:
            if taskId in self.tasks:
                del self.tasks[taskId]
        Log.Info("cancel wait convert taskId, {}".format(taskIds))
        if config.CanWaifu2x:
            from waifu2x_vulkan import waifu2x_vulkan
            waifu2x_vulkan.removeWaitProc(list(taskIds))

    def Cancel(self, cleanFlag):
        taskIds = self.flagToIds.get(cleanFlag, set())
        if not taskIds:
            return
        removeIds = []
        for taskId in taskIds:
            if taskId in self.tasks:
                del self.tasks[taskId]
                removeIds.append(taskId)
        Log.Info("cancel convert taskId, {}".format(removeIds))
        self.flagToIds.pop(cleanFlag)
        if config.CanWaifu2x:
            from waifu2x_vulkan import waifu2x_vulkan
            waifu2x_vulkan.remove(removeIds)

