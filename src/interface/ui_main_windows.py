# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_windows.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

from component.widget.animation_stack_widget import AnimationStackWidget
from component.widget.navigation_widget import NavigationWidget
from component.widget.title_bar_widget import TitleBarWidget
from view.category.category_view import CategoryView
from view.category.rank_view import RankView
from view.chat.chat_view import ChatView
from view.chat_new.chat_new_view import ChatNewView
from view.comment.comment_view import CommentView
from view.comment.game_comment_view import GameCommentView
from view.comment.my_comment_view import MyCommentView
from view.comment.sub_comment_view import SubCommentView
from view.convert.convert_view import ConvertView
from view.download.download_all_view import DownloadAllView
from view.download.download_view import DownloadView
from view.fried.fried_view import FriedView
from view.game.game_view import GameView
from view.help.help_view import HelpView
from view.index.index_view import IndexView
from view.info.book_eps_view import BookEpsView
from view.info.book_info_view import BookInfoView
from view.info.game_info_view import GameInfoView
from view.nas.nas_view import NasView
from view.read.read_view import ReadView
from view.search.search_view import SearchView
from view.setting.setting_view import SettingView
from view.tool.local_read_all_view import LocalReadAllView
from view.tool.local_read_eps_view import LocalReadEpsView
from view.tool.local_read_view import LocalReadView
from view.tool.waifu2x_tool_view import Waifu2xToolView
from view.user.favorite_view import FavoriteView
from view.user.history_view import HistoryView

