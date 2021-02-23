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
        AboutForm.resize(379, 251)
        self.gridLayout = QGridLayout(AboutForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(AboutForm)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(AboutForm)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(AboutForm)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.label_3 = QLabel(AboutForm)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)


        self.retranslateUi(AboutForm)

        QMetaObject.connectSlotsByName(AboutForm)
    # setupUi

    def retranslateUi(self, AboutForm):
        AboutForm.setWindowTitle(QCoreApplication.translate("AboutForm", u"Form", None))
        self.label.setText(QCoreApplication.translate("AboutForm", u"\u54d4\u5494\u6f2b\u753bv1.0.3", None))
        self.label_2.setText(QCoreApplication.translate("AboutForm", u"\u672c\u8f6f\u4ef6\u4e0d\u5f97\u7528\u4e8e\u5546\u4e1a\u7528\u9014\uff0c\u4ec5\u505a\u5b66\u4e60\u4ea4\u6d41", None))
        self.label_4.setText(QCoreApplication.translate("AboutForm", u"\u9879\u76ee\u5f00\u6e90\u5730\u5740\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("AboutForm", u"<a href=\"https://github.com/tonquer/picacg-windows\"> https://github.com/tonquer/picacg-windows</a>", None))
    # retranslateUi

