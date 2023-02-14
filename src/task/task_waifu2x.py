import json
import os
import threading
import time
from zlib import crc32

from config import config
from config.setting import Setting
from task.qt_task import TaskBase
from tools.log import Log
from tools.status import Status
from tools.str import Str
from tools.tool import CTime, ToolUtil


class QConvertTask(object):
    def __init__(self, taskId=0):
        self.taskId = taskId
        self.callBack = None       # addData, laveSize
        self.backParam = None
        self.cleanFlag = ""
        self.status = Status.Ok
        self.tick = 0
        self.loadPath = ""  #
        self.preDownPath = ""  #
        self.noSaveCache = False
        self.cachePath = ""  #
        self.savePath = ""  #
        self.imgData = b""
        self.saveData = b""

        self.model = {
            "model": 1,
            "scale": 2,
            "toH": 100,
            "toW": 100,
        }

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
            taskId = self._inQueue.get(True)
            self._inQueue.task_done()
            if taskId == "":
                break

            task = self.tasks.get(taskId)
            if not task:
                continue
            assert isinstance(task, QConvertTask)
            try:
                assert isinstance(task, QConvertTask)
                isFind = False

                if task.cachePath:
                    data = ToolUtil.LoadCachePicture(task.cachePath)
                    if data:
                        task.saveData = data
                        self.taskObj.convertBack.emit(taskId)
                        continue

                if task.preDownPath:
                    data = ToolUtil.LoadCachePicture(task.preDownPath)
                    if data:
                        task.saveData = data
                        self.taskObj.convertBack.emit(taskId)
                        continue

                if task.savePath:
                    if ToolUtil.IsHaveFile(task.savePath):
                        self.taskObj.convertBack.emit(taskId)
                        continue

                if task.loadPath:
                    data = ToolUtil.LoadCachePicture(task.loadPath)
                    if data:
                        w, h, mat,_ = ToolUtil.GetPictureSize(data)
                        model = ToolUtil.GetDownloadScaleModel(w, h, mat)
                        task.model = model
                        task.imgData = data

                if not task.imgData:
                    task.status = Status.FileError
                    self.taskObj.convertBack.emit(taskId)
                    continue

                if isFind:
                    continue

                err = ""
                if config.CanWaifu2x:
                    from waifu2x_vulkan import waifu2x_vulkan
                    scale = task.model.get("scale", 0)
                    # mat = task.model.get("format", "jpg")
                    tileSize = Setting.Waifu2xTileSize.GetIndexV()
                    if scale <= 0:
                        sts = waifu2x_vulkan.add(task.imgData, task.model.get('model', 0), task.taskId, task.model.get("width", 0),
                                          task.model.get("high", 0), tileSize=tileSize )
                    else:
                        sts = waifu2x_vulkan.add(task.imgData, task.model.get('model', 0), task.taskId, scale, tileSize=tileSize)

                    if sts <= 0:
                        err = waifu2x_vulkan.getLastError()

                else:
                    sts = -1
                if sts <= 0:
                    task.status = Status.AddError
                    self.taskObj.convertBack.emit(taskId)
                    Log.Warn("Waifu2x convert error, taskId: {}, model:{}, err:{}".format(str(task.taskId), task.model,
                                                                                     str(err)))
                    continue
            except Exception as es:
                Log.Error(es)
                task.status = Status.PathError
                self.taskObj.convertBack.emit(taskId)
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
            tick = round(tick, 2)
            if not info:
                continue
            if not data:
                lenData = 0
            else:
                lenData = len(data)
            if lenData <= 0:
                info.status = Status.FileFormatError
                Log.Warn("convert error, taskId: {}, dataLen:{}, sts:{} tick:{}".format(str(taskId), lenData,
                                                                                          str(convertId),
                                                                                          str(tick)))
            assert isinstance(info, QConvertTask)
            info.saveData = data
            info.tick = tick
            try:
                if not info.noSaveCache:
                    for path in [info.cachePath, info.savePath]:
                        if path and not os.path.isdir(os.path.dirname(path)):
                            os.makedirs(os.path.dirname(path))

                        if path and data:
                            with open(path, "wb+") as f:
                                f.write(data)
            except Exception as es:
                info.status = Status.SaveError
                Log.Error(es)

            self.taskObj.convertBack.emit(taskId)
            t1.Refresh("RunLoad")

    def AddConvertTaskByData(self, path, imgData, model, callBack, backParam=None, preDownPath=None, noSaveCache=False, cleanFlag=None):
        info = QConvertTask()
        info.callBack = callBack
        info.backParam = backParam
        self.taskId += 1
        self.tasks[self.taskId] = info
        info.taskId = self.taskId
        info.imgData = imgData
        info.model = model
        info.preDownPath = preDownPath
        info.noSaveCache = noSaveCache
        if not noSaveCache and path and Setting.SavePath.value:
            info.cachePath = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), os.path.join("waifu2x", path))

        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        Log.Debug("add convert info, taskId:{}, cachePath:{}".format(info.taskId, info.cachePath))
        self._inQueue.put(self.taskId)
        return self.taskId

    def AddConvertTaskByPath(self, loadPath, savePath, callBack, backParam=None, cleanFlag=None):
        info = QConvertTask()
        info.loadPath = loadPath
        info.savePath = savePath
        info.callBack = callBack
        info.backParam = backParam
        self.taskId += 1
        self.tasks[self.taskId] = info
        info.taskId = self.taskId
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        Log.Debug("add convert info, loadPath:{}, savePath:{}".format(info.loadPath, info.savePath))
        self._inQueue.put(self.taskId)
        return self.taskId

    def HandlerTask(self, taskId, isCallBack=True):
        try:
            info = self.tasks.get(taskId)
            if not info:
                return

            assert isinstance(info, QConvertTask)
            info.callBack(info.saveData, info.status, info.backParam, info.tick)
            if info.cleanFlag:
                taskIds = self.flagToIds.get(info.cleanFlag, set())
                taskIds.discard(info.taskId)
            del self.tasks[taskId]
        except Exception as es:
            Log.Error(es)

    def ClearWaitConvertIds(self, taskIds):
        if not taskIds:
            return
        for taskId in taskIds:
            if taskId in self.tasks:
                del self.tasks[taskId]
        # Log.Info("cancel wait convert taskId, {}".format(taskIds))
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

