import sys

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QWidget

app = QApplication(sys.argv)
w = QWidget()
w.resize(200, 200)
w.move(700, 700)
h = QHBoxLayout(w)
l = QLabel("test")
p = QPixmap(QImage("1.jpg"))
p.scaled()
l.setPixmap(p)
h.addWidget(l)
w.show()


# 创建主界面

sys.exit(app.exec())
