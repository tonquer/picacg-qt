import itertools

from PySide6.QtCore import Qt, QTimer, QThread, Signal, QPoint
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGridLayout, QFrame
)
from collections import deque
from config.setting import Setting

# 统计窗口：延迟/丢包都只按最近 N 条探测记录计算
HISTORY_SIZE = 100

# 两套主题的调色板定义
THEMES = {
    "dark": {
        "container_bg": "#111317",
        "container_border": "#282c37",
        "title_color": "#64748b",
        "btn_hover": "#334155",
        "tile_bg": "#1a1d24",
        "tile_border": "#282c37",
        "tile_hover_bg": "#222631",
        "tile_hover_border": "#3b82f6",
        "name_color": "#F3F3F3",
        "loss_normal": "#64748b",
        "ping_default": "#94a3b8",
        # 状态颜色
        "status_good": "#22c55e",
        "status_fair": "#eab308",
        "status_poor": "#f97316",
        "status_down": "#ef4444",
        "status_init": "#4b5563"
    },
    "light": {
        "container_bg": "#f8fafc",
        "container_border": "#cbd5e1",
        "title_color": "#64748b",
        "btn_hover": "#e2e8f0",
        "tile_bg": "#ffffff",
        "tile_border": "#e2e8f0",
        "tile_hover_bg": "#f1f5f9",
        "tile_hover_border": "#3b82f6",
        "name_color": "#31363B",
        "loss_normal": "#94a3b8",
        "ping_default": "#64748b",
        # 状态颜色
        "status_good": "#16a34a",
        "status_fair": "#ca8a04",
        "status_poor": "#ea580c",
        "status_down": "#dc2626",
        "status_init": "#94a3b8"
    }
}

def format_traffic(num_bytes, compact=True):
    """把字节数格式化成自适应单位的字符串。

    compact=True 用 B/K/M/G/T/P 这种短单位（磁贴内展示），
    compact=False 用 B/KB/MB/GB/TB/PB（提示框里展示完整单位）。
    """
    if num_bytes is None:
        return "--"

    units = ("B", "K", "M", "G", "T", "P") if compact else ("B", "KB", "MB", "GB", "TB", "PB")
    value = float(num_bytes)
    index = 0
    while value >= 1023.5 and index < len(units) - 1:
        value /= 1024
        index += 1
    # 提前进位，避免出现 1000K 这类 5 字符
    if value >= 999.5 and index < len(units) - 1:
        value /= 1024
        index += 1

    if index == 0:
        return f"{int(value)}B" if compact else f"{int(value)} B"
    if not compact:
        return f"{value:.2f} {units[index]}"
    # 磁贴空间有限：最多保留 3 位有效数字、4 个字符
    if value >= 9.95:
        return f"{value:.0f}{units[index]}"
    return f"{value:.1f}{units[index]}"


