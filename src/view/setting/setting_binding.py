from dataclasses import dataclass
from typing import Callable, Optional

from PySide6.QtCore import QObject

from config.setting import SettingValue


@dataclass(frozen=True)
class SettingBinding:
    """在同一条记录中声明设置控件的读取、回填和生效回调。"""

    setting: SettingValue
    control: QObject
    signal: object
    read: Callable[[], object]
    write: Callable[[object], None]
    after_save: Optional[Callable[[], None]] = None


def BindCheck(setting, control):
    return SettingBinding(setting, control, control.clicked,
                          lambda: int(control.isChecked()),
                          lambda value: control.setChecked(bool(value)))


def BindRadio(setting, group, buttons, after_save=None):
    for value, button in enumerate(buttons):
        group.setId(button, value)

    def write(value):
        button = group.button(value)
        if button is not None:
            button.setChecked(True)

    return SettingBinding(setting, group, group.idClicked,
                          group.checkedId, write, after_save)


def BindLine(setting, control):
    return SettingBinding(setting, control, control.editingFinished,
                          control.text, control.setText)


def BindIndex(setting, control, write=None):
    return SettingBinding(setting, control, control.currentIndexChanged,
                          control.currentIndex, write or control.setCurrentIndex)


def BindValue(setting, control, write):
    return SettingBinding(setting, control, control.currentIndexChanged,
                          lambda: control.currentData() if control.currentIndex() >= 0 else None,
                          write)


def BindSpin(setting, control, converter=int):
    return SettingBinding(setting, control, control.valueChanged,
                          lambda: converter(control.value()), control.setValue)
