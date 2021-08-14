from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt, QRectF, QPointF, QEvent, QSize
from PySide2.QtGui import QPixmap, QMatrix, QImage
from PySide2.QtWidgets import QDesktopWidget, QMessageBox

from conf import config
from src.index.book import BookMgr
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtloading import QtLoading
from src.qt.qtmain import QtOwner
from src.qt.read.qtreadimg_frame import QtImgFrame
from src.qt.struct.qt_define import QtFileData
from src.qt.util.qttask import QtTaskBase
from src.server import req
from src.util import ToolUtil, Log
from src.util.status import Status
from src.util.tool import time_me, CTime


class QtReadImg(QtWidgets.QWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.loadingForm = QtLoading(self)
        QtTaskBase.__init__(self)
        self.bookId = ""
        self.epsId = 0
        self.resetCnt = config.ResetCnt
        self.curIndex = 0

        self.pictureData = {}
        self.maxPic = 0

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QtImgFrame(self)

        self.gridLayout.addWidget(self.frame)
        self.setMinimumSize(300, 300)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ShowAndCloseTool)
        self.isStripModel = True
        self.setWindowFlags(self.windowFlags() &~ Qt.WindowMaximizeButtonHint &~ Qt.WindowMinimizeButtonHint)

        self.category = []
        self.isInit = False
        self.epsName = ""

        ToolUtil.SetIcon(self)

    @property
    def graphicsView(self):
        return self.frame.graphicsView

    @property
    def graphicsGroup(self):
        return self.frame.graphicsGroup

    @property
    def qtTool(self):
        return self.frame.qtTool

    def closeEvent(self, a0) -> None:
        self.ReturnPage()
        QtOwner().owner.bookInfoForm.show()
        self.Clear()
        a0.accept()

    def Clear(self):
        self.qtTool.UpdateText("")
        self.frame.UpdateProcessBar(None)
        self.bookId = ""
        self.epsId = 0
        self.maxPic = 0
        self.curIndex = 0
        if not self.isStripModel:
            self.qtTool.zoomSlider.setValue(100)
            self.frame.scaleCnt = 0
        else:
            self.qtTool.zoomSlider.setValue(120)
            self.frame.scaleCnt = 2
        self.pictureData.clear()
        self.ClearTask()
        self.ClearConvert()
        self.ClearQImageTask()

    def OpenPage(self, bookId, epsId, name, isLastEps=False, pageIndex=-1):
        if not bookId:
            return
        self.Clear()
        info = BookMgr().books.get(bookId)
        if info:
            self.category = info.tags[:]
            self.category.extend(info.categories)
        self.qtTool.checkBox.setChecked(config.IsOpenWaifu)
        self.qtTool.SetData(isInit=True)
        # self.graphicsGroup.setPixmap(QPixmap())
        self.frame.InitPixMap()
        self.frame.UpdatePixMap()
        self.qtTool.SetData()
        # self.qtTool.show()
        self.bookId = bookId
        self.epsId = epsId
        self.AddHistory()

        if not self.isInit:
            desktop = QDesktopWidget()
            self.resize(desktop.width()//4*3, desktop.height()-100)
            self.move(desktop.width()//8, 0)
            self.isInit = True
        # historyInfo = self.owner().historyForm.GetHistory(bookId)
        # if historyInfo and historyInfo.epsId == epsId:
        #     self.curIndex = historyInfo.picIndex
        # else:
        #     self.AddHistory()
        # self.AddHistory()
        self.epsName = name
        self.loadingForm.show()
        self.StartLoadPicUrl(isLastEps, pageIndex)
        self.setWindowTitle(self.epsName)
        self.show()
        if config.IsTips:
            config.IsTips = 0
            msg = QMessageBox()
            msg.setStyleSheet("QLabel{"
                                 "min-width: 300px;"
                                 "min-height: 300px; "
                                 "}")
            msg.setWindowTitle("操作提示")
            msg.setText("""
            操作提示：             
                下一页：
                    点击右下角区域
                    左滑图片
                    使用键盘→
                上一页：
                    点击左下角区域
                    右滑图片
                    使用键盘←
                打开菜单：
                    点击上方区域
                    点击右键
                缩放：
                    按+,-
                退出：
                    使用键盘ESC
            """)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def ReturnPage(self):
        self.AddHistory()
        QtOwner().owner.bookInfoForm.LoadHistory()
        return

    def StartLoadPicUrl(self, isLastEps=False, pageIndex=-1):
        self.AddHttpTask(req.GetComicsBookOrderReq(self.bookId, self.epsId+1), self.StartLoadPicUrlBack, (isLastEps, pageIndex))

    def CheckLoadPicture(self):
        # i = 0
        newDict = {}
        needUp = False
        removeTaskIds = []
        
        preLoadList = list(range(self.curIndex, self.curIndex + config.PreLoading))

        # 预加载上一页
        if len(preLoadList) >= 2 and self.curIndex > 0:
            preLoadList.insert(2, self.curIndex-1)

        for i, p in self.pictureData.items():
            if i in preLoadList:
                newDict[i] = p
            else:
                needUp = True
                if p.waifu2xTaskId > 0:
                    removeTaskIds.append(p.waifu2xTaskId)

        if needUp:
            self.pictureData.clear()
            self.pictureData = newDict
            self.ClearWaitConvertIds(removeTaskIds)

        for i in preLoadList:
            if i >= self.maxPic or i < 0:
                continue

            bookInfo = BookMgr().books.get(self.bookId)
            epsInfo = bookInfo.eps[self.epsId]
            picInfo = epsInfo.pics[i]
            p = self.pictureData.get(i)
            if not p:
                self.AddDownload(i, picInfo)
                break
            elif p.state == p.Downloading or p.state == p.DownloadReset:
                break

        for i in preLoadList:
            if i >= self.maxPic or i < 0:
                continue                
            if config.IsOpenWaifu:
                p = self.pictureData.get(i)
                if not p or not p.data:
                    break
                if p.waifuState == p.WaifuStateCancle or p.waifuState == p.WaifuWait:
                    p.waifuState = p.WaifuStateStart
                    bookInfo = BookMgr().books.get(self.bookId)
                    epsInfo = bookInfo.eps[self.epsId]
                    picInfo = epsInfo.pics[i]
                    self.AddCovertData(picInfo, i)
                    break
                if p.waifuState == p.WaifuStateStart:
                    break
        pass

    def StartLoadPicUrlBack(self, msg, v):
        isLastEps, pageIndex = v
        if msg != Status.Ok:
            self.StartLoadPicUrl(isLastEps, pageIndex)
        else:
            bookInfo = BookMgr().books.get(self.bookId)
            epsInfo = bookInfo.eps[self.epsId]
            self.maxPic = len(epsInfo.pics)
            if isLastEps:
                self.curIndex = self.maxPic - 1
            elif 0 < pageIndex < self.maxPic:
                self.curIndex = pageIndex
                QtBubbleLabel().ShowMsgEx(self, "继续阅读第{}页".format(pageIndex+1))
            self.qtTool.UpdateSlider()
            self.CheckLoadPicture()
            self.qtTool.InitSlider(self.maxPic)

        return

    def UpdateProcessBar(self, data, laveFileSize, backParam):
        info = self.pictureData.get(backParam)
        if not info:
            return
        if laveFileSize < 0:
            info.downloadSize = 0
        if info.size <= 0:
            info.size = laveFileSize
        info.downloadSize += len(data)
        if self.curIndex != backParam:
            return
        self.frame.UpdateProcessBar(info)

    def CompleteDownloadPic(self, data, st, index):
        self.loadingForm.close()
        p = self.pictureData.get(index)
        if not p:
            p = QtFileData()
            self.pictureData[index] = p
        bookInfo = BookMgr().books.get(self.bookId)
        epsInfo = bookInfo.eps[self.epsId]
        picInfo = epsInfo.pics[index]
        if st != Status.Ok:
            p.state = p.DownloadReset
            self.AddDownload(index, picInfo)
        else:
            p.SetData(data, self.category)
            self.AddQImageTask(data, self.ConvertQImageBack, index)
            self.CheckLoadPicture()
            # if index == self.curIndex:
            #     # self.ShowImg()
            #     pass
            # elif self.isStripModel and self.curIndex < index <= self.curIndex + 2:
            #     # self.ShowOtherPage()
            #     self.CheckLoadPicture()
            # else:
            #     self.CheckLoadPicture()
            # return

    def ConvertQImageBack(self, data, index):
        assert isinstance(data, QImage)
        p = self.pictureData.get(index)
        if not p:
            return
        assert isinstance(p, QtFileData)
        p.cacheImage = data
        if index == self.curIndex:
            self.ShowImg()
        elif self.isStripModel and self.curIndex < index <= self.curIndex + 2:
            self.ShowOtherPage()
        return

    @time_me
    def ShowOtherPage(self, isShowWaifu=True):
        for index in range(self.curIndex+1, self.curIndex+3):
            p = self.pictureData.get(index)
            if not p or (not p.data) or (not p.cacheImage):
                self.frame.SetPixIem(index-self.curIndex, QPixmap())
                continue

            assert isinstance(p, QtFileData)
            if not isShowWaifu:
                p2 = p.cacheImage

            elif p.cacheWaifu2xImage:
                p2 = p.cacheWaifu2xImage
            else:
                p2 = p.cacheImage

            pixMap = QPixmap(p2)
            self.frame.SetPixIem(index-self.curIndex, pixMap)
        # self.frame.ScalePicture()
        return True

    @time_me
    def ShowImg(self, isShowWaifu=True):
        p = self.pictureData.get(self.curIndex)

        if not p or (not p.data) or (not p.cacheImage):
            if not p or (not p.data):
                self.qtTool.SetData(state=QtFileData.Downloading)
            else:
                self.qtTool.SetData(state=QtFileData.Converting)

            self.frame.SetPixIem(0, QPixmap())

            self.qtTool.modelBox.setEnabled(False)
            self.frame.UpdateProcessBar(None)
            self.frame.process.show()
            return

        self.frame.process.hide()
        if config.CanWaifu2x:
            self.qtTool.modelBox.setEnabled(True)
        assert isinstance(p, QtFileData)
        if not isShowWaifu:
            self.frame.waifu2xProcess.hide()
            self.qtTool.SetData(waifuSize=QSize(0, 0), waifuDataLen=0)
            p2 = p.cacheImage

        elif p.cacheWaifu2xImage:
            p2 = p.cacheWaifu2xImage
            self.frame.waifu2xProcess.hide()
            self.qtTool.SetData(waifuSize=p.waifuQSize, waifuDataLen=p.waifuDataSize,
                                waifuTick=p.waifuTick)

        else:
            p2 = p.cacheImage
            if config.IsOpenWaifu:
                self.frame.waifu2xProcess.show()
            else:
                self.frame.waifu2xProcess.hide()

        self.qtTool.SetData(pSize=p.qSize, dataLen=p.size, state=p.state, waifuState=p.waifuState)
        self.qtTool.UpdateText(p.model)
        
        pixMap = QPixmap(p2)
        self.frame.SetPixIem(0, pixMap)
        # self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(pixMap.width(), pixMap.height())))
        # self.frame.ScalePicture()
        self.CheckLoadPicture()
        return True

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyPress:
            return True
        else:
            return super(self.__class__, self).eventFilter(obj, ev)

    def zoomIn(self):
        """放大"""
        self.zoom(1.1)

    def zoomOut(self):
        """缩小"""
        self.zoom(1/1.1)

    def zoom(self, scaleV):
        """缩放
        :param factor: 缩放的比例因子
        """
        # q = QMatrix()
        # q.setMatrix(1, self.graphicsView.matrix().m12(), self.graphicsView.matrix().m21(), 1, self.graphicsView.matrix().dx(), self.graphicsView.matrix().dy())
        # self.graphicsView.setMatrix(q, False)

        # _factor = self.graphicsView.transform().scale(
        #     factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        # print(_factor)
        # if _factor < 0.07 or _factor > 100:
        #     # 防止过大过小
        #     return
        if self.frame.scaleCnt == scaleV:
            return
        # for _ in range(abs(scaleV - self.frame.scaleCnt)):
        #     if scaleV - self.frame.scaleCnt > 0:
        #         self.graphicsView.scale(1.1, 1.1)
        #     else:
        #         self.graphicsView.scale(1/1.1, 1/1.1)
        self.frame.scaleCnt = scaleV
        self.frame.ScalePicture()

    def keyReleaseEvent(self, ev):
        if ev.modifiers() == Qt.ShiftModifier and ev.key() == Qt.Key_Left:
            self.qtTool.OpenLastEps()
            return
        if ev.modifiers() == Qt.ShiftModifier and ev.key() == Qt.Key_Right:
            self.qtTool.OpenNextEps()
            return
        # print(ev.modifiers, ev.key())
        if ev.key() == Qt.Key_Plus or ev.key() == Qt.Key_Equal:
            self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value()+10)
            return
        if ev.key() == Qt.Key_Minus:
            self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value()-10)
            return
        if ev.key() == Qt.Key_Left:
            self.qtTool.LastPage()
            return
        elif ev.key() == Qt.Key_Right:
            self.qtTool.NextPage()
            return
        elif ev.key() == Qt.Key_Escape:
            if self.windowState() == Qt.WindowFullScreen:
                self.showNormal()
                self.frame.qtTool.fullButton.setText("全屏")
                return
            self.qtTool.ReturnPage()
            return
        # elif ev.key() == Qt.Key_Up:
        #     point = self.graphicsItem.pos()
        #     self.graphicsItem.setPos(point.x(), point.y()+50)
        #     return
        # elif ev.key() == Qt.Key_Down:
        #     point = self.graphicsItem.pos()
        #     self.graphicsItem.setPos(point.x(), point.y()-50)
        #     return
        super(self.__class__, self).keyReleaseEvent(ev)

    def AddHistory(self):
        bookName = QtOwner().owner.bookInfoForm.bookName
        url = QtOwner().owner.bookInfoForm.url
        path = QtOwner().owner.bookInfoForm.path
        QtOwner().owner.historyForm.AddHistory(self.bookId, bookName, self.epsId, self.curIndex, url, path)
        return

    def ShowAndCloseTool(self):
        if self.qtTool.isHidden():
            self.qtTool.show()
        else:
            self.qtTool.hide()

    def Waifu2xBack(self, data, waifu2xId, index, tick):
        p = self.pictureData.get(index)
        if waifu2xId <= 0 or not p:
            Log.Error("Not found waifu2xId ：{}, index: {}".format(str(waifu2xId), str(index)))
            return
        p.SetWaifuData(data, round(tick, 2))
        self.AddQImageTask(data, self.ConvertQImageWaifu2xBack, index)
        if index == self.curIndex:
            self.qtTool.SetData(waifuState=p.waifuState)
            # self.ShowImg()
        elif self.isStripModel and self.curIndex < index <= self.curIndex + 2:
            # self.ShowOtherPage()
            self.CheckLoadPicture()
        else:
            self.CheckLoadPicture()

    def ConvertQImageWaifu2xBack(self, data, index):
        assert isinstance(data, QImage)
        p = self.pictureData.get(index)
        if not p:
            return
        assert isinstance(p, QtFileData)
        p.cacheWaifu2xImage = data
        if index == self.curIndex:
            self.ShowImg()
        elif self.isStripModel and self.curIndex < index <= self.curIndex + 2:
            self.ShowOtherPage()
        return

    def AddCovertData(self, picInfo, i):
        info = self.pictureData.get(i)
        if not info and info.data:
            return
        assert isinstance(info, QtFileData)
        # path = QtOwner().owner.downloadForm.GetConvertFilePath(self.bookId, self.epsId, i)
        info.waifu2xTaskId = self.AddConvertTask(picInfo.path, info.data, info.model, self.Waifu2xBack, i)
        if i == self.curIndex:
            self.qtTool.SetData(waifuState=info.waifuState)
            self.frame.waifu2xProcess.show()

    def AddDownload(self, i, picInfo):
        path = QtOwner().owner.downloadForm.GetDonwloadFilePath(self.bookId, self.epsId, i)
        self.AddDownloadTask(picInfo.fileServer, picInfo.path,
                                 downloadCallBack=self.UpdateProcessBar,
                                 completeCallBack=self.CompleteDownloadPic, backParam=i,
                                 isSaveCache=True, filePath=path)
        if i not in self.pictureData:
            data = QtFileData()
            self.pictureData[i] = data
        self.qtTool.SetData(state=self.pictureData[i].state)
