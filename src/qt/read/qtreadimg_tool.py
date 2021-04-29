import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import QSize, QEvent, Qt
from PySide2.QtGui import QImage, QPalette
from PySide2.QtWidgets import QApplication, QVBoxLayout, QLabel

from conf import config
from src.index.book import BookMgr
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtimg import QtImgMgr
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
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.label.setPalette(palette)
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
        print(x, x2, w, size)

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


class QtImgTool(QtWidgets.QWidget, Ui_ReadImg):

    def __init__(self, imgFrame):
        QtWidgets.QWidget.__init__(self, imgFrame)
        Ui_ReadImg.__init__(self)
        self.setupUi(self)
        self.resize(100, 400)
        self._imgFrame = weakref.ref(imgFrame)
        self.modelBox.setToolTip(
            """
            cunet通用，效果好，速度慢。
            photo写真，速度块。
            anime_style_art_rgb动漫，速度块。
            """
        )
        # self.setWindowFlags(
        #     Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # self.setStyleSheet("background-color:white;")
        self.setAttribute(Qt.WA_StyledBackground, True)
        palette = QPalette(self.palette())
        palette.setColor(QPalette.Background, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.radioButton.installEventFilter(self)
        self.radioButton_2.installEventFilter(self)
        self.downloadMaxSize = 0
        self.downloadSize = 0
        self.progressBar.setMinimum(0)
        self.slider = QtCustomSlider(self)
        self.horizontalLayout_7.addWidget(self.slider)

    @property
    def imgFrame(self):
        return self._imgFrame()

    @property
    def readImg(self):
        return self.imgFrame.readImg

    @property
    def graphicsItem(self):
        return self.imgFrame.graphicsItem

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
        if self.curIndex >= self.maxPic -1:
            QtBubbleLabel.ShowMsgEx(self.readImg, "已经最后一页")
            return
        t = CTime()
        self.curIndex += 1
        self.SetData(isInit=True)
        info = self.readImg.pictureData.get(self.curIndex)
        self.UpdateProcessBar(info)
        self.readImg.CheckLoadPicture()
        self.readImg.ShowImg()
        t.Refresh(self.__class__.__name__)
        return

    def LastPage(self):
        if self.curIndex <= 0:
            QtBubbleLabel.ShowMsgEx(self.readImg, "已经是第一页")
            return
        self.curIndex -= 1
        info = self.readImg.pictureData.get(self.curIndex)
        self.UpdateProcessBar(info)
        self.SetData(isInit=True)
        self.readImg.CheckLoadPicture()
        self.readImg.ShowImg()
        return

    def SwitchPicture(self):
        if self.radioButton.isChecked():
            self.isStripModel = False
        else:
            self.isStripModel = True
        self.graphicsItem.setPos(0, 0)
        self.scaleCnt = 0
        self.imgFrame.ScalePicture()

    def ReturnPage(self):
        self.readImg.hide()
        self.hide()
        self.readImg.owner().bookInfoForm.show()
        self.readImg.AddHistory()
        self.readImg.owner().bookInfoForm.LoadHistory()
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
            self.resolutionWaifu.setText("分辨率：{}x{}".format(str(waifuSize.width()), str(waifuSize.height())))
        if waifuDataLen or isInit:
            self.sizeWaifu.setText("大小：" + ToolUtil.GetDownloadSize(waifuDataLen))

        if state or isInit:
            self.stateLable.setText("状态：" + state)

        if waifuState or isInit:
            if waifuState == QtFileData.WaifuStateStart:
                self.stateWaifu.setStyleSheet("color:red;")
            elif waifuState == QtFileData.WaifuStateEnd:
                self.stateWaifu.setStyleSheet("color:green;")
            elif waifuState == QtFileData.WaifuStateFail:
                self.stateWaifu.setStyleSheet("color:red;")
            else:
                self.stateWaifu.setStyleSheet("color:dark;")
            if config.CanWaifu2x:
                self.stateWaifu.setText("状态：" + waifuState)
        if waifuTick or isInit:
            self.tickLabel.setText("耗时：" + str(waifuTick) + "s")

    def CopyPicture(self):
        owner = self.readImg
        p = owner.pictureData.get(owner.curIndex)
        if not p or not p.data:
            QtBubbleLabel.ShowErrorEx(owner, "下载未完成")
            return
        QtImgMgr().ShowImg(p.data)
        # clipboard = QApplication.clipboard()
        # owner = self.readImg
        #
        # if self.checkBox.isChecked():
        #     p = owner.pictureData.get(owner.curIndex)
        #     if not p or not p.waifuData:
        #         QtBubbleLabel.ShowErrorEx(owner, "解码还未完成")
        #         return
        #     img = QImage()
        #     img.loadFromData(p.waifuData)
        #     clipboard.setImage(img)
        #     QtBubbleLabel.ShowMsgEx(owner, "复制成功")

        # else:
        #     p = owner.pictureData.get(owner.curIndex)
        #     if not p or not p.data:
        #         QtBubbleLabel.ShowErrorEx(owner, "下载未完成")
        #         return
        #     img = QImage()
        #     img.loadFromData(p.data)
        #     clipboard.setImage(img)
        #     QtBubbleLabel.ShowMsgEx(owner, "复制成功")
        return

    def OpenWaifu(self):
        if self.checkBox.isChecked():
            config.IsOpenWaifu = True
            self.readImg.ShowImg(True)
        else:
            config.IsOpenWaifu = False
            self.readImg.ShowImg(False)

        return

    def UpdateProcessBar(self, info):
        if info:
            self.downloadSize = info.downloadSize
            self.downloadMaxSize = max(1, info.size)
        else:
            self.downloadSize = 0
            self.downloadMaxSize = 1
        self.progressBar.setMaximum(self.downloadMaxSize)
        self.progressBar.setValue(self.downloadSize)

    def UpdateText(self, model):
        index, noise, scale = ToolUtil.GetModelAndScale(model)
        self.modelBox.setCurrentIndex(index)
        self.label_2.setText("去噪等级：" + str(noise))
        self.label_3.setText("放大倍数：" + str(scale))
        self.label_9.setText("转码模式：" + self.readImg.owner().settingForm.GetGpuName())

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
        if epsId <= 0:
            QtBubbleLabel.ShowMsgEx(self.readImg, "已经是第一章")
            return

        if epsId >= len(bookInfo.eps):
            return

        epsInfo = bookInfo.eps[epsId]
        self.readImg.AddHistory()
        self.readImg.owner().bookInfoForm.LoadHistory()
        self.readImg.OpenPage(bookId, epsId, epsInfo.title)
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
        self.readImg.owner().bookInfoForm.LoadHistory()
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
        info = self.readImg.pictureData.get(self.curIndex)
        self.UpdateProcessBar(info)
        self.SetData(isInit=True)
        self.readImg.CheckLoadPicture()
        self.readImg.ShowImg()

    def InitSlider(self, maxIndex):
        self.slider.setMinimum(1)
        self.slider.setMaximum(maxIndex)

    def UpdateSlider(self):
        self.slider.setValue(self.readImg.curIndex+1)

    def SwitchModel(self, index):
        data = self.readImg.pictureData.get(self.readImg.curIndex)
        if not data:
            return
        if not data.model:
            return
        if not data.data:
            return
        index2, _, _ = ToolUtil.GetModelAndScale(data.model)
        if index2 == index:
            return
        data.model = ToolUtil.GetModelByIndex(index)
        data.waifuData = None
        data.waifuState = data.WaifuStateStart
        data.waifuDataSize = 0
        data.scaleW, data.scaleH = 0, 0
        data.waifuTick = 0
        self.label_2.setText("去噪等级：" + str(1))
        self.label_3.setText("放大倍数：" + str(1))
        self.SetData(waifuSize=QSize(), waifuDataLen=0, waifuTick=0)
        self.readImg.ShowImg()
        self.readImg.CheckLoadPicture()
        return