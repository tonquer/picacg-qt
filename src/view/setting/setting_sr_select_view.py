import base64

from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtWidgets import QHeaderView, QTableWidgetItem

from component.dialog.base_mask_dialog import BaseMaskDialog
from component.label.gif_label import GifLabel
from config.setting import Setting
from interface.ui_sr_select_widget import Ui_SrSelect
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.str import Str


class SettingSrSelectView(BaseMaskDialog, Ui_SrSelect):
    Close = Signal(str)

    def __init__(self, parent=None, curModelName=""):
        BaseMaskDialog.__init__(self, parent)
        Ui_SrSelect.__init__(self)
        self.widget.adjustSize()
        self.setupUi(self.widget)
        self.curModelName = curModelName
        self.saveButton.clicked.connect(self._ClickButton)
        self.closeButton.clicked.connect(self.close)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.horizontalHeader().setMinimumSectionSize(120)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 100)
        self.Init()

    def _ClickButton(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = []
        for index in selected:
            selectRows.append(index.row())
        if not selectRows:
            return
        row = selectRows[0]
        modelName1 = self.tableWidget.item(row, 0).text()
        modelName2 = self.tableWidget.item(row, 1).text().replace("-", "")
        modelName = "MODEL_" + modelName2.upper() + "_" + modelName1.upper()
        self.Close.emit(modelName)
        self.close()

    def Init(self):
        AllModelNames = [
            ("CUNET_UP1X_DENOISE0X","Waifu2x", "", "100%"),
            ("CUNET_UP1X_DENOISE1X","Waifu2x", "", "110%"),
            ("CUNET_UP1X_DENOISE2X","Waifu2x", "", "110%"),
            ("CUNET_UP1X_DENOISE3X","Waifu2x", "", "110%"),
            ("CUNET_UP2X","Waifu2x", "", "300%"),
            ("CUNET_UP2X_DENOISE0X","Waifu2x", "", "310%"),
            ("CUNET_UP2X_DENOISE1X","Waifu2x", "", "310%"),
            ("CUNET_UP2X_DENOISE2X","Waifu2x", "", "310%"),
            ("CUNET_UP2X_DENOISE3X","Waifu2x", "推荐使用", "310%"),
            ("ANIME_UP2X","Waifu2x", "", "200%"),
            ("ANIME_UP2X_DENOISE0X","Waifu2x", "", "210%"),
            ("ANIME_UP2X_DENOISE1X","Waifu2x", "", "210%"),
            ("ANIME_UP2X_DENOISE2X","Waifu2x", "", "210%"),
            ("ANIME_UP2X_DENOISE3X","Waifu2x", "推荐使用", "210%"),
            ("PHOTO_UP2X","Waifu2x", "", "180%"),
            ("PHOTO_UP2X_DENOISE0X","Waifu2x", "", "200%"),
            ("PHOTO_UP2X_DENOISE1X","Waifu2x", "", "200%"),
            ("PHOTO_UP2X_DENOISE2X","Waifu2x", "", "200%"),
            ("PHOTO_UP2X_DENOISE3X","Waifu2x", "推荐使用", "200%"),
            ("PRO_UP2X","Real-CUGAN", "", "350%"),
            ("PRO_UP2X_CONSERVATIVE","Real-CUGAN", "", "350%"),
            ("PRO_UP2X_DENOISE3X","Real-CUGAN", "推荐使用", "350%"),
            ("PRO_UP3X","Real-CUGAN", "", "500%"),
            ("PRO_UP3X_CONSERVATIVE","Real-CUGAN", "", "500%"),
            ("PRO_UP3X_DENOISE3X","Real-CUGAN", "", "500%"),
            ("SE_UP2X","Real-CUGAN", "", "300%"),
            ("SE_UP2X_CONSERVATIVE","Real-CUGAN", "", "300%"),
            ("SE_UP2X_DENOISE1X","Real-CUGAN", "", "300%"),
            ("SE_UP2X_DENOISE2X","Real-CUGAN", "", "300%"),
            ("SE_UP2X_DENOISE3X","Real-CUGAN", "推荐使用", "300%"),
            ("SE_UP3X","Real-CUGAN", "", "500%"),
            ("SE_UP3X_CONSERVATIVE","Real-CUGAN", "", "500%"),
            ("SE_UP3X_DENOISE3X","Real-CUGAN", "", "500%"),
            ("SE_UP4X","Real-CUGAN", "", "400%"),
            ("SE_UP4X_CONSERVATIVE","Real-CUGAN", "", "400%"),
            ("SE_UP4X_DENOISE3X","Real-CUGAN", "", "400%"),
            ("ANIMAVIDEOV3_UP2X","Real-ESRGAN", "推荐使用", "200%"),
            ("ANIMAVIDEOV3_UP3X","Real-ESRGAN", "", "300%"),
            ("ANIMAVIDEOV3_UP4X","Real-ESRGAN", "", "400%"),
            ("X4PLUS_UP4X","Real-ESRGAN", "", "600%"),
            ("X4PLUSANIME_UP4X", "Real-ESRGAN", "", "400%"),
        ]
        for v in AllModelNames:
            rowCont = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCont)
            self.tableWidget.setItem(rowCont, 0, QTableWidgetItem(v[0]))
            self.tableWidget.setItem(rowCont, 1, QTableWidgetItem(v[1]))
            self.tableWidget.setItem(rowCont, 2, QTableWidgetItem(v[3]))
            self.tableWidget.setItem(rowCont, 3, QTableWidgetItem(v[2]))
        pass