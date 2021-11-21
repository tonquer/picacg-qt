# coding:utf-8

from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect, QStackedWidget


class OpacityAniStackedWidget(QStackedWidget):
    """ 带淡入淡出动画效果的堆叠窗口类 """

    def __init__(self, parent=None):
        super().__init__(parent)
        # 记录动画完成后需要切换到的窗口下标
        self.__nextIndex = 0
        # 给第二个窗口添加的淡入淡出动画
        self.__opacityEffect = QGraphicsOpacityEffect(self)
        self.__opacityAni = QPropertyAnimation(
            self.__opacityEffect, b'opacity')
        # 初始化动画
        self.__opacityEffect.setOpacity(0)
        self.__opacityAni.setDuration(220)
        self.__opacityAni.finished.connect(self.__aniFinishedSlot)

    def addWidget(self, widget):
        """ 向窗口中添加堆叠窗口 """
        if self.count() == 2:
            raise Exception('最多只能有两个堆叠窗口')
        super().addWidget(widget)
        # 给第二个窗口设置淡入淡出效果
        if self.count() == 2:
            self.widget(1).setGraphicsEffect(self.__opacityEffect)

    def setCurrentIndex(self, index: int):
        """ 切换当前堆叠窗口 """
        # 如果当前下标等于目标下标就直接返回
        if index == self.currentIndex():
            return
        if index == 1:
            self.__opacityAni.setStartValue(0)
            self.__opacityAni.setEndValue(1)
            super().setCurrentIndex(1)
        elif index == 0:
            self.__opacityAni.setStartValue(1)
            self.__opacityAni.setEndValue(0)
        else:
            raise Exception('下标不能超过1')
        # 强行显示被隐藏的 widget(0)
        self.widget(0).show()
        self.__nextIndex = index
        self.__opacityAni.start()

    def setCurrentWidget(self, widget):
        """ 切换当前堆叠窗口 """
        self.setCurrentIndex(self.indexOf(widget))

    def __aniFinishedSlot(self):
        """ 动画完成后切换当前窗口 """
        super().setCurrentIndex(self.__nextIndex)
