import hashlib
import threading
import time
import zipfile
from queue import Queue

from qt_owner import QtOwner
from task.qt_task import TaskBase, QtTaskBase
from tools.log import Log
from tools.singleton import Singleton
import os
from natsort import natsorted

from tools.status import Status
from tools.str import Str


class QLocalTask(object):
    def __init__(self, taskId=0):
        self.taskId = taskId
        self.callBack = None       # addData, laveSize
        self.backParam = None
        self.cleanFlag = ""
        self.status = Status.Ok
        self.type = 0
        self.path = ""  #

        self.bookId = 0
        self.isZip = False
        self.index = 0
        self.path = ""
        self.filePath = ""
        self.fileName = ""


class LocalData(object):
    Type1 = 1    # 加载目录
    Type2 = 2    # 加载文件
    Type3 = 3    # 加载目录所有
    Type4 = 4    #
    Type5 = 5    # 批量加载
    Type6 = 6    # 批量加载目录列表

    AllPictureFormat = ["jpg", "jpeg", "webp", "gif", "apng", "png"]

    def __init__(self) -> None:
        self.id     = ""   # md5 或者 生成Id
        self.main_id = ""  # 父节点
        self.epsId = 1     # 章节ID
        self.title  = ""   # 名称
        self.file = ""     # 文件名
        self.path   = ""   # 路径
        self.cover  = ""   # 封面缓存
        self.isZipFile = True
        self.lastIndex = 0
        self.lastEpsId = 0
        self.category = ""
        self.desc = ""
        self.addTime = 0       # 添加时间
        self.lastReadTime = 0  # 上次阅读时间
        self.picCnt = 0        # 图片数
        self.pic = []          # 图片数
        self.eps = []          # 多章节

    @property
    def isWaifu2x(self):
        return "waifu2x" in self.file or "waifu2x" in self.path

    def CopyData(self, o):
        assert isinstance(o, LocalData)
        self.cover = o.cover
        self.picCnt = o.picCnt
        self.pic = []
        self.pic.extend(o.pic)

        oldDict = {}

        for v in self.eps:
            oldDict[v.id] = v

        self.eps.clear()
        for v in o.eps:
            if v.id in oldDict:
                newV = oldDict[v.id]
                newV.CopyData(v)
                self.eps.append(newV)
            else:
                self.eps.append(v)

    @property
    def sumPicCnt(self):
        a = 0
        for v in self.eps:
            a += v.picCnt
        return self.picCnt + a

    # 根据名称排序
    def SortFilePic(self):
        self.pic = natsorted(self.pic)
        if self.pic:
            self.cover = self.pic[0]
        return

    def SortEps(self):
        self.eps = natsorted(self.eps, key=lambda a:a.title)
        if self.eps:
            first = self.eps[0]
            path = first.file.replace(self.file, "").strip("\\").strip("/")
            self.cover = os.path.join(path, os.path.join(first.path, first.cover))
            for v in self.eps:
                v.main_id = self.id
        return

