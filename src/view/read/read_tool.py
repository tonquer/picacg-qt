import weakref

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtCore import QSize
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLabel

from component.label.msg_label import MsgLabel
from config import config
from config.setting import Setting
from interface.ui_read_tool import Ui_ReadImg
from qt_owner import QtOwner
from tools.book import BookMgr
from tools.str import Str
from tools.tool import CTime, ToolUtil
from view.read.read_enum import ReadMode, QtFileData


class QtCustomSlider(QtWidgets.QSlider):
    def __init__(self, parent):
        QtWidgets.QSlider.__init__(self)
        self.label = QLabel(self)
        self._qtTool = weakref.ref(parent)
        self.label.setFixedSize(QSize(20, 20))
        self.label.setAutoFillBackground(True)
        self.label.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, Qt.white)
        # self.label.setPalette(palette)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setVisible(False)
        self.label.move(0, 3)
        self.setMaximum(100)
        self.setOrientation(Qt.Horizontal)
        self.setPageStep(0)

    @property
    def qtTool(self):
        return self._qtTool()

    def mousePressEvent(self, event):
        if not self.label.isVisible():
            self.label.setVisible(True)
        x = event.pos().x()
        pos = x / self.width()

        w = self.width()
        size = int(w * self.value() / (self.maximum()))
        x2 = self.sliderPosition()

        if not (size-5 <= x <= size+5):
            self.setValue(int(pos * (self.maximum()) + self.minimum()))
            self.label.setText(str(self.value()))
            size = int((self.width() - self.label.width()) * self.value() / (self.maximum()))
            self.label.move(size, 3)
        super(self.__class__, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.label.isVisible():
            self.label.setVisible(False)
            self.qtTool.SkipPicture()
        super(self.__class__, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.label.setText(str(self.value()))
        size = int((self.width() - self.label.width()) * self.value() / (self.maximum() - self.minimum()))
        self.label.move(size, 3)
        super(self.__class__, self).mouseMoveEvent(event)

    def leaveEvent(self, event):
        super(self.__class__, self).leaveEvent(event)

    def keyPressEvent(self, event):
        return

    def keyReleaseEvent(self, event) -> None:
        return


class ReadTool(QtWidgets.QWidget, Ui_ReadImg):

    def __init__(self, imgFrame):
        QtWidgets.QWidget.__init__(self, imgFrame)
        Ui_ReadImg.__init__(self)
        self.setupUi(self)
        self.resize(100, 400)
        self._imgFrame = weakref.ref(imgFrame)
        # self.setWindowFlags(
        #     Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # self.setStyleSheet("background-color:white;")
        # self.setAttribute(Qt.WA_StyledBackground, False)
        # palette = QPalette(self.palette())
        # palette.setColor(QPalette.Background, Qt.white)
        # self.setAutoFillBackground(True)
        # self.setPalette(palette)
        # self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.downloadMaxSize = 0
        self.downloadSize = 0
        self.slider = QtCustomSlider(self)
        self.horizontalLayout_7.addWidget(self.slider)
        self.SetWaifu2xCancle()
        self.scaleBox.installEventFilter(self)
        self.zoomSlider.setMaximum(500)
        # self.buttonGroup.buttonClicked.connect(self.SwitchPicture)
        # self.buttonGroup.setId(self.radioButton, 1)
        # self.buttonGroup.setId(self.radioButton_2, 2)
        # self.buttonGroup.setId(self.radioButton_3, 3)
        # self.buttonGroup.setId(self.radioButton_4, 4)
        # self.buttonGroup.setId(self.radioButton_5, 5)
        # self.buttonGroup.setId(self.radioButton_6, 6)
        self.timerOut = QTimer()
        self.timerOut.setInterval(1000)
        self.timerOut.timeout.connect(self.TimeOut)
        self.isMaxFull = False
        self.gpuLabel.setMaximumWidth(250)
        self.curWaifu2x.clicked.connect(self.OpenCurWaifu)
        self.preDownWaifu2x.clicked.connect(self.OpenPreDownloadWaifu2x)


    @property
    def imgFrame(self):
        return self._imgFrame()

    @property
    def scrollArea(self):
        return self.readImg.scrollArea

    @property
    def readImg(self):
        return self.imgFrame.readImg

    @property
    def curIndex(self):
        return self.readImg.curIndex

    @curIndex.setter
    def curIndex(self, value):
        self.readImg.curIndex = value

    @property
    def maxPic(self):
        return self.readImg.maxPic

    @property
    def stripModel(self):
        return self.readImg.stripModel

    @stripModel.setter
    def stripModel(self, value):
        self.readImg.stripModel = value

    def Show(self, size):
        self.show()

    def Close(self, size):
        self.hide()

    @property
    def scaleCnt(self):
        return self.imgFrame.scaleCnt

    @scaleCnt.setter
    def scaleCnt(self, value):
        self.imgFrame.scaleCnt = value

    def NextPage(self):
        if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            self._LastPage()
        else:
            self._NextPage()
        self.curWaifu2x.setChecked(bool(self.readImg.GetIsWaifu2x()))

    def _NextPage(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().GetBook(bookId)

        if self.curIndex >= self.maxPic - 1:
            if self.readImg.isLocal:
                self.OpenNextEps()
                QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipNext))
                return
            elif self.readImg.isOffline:
                if not QtOwner().downloadView.IsDownloadEpsId(self.readImg.bookId, self.readImg.epsId + 1):
                    QtOwner().ShowMsg(Str.GetStr(Str.NotDownload))
                    return
                self.OpenNextEps()
            else:
                if epsId + 1 < bookInfo.epsCount:
                    QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipNext))
                    self.OpenNextEps()
                return
            self.CloseScrollAndTurn()
            QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextPage))
            return
        t = CTime()

        if ReadMode.isDouble(self.stripModel):
            self.curIndex += 2
            self.curIndex = min(self.curIndex, self.maxPic-1)
        else:
            self.curIndex += 1

        self.imgFrame.oldValue = 0
        self.SetData(isInit=True)
        # self.readImg.CheckLoadPicture()
        # self.readImg.ShowImg()
        # self.readImg.ShowOtherPage()
        self.scrollArea.ResetScrollValue(self.curIndex)
        self.scrollArea.changeNextPage.emit(self.curIndex)
        t.Refresh(self.__class__.__name__)
        return

    def LastPage(self):
        if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            self._NextPage()
        else:
            self._LastPage()
        self.curWaifu2x.setChecked(bool(self.readImg.GetIsWaifu2x()))

    def _LastPage(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId

        if self.curIndex <= 0:
            if self.readImg.isLocal:
                QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipLast))
                self.OpenLastEps()
                return
            elif self.readImg.isOffline:
                if not QtOwner().downloadView.IsDownloadEpsId(self.readImg.bookId, self.readImg.epsId - 1):
                    QtOwner().ShowMsg(Str.GetStr(Str.NotDownload))
                    return
            if epsId - 1 >= 0:
                QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipLast))
                self.OpenLastEps()
                return
            QtOwner().ShowMsg(Str.GetStr(Str.AlreadyLastPage))
            return

        if ReadMode.isDouble(self.stripModel):
            self.curIndex -= 2
            self.curIndex = max(self.curIndex, 0)
        else:
            self.curIndex -= 1

        self.imgFrame.oldValue = 0
        self.SetData(isInit=True)
        # self.readImg.CheckLoadPicture()
        # self.readImg.ShowImg()
        # self.readImg.ShowOtherPage()
        self.scrollArea.ResetScrollValue(self.curIndex)
        self.scrollArea.changeLastPage.emit(self.curIndex)
        return

    def ReturnPage(self):
        # self.readImg.hide()
        # self.hide()
        # QtOwner().owner.bookInfoForm.show()
        self.readImg.Close()
        # QtOwner().owner.bookInfoForm.LoadHistory()
        # self.readImg.Clear()
        return

    def SetData(self, pSize=None, dataLen=0, state="", waifuSize=None, waifuDataLen=0, waifuState="", waifuTick=0, isInit=False):
        self.UpdateSlider()
        self.epsLabel2.setText("{}/{}({})".format(self.readImg.curIndex + 1, self.readImg.maxPic, "{}-{}".format(self.readImg.epsId+1, self.readImg.epsName)))
        if pSize or isInit:
            if not pSize:
                pSize = QSize(0, 0)
            self.resolutionLabel2.setText("{}x{}".format(str(pSize.width()), str(pSize.height())))

        if dataLen or isInit:
            self.sizeLabel2.setText(ToolUtil.GetDownloadSize(dataLen))

        if waifuSize or isInit:
            if not waifuSize:
                waifuSize = QSize(0, 0)
            self.waifu2xRes.setText("{}x{}".format(str(waifuSize.width()), str(waifuSize.height())))
        if waifuDataLen or isInit:
            self.waifu2xSize.setText("" + ToolUtil.GetDownloadSize(waifuDataLen))

        if state or isInit:
            self.stateLable2.setText(Str.GetStr(state))

        if waifuState or isInit:
            if waifuState == QtFileData.WaifuStateStart:
                self.waifu2xStatus.setStyleSheet("color:red;")
            elif waifuState == QtFileData.WaifuStateEnd:
                self.waifu2xStatus.setStyleSheet("color:green;")
            elif waifuState == QtFileData.WaifuStateFail:
                self.waifu2xStatus.setStyleSheet("color:red;")
            else:
                self.waifu2xStatus.setStyleSheet("color:dark;")
            if config.CanWaifu2x:
                self.waifu2xStatus.setText(Str.GetStr(waifuState))
        if waifuTick or isInit:
            self.waifu2xTick.setText(str(waifuTick) + "s")

    def CopyPicture(self):
        owner = self.readImg
        p = owner.pictureData.get(owner.curIndex)
        if not p or not p.data:
            MsgLabel.ShowErrorEx(owner, Str.GetStr(Str.DownloadNot))
            return
        # TODO
        # QtOwner().OpenWaifu2xTool(p.data)
        return

    def OpenCurWaifu(self):
        if self.curWaifu2x.isChecked():
            self.readImg.SetIsWaifu2x(1)
        else:
            self.readImg.SetIsWaifu2x(0)
        # self.scrollArea.changeScale.emit(self.scaleCnt)
        self.readImg.ShowImgAll()
        self.readImg.CheckLoadPicture()
        return

    def OpenPreDownloadWaifu2x(self):
        Setting.PreDownWaifu2x.SetValue(int(self.preDownWaifu2x.isChecked()))
        return

    def OpenWaifu(self):
        if self.checkBox.isChecked():
            Setting.IsOpenWaifu.SetValue(1)
            if config.EncodeGpu == "CPU":
                QtOwner().ShowMsg(Str.GetStr(Str.NotRecommendWaifu2x))
        else:
            Setting.IsOpenWaifu.SetValue(0)

        self.readImg.ShowImgAll()
        # self.readImg.CheckLoadPicture()
        # self.scrollArea.changeScale.emit(self.scaleCnt)
        return

    def UpdateText(self, model):
        model, noise, scale = ToolUtil.GetModelAndScale(model)
        self.modelLabel.setText(model)
        self.noiseLabel.setText(str(noise))
        self.scaleLabel.setText(str(scale))
        self.gpuLabel.setText(QtOwner().settingView.GetGpuName())

    def OpenLastEps(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().GetBook(bookId)

        lasEps = epsId - 1
        if self.readImg.isLocal:
            if epsId < 0:
                QtOwner().ShowMsg(Str.GetStr(Str.AlreadyLastChapter))
                return
            self.readImg.OpenLocalPage(self.readImg._cacheBook, lasEps, 9999)
            return
        elif self.readImg.isOffline:
            if not QtOwner().downloadView.IsDownloadEpsId(self.readImg.bookId, self.readImg.epsId - 1):
                QtOwner().ShowMsg(Str.GetStr(Str.NotDownload))
                return
        else:
            if lastEps >= bookInfo.epsCount:
                return

        if lasEps < 0:
            QtOwner().ShowMsg(Str.GetStr(Str.AlreadyLastChapter))
            return

        self.readImg.AddHistory()
        QtOwner().bookInfoView.LoadHistory()
        self.readImg.OpenPage(bookId, lasEps, 9999)
        return

    def OpenNextEps(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().GetBook(bookId)
        nextEps = epsId + 1
        if self.readImg.isLocal:
            if nextEps >= len(self.readImg._cacheBook.eps):
                QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextChapter))
                return
            self.readImg.OpenLocalPage(self.readImg._cacheBook, nextEps, 0)
            return
        elif self.readImg.isOffline:
            if not QtOwner().downloadView.IsDownloadEpsId(self.readImg.bookId, self.readImg.epsId + 1):
                QtOwner().ShowMsg(Str.GetStr(Str.NotDownload))
                return
        else:
            if nextEps >= bookInfo.epsCount:
                QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextChapter))
                return

        # title = bookInfo.GetEpsTitle(epsId)
        self.readImg.AddHistory()
        QtOwner().bookInfoView.LoadHistory()
        self.readImg.OpenPage(bookId, nextEps)
        return

    def SkipPicture(self, index=0):
        value = self.slider.value()
        if value <= 0:
            return
        oldValue = self.curIndex
        if self.curIndex == value-1:
            return
        if value-1 > self.maxPic -1:
            return
        self.curIndex = value - 1
        self.SetData(isInit=True)
        # self.readImg.CheckLoadPicture()
        # self.readImg.ShowImg()
        # self.readImg.ShowOtherPage()
        self.scrollArea.changePage.emit(oldValue, self.curIndex)

    def InitSlider(self, maxIndex):
        self.slider.setMinimum(1)
        self.slider.setMaximum(maxIndex)

    def UpdateSlider(self):
        self.slider.setValue(self.readImg.curIndex+1)
        if self.readImg.epsName:
            QtOwner().SetSubTitle(self.readImg.epsName + "（{}/{}）".format(self.slider.value(), self.slider.maximum()))

    def FullScreen(self, isClear=False):
        if QtOwner().owner.windowState() == Qt.WindowFullScreen:

            if self.isMaxFull:
                QtOwner().owner.showMaximized()
            else:
                QtOwner().owner.showNormal()
            self.fullButton.setText(Str.GetStr(Str.FullScreen))
            if not isClear:
                Setting.LookReadFull.SetValue(0)
        else:
            self.isMaxFull = self.window().isMaximized()
            QtOwner().owner.showFullScreen()
            self.fullButton.setText(Str.GetStr(Str.ExitFullScreen))
            Setting.LookReadFull.SetValue(1)

    def Waifu2xSave(self):
        self.SetWaifu2xCancle(True)

    def Waifu2xCancle(self):
        Setting.LookNoise.SetValue(self.noiseBox.currentIndex() -1)
        Setting.LookScale.SetValue(self.scaleBox.value())
        Setting.LookModel.SetValue(self.modelBox.currentIndex())

        for data in self.readImg.pictureData.values():

            model = ToolUtil.GetLookScaleModel(self.readImg.category, data.w, data.h, data.mat)
            if data.model.get("model") == model.get("model") and data.model.get("scale") == model.get("scale"):
                continue
            data.model = model
            data.waifuData = None
            data.cacheWaifu2xImage = None

            w, h, _, isAnima = ToolUtil.GetPictureSize(data.data)
            if max(w, h) <= Setting.LookMaxNum.value:
               data.waifuState = data.WaifuWait
            else:
                if data._isWaifu2x == -1:
                    data.waifuState = data.OverResolution
                else:
                    data.waifuState = data.WaifuWait

            if data._isWaifu2x == -1 and isAnima:
                data.waifuState = data.AnimationNotAuto

            data.waifuDataSize = 0
            data.scaleW, data.scaleH = 0, 0
            data.waifuTick = 0

        self.readImg.ShowImgAll()
        # self.readImg.CheckLoadPicture()

        self.SetWaifu2xCancle(False)

    def SetWaifu2xCancle(self, isVisibel=False):
        self.waifu2xSave.setVisible(not isVisibel)
        self.noiseLabel.setVisible(not isVisibel)
        self.scaleLabel.setVisible(not isVisibel)
        self.modelLabel.setVisible(not isVisibel)

        self.waifu2xCancle.setVisible(isVisibel)
        self.noiseBox.setVisible(isVisibel)
        self.scaleBox.setVisible(isVisibel)
        self.modelBox.setVisible(isVisibel)

    def ScalePicture2(self, value):
        self.zoomSlider.setValue(value)

    def ScalePicture(self, value):
        self.zoomLabel.setText(Str.GetStr(Str.Scale)+"（{}%）".format(str(value)))
        scaleV = value//10-10
        oldV = self.imgFrame.scaleCnt
        if self.imgFrame.scaleCnt == scaleV:
            return
        self.imgFrame.scaleCnt = scaleV

        changeV = scaleV - oldV
        if scaleV == 0:
            self.scrollArea.ScaleReset(changeV)

        self.readImg.scrollArea.changeScale.emit(changeV)

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyRelease:
            return True
        elif ev.type() == QEvent.KeyPress:
            return True
        return False

    def ChangeReadMode(self, index):
        self.ChangeReadMode2(index)
        self.imgFrame.InitHelp()
        
    def ChangeReadMode2(self, index):
        self.imgFrame.isLastPageMode = False
        self.stripModel = ReadMode(index)
        self.scrollArea.initReadMode = self.stripModel
        self.scrollArea.allItemsState.clear()

        self.ScalePicture2(100)
        if self.stripModel in [ReadMode.UpDown, ReadMode.Samewight]:
            self.ScalePicture2(80)
        elif self.stripModel == ReadMode.LeftRight:
            pass
            # self.zoomSlider.setValue(100)
            # properties = QScroller.scroller(self.readImg.scrollArea).scrollerProperties()
            # properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 2)
            # properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 2)
            # QScroller.scroller(self.readImg.scrollArea).setScrollerProperties(properties)
        elif ReadMode.isDouble(self.stripModel):
            pass
            # self.zoomSlider.setValue(100)
            # properties = QScroller.scroller(self.readImg.scrollArea).scrollerProperties()
            # properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 2)
            # properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 2)
            # QScroller.scroller(self.readImg.scrollArea).setScrollerProperties(properties)
        elif self.stripModel in [ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            pass
            # self.zoomSlider.setValue(100)
            # properties = QScroller.scroller(self.readImg.scrollArea).scrollerProperties()
            # properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 2)
            # properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 1)
            # QScroller.scroller(self.readImg.scrollArea).setScrollerProperties(properties)
            # self.imgFrame.graphicsView.verticalScrollBar().blockSignals(True)
            # self.imgFrame.graphicsView.horizontalScrollBar().blockSignals(False)

        else:
            pass
            # self.zoomSlider.setValue(100)
            # properties = QScroller.scroller(self.readImg.scrollArea).scrollerProperties()
            # properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 1)
            # properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 2)
            # QScroller.scroller(self.readImg.scrollArea).setScrollerProperties(properties)
            # self.imgFrame.graphicsView.verticalScrollBar().blockSignals(False)
            # self.imgFrame.graphicsView.horizontalScrollBar().blockSignals(True)
        self.ClearQImage()
        self.readImg.scrollArea.InitAllQLabel(self.readImg.maxPic, self.readImg.curIndex)
        # self.readImg.CheckLoadPicture()
        self.readImg.ShowImgAll()

        Setting.LookReadMode.SetValue(index)
        # QtOwner().SetV("Read/LookReadMode", config.LookReadMode)

    def ClearQImage(self):
        for index, v in self.readImg.pictureData.items():
            assert isinstance(v, QtFileData)
            v.cacheWaifu2xImage = None
            v.cacheImage = None
            if v.cacheImageTaskId:
                self.readImg.ClearQImageTaskById(v.cacheImageTaskId)
                v.cacheImageTaskId = 0
            if v.cacheWaifu2xImageTaskId:
                self.readImg.ClearQImageTaskById(v.cacheWaifu2xImageTaskId)
                v.cacheWaifu2xImageTaskId = 0

            # self.readImg.CheckToQImage(index, v, False)
            # self.readImg.CheckToQImage(index, v, True)

    def SwitchScrollAndTurn(self):
        if self.IsStartScrollAndTurn():
            self.CloseScrollAndTurn()
        else:
            self.StartScrollAndTurn()
        return

    def IsStartScrollAndTurn(self):
        if self.timerOut.isActive():
            return True
        return False

    def StartScrollAndTurn(self):
        self.CloseScrollAndTurn()
        if self.stripModel in [ReadMode.LeftRightScroll, ReadMode.RightLeftScroll, ReadMode.UpDown]:
            self.AutoScroll()
        else:
            self.AutoTurn()

    def CloseScrollAndTurn(self):
        if self.timerOut.isActive():
            QtOwner().ShowMsg(Str.GetStr(Str.StopAutoScroll))
            self.timerOut.stop()
        self.imgFrame.scrollArea.vScrollBar.StopScroll()
        self.imgFrame.scrollArea.hScrollBar.StopScroll()
        pass

    def AutoScroll(self):
        self.timerOut.setInterval(1000)
        self.timerOut.start()
        pass

    def AutoTurn(self):
        tick = int(self.turnSpeed.value()*1000)
        self.timerOut.setInterval(tick)
        self.timerOut.start()
        pass

    def TimeOut(self):
        if self.stripModel in [ReadMode.LeftRightScroll, ReadMode.RightLeftScroll, ReadMode.UpDown]:
            value = int(self.scrollSpeed.value())
            if self.stripModel == ReadMode.UpDown:
                if self.imgFrame.scrollArea.vScrollBar.value() >= self.imgFrame.scrollArea.vScrollBar.maximum():
                    self.CloseScrollAndTurn()
                self.imgFrame.scrollArea.vScrollBar.scrollValue(value)
            elif self.stripModel == ReadMode.LeftRightScroll:
                if self.imgFrame.scrollArea.hScrollBar.value() >= self.imgFrame.scrollArea.hScrollBar.maximum():
                    self.CloseScrollAndTurn()
                self.imgFrame.scrollArea.hScrollBar.scrollValue(value)
            elif self.stripModel == ReadMode.RightLeftScroll:
                if self.imgFrame.scrollArea.hScrollBar.value() <= self.imgFrame.scrollArea.hScrollBar.minimum():
                    self.CloseScrollAndTurn()
                self.imgFrame.scrollArea.hScrollBar.scrollValue(-value)
        else:
            self._NextPage()
        pass