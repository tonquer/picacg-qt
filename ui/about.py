# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_AboutForm(object):
    def setupUi(self, AboutForm):
        if not AboutForm.objectName():
            AboutForm.setObjectName(u"AboutForm")
        AboutForm.resize(379, 284)
        self.gridLayout = QGridLayout(AboutForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_4 = QFrame(AboutForm)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_4, 8, 0, 1, 1)

        self.line_3 = QFrame(AboutForm)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 0, 0, 1, 1)

        self.line = QFrame(AboutForm)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)

        self.line_2 = QFrame(AboutForm)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 5, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(AboutForm)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 3, 4, 1, 1)

        self.label_8 = QLabel(AboutForm)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 4, 4, 1, 1)

        self.line_8 = QFrame(AboutForm)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.VLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_8, 5, 1, 1, 1)

        self.label_2 = QLabel(AboutForm)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 4, 1, 1)

        self.line_7 = QFrame(AboutForm)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.VLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_7, 4, 1, 1, 1)

        self.label_10 = QLabel(AboutForm)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 5, 4, 1, 1)

        self.line_9 = QFrame(AboutForm)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.VLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_9, 1, 1, 1, 1)

        self.label_5 = QLabel(AboutForm)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_7 = QLabel(AboutForm)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)

        self.line_6 = QFrame(AboutForm)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_6, 3, 1, 1, 1)

        self.label = QLabel(AboutForm)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.label_4 = QLabel(AboutForm)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_9 = QLabel(AboutForm)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 5, 0, 1, 1)

        self.label_3 = QLabel(AboutForm)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 4, 1, 1)

        self.line_5 = QFrame(AboutForm)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_5, 2, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 4, 0, 1, 1)


        self.retranslateUi(AboutForm)

        QMetaObject.connectSlotsByName(AboutForm)
    # setupUi

    def retranslateUi(self, AboutForm):
        AboutForm.setWindowTitle(QCoreApplication.translate("AboutForm", u"Form", None))
        self.label_6.setText(QCoreApplication.translate("AboutForm", u"1.0.2", None))
        self.label_8.setText(QCoreApplication.translate("AboutForm", u"<a href=\"https://github.com/tonquer/waifu2x-ncnn-vulkan-python\"> waifu2x-ncnn-vulkan-python</a>", None))
        self.label_2.setText(QCoreApplication.translate("AboutForm", u"\u672c\u8f6f\u4ef6\u4e0d\u5f97\u7528\u4e8e\u5546\u4e1a\u7528\u9014\uff0c\u4ec5\u505a\u5b66\u4e60\u4ea4\u6d41", None))
        self.label_10.setText(QCoreApplication.translate("AboutForm", u"<a href=\"https://github.com/tonquer/ehentai-read\"> https://github.com/tonquer/ehentai-read</a>", None))
        self.label_5.setText(QCoreApplication.translate("AboutForm", u"waifu2x\u7248\u672c\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("AboutForm", u"waifu2x\u5730\u5740", None))
        self.label.setText(QCoreApplication.translate("AboutForm", u"\u54d4\u5494\u6f2b\u753bv1.0.5", None))
        self.label_4.setText(QCoreApplication.translate("AboutForm", u"\u9879\u76ee\u5f00\u6e90\u5730\u5740\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("AboutForm", u"E-hentai", None))
        self.label_3.setText(QCoreApplication.translate("AboutForm", u"<a href=\"https://github.com/tonquer/picacg-windows\"> https://github.com/tonquer/picacg-windows</a>", None))
    # retranslateUi

