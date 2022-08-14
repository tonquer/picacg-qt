# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_comment.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

from component.list.user_list_widget import UserListWidget

class Ui_Comment(object):
    def setupUi(self, Comment):
        if not Comment.objectName():
            Comment.setObjectName(u"Comment")
        Comment.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Comment)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget = UserListWidget(Comment)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.commentLine = QLineEdit(Comment)
        self.commentLine.setObjectName(u"commentLine")

        self.horizontalLayout.addWidget(self.commentLine)

        self.pushButton = QPushButton(Comment)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.nums = QLabel(Comment)
        self.nums.setObjectName(u"nums")

        self.horizontalLayout.addWidget(self.nums)

        self.spinBox = QSpinBox(Comment)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout.addWidget(self.spinBox)

        self.skipButton = QPushButton(Comment)
        self.skipButton.setObjectName(u"skipButton")

        self.horizontalLayout.addWidget(self.skipButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Comment)

        QMetaObject.connectSlotsByName(Comment)
    # setupUi

    def retranslateUi(self, Comment):
        Comment.setWindowTitle(QCoreApplication.translate("Comment", u"\u8bc4\u8bba", None))
        self.pushButton.setText(QCoreApplication.translate("Comment", u"\u56de\u590d", None))
#if QT_CONFIG(shortcut)
        self.pushButton.setShortcut(QCoreApplication.translate("Comment", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.nums.setText(QCoreApplication.translate("Comment", u"TextLabel", None))
        self.skipButton.setText(QCoreApplication.translate("Comment", u"\u8df3\u8f6c", None))
    # retranslateUi

