


import sys

from PySide6.QtWidgets import QApplication

from component.widget.navigation_widget import NavigationWidget

app = QApplication(sys.argv)
# 创建主界面
main = NavigationWidget()
main.show()
sys.exit(app.exec())
