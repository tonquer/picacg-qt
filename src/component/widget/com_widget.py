from enum import Enum

from PySide6.QtCore import QPointF


class MoveEnum(Enum):
    LEFT_TOP = 11
    TOP = 12
    RIGHT_TOP = 13
    LEFT = 21
    CENTER = 22
    RIGHT = 23
    LEFT_BOTTOM = 31
    BOTTOM = 32
    RIGHT_BOTTOM = 33


class ComWidget:

    @staticmethod
    def moveArea(width, height, pos: QPointF):
        BORDER_WIDTH = 10
        if pos.y() < BORDER_WIDTH:
            k = 10
        elif pos.y() > height - BORDER_WIDTH:
            k = 30
        else:
            k = 20

        if pos.x() < BORDER_WIDTH:
            v = 1
        elif pos.x() > width - BORDER_WIDTH:
            v = 3
        else:
            v = 2

        return k + v