from PySide6.QtWidgets import QPushButton, QGridLayout

from consts import MEDIUM_FONT_SIZE
from utils import isEmpty, isNumOrDot
from display import Display


class Button(QPushButton):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        # self.setStyleSheet(f"font-size: {MEDIUM_FONT_SIZE}px")  (fazendo dessa forma corre o risco de sobrescrever o style anterior)
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonGrid(QGridLayout):
    def __init__(self, display: Display, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._gridMask = [
            ["C", "<", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]

        self.display = display
        self._makeGrid()

    def _makeGrid(self):
        buttonsAdd = []
        for row, buttonData in enumerate(self._gridMask):
            for column, buttonText in enumerate(buttonData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")

                buttonsAdd.append(buttonText)
                if "0" in buttonsAdd:
                    if buttonsAdd[-1] == "0":
                        self.addWidget(button, row, column, 1, 2)
                    else:
                        column += 1
                        self.addWidget(button, row, column)
                else:
                    self.addWidget(button, row, column)

                button.clicked.connect(self._insertButtonTextToDisplay)

    def _insertButtonTextToDisplay(self):
        buttunText = self.sender().text()
        self.display.insert(buttunText)