class TaskLocal(TaskBase, QtTaskBase):
    def __init__(self) -> None:
        TaskBase.__init__(self)
        QtTaskBase.__init__(self)

        # self.thread.start()
        #
        # self.cacheBookZipName = ""
        # self.cacheBookZip = None
        self._inQueue = Queue()
        self._loadQueue = Queue()
        self.thread.start()

        self.thread2 = threading.Thread(target=self.RunLoad2)
        self.thread2.setName("Task-" + str("Waifu2x"))
        self.thread2.setDaemon(True)
        self.thread2.start()

        self.taskObj.localBack.connect(self.HandlerTask)
        self.taskObj.localReadBack.connect(self.HandlerTask2)

        self.cacheBookZip = None
        self.cacheBookId = ""

    def Run(self):
        while True:
            taskId = self._inQueue.get(True)
            self._inQueue.task_done()
            try:
                if taskId == "":
                    break
                self._LoadRead(taskId)
            except Exception as es:
                Log.Error(es)
        pass

    def RunLoad2(self):
        while True:
            task = self._loadQueue.get(True)
            self._loadQueue.task_done()
            try:
                if task == "":
                    break
                self._LoadRead2(task)
            except Exception as es:
                Log.Error(es)
        pass

    def Stop(self):
        self._inQueue.put("")

    def ClearQImageTaskById(self, taskId):
        if taskId in self.tasks:
            self.tasks.pop(taskId)

    def HandlerTask(self, taskId, st, newData):
        try:
            info = self.tasks.get(taskId)
            if not info:
                Log.Warn("[TaskLocal] not find taskId:{}, {}".format(taskId, len(newData)))
                return
            assert isinstance(info, QLocalTask)
            if info.cleanFlag:
                taskIds = self.flagToIds.get(info.cleanFlag, set())
                taskIds.discard(info.taskId)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(st, newData)
                else:
                    info.callBack(st, newData, info.backParam)
                del info.callBack
            del self.tasks[taskId]
        except Exception as es:
            Log.Error(es)

    def HandlerTask2(self, taskId, st, newData):
        try:
            info = self.tasks.get(taskId)
            if not info:
                Log.Warn("[TaskLocal] not find taskId:{}, {}".format(taskId, len(newData)))
                return
            assert isinstance(info, QLocalTask)
            if info.cleanFlag:
                taskIds = self.flagToIds.get(info.cleanFlag, set())
                taskIds.discard(info.taskId)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(newData, st)
                else:
                    info.callBack(newData, st, info.backParam)
                del info.callBack
            del self.tasks[taskId]
        except Exception as es:
            Log.Error(es)

    def _LoadRead(self, taskId):
        task = self.tasks.get(taskId)
        if not task:
            return
        type = task.type
        dir = task.path
        if type == LocalData.Type1:
            st, data = self.ParseBookInfoByDir(dir)
            datas = [data]
        elif type == LocalData.Type2:
            st, data = self.ParseBookInfoByFile(dir)
            datas = [data]
        elif type == LocalData.Type3:
            st, data = self.ParseBookInfoByDirRecursion(dir)
            datas = [data]
        elif type == LocalData.Type4:
            st, datas = self.ParseBookInfoByFile(dir)
        elif type == LocalData.Type5:
            st, datas = self.ParseBookInfoByFileAll(dir)
        elif type == LocalData.Type6:
            datas = []
            for d in dir:
                st, data = self.ParseBookInfoByDirRecursion(d)
                if st == Str.Ok:
                    datas.append(data)
            st = Str.Ok
        self.taskObj.localBack.emit(taskId, st, datas)

    def _LoadRead2(self, taskId):
        task = self.tasks.get(taskId)
        if not task:
            return
        st, data = self.GetBookPicture(task)
        self.taskObj.localReadBack.emit(taskId, st, data)

    def AddLoadRead(self, type, path, backParam, callBack, cleanFlag):
        self.taskId += 1
        info = QLocalTask(self.taskId)
        info.callBack = callBack
        info.backParam = backParam
        info.type = type
        info.path = path

        self.tasks[self.taskId] = info
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        self._inQueue.put(self.taskId)
        return self.taskId

    def AddLoadReadPicture(self, v2, index, backParam, callBack, cleanFlag):
        self.taskId += 1
        assert isinstance(v2, LocalData)
        if index == -1 and v2.eps:
            v = v2.eps[0]
        else:
            v = v2

        info = QLocalTask(self.taskId)
        info.callBack = callBack
        info.backParam = backParam
        info.bookId = v.id
        info.index = index
        if index == -1:
            info.fileName = v.cover
        else:
            if index >= len(v.pic):
                assert False
            info.fileName = v.pic[index]

        info.filePath = v.path
        info.isZip = v.isZipFile
        info.path = v.file

        self.tasks[self.taskId] = info
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        self._loadQueue.put(self.taskId)
        return self.taskId

    def ParseBookInfoByDir(self, dirName):
        # 解析目录
        # 判断是否是下一层有文件
        try:
            path = dirName
            if not os.path.isdir(dirName):
                return Str.ErrorPath, ""
            nextPath = ""
            allPictureName = []
            while True:
                firstDirName = ""
                isNotPicture = True
                allPictureName = []
                for v in os.scandir(os.path.join(path, nextPath)):
                    isinstance(v, os.DirEntry)

                    if v.is_dir():
                        if not firstDirName:
                            firstDirName = v.name
                        continue
                    if not v.is_file:
                        continue
                    data = v.name.split(".")
                    if len(data) < 2:
                        continue
                    mat = data[-1]
                    if mat not in LocalData.AllPictureFormat:
                        continue
                    isNotPicture = False
                    allPictureName.append(v.name)
                if not isNotPicture:
                    break
                else:
                    if not firstDirName:
                        break
                nextPath = os.path.join(nextPath, firstDirName)

            if not allPictureName:
                return Str.NotPictureFile, ""
            l = LocalData()
            l.path = nextPath
            l.file = dirName
            l.id = hashlib.md5(l.file.encode("utf-8")).hexdigest()
            l.main_id = l.id
            l.title = os.path.basename(dirName)
            l.isZipFile = False
            l.addTime = int(time.time())
            l.pic = allPictureName
            l.picCnt = len(l.pic)
            l.SortFilePic()

        except Exception as es:
            Log.Error(es)
            return Str.ErrorPath, ""
        return Status.Ok, l

    def ParseBookInfoByDirRecursion(self, dirName):
        # 解析递归目录

        # 获取目录名称
        path = dirName

        try:
            if not os.path.isdir(dirName):
                return Str.ErrorPath, ""
            nextPath = ""
            allData = self.ParseBookInfoByDirRecursion2(dirName)
            if not allData:
                return Str.ErrorPath, ""
            if len(allData) <= 1 :
                return self.ParseBookInfoByDir(dirName)
            l = LocalData()
            l.eps = allData
            l.title = os.path.basename(dirName)
            l.file = dirName
            l.id = hashlib.md5(l.file.encode("utf-8")).hexdigest()
            l.SortEps()
            l.path = ""

            l.main_id = l.id
            l.isZipFile = False
            l.addTime = int(time.time())

        except Exception as es:
            Log.Error(es)
            return Str.ErrorPath, ""
        return Status.Ok, l

    def ParseBookInfoByDirRecursion2(self, dirName):
        allData = []
        try:
            if not os.path.isdir(dirName):
                return []
            allDir = []
            zipFile = []
            picNum = 0
            for v in os.scandir(dirName):
                isinstance(v, os.DirEntry)

                if v.is_dir():
                    allDir.append(v.name)
                elif v.is_file():
                    data = v.name.split(".")
                    if len(data) < 2:
                        continue
                    mat = data[-1]
                    if mat == "zip":
                        zipFile.append(v.name)
                    if mat in LocalData.AllPictureFormat:
                        picNum += 1
            for zipName in zipFile:
                st, l = self.ParseBookInfoByFile(os.path.join(dirName, zipName))
                if st == Status.Ok:
                    allData.append(l)
            if picNum > 1:
                st, l = self.ParseBookInfoByDir(dirName)
                if st == Status.Ok:
                    allData.append(l)
            else:
                for file in allDir:
                    newAllData = self.ParseBookInfoByDirRecursion2(os.path.join(dirName, file))
                    allData.extend(newAllData)
        except Exception as es:
            Log.Error(es)
        return allData


    def ParseBookInfoByFile(self, fileName):
        # 解析
        # 判断ZIP是否存在
        path = fileName
        if not os.path.isfile(path):
            return Str.ErrorPath, ""

        if not zipfile.is_zipfile(path):
            return Str.NotZIPFile, ""

        try:
            with zipfile.ZipFile(fileName, 'r') as zfile:
                dirPictures = {}
                for v in zfile.infolist():
                    # zfile.read(v)
                    assert isinstance(v, zipfile.ZipInfo)
                    if v.is_dir():
                        continue

                    data = v.filename.split(".")
                    if len(data) < 2:
                        continue
                    mat = data[-1]
                    if mat not in LocalData.AllPictureFormat:
                        continue
                    path = os.path.dirname(v.filename)
                    name = os.path.basename(v.filename)
                    allData = dirPictures.setdefault(path, [])
                    allData.append(name)

                allPictureName = []
                nextPath = ""
                for k, v in dirPictures.items():
                    if len(v) <= 1:
                        continue
                    nextPath = k
                    allPictureName = v

                if not allPictureName:
                    return Str.NotPictureFile, ""

                l = LocalData()
                l.file = fileName
                l.path = nextPath
                l.id = hashlib.md5(fileName.encode("utf-8")).hexdigest()
                l.main_id = l.id
                l.title = os.path.basename(fileName).replace(".zip", "")
                l.isZipFile = True
                l.addTime = int(time.time())
                l.pic = allPictureName
                l.picCnt = len(l.pic)
                l.SortFilePic()
                # 读取第一张图片当封面
        except RuntimeError as es:
            if 'encrypted' in str(es):
                return Str.FileLock, ""
            else:
                Log.Error(es)
                return Str.ErrorPath, ""
        except Exception as es:
            Log.Error(es)
            return Str.ErrorPath, ""
        return Status.Ok, l

    def ParseBookInfoByFileAll(self, fileNames):
        allBooks = []
        for url in fileNames:
            if os.path.isfile(url):
                st, v = self.ParseBookInfoByFile(url)
            elif os.path.isdir(url):
                st, v = self.ParseBookInfoByDirRecursion(url)
            else:
                st = Status.Error
            if st == Status.Ok:
                allBooks.append(v)
        return Status.Ok, allBooks

    def GetBookCover(self, v):
        return self.GetBookPicture(v, 0, 1)

    def GetBookPicture(self, v):
        assert isinstance(v, QLocalTask)
        # # 解析图片
        # assert isinstance(v, LocalData)
        # if v.epsId != epsId:
        #     if epsId - 1 >= len(v.eps):
        #         return Str.NotFoundEps, ""
        #     v = v.eps[epsId-1]
        try:
            if v.isZip:
                if self.cacheBookId == v.bookId and self.cacheBookZip:
                    f = self.cacheBookZip
                    if v.filePath:
                        data = f.read(v.filePath + "/" + v.fileName)
                    else:
                        data = f.read(v.fileName)
                else:
                    f = zipfile.ZipFile(v.path, 'r')
                    if self.cacheBookZip:
                        self.cacheBookZip.close()
                        self.cacheBookZip = None

                    if v.index != -1:
                        self.cacheBookZip = f
                        self.cacheBookId = v.bookId
                    if v.filePath:
                        data = f.read(v.filePath+"/"+v.fileName)
                    else:
                        data = f.read(v.fileName)
                    if v.index == -1:
                        f.close()
            else:
                filePath = os.path.join(v.path, os.path.join(v.filePath, v.fileName))
                if not os.path.isfile(filePath):
                    return Str.NotFoundPicture, ""
                f = open(filePath, "rb")
                data = f.read()
                f.close()
        except RuntimeError as es:
            if 'encrypted' in str(es):
                return Str.FileLock, b""
            else:
                Log.Error(es)
                return Str.ErrorPath, b""
        except Exception as es:
            Log.Error(es)
            return Str.NotFoundPicture, b""
        return Status.Ok, data
