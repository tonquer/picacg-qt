import copy
import os
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import ExitStack
from unittest.mock import Mock, patch


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtCore import QSettings, QTranslator
from PySide6.QtWidgets import QApplication

from config import config
from config.setting import Setting, SettingValue
from view.setting import setting_view
from view.setting.setting_view import SettingView


class SettingValueTests(unittest.TestCase):
    def test_false_values_are_not_replaced_by_defaults(self):
        cases = ((0, 1, 0), (False, True, False), (0.0, 2.0, 0.0),
                 ("", "原默认值", ""), ([], ["原默认值"], []),
                 ({}, {"原键": 1}, {}), (None, 7, 7))
        for value, default, expected in cases:
            with self.subTest(value=value, default=default):
                actual = SettingValue.GetSettingV(value, default)
                self.assertEqual(expected, actual)
                self.assertIs(type(expected), type(actual))

    def test_qsettings_strings_and_invalid_numbers(self):
        cases = (("false", True, False), ("True", False, True),
                 ("false", 1, 0), ("0", 1, 0), ("1.5", 2.0, 1.5),
                 ("单项", [], ["单项"]), ("", [], []))
        for value, default, expected in cases:
            with self.subTest(value=value, default=default):
                self.assertEqual(expected, SettingValue.GetSettingV(value, default))
        with patch.object(setting_view.Log, "Error") as error:
            self.assertEqual(3, SettingValue.GetSettingV("损坏值", 3))
            self.assertEqual(2.5, SettingValue.GetSettingV("损坏值", 2.5))
            self.assertEqual(2, error.call_count)

    def test_real_ini_round_trip_and_restart_semantics(self):
        cases = ((1, 0, False), (True, False, False), (2.0, 1.5, False),
                 ("旧值", "", True), (0, 3, True))
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(Setting, "GetConfigPath", return_value=directory):
                for index, (default, selected, restart) in enumerate(cases):
                    with self.subTest(default=default, selected=selected):
                        name = f"Item{index}"
                        item = SettingValue("测试", default, restart)
                        item.InitValue(default, name)
                        item.SetValue(selected)
                        self.assertEqual(selected, item.setV)
                        self.assertEqual(default if restart else selected, item.value)
                        stored = QSettings(str(Path(directory) / "config.ini"), QSettings.IniFormat)
                        stored.sync()
                        loaded = SettingValue("测试", default, restart)
                        loaded.InitValue(stored.value(f"测试/{name}"), name)
                        self.assertEqual(selected, loaded.value)
                        self.assertEqual(selected, loaded.setV)


class DefaultLabelTranslator(QTranslator):
    def __init__(self, label):
        super().__init__()
        self.label = label

    def isEmpty(self):
        return False

    def translate(self, context, sourceText, disambiguation=None, n=-1):
        return self.label if sourceText == "默认" else ""


class SettingViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.saved_settings = []
        for name in dir(Setting):
            item = getattr(Setting, name)
            if isinstance(item, SettingValue):
                self.saved_settings.append((item, copy.deepcopy(item.__dict__)))
                item.InitValue(copy.deepcopy(item.defaultV), name)
        self.addCleanup(self.restore_settings)
        self.saved_config = (config.Encode, config.EncodeGpu, config.UseCpuNum)
        self.addCleanup(self.restore_config)
        self.owner = Mock()
        self.owner.app = self.app
        self.stack.enter_context(patch.object(setting_view, "QtOwner", return_value=self.owner))
        self.save = self.stack.enter_context(patch.object(Setting, "SaveSettingV"))
        self.stack.enter_context(patch.object(setting_view.Log, "Warn"))
        self.view = SettingView()
        self.addCleanup(self.delete_view)
        self.view.SetTheme = Mock()
        self.view.SetLanguage = Mock()
        self.log_level = self.stack.enter_context(patch.object(setting_view.Log, "UpdateLoggingLevel"))
        self.view.InitSetting()
        self.view.SetGpuInfos(["测试 GPU A", "测试 GPU B"], 4)
        self.view.fontBox.addItem("测试字体", "测试字体")
        self.save.assert_not_called()
        self.owner.ShowMsgOne.assert_not_called()
        self.owner.ShowErrOne.assert_not_called()

    def restore_settings(self):
        for item, state in self.saved_settings:
            item.__dict__.clear()
            item.__dict__.update(state)

    def restore_config(self):
        config.Encode, config.EncodeGpu, config.UseCpuNum = self.saved_config

    def delete_view(self):
        self.view.close()
        self.view.deleteLater()
        self.app.processEvents()

    def assert_refresh_preserves(self, item, selected, active, read):
        self.save.reset_mock()
        self.owner.reset_mock()
        for refresh in (self.view.InitSetting, self.view.SwitchCurrent,
                        lambda: self.view.retranslateUi(self.view)):
            refresh()
            self.assertEqual(selected, item.setV)
            self.assertEqual(active, item.value)
            self.assertEqual(selected, read())
        self.save.assert_not_called()
        self.owner.ShowMsgOne.assert_not_called()
        self.owner.ShowErrOne.assert_not_called()

    def test_checkboxes_keep_pending_values_on_reentry(self):
        controls = (
            ("mainScaleBox", "IsUseScaleFactor"), ("checkBox_IsUpdate", "IsUpdate"),
            ("chatProxy", "ChatProxy"), ("readCheckBox", "IsOpenWaifu"),
            ("preDownWaifu2x", "PreDownWaifu2x"), ("coverCheckBox", "CoverIsOpenWaifu"),
            ("downAuto", "DownloadAuto"), ("openglBox", "IsOpenOpenGL"),
            ("crossChapterPrefetch", "CrossChapterPrefetch"),
            ("prefetchWholeChapter", "PrefetchWholeChapter"), ("grabGestureBox", "IsGrabGesture"))
        for control_name, setting_name in controls:
            with self.subTest(control=control_name):
                item = getattr(Setting, setting_name)
                item.InitValue(0, setting_name)
                self.view.InitSetting()
                control = getattr(self.view, control_name)
                self.save.reset_mock()
                control.click()
                self.assertEqual(1, item.setV)
                self.assertIs(int, type(item.setV))
                self.save.assert_called_once_with(item)
                self.assert_refresh_preserves(item, 1, 0 if item.isNeedReset else 1,
                                              lambda: int(control.isChecked()))

    def test_numeric_controls_preserve_types_and_loaded_limits(self):
        controls = (
            ("scaleBox", "ScaleFactor", 150), ("coverSize", "CoverSize", 150),
            ("categorySize", "CategorySize", 120), ("lookMaxBox", "LookMaxNum", 1024),
            ("coverMaxBox", "CoverMaxNum", 800), ("prefetchCount", "PicturePrefetchCount", 8),
            ("prefetchFrontCount", "PicturePrefetchFrontCount", 4),
            ("showCount", "PictureShowCount", 6), ("showFrontCount", "PictureShowFrontCount", 3),
            ("readScale", "LookScale", 1.5), ("coverScale", "CoverLookScale", 2.7),
            ("downScale", "DownloadScale", 1.5))
        for control_name, setting_name, selected in controls:
            with self.subTest(control=control_name):
                item = getattr(Setting, setting_name)
                active = item.value
                control = getattr(self.view, control_name)
                self.save.reset_mock()
                control.setValue(selected)
                self.assertEqual(selected, item.setV)
                self.assertIs(type(selected), type(item.setV))
                self.save.assert_called_once_with(item)
                self.assert_refresh_preserves(item, selected, active if item.isNeedReset else selected,
                                              control.value)

    def test_combo_boxes_keep_wire_values_and_pending_choices(self):
        controls = (
            ("coverLvBox", "DownloadCoverLv", 3, 3),
            ("threadSelect", "Waifu2xCpuCore", 3, 3),
            ("titleLineBox", "TitleLine", 4, 4),
            ("categoryBox", "NotCategoryShow", 1, 1),
            ("fontStyle", "FontStyle", 4, 4),
            ("tileComboBox", "Waifu2xTileSize", 1, 1),
            ("encodeSelect", "SelectEncodeGpu", 1, "测试 GPU B"),
            ("fontBox", "FontName", self.view.fontBox.findData("测试字体"), "测试字体"),
            ("fontSize", "FontSize", 3, "14"))
        for control_name, setting_name, index, selected in controls:
            with self.subTest(control=control_name):
                item = getattr(Setting, setting_name)
                active = item.value
                control = getattr(self.view, control_name)
                self.save.reset_mock()
                control.setCurrentIndex(index)
                self.assertEqual(selected, item.setV)
                self.assertIs(type(selected), type(item.setV))
                self.save.assert_called_once_with(item)
                read = control.currentData if isinstance(selected, str) else control.currentIndex
                self.assert_refresh_preserves(item, selected, active if item.isNeedReset else selected, read)
        self.view.threadSelect.setCurrentIndex(0)
        self.assertEqual(0, Setting.Waifu2xCpuCore.setV)
        self.assertEqual(200, Setting.Waifu2xTileSize.GetIndexV())

    def test_radio_buttons_save_ids_and_only_apply_their_effect(self):
        controls = (("themeButton2", "ThemeIndex", 2, "theme"),
                    ("languageButton3", "Language", 3, "language"),
                    ("logutton2", "LogIndex", 2, "log"),
                    ("proxy3", "IsHttpProxy", 3, None),
                    ("saveNameButton2", "SaveNameType", 2, None),
                    ("showCloseButton1", "ShowCloseType", 1, None))
        callbacks = {"theme": self.view.SetTheme, "language": self.view.SetLanguage,
                     "log": self.log_level}
        for control_name, setting_name, selected, effect in controls:
            with self.subTest(control=control_name):
                for callback in callbacks.values():
                    callback.reset_mock()
                self.save.reset_mock()
                control = getattr(self.view, control_name)
                control.click()
                item = getattr(Setting, setting_name)
                self.assertEqual(selected, item.value)
                self.save.assert_called_once_with(item)
                self.assert_refresh_preserves(item, selected, selected,
                                              lambda: selected if control.isChecked() else None)
                for name, callback in callbacks.items():
                    self.assertEqual(int(name == effect), callback.call_count)

    def test_proxy_lines_save_when_editing_finishes(self):
        for control_name, setting_name in (("httpEdit", "HttpProxy"), ("sockEdit", "Sock5Proxy")):
            with self.subTest(control=control_name):
                control = getattr(self.view, control_name)
                item = getattr(Setting, setting_name)
                self.save.reset_mock()
                control.setText("http://127.0.0.1:7890")
                self.save.assert_not_called()
                control.editingFinished.emit()
                self.save.assert_called_once_with(item)
                self.assert_refresh_preserves(item, control.text(), control.text(), control.text)

    def test_default_font_values_are_independent_of_translated_labels(self):
        for label in ("默认", "默認", "Default"):
            with self.subTest(label=label):
                translator = DefaultLabelTranslator(label)
                self.app.installTranslator(translator)
                try:
                    self.save.reset_mock()
                    self.owner.reset_mock()
                    self.view.retranslateUi(self.view)
                    self.save.assert_not_called()
                    self.owner.ShowMsgOne.assert_not_called()
                    self.owner.ShowErrOne.assert_not_called()
                    self.assertEqual(label, self.view.fontBox.itemText(0))
                    self.assertEqual(label, self.view.fontSize.itemText(0))
                    for control_name, setting_name in (("fontBox", "FontName"), ("fontSize", "FontSize")):
                        control = getattr(self.view, control_name)
                        item = getattr(Setting, setting_name)
                        control.setCurrentIndex(1)
                        control.setCurrentIndex(0)
                        self.assertEqual("", item.setV)
                        item.InitValue(label, setting_name)
                        self.save.reset_mock()
                        self.view.InitSetting()
                        self.assertEqual(0, control.currentIndex())
                        self.assertEqual(label, item.setV)
                        self.save.assert_not_called()
                finally:
                    self.app.removeTranslator(translator)

    def test_hardware_fallback_does_not_overwrite_preferences(self):
        cases = (([], "已移除 GPU", 8, "CPU", -1, 4),
                 (["测试 GPU A"], "已移除 GPU", 8, "测试 GPU A", 0, 4),
                 (["测试 GPU A"], "CPU", 0, "CPU", -1, 0))
        for gpu_list, preferred, cores, actual, index, actual_cores in cases:
            with self.subTest(gpus=gpu_list, preferred=preferred):
                Setting.SelectEncodeGpu.InitValue(preferred, "SelectEncodeGpu")
                Setting.Waifu2xCpuCore.InitValue(cores, "Waifu2xCpuCore")
                self.save.reset_mock()
                self.view.SetGpuInfos(gpu_list, 4)
                self.view.InitSetting()
                self.assertEqual((actual, index, actual_cores),
                                 (config.EncodeGpu, config.Encode, config.UseCpuNum))
                self.assertEqual(actual, self.view.encodeSelect.currentData())
                self.assertEqual(actual_cores, self.view.threadSelect.currentIndex())
                self.assertEqual(preferred, Setting.SelectEncodeGpu.setV)
                self.assertEqual(cores, Setting.Waifu2xCpuCore.setV)
                self.save.assert_not_called()
        Setting.SelectEncodeGpu.InitValue("测试 GPU A", "SelectEncodeGpu")
        Setting.SelectEncodeGpu.SetValue("测试 GPU B")
        self.save.reset_mock()
        self.view.SetGpuInfos(["测试 GPU A", "测试 GPU B"], 4)
        self.assertEqual("测试 GPU A", config.EncodeGpu)
        self.assertEqual("测试 GPU B", self.view.encodeSelect.currentData())
        self.save.assert_not_called()

    def test_model_selection_updates_only_the_selected_model(self):
        for control_name, setting_name in (("readModelName", "LookModelName"),
                                           ("coverModelName", "CoverLookModelName"),
                                           ("downModelName", "DownloadModelName")):
            with self.subTest(control=control_name):
                item = getattr(Setting, setting_name)
                control = getattr(self.view, control_name)
                self.save.reset_mock()
                control.click()
                self.save.assert_not_called()
                selected, callback = self.owner.OpenSrSelectModel.call_args.args
                self.assertEqual(item.setV, selected)
                callback("MODEL_WAIFU2X_CUNET_UP2X")
                self.save.assert_called_once_with(item)
                self.assert_refresh_preserves(item, "MODEL_WAIFU2X_CUNET_UP2X",
                                              "MODEL_WAIFU2X_CUNET_UP2X", control.text)


if __name__ == "__main__":
    unittest.main()
