from PySide6 import QtWidgets

from interface.ui_book_right import Ui_BookRight


class BookInfoRight(QtWidgets.QWidget, Ui_BookRight):

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookRight.__init__(self)
        self.setupUi(self)