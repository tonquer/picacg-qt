from PySide6.QtWidgets import QComboBox


class WheelComboBox(QComboBox):
    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)

    def wheelEvent(self, event):
        event.ignore()

