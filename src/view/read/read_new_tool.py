from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from view.read.read_new_frame import ReadNewFrame
    from view.read.read_new_view import ReadNewView

import sys
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
from view.read.read_new_graphics import ReadNewGraphics


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
    def qtTool(self) -> ReadNewTool:
        return self._qtTool()

    def mousePressEvent(self, event):
        if not self.label.isVisible():
            self.label.setVisible(True)
        x = event.pos().x()
        pos = x / self.width()

        w = self.width()
        size = int(w * self.value() / (self.maximum()))
        x2 = self.sliderPosition()

        if not (size - 5 <= x <= size + 5):
            self.setValue(int(pos * (self.maximum()) + self.minimum()))
            self.label.setText(str(self.value()))
            size = int((self.width() - self.label.width()) * self.value() / (self.maximum()))
            self.label.move(size, 3)
        super(self.__class__, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.label.isVisible():
            self.label.setVisible(False)
            self.qtTool.SkipPicture(self.value())
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


class ReadNewTool(QtWidgets.QWidget, Ui_ReadImg):

    def __init__(self, imgFrame):
        QtWidgets.QWidget.__init__(self, imgFrame)
        Ui_ReadImg.__init__(self)
        self.setupUi(self)
        self.resize(100, 400)
        self._imgFrame = weakref.ref(imgFrame)
        self.downloadMaxSize = 0
        self.downloadSize = 0
        self.slider = QtCustomSlider(self)
        self.horizontalLayout_7.addWidget(self.slider)
        self.SetWaifu2xCancle()
        self.scaleBox.installEventFilter(self)
        self.zoomSlider.setMinimum(int(100*ReadNewGraphics.MIN_ZOOM))
        self.zoomSlider.setMaximum(int(100*ReadNewGraphics.MAX_ZOOM))

        self.isMaxFull = False
        self.gpuLabel.setMaximumWidth(250)
        self.curWaifu2x.clicked.connect(self.OpenCurWaifu)
        self.preDownWaifu2x.clicked.connect(self.OpenPreDownloadWaifu2x)
        self.modelNameButton.setText(ToolUtil.GetShowModelName(Setting.LookModelName.value))
        self.modelNameButton.setToolTip(Setting.LookModelName.value)
        self.modelNameButton.clicked.connect(self.OpenSrSelect)
        self.modelNameButton.setEnabled(False)
        self.openGLBox.setChecked(bool(Setting.IsOpenOpenGL.value))
        self.openGLBox.clicked.connect(self.SwitchOpenGL)

    def SwitchOpenGL(self, value):
        Setting.IsOpenOpenGL.SetValue(int(value))
        self.scrollArea.set_opengl(bool(value))

    def OpenSrSelect(self):
        QtOwner().OpenSrSelectModel(self.modelNameButton.toolTip(), self.OpenSrSelectBack)

    def OpenSrSelectBack(self, newModName):
        Setting.LookModelName.SetValue(newModName)
        self.modelNameButton.setText(ToolUtil.GetShowModelName(Setting.LookModelName.value))
        self.modelNameButton.setToolTip(Setting.LookModelName.value)

    @property
    def imgFrame(self) -> ReadNewFrame:
        return self._imgFrame()

    @property
    def scrollArea(self) -> ReadNewGraphics:
        return self.readImg.scrollArea

    @property
    def readImg(self) -> ReadNewView:
        return self.imgFrame.readImg

    @property
    def curIndex(self):
        return self.scrollArea._cur_idx

    @property
    def maxPic(self):
        return self.readImg.maxPic

    @property
    def stripModel(self):
        return self.scrollArea._mode

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
        # self.curWaifu2x.setChecked(bool(self.readImg.GetIsWaifu2x()))

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
                if not bookInfo:
                    return
                if epsId + 1 < bookInfo.epsCount:
                    QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipNext))
                    self.OpenNextEps()
                return
            # self.CloseScrollAndTurn()
            QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextPage))
            return
        if ReadMode.isDouble(self.stripModel):
            index = self.scrollArea._cur_idx + 2
        else:
            index = self.scrollArea._cur_idx + 1
        self.scrollArea.jump_to_index(index)
        return

    def LastPage(self):
        if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            self._NextPage()
        else:
            self._LastPage()
        # self.curWaifu2x.setChecked(bool(self.readImg.GetIsWaifu2x()))

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
            index = self.scrollArea._cur_idx - 2
        else:
            index = self.scrollArea._cur_idx - 1
        self.scrollArea.jump_to_index(index)
        return

    def ReturnPage(self):
        # self.readImg.hide()
        # self.hide()
        # QtOwner().owner.bookInfoForm.show()
        self.readImg.Close()
        # QtOwner().owner.bookInfoForm.LoadHistory()
        # self.readImg.Clear()
        return

    def SetData(self, pSize=None, dataLen=0, state="",
                waifuSize=None, waifuDataLen=0,
                waifuState="", waifuTick=0,
                isInit=False):
        if self.readImg.epsName:
            QtOwner().SetSubTitle(self.readImg.epsName + "（{}/{}）".format(self.slider.value(), self.slider.maximum()))

        self.epsLabel2.setText("{}/{}({})".format(self.slider.value(), self.slider.maximum(), self.readImg.epsName))
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

    # def CopyPicture(self):
    #     owner = self.readImg
    #     p = owner.pictureData.get(owner.curIndex)
    #     if not p or not p.data:
    #         MsgLabel.ShowErrorEx(owner, Str.GetStr(Str.DownloadNot))
    #         return
    #     # TODO
    #     # QtOwner().OpenWaifu2xTool(p.data)
    #     return

    def OpenCurWaifu(self):
        self.scrollArea.switch_cur_waifu2x_state()
        # if self.curWaifu2x.isChecked():
        #     self.readImg.SetIsWaifu2x(1)
        # else:
        #     self.readImg.SetIsWaifu2x(0)
        # # self.scrollArea.changeScale.emit(self.scaleCnt)
        # self.readImg.ShowImgAll()
        # self.readImg.CheckLoadPicture()
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

        # self.readImg.ShowImgAll()
        self.scrollArea.check_waifu2x_state()
        return

    def UpdateText(self, model):
        if not model:
            self.scaleLabel.setText(str(Setting.LookScale.value))
            self.modelNameButton.setText(ToolUtil.GetShowModelName(Setting.LookModelName.value))
            self.modelNameButton.setToolTip(Setting.LookModelName.value)
        else:
            scale = model.get('scale', 0)
            modelName = model.get('model_name', "")
            self.scaleLabel.setText(str(scale))
            self.modelNameButton.setText(ToolUtil.GetShowModelName(modelName))
            self.modelNameButton.setToolTip(modelName)
        self.gpuLabel.setText(QtOwner().settingView.GetGpuName())

    def OpenLastEps(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        bookInfo = BookMgr().GetBook(bookId)

        lasEps = epsId - 1
        if self.readImg.isLocal:
            if lasEps < 0:
                QtOwner().ShowMsg(Str.GetStr(Str.AlreadyLastChapter))
                return
            self.readImg.OpenLocalPage(self.readImg._cacheBook, lasEps, 9999)
            return
        elif self.readImg.isOffline:
            if not QtOwner().downloadView.IsDownloadEpsId(self.readImg.bookId, self.readImg.epsId - 1):
                QtOwner().ShowMsg(Str.GetStr(Str.NotDownload))
                return
        else:
            if not bookInfo:
                return
            if lasEps >= bookInfo.epsCount:
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
            if not bookInfo:
                return
            if nextEps >= bookInfo.epsCount:
                QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextChapter))
                return

        # title = bookInfo.GetEpsTitle(epsId)
        self.readImg.AddHistory()
        QtOwner().bookInfoView.LoadHistory()
        self.readImg.OpenPage(bookId, nextEps)
        return

    def SkipPicture(self, index=0):
        self.scrollArea.jump_to_index(index)

    def InitSlider(self, maxIndex):
        self.slider.setMinimum(1)
        self.slider.setMaximum(maxIndex)

    def UpdateSlider(self):
        return
        # self.slider.setValue(self.readImg.curIndex + 1)

    def FullScreen(self, isClear=False):
        if QtOwner().owner.windowState() == Qt.WindowFullScreen:
            if not sys.platform == "darwin":
                if QtOwner().isMaxSize:
                    QtOwner().owner.showMaximized()
                else:
                    QtOwner().owner.showNormal()
            else:
                pass
                # QtOwner().owner.showNormal()
            self.fullButton.setText(Str.GetStr(Str.FullScreen))
            if not isClear:
                Setting.LookReadFull.SetValue(0)
        else:
            QtOwner().owner.BackOldSize()
            # self.isMaxFull = self.window().isMaximized()
            if QtOwner().isMaxSize:
                QtOwner().owner.showNormal()
            QtOwner().owner.showFullScreen()
            self.fullButton.setText(Str.GetStr(Str.ExitFullScreen))
            Setting.LookReadFull.SetValue(1)

    def Waifu2xSave(self):
        self.SetWaifu2xCancle(True)

    def Waifu2xCancle(self):
        if self.modelNameButton.toolTip():
            Setting.LookModelName.SetValue(self.modelNameButton.toolTip())
        # Setting.LookNoise.SetValue(self.noiseBox.currentIndex() -1)
        Setting.LookScale.SetValue(self.scaleBox.value())

        self.SetWaifu2xCancle(False)

    def SetWaifu2xCancle(self, isVisibel=False):
        self.waifu2xSave.setVisible(not isVisibel)
        # self.noiseLabel.setVisible(not isVisibel)
        self.scaleLabel.setVisible(not isVisibel)
        # self.modelLabel.setVisible(not isVisibel)
        # self.modelNameButton.setVisible(isVisibel)
        self.modelNameButton.setEnabled(isVisibel)
        self.waifu2xCancle.setVisible(isVisibel)
        # self.noiseBox.setVisible(isVisibel)
        self.scaleBox.setVisible(isVisibel)
        # self.modelBox.setVisible(isVisibel)

    def ScalePicture2(self, value):
        self.zoomSlider.setValue(value)

    def ScalePicture(self, value):
        self.scrollArea.set_zoom(value/100, None)

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyRelease:
            return True
        elif ev.type() == QEvent.KeyPress:
            return True
        return False

    def ChangeReadMode(self, index):
        self.comboBox.setCurrentIndex(index)
        self.imgFrame.InitHelp()

    def ChangeReadMode2(self, index):
        Setting.LookReadMode.SetValue(index)
        self.scrollArea.set_mode(index)
        if self.stripModel == ReadMode.UpDown:
            self.zoomSlider.setValue(80)
        return

    def SwitchScrollAndTurn(self):
        if self.IsStartScrollAndTurn():
            self.CloseScrollAndTurn()
        else:
            self.StartScrollAndTurn()
        return

    def StartScrollAndTurn(self):
        self.CloseScrollAndTurn()
        if ReadMode.isScroll(self.scrollArea._mode):
            self.scrollArea.set_auto_scroll(Setting.ScrollSpeed.value)
        else:
            self.scrollArea.set_auto_scroll(Setting.TurnSpeed.value/ 1000)

    def CloseScrollAndTurn(self):
        if self.IsStartScrollAndTurn():
            QtOwner().ShowMsg(Str.GetStr(Str.StopAutoScroll))
            self.scrollArea.stop_auto()
        pass

    def IsStartScrollAndTurn(self):
        return self.scrollArea.is_auto

