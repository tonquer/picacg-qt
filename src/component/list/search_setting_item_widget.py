from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from component.button.switch_button import SwitchButton


class SearchSettingItemWidget(QWidget):
    def __init__(self, parent=None, text="", state=True):
        QWidget.__init__(self, parent)
        self.horizontalLayout = QHBoxLayout(self)
        self.label = QLabel(text)
        self.horizontalLayout.addWidget(self.label)
        self.switchButton = SwitchButton(state=state)
        self.horizontalLayout.addWidget(self.switchButton)