class Ui_MainWindows(object):
    def setupUi(self, MainWindows):
        if not MainWindows.objectName():
            MainWindows.setObjectName(u"MainWindows")
        MainWindows.resize(903, 489)
        self.verticalLayout = QVBoxLayout(MainWindows)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.widget = TitleBarWidget(MainWindows)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 40))
        self.widget.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.widget)

        self.totalStackWidget = QStackedWidget(MainWindows)
        self.totalStackWidget.setObjectName(u"totalStackWidget")
        self.subMainWindow = QWidget()
        self.subMainWindow.setObjectName(u"subMainWindow")
        self.horizontalLayout_2 = QHBoxLayout(self.subMainWindow)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.navigationWidget = NavigationWidget(self.subMainWindow)
        self.navigationWidget.setObjectName(u"navigationWidget")
        self.navigationWidget.setMinimumSize(QSize(240, 0))
        self.navigationWidget.setMaximumSize(QSize(280, 16777215))

        self.horizontalLayout_2.addWidget(self.navigationWidget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.menuLayout = QHBoxLayout()
        self.menuLayout.setObjectName(u"menuLayout")
        self.menuButton = QPushButton(self.subMainWindow)
        self.menuButton.setObjectName(u"menuButton")

        self.menuLayout.addWidget(self.menuButton)

        self.label = QLabel(self.subMainWindow)
        self.label.setObjectName(u"label")

        self.menuLayout.addWidget(self.label)


        self.horizontalLayout_3.addLayout(self.menuLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.subStackWidget = AnimationStackWidget(self.subMainWindow)
        self.subStackWidget.setObjectName(u"subStackWidget")
        self.indexView = IndexView()
        self.indexView.setObjectName(u"indexView")
        self.subStackWidget.addWidget(self.indexView)
        self.helpView = HelpView()
        self.helpView.setObjectName(u"helpView")
        self.subStackWidget.addWidget(self.helpView)
        self.myCommentView = MyCommentView()
        self.myCommentView.setObjectName(u"myCommentView")
        self.subStackWidget.addWidget(self.myCommentView)
        self.settingView = SettingView()
        self.settingView.setObjectName(u"settingView")
        self.subStackWidget.addWidget(self.settingView)
        self.downloadView = DownloadView()
        self.downloadView.setObjectName(u"downloadView")
        self.subStackWidget.addWidget(self.downloadView)
        self.categoryView = CategoryView()
        self.categoryView.setObjectName(u"categoryView")
        self.subStackWidget.addWidget(self.categoryView)
        self.searchView = SearchView()
        self.searchView.setObjectName(u"searchView")
        self.subStackWidget.addWidget(self.searchView)
        self.searchView2 = SearchView()
        self.searchView2.setObjectName(u"searchView2")
        self.subStackWidget.addWidget(self.searchView2)
        self.rankView = RankView()
        self.rankView.setObjectName(u"rankView")
        self.subStackWidget.addWidget(self.rankView)
        self.commentView = CommentView()
        self.commentView.setObjectName(u"commentView")
        self.subStackWidget.addWidget(self.commentView)
        self.subCommentView = SubCommentView()
        self.subCommentView.setObjectName(u"subCommentView")
        self.subStackWidget.addWidget(self.subCommentView)
        self.chatView = ChatView()
        self.chatView.setObjectName(u"chatView")
        self.subStackWidget.addWidget(self.chatView)
        self.favorityView = FavoriteView()
        self.favorityView.setObjectName(u"favorityView")
        self.subStackWidget.addWidget(self.favorityView)
        self.historyView = HistoryView()
        self.historyView.setObjectName(u"historyView")
        self.subStackWidget.addWidget(self.historyView)
        self.bookInfoView = BookInfoView()
        self.bookInfoView.setObjectName(u"bookInfoView")
        self.subStackWidget.addWidget(self.bookInfoView)
        self.gameCommentView = GameCommentView()
        self.gameCommentView.setObjectName(u"gameCommentView")
        self.subStackWidget.addWidget(self.gameCommentView)
        self.gameInfoView = GameInfoView()
        self.gameInfoView.setObjectName(u"gameInfoView")
        self.subStackWidget.addWidget(self.gameInfoView)
        self.gameView = GameView()
        self.gameView.setObjectName(u"gameView")
        self.subStackWidget.addWidget(self.gameView)
        self.waifu2xToolView = Waifu2xToolView()
        self.waifu2xToolView.setObjectName(u"waifu2xToolView")
        self.subStackWidget.addWidget(self.waifu2xToolView)
        self.downloadAllView = DownloadAllView()
        self.downloadAllView.setObjectName(u"downloadAllView")
        self.subStackWidget.addWidget(self.downloadAllView)
        self.localReadView = LocalReadView()
        self.localReadView.setObjectName(u"localReadView")
        self.subStackWidget.addWidget(self.localReadView)
        self.chatNewView = ChatNewView()
        self.chatNewView.setObjectName(u"chatNewView")
        self.subStackWidget.addWidget(self.chatNewView)
        self.localReadEpsView = LocalReadEpsView()
        self.localReadEpsView.setObjectName(u"localReadEpsView")
        self.subStackWidget.addWidget(self.localReadEpsView)
        self.convertView = ConvertView()
        self.convertView.setObjectName(u"convertView")
        self.subStackWidget.addWidget(self.convertView)
        self.localReadAllView = LocalReadAllView()
        self.localReadAllView.setObjectName(u"localReadAllView")
        self.subStackWidget.addWidget(self.localReadAllView)
        self.nasView = NasView()
        self.nasView.setObjectName(u"nasView")
        self.subStackWidget.addWidget(self.nasView)
        self.bookEpsView = BookEpsView()
        self.bookEpsView.setObjectName(u"bookEpsView")
        self.subStackWidget.addWidget(self.bookEpsView)
        self.friedView = FriedView()
        self.friedView.setObjectName(u"friedView")
        self.subStackWidget.addWidget(self.friedView)

        self.verticalLayout_2.addWidget(self.subStackWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.totalStackWidget.addWidget(self.subMainWindow)
        self.readView = ReadView()
        self.readView.setObjectName(u"readView")
        self.totalStackWidget.addWidget(self.readView)

        self.verticalLayout.addWidget(self.totalStackWidget)


        self.retranslateUi(MainWindows)

        self.subStackWidget.setCurrentIndex(25)


        QMetaObject.connectSlotsByName(MainWindows)
    # setupUi

    def retranslateUi(self, MainWindows):
        MainWindows.setWindowTitle(QCoreApplication.translate("MainWindows", u"PicACG", None))
        self.menuButton.setText(QCoreApplication.translate("MainWindows", u"\u83dc\u5355", None))
        self.label.setText(QCoreApplication.translate("MainWindows", u">", None))
    # retranslateUi