# 微型节点磁贴
class MiniNodeTileFrame(QFrame):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.name = ""
        self.host = ""
        # 最近 N 次探测结果：>=0 为延迟毫秒，-1 为超时/丢包
        self.history = deque(maxlen=HISTORY_SIZE)
        # 累计总流量（字节），由外部通过 set_traffic() 注入；None 表示暂无数据
        self.traffic_total = None
        self.current_theme = "light"

        # self.setFixedSize(82, 42)
        # self.setToolTip(f"{name}\n{host}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 3, 4, 3)
        layout.setSpacing(1)

        # 1. 顶部：圆点 + 节点名
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(4)

        self.dot = QLabel()
        # self.dot.setFixedSize(6, 6)

        self.lbl_name = QLabel()
        self.lbl_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        top_layout.addWidget(self.dot)
        top_layout.addWidget(self.lbl_name, 1)
        layout.addLayout(top_layout)

        # 2. 底部：延迟(左) + 总流量(中) + 丢包(右)
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(2)

        self.lbl_ping = QLabel("--")
        self.lbl_traffic = QLabel("--")
        self.lbl_traffic.setAlignment(Qt.AlignCenter)
        self.lbl_loss = QLabel("0% loss")
        self.lbl_loss.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        bottom_layout.addWidget(self.lbl_ping)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.lbl_traffic)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.lbl_loss)
        layout.addLayout(bottom_layout)
        self.apply_theme(self.current_theme)

    def setText(self, text):
        if text != self.lbl_name.text():
            self.reset_stats()
        self.lbl_name.setText(text)

    def update_theme(self):
        if Setting.ThemeIndex.autoValue == 1:
            self.apply_theme("dark")
        else:
            self.apply_theme("light")
        return

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        palette = THEMES[theme_name]

        self.setStyleSheet(f"""
            MiniNodeTile {{
                background-color: {palette["tile_bg"]};
                border: 1px solid {palette["tile_border"]};
                border-radius: 5px;
            }}
            MiniNodeTile:hover {{
                background-color: {palette["tile_hover_bg"]};
                border-color: {palette["tile_hover_border"]};
            }}
        """)
        self.lbl_name.setStyleSheet(f"color: {palette['name_color']}; font-size: 11px; font-weight: bold;")
        self.refresh_display()

    def update_result(self, latency):
        """记录一次探测结果（>=0 为延迟毫秒，-1 为超时）。

        这里只写数据、不刷新界面；界面由 UltraCompactMonitor 的刷新
        定时器统一调用 refresh_display() 重绘，避免每个结果都触发重绘。
        """
        self.history.append(latency)

    def reset_stats(self):
        """清空统计窗口，回到未测试状态。"""
        self.history.clear()
        self.traffic_total = None
        self.refresh_display()

    def add_traffic(self, total_bytes):
        """外部注入累计总流量（字节）。

        只更新数据，不触发重绘；界面由 2 秒刷新定时器统一重绘。
        传 None 表示暂无数据（显示 --）。
        """
        if not self.traffic_total:
            self.traffic_total = 0
        self.traffic_total += max(0, int(total_bytes))

    def valid_samples(self):
        return [v for v in self.history if v >= 0]

    def average_latency(self):
        samples = self.valid_samples()
        return sum(samples) / len(samples) if samples else None

    def loss_rate(self):
        if not self.history:
            return 0.0
        return sum(1 for v in self.history if v < 0) / len(self.history) * 100

    def refresh_display(self):
        palette = THEMES[self.current_theme]
        avg = self.average_latency()
        loss_rate = self.loss_rate()
        samples = self.valid_samples()

        # 未开始测试 / 刚清空
        if not self.history:
            self.dot.setStyleSheet(f"background-color: {palette['status_init']}; border-radius: 3px;")
            self.lbl_ping.setText("--")
            self.lbl_ping.setStyleSheet(f"color: {palette['ping_default']}; font-size: 10px; font-family: Consolas;")
        # 窗口内全部丢包/超时
        elif avg is None:
            self.dot.setStyleSheet(f"background-color: {palette['status_down']}; border-radius: 3px;")
            self.lbl_ping.setText("超时")
            self.lbl_ping.setStyleSheet(f"color: {palette['status_down']}; font-size: 10px; font-weight: bold;")
        # 最近 N 条的平均延迟
        else:
            self.lbl_ping.setText(f"{avg:.0f}ms")
            if avg < 60:
                color = palette['status_good']
            elif avg < 150:
                color = palette['status_fair']
            else:
                color = palette['status_poor']

            self.dot.setStyleSheet(f"background-color: {color}; border-radius: 3px;")
            self.lbl_ping.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: bold; font-family: Consolas;")

        # 丢包率（同样按最近 N 条统计）
        if loss_rate == 0:
            self.lbl_loss.setText("0% loss")
            self.lbl_loss.setStyleSheet(f"color: {palette['loss_normal']}; font-size: 9px; font-family: Consolas;")
        else:
            self.lbl_loss.setText(f"{loss_rate:.0f}% loss")
            self.lbl_loss.setStyleSheet(
                f"color: {palette['status_down']}; font-size: 9px; font-weight: bold; font-family: Consolas;")

        # 总流量（外部注入，单位自适应；只做数据展示，不参与延迟/丢包计算）
        self.lbl_traffic.setText(format_traffic(self.traffic_total))
        self.lbl_traffic.setStyleSheet(f"color: {palette['ping_default']}; font-size: 8px; font-family: Consolas;")

        self._update_tooltip(avg, samples, loss_rate)

    def _update_tooltip(self, avg, samples, loss_rate):
        lines = [self.name, self.host]
        if not self.history:
            lines.append(f"样本: 0/{HISTORY_SIZE}（未开始）")
        else:
            lines.append(f"样本: {len(self.history)}/{HISTORY_SIZE}  丢包: {loss_rate:.0f}% loss")
            if samples:
                lines.append(f"平均: {avg:.1f}ms  最低: {min(samples):.0f}ms  最高: {max(samples):.0f}ms")
            lines.append("最近: " + "  ".join("超时" if v < 0 else f"{v:.0f}ms" for v in itertools.islice(self.history, 1, 10)))

        if self.traffic_total is None:
            lines.append("总流量: --（等待外部数据）")
        else:
            lines.append(f"总流量: {format_traffic(self.traffic_total, compact=False)}（{self.traffic_total:,} 字节）")

        self.setToolTip("\n".join(lines))


    def mousePressEvent(self, event):
        QFrame.mousePressEvent(self, event)
        self.clicked.emit()
