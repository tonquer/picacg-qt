import weakref

from PySide2 import QtWidgets
from PySide2.QtCore import QSize, QEvent, Qt
from PySide2.QtGui import QImage
from PySide2.QtWidgets import QApplication, QVBoxLayout, QLabel

from conf import config
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.util import ToolUtil
from src.util.tool import CTime
from ui.readimg import Ui_ReadImg


class QtImgTool(QtWidgets.QWidget, Ui_ReadImg):

    def __init__(self, imgFrame):
        QtWidgets.QWidget.__init__(self, imgFrame)
        Ui_ReadImg.__init__(self)
        self.setupUi(self)
        self.resize(100, 300)
        self._imgFrame = weakref.ref(imgFrame)
        # self.setWindowFlags(
        #     Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setStyleSheet("background-color:white;")
        self.radioButton.installEventFilter(self)
        self.radioButton_2.installEventFilter(self)
        self.downloadMaxSize = 0
        self.downloadSize = 0
        self.progressBar.setMinimum(0)

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
        return self.readImg.scaleCnt

    @scaleCnt.setter
    def scaleCnt(self, value):
        self.readImg.scaleCnt = value

    def NextPage(self):
        if self.curIndex >= self.maxPic -1:
            QtBubbleLabel.ShowMsgEx(self.readImg, "已经最后一页")
            return
        t = CTime()
        self.curIndex += 1
        self.SetData(isInit=True)
        info = self.readImg.pictureData.get(self.curIndex)
        if info:
            self.UpdateProcessBar(info.downloadSize, info.size)

        self.readImg.ShowImg()
        t.Refresh(self.__class__.__name__)
        return

    def LastPage(self):
        if self.curIndex <= 0:
            QtBubbleLabel.ShowMsgEx(self.readImg, "已经是第一页")
            return
        self.curIndex -= 1
        info = self.readImg.pictureData.get(self.curIndex)
        if info:
            self.UpdateProcessBar(info.downloadSize, info.size)
        self.SetData(isInit=True)
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
            self.stateWaifu.setText("状态：" + waifuState)
        if waifuTick or isInit:
            self.tickLabel.setText("耗时：" + str(waifuTick) + "s")

    def CopyPicture(self):
        clipboard = QApplication.clipboard()
        owner = self.readImg

        if self.checkBox.isChecked():
            p = owner.pictureData.get(owner.curIndex)
            if not p or not p.waifuData:
                QtBubbleLabel.ShowErrorEx(owner, "解码还未完成")
                return
            img = QImage()
            img.loadFromData(p.waifuData)
            clipboard.setImage(img)
            QtBubbleLabel.ShowMsgEx(owner, "复制成功")

        else:
            p = owner.pictureData.get(owner.curIndex)
            if not p or not p.data:
                QtBubbleLabel.ShowErrorEx(owner, "下载未完成")
                return
            img = QImage()
            img.loadFromData(p.data)
            clipboard.setImage(img)
            QtBubbleLabel.ShowMsgEx(owner, "复制成功")
        return

    def OpenWaifu(self):
        if self.checkBox.isChecked():
            config.IsOpenWaifu = True
            self.readImg.ShowImg(True)
        else:
            config.IsOpenWaifu = False
            self.readImg.ShowImg(False)

        return

    def UpdateProcessBar(self, size, maxSize):
        self.downloadSize = size
        self.downloadMaxSize = maxSize
        self.progressBar.setMaximum(maxSize)
        self.progressBar.setValue(self.downloadSize)

    def UpdateText(self, noise, scale, model):
        self.label_2.setText("去噪等级：" + str(noise))
        self.label_3.setText("放大倍数：" + str(scale))
        self.label_9.setText("转码模式：" + model)
