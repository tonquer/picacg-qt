import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyle, QErrorMessage, QLabel, QCheckBox, QPushButton


def showError(message, app):
    app.setQuitOnLastWindowClosed(True)
    # 设置内置错误图标
    app.setWindowIcon(app.style().standardIcon(QStyle.SP_MessageBoxCritical))
    w = QErrorMessage()
    w.finished.connect(lambda _: app.quit)
    w.resize(600, 400)
    # 去掉右上角?
    w.setWindowFlags(w.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    w.setWindowTitle(w.tr('Error'))
    # 隐藏图标、勾选框、按钮
    w.findChild(QLabel, '').setVisible(False)
    w.findChild(QCheckBox, '').setVisible(False)
    w.findChild(QPushButton, '').setVisible(False)
    w.showMessage(escape(message))
    app.exec()

def showError2(message, app):
    # app.setQuitOnLastWindowClosed(True)
    # # 设置内置错误图标
    # app.setWindowIcon(app.style().standardIcon(QStyle.SP_MessageBoxCritical))
    w = QErrorMessage()
    w.setWindowIcon(w.style().standardIcon(QStyle.SP_MessageBoxCritical))
    # w.finished.connect(lambda _: app.quit)
    w.resize(600, 400)
    # 去掉右上角?
    w.setWindowFlags(w.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    w.setWindowTitle(w.tr('Error'))
    # 隐藏图标、勾选框、按钮
    w.findChild(QLabel, '').setVisible(False)
    w.findChild(QCheckBox, '').setVisible(False)
    w.findChild(QPushButton, '').setVisible(False)
    w.showMessage(escape(message))
    w.exec()

def escape(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace('\'', "&#x27;")
    s = s.replace('\n', '<br/>')
    s = s.replace(' ', '&nbsp;')
    return s