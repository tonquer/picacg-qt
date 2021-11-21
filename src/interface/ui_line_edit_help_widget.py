# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_line_edit_help_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListView,
    QSizePolicy, QVBoxLayout, QWidget)

from component.button.switch_button import SwitchButton

class Ui_LineEditHelp(object):
    def setupUi(self, LineEditHelp):
        if not LineEditHelp.objectName():
            LineEditHelp.setObjectName(u"LineEditHelp")
        LineEditHelp.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(LineEditHelp)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(LineEditHelp)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.listView = QListView(LineEditHelp)
        self.listView.setObjectName(u"listView")

        self.verticalLayout_2.addWidget(self.listView)

        self.label_2 = QLabel(LineEditHelp)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(LineEditHelp)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.localWidget = SwitchButton(LineEditHelp)
        self.localWidget.setObjectName(u"localWidget")

        self.horizontalLayout_2.addWidget(self.localWidget)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.titleLabel = QLabel(LineEditHelp)
        self.titleLabel.setObjectName(u"titleLabel")

        self.horizontalLayout_4.addWidget(self.titleLabel)

        self.titleWidget = SwitchButton(LineEditHelp)
        self.titleWidget.setObjectName(u"titleWidget")

        self.horizontalLayout_4.addWidget(self.titleWidget)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.desLabel = QLabel(LineEditHelp)
        self.desLabel.setObjectName(u"desLabel")

        self.horizontalLayout_5.addWidget(self.desLabel)

        self.desWidget = SwitchButton(LineEditHelp)
        self.desWidget.setObjectName(u"desWidget")

        self.horizontalLayout_5.addWidget(self.desWidget)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.categoryLabel = QLabel(LineEditHelp)
        self.categoryLabel.setObjectName(u"categoryLabel")

        self.horizontalLayout_3.addWidget(self.categoryLabel)

        self.categoryWidget = SwitchButton(LineEditHelp)
        self.categoryWidget.setObjectName(u"categoryWidget")

        self.horizontalLayout_3.addWidget(self.categoryWidget)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tagLabel = QLabel(LineEditHelp)
        self.tagLabel.setObjectName(u"tagLabel")

        self.horizontalLayout.addWidget(self.tagLabel)

        self.tagWidget = SwitchButton(LineEditHelp)
        self.tagWidget.setObjectName(u"tagWidget")

        self.horizontalLayout.addWidget(self.tagWidget)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.authorLabel = QLabel(LineEditHelp)
        self.authorLabel.setObjectName(u"authorLabel")

        self.horizontalLayout_6.addWidget(self.authorLabel)

        self.authorWidget = SwitchButton(LineEditHelp)
        self.authorWidget.setObjectName(u"authorWidget")

        self.horizontalLayout_6.addWidget(self.authorWidget)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.retranslateUi(LineEditHelp)

        QMetaObject.connectSlotsByName(LineEditHelp)
    # setupUi

    def retranslateUi(self, LineEditHelp):
        LineEditHelp.setWindowTitle(QCoreApplication.translate("LineEditHelp", u"Form", None))
        self.label.setText(QCoreApplication.translate("LineEditHelp", u"\u8054\u60f3\u8bcd", None))
        self.label_2.setText(QCoreApplication.translate("LineEditHelp", u"\u6761\u4ef6", None))
        self.label_4.setText(QCoreApplication.translate("LineEditHelp", u"\u4f7f\u7528\u672c\u5730\u5e93", None))
        self.titleLabel.setText(QCoreApplication.translate("LineEditHelp", u"\u6807\u9898", None))
        self.desLabel.setText(QCoreApplication.translate("LineEditHelp", u"\u63cf\u8ff0", None))
        self.categoryLabel.setText(QCoreApplication.translate("LineEditHelp", u"\u5206\u7c7b", None))
        self.tagLabel.setText(QCoreApplication.translate("LineEditHelp", u"TAG", None))
        self.authorLabel.setText(QCoreApplication.translate("LineEditHelp", u"\u4f5c\u8005", None))
    # retranslateUi

