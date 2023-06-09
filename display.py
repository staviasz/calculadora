from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent

from consts import BIG_FONT_SIZE, MARGIN_DEFAULT
from utils import isEmpty, isNumOrDot


class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    negativePressed = Signal(str)
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        margins = [MARGIN_DEFAULT for _ in range(4)]
        self.setStyleSheet(f"font-size: { BIG_FONT_SIZE}px")
        self.setMinimumHeight(BIG_FONT_SIZE * 1.5)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        keyText = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isClear = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [
            KEYS.Key_Plus,
            KEYS.Key_Slash,
            KEYS.Key_Asterisk,
            KEYS.Key_P,
        ]
        isNegative = key in [KEYS.Key_Minus]

        if isEnter:
            self.eqPressed.emit()
            return event.ignore()
        if isDelete:
            self.delPressed.emit()
            return event.ignore()
        if isClear:
            self.clearPressed.emit()
            return event.ignore()
        if isOperator:
            if keyText.lower() == "p":
                keyText = "^"
            self.operatorPressed.emit(keyText)
            return event.ignore()
        if isNegative:
            self.negativePressed.emit(keyText)
            return event.ignore()
        if isEmpty(keyText):
            return event.ignore()

        if isNumOrDot(keyText):
            self.inputPressed.emit(keyText)
            return event.ignore()
