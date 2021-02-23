import weakref

from PySide2.QtGui import QPixmap

from conf import config
from src.qt.util.qttask import QtTask
from src.user.user import User
from src.util.status import Status
from ui.login import Ui_Login
from PySide2 import QtWidgets


class QtLogin(QtWidgets.QWidget, Ui_Login):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_Login.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.setWindowTitle("登陆")
        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(self.selectIp1)
        self.selectIp1.setChecked(True)

    def Login(self):
        self.SetSelectIp()
        userId = self.userIdEdit.text()
        passwd = self.passwdEdit.text()
        User().SetUserInfo(userId, passwd)
        QtTask().AddHttpTask(lambda x: User().Login(x), self.LoginBack)

        self.owner().loadingForm.show()
        # self.close()
        # self.owner().show()

    def LoginBack(self, msg):
        self.owner().loadingForm.close()
        if msg == Status.Ok:
            # self.close()
            self.owner().stackedWidget.setCurrentIndex(1)
            self.owner().qtTask.AddHttpTask(lambda x: User().UpdateUserInfo(x), self.UpdateUserBack)
            self.owner().searchForm.InitKeyWord()
        else:
            # QtWidgets.QMessageBox.information(self, '登陆失败', msg, QtWidgets.QMessageBox.Yes)
            self.owner().msgForm.ShowError("登陆失败, " + msg)

    def UpdateUserBack(self, msg):
        self.owner().userForm.UpdateLabel(User().name, User().level, User().exp, User().isPunched)
        url = User().avatar.get("fileServer")
        path = User().avatar.get("path")
        if url and path and config.IsLoadingPicture:
            self.owner().qtTask.AddDownloadTask(url, path, None, self.ShowUserImg)

    def ShowUserImg(self, data, st):
        if st == Status.Ok:
            a = QPixmap()
            a.loadFromData(data)
            self.owner().userForm.icon.setPixmap(a)

    def OpenRegister(self):
        self.SetSelectIp()
        self.owner().registerForm.show()
        return

    def Init(self):
        self.owner().loadingForm.show()
        QtTask().AddHttpTask(lambda x: User().Init(x), self.InitBack)
        return

    def InitBack(self, msg):
        self.owner().loadingForm.close()
        if msg == Status.Ok:
            for index, ip in enumerate(User().addresss, 2):
                selectIp = QtWidgets.QRadioButton(self)
                selectIp.setObjectName("selectIp"+str(index))
                self.horizontalLayout_4.addWidget(selectIp)
                self.buttonGroup.addButton(selectIp)
                selectIp.setText("分流" + str(index))
            self.update()
        else:
            # QtWidgets.QMessageBox.information(self, , QtWidgets.QMessageBox.Yes)
            self.owner().msgForm.ShowError("无法获取哔咔分流列表")
        pass

    def SetSelectIp(self):
        index = int(self.buttonGroup.checkedButton().objectName().replace("selectIp", "")) - 1
        if index == 0:
            User().address = ""
        else:
            User().address = User().addresss[index-1]
