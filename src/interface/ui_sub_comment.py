# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_sub_comment.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout, QWidget)

from component.widget.comment_item_widget import CommentItemWidget
from component.widget.comment_widget import CommentWidget

class Ui_SubComment(object):
    def setupUi(self, SubComment):
        if not SubComment.objectName():
            SubComment.setObjectName(u"SubComment")
        SubComment.resize(400, 300)
        self.verticalLayout = QVBoxLayout(SubComment)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.comment = CommentItemWidget(SubComment)
        self.comment.setObjectName(u"comment")

        self.verticalLayout.addWidget(self.comment)

        self.commentList = CommentWidget(SubComment)
        self.commentList.setObjectName(u"commentList")

        self.verticalLayout.addWidget(self.commentList)


        self.retranslateUi(SubComment)

        QMetaObject.connectSlotsByName(SubComment)
    # setupUi

    def retranslateUi(self, SubComment):
        SubComment.setWindowTitle(QCoreApplication.translate("SubComment", u"\u5b50\u8bc4\u8bba", None))
    # retranslateUi

