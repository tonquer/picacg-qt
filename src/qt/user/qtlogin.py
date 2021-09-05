from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel

from conf import config
from src.qt.qtmain import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import Server, req
from src.user.user import User
from src.util.status import Status
from ui.login import Ui_Login


class QtLogin(QtWidgets.QWidget, Ui_Login, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Login.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        # self.buttonGroup = QtWidgets.QButtonGroup(self)
        # self.buttonGroup.addButton(self.selectIp1)
        # self.selectIp1.setChecked(True)

    def Login(self):
        userId = self.userIdEdit.text()
        passwd = self.passwdEdit.text()
        User().SetUserInfo(userId, passwd)
        self.AddHttpTask(req.LoginReq(userId, passwd), self.LoginBack)

        QtOwner().owner.loadingForm.show()
        # self.close()
        # self.owner().show()

    def LoginBack(self, msg):
        QtOwner().owner.loadingForm.close()
        if msg == Status.Ok:
            # self.close()
            QtOwner().owner.stackedWidget.setCurrentIndex(1)
            self.InitUser()

            QtOwner().owner.UpdateDbInfo()
            QtOwner().owner.userForm.toolButton0.click()
            QtOwner().owner.searchForm.InitKeyWord()
            QtOwner().owner.indexForm.Init()
            QtOwner().owner.favoriteForm.InitFavorite()
        else:
            # QtWidgets.QMessageBox.information(self, '登陆失败', msg, QtWidgets.QMessageBox.Yes)
            QtOwner().owner.msgForm.ShowError(self.tr("登陆失败, ") + QtOwner().owner.GetStatusStr(msg))

    def InitUser(self):
        self.AddHttpTask(req.GetUserInfo(), self.UpdateUserBack)
        return

    def UpdateUserBack(self, msg):
        QtOwner().owner.userForm.UpdateLabel(User().name, User().level, User().exp, User().title, User().isPunched)
        if not User().avatar:
            return

        url = User().avatar.get("fileServer")
        path = User().avatar.get("path")
        if url and path and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.ShowUserImg)

    def ShowUserImg(self, data, st):
        if st == Status.Ok:
            QtOwner().owner.userForm.SetPicture(data)

    def OpenRegister(self):
        QtOwner().owner.registerForm.show()
        return

    def Init(self):
        # QtOwner().owner.loadingForm.show()
        # request = req.InitReq()
        # request.proxy = {}
        # self.AddHttpTask(request, self.InitBack)
        return

    # def InitBack(self, msg):
    #     QtOwner().owner.loadingForm.close()
    #     if msg == Status.Ok:
    #         # for index, ip in enumerate(User().addresss, 2):
    #         #     selectIp = QtWidgets.QRadioButton(self)
    #         #     selectIp.setObjectName("selectIp"+str(index))
    #             # self.buttonGroup.addButton(selectIp)
    #             # count = self.gridLayout_4.rowCount()
    #             # self.gridLayout_4.addWidget(selectIp, count, 0, 1, 1)
    #             # selectIp.setText("分流" + str(index))
    #         self.update()
    #     else:
    #         # QtWidgets.QMessageBox.information(self, , QtWidgets.QMessageBox.Yes)
    #         QtOwner().owner.msgForm.ShowError("无法更新哔咔分流列表")
    #     pass


    def OpenProxy(self):
        QtOwner().owner.loginProxyForm.show()
