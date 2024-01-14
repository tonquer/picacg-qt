import os
import time

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF, QEvent
from PySide6.QtGui import QPainter, QPixmap, QDoubleValidator, \
    QIntValidator, QMouseEvent, QImage
from PySide6.QtWidgets import QFrame, QGraphicsPixmapItem, QGraphicsScene, QApplication, QFileDialog, QLabel, QGraphicsView

from config import config
from interface.ui_waifu2x_tool import Ui_Waifu2xTool
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil
from view.read.read_qgraphics_proxy_widget import ReadQGraphicsProxyWidget


class Waifu2xToolView(QtWidgets.QWidget, Ui_Waifu2xTool, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Waifu2xTool.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookId = ""
        self.epsId = 0
        self.curIndex = 0
        # self.resize(800, 900)
        self.checkBox.setChecked(True)
        self.index = 0
        self.comboBox.setCurrentIndex(self.index)
        validator = QIntValidator(0, 9999999)
        self.heighEdit.setValidator(validator)
        self.widthEdit.setValidator(validator)
        exp = QDoubleValidator(0.1, 64, 1)
        # exp.setNotation(exp.StandardNotation)
        self.scaleEdit.setValidator(exp)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.graphicsView.setFrameStyle(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")

        # self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        self.graphicsView.setCursor(Qt.OpenHandCursor)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setRenderHints(QPainter.Antialiasing |
                                         QPainter.SmoothPixmapTransform)
        self.graphicsView.setCacheMode(QGraphicsView.CacheBackground)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

        self.graphicsItem = ReadQGraphicsProxyWidget()
        self.graphicsItem.setFlags(QGraphicsPixmapItem.ItemIsFocusable |
                                   QGraphicsPixmapItem.ItemIsMovable)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.CopyPicture)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.graphicsItem.setWidget(QLabel())
        # self.graphicsItem.setPixmap(QPixmap())
        # self.graphicsItem.setTransformationMode(Qt.SmoothTransformation)
        self.graphicsScene.addItem(self.graphicsItem)
        self.graphicsItem.setPos(QPointF(0, 0))
        self.graphicsView.setMinimumSize(10, 10)
        # self.pixMapData = None
        self.pixMap = QImage(Str.GetStr(Str.LoadingPicture))
        # self.graphicsItem.setPixmap(self.pixMap)
        # self.radioButton.setChecked(True)
        self.isStripModel = False

        # self.radioButton.installEventFilter(self)
        # self.radioButton_2.installEventFilter(self)
        # self.graphicsItem.installSceneEventFilter(self.graphicsItem)
        # self.graphicsView.installEventFilter(self)
        self.graphicsScene.installEventFilter(self)
        self.graphicsView.setWindowFlag(Qt.FramelessWindowHint)

        self._delta = 0.1
        self.scaleCnt = 0

        self.data = ""
        self.waifu2xData = ""
        self.backStatus = ""

    def SwitchCurrent(self, **kwargs):
        data = kwargs.get("data")
        self.gpuLabel.setText(config.EncodeGpu)
        if data:
            self.data = data
            self.waifu2xData = None
            self.ClearConvert()
            if config.CanWaifu2x:
                self.comboBox.setEnabled(True)
                self.changeButton.setEnabled(True)
            self.changeButton.setText(Str.GetStr(Str.Convert))
            self.backStatus = ""
            self.CheckScaleRadio()

        else:
            return

        # elif self.data:
        #     if config.CanWaifu2x:
        #         self.comboBox.setEnabled(True)
        #         self.changeButton.setEnabled(True)
        #     self.changeButton.setText(Str.GetStr(Str.Convert))
        # else:
        #     if config.CanWaifu2x:
        #         self.comboBox.setEnabled(True)
        #         self.changeButton.setEnabled(True)
        #     self.changeButton.setText(Str.GetStr(Str.Convert))
        #     return
        self.ShowImg(self.data)

    def ShowImg(self, data):
        self.gpuLabel.setText(config.EncodeGpu)
        self.scaleCnt = 0
        # radio = self.devicePixelRatio()
        # p.setDevicePixelRatio(radio)
        # self.pixMapData = data
        self.show()
        self.pixMap = QImage()
        self.pixMap.loadFromData(data)

        self.graphicsItem.SetGifData(data, self.pixMap.width(), self.pixMap.height())
        self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixMap.width(), self.pixMap.height())))
        # self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixMap.width()*radio, self.pixMap.height()*radio)))

        size = ToolUtil.GetDownloadSize(len(data))
        self.sizeLabel.setText(size)
        weight, height, mat, _ = ToolUtil.GetPictureSize(data)
        self.format.setText(mat)
        self.resolutionLabel.setText(str(weight) + "x" + str(height))
        self.ScalePicture()
        self.CheckScaleRadio()

    def ScalePicture(self):
        rect = QRectF(self.graphicsItem.pos(), QSizeF(
            self.pixMap.size()))
        unity = self.graphicsView.transform().mapRect(QRectF(0, 0, 1, 1))
        width = unity.width()
        height = unity.height()
        if width <= 0 or height <= 0:
            return
        self.graphicsView.scale(1 / width, 1 / height)
        viewRect = self.graphicsView.viewport().rect()
        sceneRect = self.graphicsView.transform().mapRect(rect)
        if sceneRect.width() <= 0 or sceneRect.height() <= 0:
            return
        x_ratio = viewRect.width() / sceneRect.width()
        y_ratio = viewRect.height() / sceneRect.height()
        x_ratio = y_ratio = min(x_ratio, y_ratio)

        self.graphicsView.scale(x_ratio, y_ratio)
        # if self.readImg.isStripModel:
        #     height2 = self.pixMap.size().height() / 2
        #     height3 = self.graphicsView.size().height()/2
        #     height3 = height3/x_ratio
        #     p = self.graphicsItem.pos()
        #     self.graphicsItem.setPos(p.x(), p.y()+height2-height3)
        self.graphicsView.centerOn(rect.center())

        for _ in range(abs(self.scaleCnt)):
            if self.scaleCnt > 0:
                self.graphicsView.scale(1.1, 1.1)
            else:
                self.graphicsView.scale(1/1.1, 1/1.1)

    def keyReleaseEvent(self, ev):
        if ev.key() == Qt.Key_Escape:
            # self.hide()
            ev.ignore()
            return
        if ev.key() == Qt.Key_Plus or ev.key() == Qt.Key_Equal:
            self.zoomIn()
            return
        if ev.key() == Qt.Key_Minus:
            self.zoomOut()
            return
        super(self.__class__, self).keyReleaseEvent(ev)

    def resizeEvent(self, event) -> None:
        super(self.__class__, self).resizeEvent(event)
        self.ScalePicture()

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyPress:

            return True
        elif ev.type() == QEvent.GraphicsSceneMousePress:
            if ev.button() == Qt.ForwardButton:
                return True
            elif ev.button() == Qt.BackButton:
                return True
            return False
        elif ev.type() == QEvent.GraphicsSceneMouseRelease:
            if ev.button() == Qt.ForwardButton:
                return True
            elif ev.button() == Qt.BackButton:
                return True
            return False
        else:
            return super(self.__class__, self).eventFilter(obj, ev)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.ForwardButton:
            # QtOwner().SwitchWidgetNext()
            event.ignore()
        elif event.button() == Qt.BackButton:
            event.ignore()
            # QtOwner().SwitchWidgetLast()
        return super(self.__class__, self).mousePressEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def zoomIn(self):
        """放大"""
        self.zoom(1.1)

    def zoomOut(self):
        """缩小"""
        self.zoom(1/1.1)

    def zoom(self, factor):
        """缩放
        :param factor: 缩放的比例因子
        """
        _factor = self.graphicsView.transform().scale(
            factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        if _factor < 0.07 or _factor > 100:
            # 防止过大过小
            return
        if factor >= 1:
            self.scaleCnt += 1
        else:
            self.scaleCnt -= 1
        self.graphicsView.scale(factor, factor)

    def CopyPicture(self):
        clipboard = QApplication.clipboard()
        clipboard.setImage(self.pixMap)
        QtOwner().ShowMsg(Str.GetStr(Str.CopySuc))
        return

    def ReduceScalePic(self):
        self.zoom(1/1.1)
        return

    def AddScalePic(self):
        self.zoom(1.1)
        return

    def OpenPicture(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Open Image", ".", "Image Files(*.jpg *.png *.gif *.webp)")
            if filename and len(filename) >= 1:
                name = filename[0]
                if os.path.isfile(name):
                    f = open(name, "rb")
                    data = f.read()
                    f.close()
                    self.data = data
                    self.waifu2xData = None
                    self.ClearConvert()
                    self.backStatus = ""
                    self.ShowImg(data)
        except Exception as ex:
            Log.Error(ex)
        return

    def StartWaifu2x(self):
        if not self.data:
            return
        if not config.CanWaifu2x:
            return
        from waifu2x_vulkan import waifu2x_vulkan
        self.comboBox.setEnabled(False)
        self.changeButton.setEnabled(False)
        self.SetStatus(False)
        self.index = self.comboBox.currentIndex()
        index = self.comboBox.currentIndex()
        noise = int(self.noiseCombox.currentText())
        if index == 0:
            modelName = "CUNET"
        elif index == 1:
            modelName = "PHOTO"
        elif index == 2:
            modelName = "ANIME_STYLE_ART_RGB"
        else:
            return
        if noise == -1:
            noiseName = "NO_NOISE"
        else:
            noiseName = "NOISE"+str(noise)
        if modelName == "CUNET" and self.scaleRadio.isChecked() and round(float(self.scaleEdit.text()), 1) <= 1:
            modelInsence = "MODEL_{}_NO_SCALE_{}".format(modelName, noiseName)
        else:
            modelInsence = "MODEL_{}_{}".format(modelName, noiseName)
        if self.ttaModel.isChecked():
            modelInsence += "_TTA"

        model = {
            "model":  getattr(waifu2x_vulkan, modelInsence),
        }
        if self.scaleRadio.isChecked():
            model['scale'] = round(float(self.scaleEdit.text()), 1)
        else:
            model['width'] = int(self.widthEdit.text())
            model['high'] = int(self.heighEdit.text())
        # _, _, mat = ToolUtil.GetPictureSize(self.data)
        # model["format"] = mat
        self.backStatus = self.GetStatus()
        self.AddConvertTask("", self.data, model, self.AddConvertBack)
        self.changeButton.setText(Str.GetStr(Str.Converting))
        return

    def AddConvertBack(self, data, waifuId, backParam, tick):
        if data:
            self.waifu2xData = data
            if self.checkBox.isChecked():
                self.ShowImg(data)
            self.changeButton.setText(Str.GetStr(Str.ConvertSuccess))
            self.tickLabel.setText(str(round(tick, 3)) + "s")
            self.changeButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
        self.SetStatus(True)
        self.comboBox.setEnabled(True)
        return

    def SavePicture(self):
        data = self.waifu2xData if self.waifu2xData else self.data
        if not data:
            return
        try:
            today = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            filepath = QFileDialog.getSaveFileName(self, Str.GetStr(Str.Save), "{}.{}".format(today, self.format.text()))
            if filepath and len(filepath) >= 1:
                name = filepath[0]
                if not name:
                    return
                f = open(name, "wb")
                f.write(data)
                f.close()
        except Exception as es:
            Log.Error(es)
        return

    def SwithPicture(self):
        if self.checkBox.isChecked() and self.waifu2xData:
            self.ShowImg(self.waifu2xData)
        else:
            self.ShowImg(self.data)
        return

    def ChangeModel(self, index):
        if self.comboBox.currentIndex() == self.index:
            return
        # self.index = self.comboBox.currentIndex()
        self.changeButton.setText(Str.GetStr(Str.Convert))
        self.changeButton.setEnabled(True)
        return

    def GetStatus(self):
        data = str(self.noiseCombox.currentText()) + \
            str(self.buttonGroup_2.checkedId()) + \
            str(self.scaleEdit.text()) + \
            str(self.heighEdit.text()) + \
            str(int(self.ttaModel.isChecked())) + \
            str(self.widthEdit.text()) + \
            str(self.comboBox.currentIndex())
        return data

    def SetStatus(self, status):
        self.scaleRadio.setEnabled(status)
        self.heighRadio.setEnabled(status)
        self.scaleEdit.setEnabled(status)
        self.widthEdit.setEnabled(status)
        self.heighEdit.setEnabled(status)
        self.noiseCombox.setEnabled(status)
        # self.radioButton_4.setEnabled(status)
        # self.radioButton_5.setEnabled(status)
        # self.radioButton_6.setEnabled(status)
        # self.radioButton_7.setEnabled(status)
        # self.radioButton_8.setEnabled(status)
        # self.ttaModel.setEnabled(status)
        self.CheckScaleRadio()

    def SetEnable(self):
        self.SetStatus(True)

    def SetDisEnable(self):
        self.SetStatus(False)

    def CheckScaleRadio(self):
        if self.scaleRadio.isChecked() and self.scaleRadio.isEnabled():
            self.scaleEdit.setEnabled(True)
            self.widthEdit.setEnabled(False)
            self.heighEdit.setEnabled(False)
        elif self.heighRadio.isChecked() and self.heighRadio.isEnabled():
            self.scaleEdit.setEnabled(False)
            self.widthEdit.setEnabled(True)
            self.heighEdit.setEnabled(True)
        data = self.GetStatus()
        if self.backStatus != data:
            self.changeButton.setEnabled(True)
            self.changeButton.setText(Str.GetStr(Str.Convert))
        else:
            self.changeButton.setEnabled(False)
            self.changeButton.setText(Str.GetStr(Str.Convert))

    def SetHead(self):
        data = self.waifu2xData if self.waifu2xData else self.data
        if not data:
            return
        QtOwner().owner.navigationWidget.UpdatePictureData(data)
        QtOwner().ShowMsg(Str.GetStr(Str.HeadUpload))
        # QtImgMgr().SetHeadStatus(not self.isHeadUp)

    # def dragEnterEvent(self, event):
    #     if(event.mimeData().hasUrls()):
    #         event.acceptProposedAction()
    #     else:
    #         event.ignore()
    #
    # def dragMoveEvent(self, evemt):
    #     return
    #
    # def dropEvent(self, event):
    #     mimeData  = event.mimeData()
    #     if(mimeData.hasUrls()):
    #         urls = mimeData.urls()
    #         QtOwner().ShowLoading()
    #         fileNames = [str(i.toLocalFile()) for i in urls]
    #         if not fileNames:
    #             return
    #         name = fileNames[0]
    #         if os.path.isfile(name):
    #             f = open(name, "rb")
    #             data = f.read()
    #             f.close()
    #             self.data = data
    #             self.waifu2xData = None
    #             self.ClearConvert()
    #             self.backStatus = ""
    #             self.ShowImg(data)