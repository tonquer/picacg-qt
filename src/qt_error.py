import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyle, QErrorMessage, QLabel, QCheckBox, QPushButton

from tools.tool import ToolUtil


def showError(message, app):
    app.setQuitOnLastWindowClosed(True)
    # 设置内置错误图标
    w = QErrorMessage()
    w.setWindowIcon(app.style().standardIcon(QStyle.SP_MessageBoxCritical))
    w.finished.connect(lambda _: app.quit)
    w.resize(600, 400)
    # 去掉右上角?
    w.setWindowFlags(w.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    w.setWindowTitle(w.tr('Error'))
    # 隐藏图标、勾选框、按钮
    w.findChild(QLabel, '').setVisible(False)
    w.findChild(QCheckBox, '').setVisible(False)
    w.findChild(QPushButton, '').setVisible(False)
    w.showMessage(ToolUtil.Escape(message))
    app.exec()

