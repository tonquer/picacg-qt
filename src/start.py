# -*- coding: utf-8 -*-
"""第一个程序"""
import os
import sys
# macOS 修复
import time
import traceback
import signal

from config import config
from config.setting import Setting, SettingValue
from qt_error import showError, showError2
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str

if sys.platform == 'darwin':
    # 确保工作区为当前可执行文件所在目录
    current_path = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')
    os.chdir(current_dir)

try:
    from sr_vulkan import sr_vulkan as sr

    config.CanWaifu2x = True
except ModuleNotFoundError as es:
    config.CanWaifu2x = False
    config.CloseWaifu2x = True
    if hasattr(es, "msg"):
        config.ErrorMsg = es.msg
except Exception as es:
    config.CanWaifu2x = False
    if hasattr(es, "msg"):
        config.ErrorMsg = es.msg

from PySide6.QtGui import QFont
from PySide6 import QtWidgets, QtGui  # 导入PySide6部件
from PySide6.QtNetwork import QLocalSocket, QLocalServer
# 此处不能删除
import images_rc
from server.sql_server import DbBook as DbBook
DbBook()

if __name__ == "__main__":
    try:
        Log.Init()
        Setting.Init()
        Setting.InitLoadSetting()
        os.environ['QT_IMAGEIO_MAXALLOC'] = "10000000000000000000000000000000000000000000000000000000000000000"
        QtGui.QImageReader.setAllocationLimit(0)
        if Setting.IsUseScaleFactor.value > 0:
            indexV = Setting.ScaleFactor.value
            # os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
            os.environ["QT_SCALE_FACTOR"] = str(indexV / 100)

    except Exception as es:
        Log.Error(es)
        app = QtWidgets.QApplication(sys.argv)
        showError(traceback.format_exc(), app)
        if config.CanWaifu2x:
            sr.stop()
        sys.exit(-111)

    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    serverName = 'Picacg-qt'
    socket = QLocalSocket()
    socket.connectToServer(serverName)
    if socket.waitForConnected(500):
        socket.write(b"restart")
        socket.flush()
        socket.close()
        app.quit()
        Log.Warn("server already star")
        sys.exit(1)

    localServer = QLocalServer()  # 没有实例运行，创建服务器
    localServer.listen(serverName)

    Log.Warn("init scene ratio: {}".format(app.devicePixelRatio()))
    try:
        Str.Reload()
        QtOwner().SetApp(app)
        QtOwner().SetLocalServer(localServer)
        QtOwner().SetFont()
        from view.main.main_view import MainView

        main = MainView()
        main.show()  # 显示窗体
        main.Init()
        localServer.newConnection.connect(main.OnNewConnection)
    except Exception as es:
        Log.Error(es)
        showError(traceback.format_exc(), app)
        if config.CanWaifu2x:
            sr.stop()
        sys.exit(-111)

    oldHook = sys.excepthook


    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        Log.Error(tb)
        showError2(tb, app)


    sys.excepthook = excepthook
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sts = app.exec()
    sys.excepthook = oldHook
    socket.close()
    main.Close()
    if config.CanWaifu2x:
        sr.stop()
    time.sleep(2)
    print(sts)
    sys.exit(sts)
