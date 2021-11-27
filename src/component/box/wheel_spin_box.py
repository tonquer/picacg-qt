from PySide6.QtWidgets import QSpinBox


class WheelSpinBox(QSpinBox):
    def __init__(self, parent=None):
        QSpinBox.__init__(self, parent)

    def wheelEvent(self, event):
        event.ignore()

