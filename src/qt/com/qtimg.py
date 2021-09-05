import os
import time

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt, QRectF, QPointF, QSizeF, QEvent
from PySide2.QtGui import QColor, QPainter, QPixmap, QDoubleValidator, \
    QIntValidator
from PySide2.QtWidgets import QFrame, QGraphicsPixmapItem, QGraphicsScene, QApplication, QFileDialog

from conf import config
from src.qt.com.qtmsg import QtMsgLabel
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.util import Singleton, ToolUtil, Log
from ui.img import Ui_Img


class QtImgMgr(Singleton):
    def __init__(self):
        self.obj = QtImg()
        self.data = None
        self.waifu2xData = None

    def ShowImg(self, data):
        if data:
            self.data = data
            self.waifu2xData = None
            self.obj.ClearConvert()
            if config.CanWaifu2x:
                self.obj.comboBox.setEnabled(True)
                self.obj.changeButton.setEnabled(True)
            self.obj.changeButton.setText(self.obj.tr("转换"))
            self.obj.ShowImg(data)
        elif self.data:
            if config.CanWaifu2x:
                self.obj.comboBox.setEnabled(True)
                self.obj.changeButton.setEnabled(True)
            self.obj.changeButton.setText(self.obj.tr("转换"))
            self.obj.ShowImg(self.data)
        else:
            if config.CanWaifu2x:
                self.obj.comboBox.setEnabled(True)
                self.obj.changeButton.setEnabled(True)
            self.obj.changeButton.setText(self.obj.tr("转换"))
            self.obj.show()

    def SetHeadStatus(self, isSet):
        self.obj.headButton.setEnabled(isSet)


class QtImg(QtWidgets.QWidget, Ui_Img, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Img.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookId = ""
        self.epsId = 0
        self.curIndex = 0
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(800, 900)
        self.checkBox.setChecked(True)
        self.index = 0
        self.comboBox.setCurrentIndex(self.index)
        validator = QIntValidator(0, 9999999)
        self.heighEdit.setValidator(validator)
        self.widthEdit.setValidator(validator)
        exp = QDoubleValidator(0.1, 64, 1)
        exp.setNotation(exp.StandardNotation)
        self.scaleEdit.setValidator(exp)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.graphicsView.setFrameStyle(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")

        # self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        self.graphicsView.setCursor(Qt.OpenHandCursor)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                                         QPainter.SmoothPixmapTransform)
        self.graphicsView.setCacheMode(self.graphicsView.CacheBackground)
        self.graphicsView.setViewportUpdateMode(self.graphicsView.SmartViewportUpdate)

        self.graphicsItem = QGraphicsPixmapItem()
        self.graphicsItem.setFlags(QGraphicsPixmapItem.ItemIsFocusable |
                                   QGraphicsPixmapItem.ItemIsMovable)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.CopyPicture)

        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsItem.setTransformationMode(Qt.SmoothTransformation)
        self.graphicsScene.addItem(self.graphicsItem)
        self.graphicsView.setMinimumSize(10, 10)
        self.pixMap = QPixmap(self.tr("加载中"))
        self.graphicsItem.setPixmap(self.pixMap)
        # self.radioButton.setChecked(True)
        self.isStripModel = False

        # self.radioButton.installEventFilter(self)
        # self.radioButton_2.installEventFilter(self)
        self.graphicsView.installEventFilter(self)
        self.graphicsView.setWindowFlag(Qt.FramelessWindowHint)
        # tta有BUG，暂时屏蔽 TODO
        self.ttaModel.setEnabled(False)

        self._delta = 0.1
        self.scaleCnt = 0

        self.backStatus = ""

        ToolUtil.SetIcon(self)

    def ShowImg(self, data):
        self.scaleCnt = 0
        self.pixMap = QPixmap()
        self.pixMap.loadFromData(data)
        self.show()
        self.graphicsItem.setPixmap(self.pixMap)
        self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixMap.width(), self.pixMap.height())))
        size = ToolUtil.GetDownloadSize(len(data))
        self.sizeLabel.setText(size)
        weight, height = ToolUtil.GetPictureSize(data)
        self.resolutionLabel.setText(str(weight) + "x" + str(height))
        self.ScalePicture()

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
            self.hide()
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
        else:
            return super(self.__class__, self).eventFilter(obj, ev)

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
        clipboard.setPixmap(self.pixMap)
        QtMsgLabel.ShowMsgEx(self, self.tr("复制成功"))
        return

    def ReduceScalePic(self):
        self.zoom(1/1.1)
        return

    def AddScalePic(self):
        self.zoom(1.1)
        return

    def OpenPicture(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Open Image", ".", "Image Files(*.jpg *.png)")
            if filename and len(filename) >= 1:
                name = filename[0]
                if os.path.isfile(name):
                    f = open(name, "rb")
                    data = f.read()
                    f.close()
                    QtImgMgr().ShowImg(data)
        except Exception as ex:
            Log.Error(ex)
        return

    def StartWaifu2x(self):
        if not QtImgMgr().data:
            return
        if not config.CanWaifu2x:
            return
        import waifu2x
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
            "model":  getattr(waifu2x, modelInsence),
        }
        if self.scaleRadio.isChecked():
            model['scale'] = round(float(self.scaleEdit.text()), 1)
        else:
            model['width'] = int(self.widthEdit.text())
            model['high'] = int(self.heighEdit.text())
        self.backStatus = self.GetStatus()
        self.AddConvertTask("", QtImgMgr().data, model, self.AddConvertBack)
        self.changeButton.setText(self.tr("正在转换"))
        return

    def AddConvertBack(self, data, waifuId, backParam, tick):
        if data:
            QtImgMgr().waifu2xData = data
            if self.checkBox.isChecked():
                self.ShowImg(data)
            self.changeButton.setText(self.tr("已转换"))
            self.tickLabel.setText(str(round(tick, 3)) + "s")
            self.changeButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
        self.SetStatus(True)
        self.comboBox.setEnabled(True)
        return

    def SavePicture(self):
        data = QtImgMgr().waifu2xData if QtImgMgr().waifu2xData else QtImgMgr().data
        if not data:
            return
        try:
            today = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            filepath = QFileDialog.getSaveFileName(self, self.tr("保存"), "{}.jpg".format(today))
            if filepath and len(filepath) >= 1:
                name = filepath[0]
                f = open(name, "wb")
                f.write(data)
                f.close()
        except Exception as es:
            Log.Error(es)
        return

    def SwithPicture(self):
        if self.checkBox.isChecked() and QtImgMgr().waifu2xData:
            self.ShowImg(QtImgMgr().waifu2xData)
        else:
            self.ShowImg(QtImgMgr().data)
        return

    def ChangeModel(self, index):
        if self.comboBox.currentIndex() == self.index:
            return
        # self.index = self.comboBox.currentIndex()
        self.changeButton.setText(self.tr("转换"))
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
            self.changeButton.setText(self.tr("转换"))
        else:
            self.changeButton.setEnabled(False)
            self.changeButton.setText(self.tr("转换"))

    def SetHead(self):
        data = QtImgMgr().waifu2xData if QtImgMgr().waifu2xData else QtImgMgr().data
        if not data:
            return
        QtOwner().owner.userForm.UpdatePictureData(data)
        QtMsgLabel.ShowMsgEx(self, self.tr("头像上传中......"))
        return
