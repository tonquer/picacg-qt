import sys

from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel

from component.widget.frame_less_widget import FrameLessWidget

app = QApplication(sys.argv)
w = FrameLessWidget()
w.resize(200, 200)
w.move(700, 700)
h = QHBoxLayout(w)
l = QLabel("test")
h.addWidget(l)
w.show()


# 创建主界面

sys.exit(app.exec())
