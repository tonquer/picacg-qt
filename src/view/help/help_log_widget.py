import logging
import random
import re
import sys
from io import TextIOWrapper

from PySide6.QtCore import QUrl, Signal, QTimer
from PySide6.QtGui import QDesktopServices, Qt, QTextCursor, QColor
from PySide6.QtWidgets import QWidget, QMessageBox, QTextEdit, QStyle
from interface.ui_help_log_widget import Ui_HelpLogWidget
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.tool import ToolUtil


class HelpLogWidget(QWidget, Ui_HelpLogWidget):
    logMsg = Signal(int, str)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_HelpLogWidget.__init__(self)
        self.setupUi(self)
        self.buttonGroup.setId(self.warnButton, logging.WARN)
        self.buttonGroup.setId(self.infoButton, logging.INFO)
        self.buttonGroup.setId(self.debugButton, logging.DEBUG)
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setOpenExternalLinks(True)
        self.logMsg.connect(self.AddLog)
        Log.InstallFilter(self)
        self.defaultColor = None
        self.runEnable = False
        self._SetRunEnable(self.runEnable)
        self.toolButton.clicked.connect(self.SwitchRunEnable)
        self.runButton.clicked.connect(self.RunCode)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

    def write(self, levelNo, info):
        self.logMsg.emit(levelNo, info)

    def AddLog(self, logLevel, logData):
        if self.isHidden():
            return
        if logLevel < self.buttonGroup.checkedId():
            return
        if logLevel == logging.ERROR:
            self._AddLog(logData, "#ff0000")
        else:
            self._AddLog(logData)
        return

    def _AddLog(self, logData, color=None):
        if not self.defaultColor:
            self.defaultColor = QColor(255, 64, 129)
        self.textBrowser.moveCursor(QTextCursor.Start)
        if not color:
            color = "#ff4081"
        #     logData = "<font color=#1661ab>{}</font>".format(logData)
            self.textBrowser.setTextColor(color)
        else:
            self.textBrowser.setTextColor(self.defaultColor)

        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = re.findall(pattern, logData)
        if urls:
            url = urls[0]
            data = logData.split(url, 2)
            if len(data) == 2:
                logData = ToolUtil.Escape(data[0]) + "<a href=\"{}\">{}</a>".format(url, url) + ToolUtil.Escape(data[1])
                self.textBrowser.insertHtml("<p>{}</p>".format(logData))
                return
        self.textBrowser.insertHtml("<p style=\"color: {}\">{}</p>".format(color, ToolUtil.Escape(logData)))
        # self.textEdit.setTextColor(self.defaultColor)

    def SwitchRunEnable(self):
        self.runEnable = not self.runEnable
        self._SetRunEnable(self.runEnable)

    def _SetRunEnable(self, isEnable):
        if isEnable:
            self.toolButton.setArrowType(Qt.UpArrow)
            self.textEdit.setVisible(True)
            self.runButton.setVisible(True)
        else:
            self.toolButton.setArrowType(Qt.DownArrow)
            self.textEdit.setVisible(False)
            self.runButton.setVisible(False)

    def RunCode(self):
        text = self.textEdit.toPlainText()
        try:
            for v in text.split("\n"):
                Log.Info("Run code: {}".format(v))
                exec(v)
            self.textEdit.setText("")
        except Exception as es:
            Log.Error(es)