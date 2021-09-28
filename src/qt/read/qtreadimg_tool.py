import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import QEvent, Qt
from PySide2.QtCore import QSize
from PySide2.QtGui import QPalette, QPixmap
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QLabel, QScroller, QScrollerProperties

from conf import config
from src.index.book import BookMgr
from src.qt.com.qtmsg import QtMsgLabel
from src.qt.com.qtimg import QtImgMgr
from src.qt.qtmain import QtOwner
from src.qt.struct.qt_define import QtFileData
from src.util import ToolUtil
from src.util.tool import CTime
from ui.readimg import Ui_ReadImg


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


class QtImgTool(QtWidgets.QWidget, Ui_ReadImg):

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
        self.setAutoFillBackground(True)
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
        self.show()

    @property
    def scaleCnt(self):
        return self.imgFrame.scaleCnt

    @scaleCnt.setter
    def scaleCnt(self, value):
        self.imgFrame.scaleCnt = value

    def NextPage(self):
        from src.qt.read.qtreadimg import ReadMode
        if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            self._LastPage()
        else:
            self._NextPage()

    def _NextPage(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().books.get(bookId)

        if self.curIndex >= self.maxPic -1:
            if epsId + 1 < len(bookInfo.eps):
                QtMsgLabel.ShowMsgEx(self.readImg, self.tr("自动跳转到下一章"))
                self.OpenNextEps()
                return
            QtMsgLabel.ShowMsgEx(self.readImg, self.tr("已经最后一页"))
            return
        t = CTime()

        from src.qt.read.qtreadimg import ReadMode
        if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.LeftRightDouble]:
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
        from src.qt.read.qtreadimg import ReadMode
        if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            self._NextPage()
        else:
            self._LastPage()

    def _LastPage(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().books.get(bookId)

        if self.curIndex <= 0:
            if epsId - 1 >= 0:
                QtMsgLabel.ShowMsgEx(self.readImg, self.tr("自动跳转到上一章"))
                self.OpenLastEps()
                return
            QtMsgLabel.ShowMsgEx(self.readImg, self.tr("已经是第一页"))
            return

        from src.qt.read.qtreadimg import ReadMode
        if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.LeftRightDouble]:
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
        self.readImg.hide()
        self.hide()
        QtOwner().owner.bookInfoForm.show()
        self.readImg.AddHistory()
        QtOwner().owner.bookInfoForm.LoadHistory()
        self.readImg.Clear()
        return

    def SetData(self, pSize=None, dataLen=0, state="", waifuSize=None, waifuDataLen=0, waifuState="", waifuTick=0, isInit=False):
        self.UpdateSlider()
        self.epsLabel.setText(self.tr("位置")+"：{}/{}".format(self.readImg.curIndex + 1, self.readImg.maxPic))
        if pSize or isInit:
            if not pSize:
                pSize = QSize(0, 0)
            self.resolutionLabel.setText(self.tr("分辨率")+"：{}x{}".format(str(pSize.width()), str(pSize.height())))

        if dataLen or isInit:
            self.sizeLabel.setText(self.tr("大小")+": " + ToolUtil.GetDownloadSize(dataLen))

        if waifuSize or isInit:
            if not waifuSize:
                waifuSize = QSize(0, 0)
            self.waifu2xRes.setText("{}x{}".format(str(waifuSize.width()), str(waifuSize.height())))
        if waifuDataLen or isInit:
            self.waifu2xSize.setText("" + ToolUtil.GetDownloadSize(waifuDataLen))

        if state or isInit:
            self.stateLable.setText(self.tr("状态：") + self.GetStatus(state))

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
                self.waifu2xStatus.setText(self.GetStatus(waifuState))
        if waifuTick or isInit:
            self.waifu2xTick.setText(str(waifuTick) + "s")

    def GetStatus(self, data):
        if data == QtFileData.Downloading:
            return self.tr("开始下载")
        elif data == QtFileData.Downloading:
            return self.tr("转换中")
        elif data == QtFileData.DownloadSuc:
            return self.tr("下载完成")
        elif data == QtFileData.DownloadError:
            return self.tr("下载错误")
        elif data == QtFileData.DownloadReset:
            return self.tr("重新下载")
        elif data == QtFileData.WaifuWait:
            return self.tr("等待中")
        elif data == QtFileData.WaifuStateStart:
            return self.tr("转换开始")
        elif data == QtFileData.WaifuStateCancle:
            return self.tr("不转换")
        elif data == QtFileData.WaifuStateEnd:
            return self.tr("转换完成")
        elif data == QtFileData.WaifuStateEnd:
            return self.tr("转换失败")
        return data

    def CopyPicture(self):
        owner = self.readImg
        p = owner.pictureData.get(owner.curIndex)
        if not p or not p.data:
            QtMsgLabel.ShowErrorEx(owner, self.tr("下载未完成"))
            return
        QtImgMgr().ShowImg(p.data)
        return

    def OpenWaifu(self):
        if self.checkBox.isChecked():
            config.IsOpenWaifu = 1
        else:
            config.IsOpenWaifu = 0
        self.scrollArea.changeScale.emit(self.scaleCnt)
        return

    def UpdateText(self, model):
        model, noise, scale = ToolUtil.GetModelAndScale(model)
        self.modelLabel.setText(model)
        self.noiseLabel.setText(str(noise))
        self.scaleLabel.setText(str(scale))
        self.gpuLabel.setText(QtOwner().owner.settingForm.GetGpuName())

    def OpenLastEps(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().books.get(bookId)

        epsId -= 1
        if epsId < 0:
            QtMsgLabel.ShowMsgEx(self.readImg, self.tr("已经是第一章"))
            return

        if epsId >= len(bookInfo.eps):
            return

        epsInfo = bookInfo.eps[epsId]
        self.readImg.AddHistory()
        QtOwner().owner.bookInfoForm.LoadHistory()
        self.readImg.OpenPage(bookId, epsId, epsInfo.title, True)
        return

    def OpenNextEps(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().books.get(bookId)

        epsId += 1
        if epsId >= len(bookInfo.eps):
            QtMsgLabel.ShowMsgEx(self.readImg, self.tr("已经是最后一章"))
            return

        if epsId >= len(bookInfo.eps):
            return

        epsInfo = bookInfo.eps[epsId]
        self.readImg.AddHistory()
        QtOwner().owner.bookInfoForm.LoadHistory()
        self.readImg.OpenPage(bookId, epsId, epsInfo.title)
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
        self.readImg.setWindowTitle(self.readImg.epsName + "（{}/{}）".format(self.slider.value(), self.slider.maximum()))

    def FullScreen(self):
        if self.readImg.windowState() == Qt.WindowFullScreen:
            self.readImg.showNormal()
            self.fullButton.setText(self.tr("全屏"))
            config.LookReadFull = 0
        else:
            self.readImg.showFullScreen()
            self.fullButton.setText(self.tr("退出全屏"))
            config.LookReadFull = 1
        self.scrollArea.changeScale.emit(self.scaleCnt)
        QtOwner().SetV("Read/LookReadFull", config.LookReadFull)

    def Waifu2xSave(self):
        self.SetWaifu2xCancle(True)

    def Waifu2xCancle(self):
        config.LookNoise = self.noiseBox.currentIndex() -1
        config.LookScale = self.scaleBox.value()
        config.LookModel = self.modelBox.currentIndex()

        for data in self.readImg.pictureData.values():

            model = ToolUtil.GetLookScaleModel(self.readImg.category)
            if data.model.get("model") == model.get("model") and data.model.get("scale") == model.get("scale"):
                continue
            data.model = model
            data.waifuData = None
            data.cacheWaifu2xImage = None
            data.waifuState = data.WaifuWait
            data.waifuDataSize = 0
            data.scaleW, data.scaleH = 0, 0
            data.waifuTick = 0

        self.readImg.ShowImg()
        self.readImg.ShowOtherPage()
        self.readImg.CheckLoadPicture()

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

    def ScalePicture(self, value):
        self.zoomLabel.setText(self.tr("缩放")+"（{}%）".format(str(value)))
        scaleV = value//10-10
        if self.imgFrame.scaleCnt == scaleV:
            return
        self.imgFrame.scaleCnt = scaleV
        self.readImg.scrollArea.changeScale.emit(scaleV)

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyRelease:
            return True
        elif ev.type() == QEvent.KeyPress:
            return True
        return False

    def ChangeReadMode(self, index):
        from src.qt.read.qtreadimg import ReadMode
        self.stripModel = ReadMode(index)
        if self.stripModel == ReadMode.LeftRight:
            self.zoomSlider.setValue(100)
            self.scaleCnt = 0
            properties = QScroller.scroller(self.readImg.scrollArea).scrollerProperties()
            properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 2)
            properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 2)
            QScroller.scroller(self.readImg.scrollArea).setScrollerProperties(properties)
        elif self.stripModel in [ReadMode.RightLeftDouble, ReadMode.LeftRightDouble]:
            self.zoomSlider.setValue(100)
            self.scaleCnt = 0
            properties = QScroller.scroller(self.readImg.scrollArea).scrollerProperties()
            properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 2)
            properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 2)
            QScroller.scroller(self.readImg.scrollArea).setScrollerProperties(properties)
        elif self.stripModel in [ReadMode.RightLeftScroll, ReadMode.LeftRightScroll]:
            self.zoomSlider.setValue(100)
            self.scaleCnt = 0
            properties = QScroller.scroller(self.readImg.scrollArea).scrollerProperties()
            properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 2)
            properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 1)
            QScroller.scroller(self.readImg.scrollArea).setScrollerProperties(properties)
            # self.imgFrame.graphicsView.verticalScrollBar().blockSignals(True)
            # self.imgFrame.graphicsView.horizontalScrollBar().blockSignals(False)

        else:
            self.zoomSlider.setValue(100)
            self.scaleCnt = 0
            properties = QScroller.scroller(self.readImg.scrollArea).scrollerProperties()
            properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, 1)
            properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, 2)
            QScroller.scroller(self.readImg.scrollArea).setScrollerProperties(properties)
            # self.imgFrame.graphicsView.verticalScrollBar().blockSignals(False)
            # self.imgFrame.graphicsView.horizontalScrollBar().blockSignals(True)

        self.readImg.scrollArea.InitAllQLabel(self.readImg.maxPic, self.readImg.curIndex)
        self.readImg.CheckLoadPicture()
        self.readImg.ShowImg()
        self.readImg.ShowOtherPage()

        config.LookReadMode = index
        QtOwner().SetV("Read/LookReadMode", config.LookReadMode)
        self.imgFrame.InitHelp()




















