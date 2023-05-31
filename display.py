from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt

from consts import BIG_FONT_SIZE, MARGIN_DEFAULT


class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        margins = [MARGIN_DEFAULT for _ in range(4)]
        self.setStyleSheet(f"font-size: { BIG_FONT_SIZE}px")
        self.setMinimumHeight(BIG_FONT_SIZE * 1.5)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)
