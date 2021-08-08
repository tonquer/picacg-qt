import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import QEvent, Qt
from PySide2.QtCore import QSize
from PySide2.QtGui import QPalette, QPixmap
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QLabel

from conf import config
from src.index.book import BookMgr
from src.qt.com.qtbubblelabel import QtBubbleLabel
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
        self.radioButton.installEventFilter(self)
        self.radioButton_2.installEventFilter(self)
        self.downloadMaxSize = 0
        self.downloadSize = 0
        self.slider = QtCustomSlider(self)
        self.horizontalLayout_7.addWidget(self.slider)
        self.SetWaifu2xCancle()
        self.scaleBox.installEventFilter(self)
        self.zoomSlider.setMaximum(500)

    @property
    def imgFrame(self):
        return self._imgFrame()

    @property
    def readImg(self):
        return self.imgFrame.readImg

    @property
    def graphicsGroup(self):
        return self.imgFrame.graphicsGroup

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
    def isStripModel(self):
        return self.readImg.isStripModel

    @isStripModel.setter
    def isStripModel(self, value):
        self.readImg.isStripModel = value

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
        self.graphicsGroup.setPos(0, 0)
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().books.get(bookId)

        if self.curIndex >= self.maxPic -1:
            if epsId + 1 < len(bookInfo.eps):
                QtBubbleLabel.ShowMsgEx(self.readImg, "自动跳转到下一章")
                self.OpenNextEps()
                return
            QtBubbleLabel.ShowMsgEx(self.readImg, "已经最后一页")
            return
        t = CTime()
        self.curIndex += 1
        self.SetData(isInit=True)
        self.readImg.CheckLoadPicture()
        self.readImg.ShowImg()
        self.readImg.ShowOtherPage()
        t.Refresh(self.__class__.__name__)
        return

    def LastPage(self):
        self.graphicsGroup.setPos(0, 0)
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().books.get(bookId)

        if self.curIndex <= 0:
            if epsId - 1 >= 0:
                QtBubbleLabel.ShowMsgEx(self.readImg, "自动跳转到上一章")
                self.OpenLastEps()
                return
            QtBubbleLabel.ShowMsgEx(self.readImg, "已经是第一页")
            return
        self.curIndex -= 1
        self.SetData(isInit=True)
        self.readImg.CheckLoadPicture()
        self.readImg.ShowImg()
        self.readImg.ShowOtherPage()
        return

    def SwitchPicture(self):
        if self.radioButton.isChecked():
            self.isStripModel = False
            self.imgFrame.SetPixIem(1, QPixmap())
            self.imgFrame.SetPixIem(2, QPixmap())
            self.zoomSlider.setValue(100)
            self.scaleCnt = 0
        else:
            self.isStripModel = True
            self.readImg.ShowOtherPage()
            self.zoomSlider.setValue(120)
            self.scaleCnt = 2
        self.graphicsGroup.setPos(0, 0)
        self.imgFrame.ScalePicture()

    def ReturnPage(self):
        self.readImg.hide()
        self.hide()
        QtOwner().owner.bookInfoForm.show()
        self.readImg.AddHistory()
        QtOwner().owner.bookInfoForm.LoadHistory()
        self.readImg.Clear()
        return

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyPress:
            return True
        else:
            return super(self.__class__, self).eventFilter(obj, ev)

    def SetData(self, pSize=None, dataLen=0, state="", waifuSize=None, waifuDataLen=0, waifuState="", waifuTick=0, isInit=False):
        self.UpdateSlider()
        self.epsLabel.setText("位置：{}/{}".format(self.readImg.curIndex + 1, self.readImg.maxPic))
        if pSize or isInit:
            if not pSize:
                pSize = QSize(0, 0)
            self.resolutionLabel.setText("分辨率：{}x{}".format(str(pSize.width()), str(pSize.height())))

        if dataLen or isInit:
            self.sizeLabel.setText("大小: " + ToolUtil.GetDownloadSize(dataLen))

        if waifuSize or isInit:
            if not waifuSize:
                waifuSize = QSize(0, 0)
            self.waifu2xRes.setText("{}x{}".format(str(waifuSize.width()), str(waifuSize.height())))
        if waifuDataLen or isInit:
            self.waifu2xSize.setText("" + ToolUtil.GetDownloadSize(waifuDataLen))

        if state or isInit:
            self.stateLable.setText("状态：" + state)

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
                self.waifu2xStatus.setText(waifuState)
        if waifuTick or isInit:
            self.waifu2xTick.setText(str(waifuTick) + "s")

    def CopyPicture(self):
        owner = self.readImg
        p = owner.pictureData.get(owner.curIndex)
        if not p or not p.data:
            QtBubbleLabel.ShowErrorEx(owner, "下载未完成")
            return
        QtImgMgr().ShowImg(p.data)
        return

    def OpenWaifu(self):
        if self.checkBox.isChecked():
            config.IsOpenWaifu = 1
            self.readImg.ShowImg(True)
            self.readImg.ShowOtherPage(True)
        else:
            config.IsOpenWaifu = 0
            self.readImg.ShowImg(False)
            self.readImg.ShowOtherPage(False)

        return

    def UpdateText(self, model):
        model, noise, scale = ToolUtil.GetModelAndScale(model)
        self.modelLabel.setText(model)
        self.noiseLabel.setText(str(noise))
        self.scaleLabel.setText(str(scale))
        self.gpuLabel.setText(QtOwner().owner.settingForm.GetGpuName())

    def ReduceScalePic(self):
        self.readImg.zoom(1/1.1)
        return

    def AddScalePic(self):
        self.readImg.zoom(1.1)
        return

    def OpenLastEps(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().books.get(bookId)

        epsId -= 1
        if epsId < 0:
            QtBubbleLabel.ShowMsgEx(self.readImg, "已经是第一章")
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
            QtBubbleLabel.ShowMsgEx(self.readImg, "已经是最后一章")
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
        if self.curIndex == value-1:
            return
        if value-1 > self.maxPic -1:
            return
        self.curIndex = value - 1
        self.SetData(isInit=True)
        self.readImg.CheckLoadPicture()
        self.readImg.ShowImg()
        self.readImg.ShowOtherPage()

    def InitSlider(self, maxIndex):
        self.slider.setMinimum(1)
        self.slider.setMaximum(maxIndex)

    def UpdateSlider(self):
        self.slider.setValue(self.readImg.curIndex+1)
        self.readImg.setWindowTitle(self.readImg.epsName + "（{}/{}）".format(self.slider.value(), self.slider.maximum()))

    def FullScreen(self):
        if self.readImg.windowState() == Qt.WindowFullScreen:
            self.readImg.showNormal()
            self.fullButton.setText("全屏")
        else:
            self.readImg.showFullScreen()
            self.fullButton.setText("退出全屏")

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
        self.zoomLabel.setText("缩放（{}%）".format(str(value)))
        self.readImg.zoom(value//10-10)

    def eventFilter(self, obj, ev):
        if obj == self.scaleBox:
            if ev.type() == QEvent.KeyRelease:
                return True
            elif ev.type() == QEvent.KeyPress:
                return True
        return False





















