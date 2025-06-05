import weakref

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation, Qt
from PySide6.QtWidgets import QScrollBar

from qt_owner import QtOwner
from tools.str import Str
from view.read.read_enum import ReadMode


class ReadScroll(QScrollBar):
    def __init__(self, parent):
        QScrollBar.__init__(self)
        self._owner = weakref.ref(parent)
        self.scrollTime = 200
        self.maxScrollTme = 500
        self.maxRate = 10

        self.ani = QPropertyAnimation()
        self.ani.setTargetObject(self)
        self.ani.setPropertyName(b"value")
        self.ani.setEasingCurve(QEasingCurve.Linear)
        self.ani.setDuration(self.scrollTime)
        self.__value = self.value()
        self.ani.finished.connect(self.Finished)
        self.setSingleStep(1)
        # self.oldupdateCurrentValue = self.ani.updateCurrentValue
        # self.ani.updateCurrentValue = self.UpdateCurrentValue
        # self.ani.valueChanged.connect(self.AniValueChange)
        self.priV = 0

        self.lastAniStartV = 0
        self.lastAniEndV = 0
        self.lastScrollTime = 0
        # self.valueChanged.connect(self.ValueChange)
        self.oldv = 0
        self.changeState = False
        
        self.lastSubV = 0

        
    @property
    def stripModel(self):
        return self._owner().qtTool.stripModel

    @property
    def isCurReadModel(self):
        if self.orientation() == Qt.Orientation.Vertical:
            return self.stripModel == ReadMode.UpDown
        else:
            return True

    #
    # def ValueChange(self,value):
    #     # self.oldv = value
    #     print("2, {}".format(value))
    #
    # def AniValueChange(self, value):
    #     print("1, {}".format(value))

    #
    # def UpdateCurrentValue(self, value):
    #     print("2, {}".format(value))
    #     self.oldupdateCurrentValue(value)

    def ResetAniValueByAdd(self, oldV, addV):
        print("reset1 setV, {}".format(oldV+addV))
        QScrollBar.setValue(self, oldV+addV)
        changeV = self.lastAniEndV - self.lastAniStartV
        laveV  = self.lastAniEndV - oldV
        scrollTime = 0
        if changeV != 0:
            scrollTime = min(self.maxScrollTme, int(laveV / changeV * self.lastScrollTime))
        if scrollTime > 0:
            self.ani.stop()
            # print("ani stop 5")
            self.StartAni(self.value(), self.lastAniEndV, scrollTime)
        else:
            self.ani.stop()
            # print("ani stop 6")
            self.StartAni(self.value(), self.value(), self.scrollTime)

    def AniValueByAdd(self, addV):
        changeV = self.lastAniEndV - self.lastAniStartV
        addV2 = self.lastAniEndV - self.value()
        self.lastAniStartV = self.value()
        if addV <= 0 :
            v = max(self.maxRate * addV, addV + addV2)
        else:
            v = min(self.maxRate * addV, addV + addV2)
        self.lastAniEndV = self.lastAniStartV + v
        laveV = self.lastAniEndV - self.lastAniStartV

        scrollTime = self.scrollTime
        # if changeV != 0:
        #     scrollTime = min(self.maxScrollTme, int(laveV / changeV * self.lastScrollTime))
        # if scrollTime <= 0:
        #     scrollTime = self.scrollTime

        # print("add setV, {}, {}, {}".format(scrollTime,self.value(), self.lastAniEndV))
        self.ani.stop()
        # print("ani stop 1")
        self.StartAni(self.value(), self.lastAniEndV, scrollTime)

    # def AniValueChange(self, value):
    #     print("{}, {}".format(value, value - self.priV))
    #     self.priV = value

    @property
    def frame(self):
        return self._owner()

    @property
    def scrollArea(self):
        return self._owner().scrollArea

    @property
    def labelSize(self):
        return self.scrollArea.labelSize

    @property
    def readImg(self):
        return self.scrollArea.readImg

    def Finished(self):
        self.OnValueChange(self.value())

    def StopScroll(self):
        self.ani.stop()
        # print("ani stop 2")
    #
    # def Scroll(self, value, time=0):
    #     if self.ani.state() == QAbstractAnimation.State.Running:
    #         self.ani.stop()
    #     oldValue = self.value()
    #     self.ani.setStartValue(oldValue)
    #     if not time:
    #         self.ani.setDuration(self.scrollTime)
    #     else:
    #         self.ani.setDuration(time)
    #     self.ani.setEndValue(oldValue + value)
    #     self.ani.start()

    def ForceSetValue(self, value):
        self.ani.stop()
        # print("ani stop 3")
        if self.orientation() == Qt.Orientation.Vertical:
            print("force setV, {}".format(value))
        QScrollBar.setValue(self, value)
        self.StartAni(value, value, self.scrollTime)

    # def ForceSetValue2(self, value, isAdd):
    #     if value == self.value():
    #         if isAdd and self.stripModel != ReadMode.RightLeftScroll:
    #             self.__value = self.__value + 1
    #         else:
    #             self.__value = self.__value - 1

    #     self.ani.stop()
    #     # print("ani stop 3")
    #     print("force setV2, {}".format(value))
    #     QScrollBar.setValue(self, value)
    #     self.StartAni(value, value, self.scrollTime)

    def StartAni(self, start, end, duration):
        self.lastAniEndV = end
        self.lastAniStartV = start
        self.lastScrollTime = duration
        self.ani.setStartValue(start)
        self.ani.setEndValue(end)
        self.ani.setDuration(duration)
        self.ani.start()
        if self.orientation() == Qt.Orientation.Vertical:
            print("start ani, start:{}, end:{}".format(start, end))

    def setValue(self, value: int):
        print("setV, {}".format(value))
        if value == self.value():
            return

        # stop running animation
        if self.ani.state() == self.ani.State.Running:
            self.AniValueByAdd(value-self.value())
            # print("ani stop 1")
            # self.StartAni(self.value(), value, self.scrollTime)
        else:
            self.ani.stop()
            # print("ani stop 4")
            self.StartAni(self.value(), value, self.scrollTime)

    def scrollValue(self, value: int):
        """ scroll the specified distance """
        # self.__value += value
        # self.__value = max(self.minimum(), self.__value)
        # self.__value = min(self.maximum(), self.__value)
        self.setValue(self.value()+value)

    # def scrollTo(self, value: int):
    #     """ scroll to the specified position """
    #     self.__value = value
    #     self.__value = max(self.minimum(), self.__value)
    #     self.__value = min(self.maximum(), self.__value)
    #     self.setValue(self.__value)

    # def SetChangeState(self, state):
    #     self.changeState = state

    # value变化后，重新定位位置信息
    def SaveLastPosition(self):
        if not self.isCurReadModel:
            return
        
        if not ReadMode.isScroll(self.stripModel):
            return

        oldV = self.value()
        oldMinV = max(1, self.labelSize.get(self.readImg.curIndex, 0))
        height =  max(1,self.labelSize.get(self.readImg.curIndex-1, 0))
        subV = (oldV - oldMinV)/height
        if self.isCurReadModel:
            print("set lastV, {}, {}".format(oldV, subV))
        self.lastSubV = subV
        self.changeState = True
        return
    
    def SaveLastPositionEnd(self):
        if not self.isCurReadModel:
            return
        
        if not ReadMode.isScroll(self.stripModel):
            return    

        oldV = self.value()
        oldMinV = max(1, self.labelSize.get(self.readImg.curIndex, 0))
        height =  max(1,self.labelSize.get(self.readImg.curIndex-1, 0))
        newV = int(oldMinV + height*self.lastSubV)
        if oldV == newV:
            self.__value = newV
            self.lastSubV = 0
            self.changeState = False
            return
        self.ani.stop()
        QScrollBar.setValue(self, newV)
        if self.isCurReadModel:
            print("set lastV2, {}, {}".format(oldV, newV))
        self.__value = newV
        self.lastSubV = 0
        self.changeState = False
        return
    
    def OnValueChange(self, value):
        if self.changeState:
            return
        curV = self.value()
        addValue = value - self.__value
        # self.UpdateScrollBar(value)
        self.__value = value

        if not self.isCurReadModel:
            return
        if not ReadMode.isScroll(self.scrollArea.initReadMode):
            return

        changeIndex = self.readImg.curIndex
        if self.scrollArea.initReadMode == ReadMode.RightLeftScroll:
            newValue = value + self.scrollArea.width()
            curPictureSize = self.labelSize.get(self.readImg.curIndex)
            nextPictureSize = self.labelSize.get(self.readImg.curIndex - 1, 0)
            while True:
                ## 切换上一图片
                if addValue > 0 and newValue >= nextPictureSize:
                    if changeIndex <= 0:
                        break
                    changeIndex -= 1
                    # print(self.readImg.curIndex)

                    # self.scrollArea.changeLastPage.emit(self.readImg.curIndex)

                ## 切换下一图片
                elif addValue < 0 and newValue < curPictureSize:
                    if changeIndex >= self.readImg.maxPic - 1:
                        break
                    changeIndex += 1
                    # print(self.readImg.curIndex)
                    # self.scrollArea.changeNextPage.emit(self.readImg.curIndex)
                else:
                    break
                curPictureSize = self.labelSize.get(changeIndex)
                nextPictureSize = self.labelSize.get(changeIndex - 1, 0)
        else:
            curPictureSize = self.labelSize.get(self.readImg.curIndex)
            nextPictureSize = self.labelSize.get(self.readImg.curIndex + 1, 0)
            while True:
                ## 切换上一图片
                if addValue < 0 and value < curPictureSize:
                    if changeIndex <= 0:
                        break
                    changeIndex -= 1
                    # print("last page, addv:{}, val:{}, cur:{}, next:{}".format(addValue, value, curPictureSize, nextPictureSize))
                    # self.scrollArea.changeLastPage.emit(self.readImg.curIndex)

                ## 切换下一图片
                elif addValue > 0 and value >= nextPictureSize:
                    if changeIndex >= self.readImg.maxPic - 1:
                        break
                    changeIndex += 1
                    # print("next page, addv:{}, val:{}, cur:{}, next:{}".format(addValue, value, curPictureSize, nextPictureSize))
                    # self.scrollArea.changeNextPage.emit(self.readImg.curIndex)
                else:
                    break
                curPictureSize = self.labelSize.get(changeIndex)
                nextPictureSize = self.labelSize.get(changeIndex + 1, 0)
        print("change, {}->{}, {}->{}, curV:{}, value:{}, addV:{}".format(self.readImg.curIndex, changeIndex, curPictureSize, nextPictureSize, curV, value, addValue))

        if self.readImg.curIndex == changeIndex:
            return
        elif self.readImg.curIndex > changeIndex:
            self.readImg.curIndex = changeIndex
            self.scrollArea.changeLastPage.emit(self.readImg.curIndex)
        elif self.readImg.curIndex < changeIndex:
            self.readImg.curIndex = changeIndex
            self.scrollArea.changeNextPage.emit(self.readImg.curIndex)
        return