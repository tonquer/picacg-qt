from PySide6 import QtWidgets

from interface.ui_login_widget import Ui_LoginWidget
from qt_owner import QtOwner
from server import req, Status, config
from task.qt_task import QtTaskBase
from tools.str import Str
from tools.user import User


class LoginWidget(QtWidgets.QWidget, Ui_LoginWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LoginWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        # self.buttonGroup = QtWidgets.QButtonGroup(self)
        # self.buttonGroup.addButton(self.selectIp1)
        # self.selectIp1.setChecked(True)

    def Init(self):
        # self.userEdit_2.setText()
        # request = req.InitReq()
        # request.proxy = {}
        # self.AddHttpTask(request, self.InitBack)
        return

    def ClickButton(self):
        self.Login()

    def Login(self):
        QtOwner().ShowLoading()
        userId = self.userEdit_2.text()
        passwd = self.passwdEdit_2.text()
        User().SetUserInfo(userId, passwd)
        self.AddHttpTask(req.LoginReq(userId, passwd), self.LoginBack)

        # self.close()
        # self.owner().show()

    def LoginBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            # self.close()
            self.InitUser()
            # LoginView.CloseLogin.emit()
            self.parent().parent().parent().parent().close()
            # QtOwner().owner.UpdateDbInfo()
            # QtOwner().owner.userForm.toolButton0.click()
            # QtOwner().owner.searchForm.InitKeyWord()
            # QtOwner().owner.indexForm.Init()
            # QtOwner().owner.favoriteForm.InitFavorite()
            QtOwner().settingView.userId = self.userEdit_2.text()
            QtOwner().settingView.passwd = self.passwdEdit_2.text()


        else:
            # QtWidgets.QMessageBox.information(self, '登陆失败', msg, QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(Str.GetStr(Str.LoginFail) + ", " + Str.GetStr(st))

    def InitUser(self):
        self.AddHttpTask(req.GetUserInfo(), self.UpdateUserBack)
        return

    def UpdateUserBack(self, msg):
        # QtOwner().owner.userForm.UpdateLabel(User().name, User().level, User().exp, User().title, User().isPunched)
        return
        if not User().avatar:
            return

        url = User().avatar.get("fileServer")
        path = User().avatar.get("path")
        if url and path and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.ShowUserImg)

    def ShowUserImg(self, data, st):
        if st == Status.Ok:
            QtOwner().owner.userForm.SetPicture(data)

    # def InitBack(self, msg):
    #     QtOwner().CloseLoading()
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
