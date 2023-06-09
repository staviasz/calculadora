import math
from PySide6.QtWidgets import QPushButton, QGridLayout, QMessageBox

from consts import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber
from display import Display
from infoLabel import Info


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        # self.setStyleSheet(f"font-size: {MEDIUM_FONT_SIZE}px;") #evite escrever dessa forma pois pode sobrescrever um estilo anterior
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ["C", "◀", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]
        self.display = display
        self.info = info
        self._equation = ""
        self._left = None
        self._right = None
        self._operator = None
        self.msgBox = QMessageBox()
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._insertOperator)
        self.display.negativePressed.connect(self._negativeNumber)

        buttonsAdd = []
        for row, buttonData in enumerate(self._gridMask):
            for column, buttonText in enumerate(buttonData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)

                buttonsAdd.append(buttonText)
                if "0" in buttonsAdd:
                    if buttonsAdd[-1] == "0":
                        self.addWidget(button, row, column, 1, 2)
                    else:
                        column += 1
                        self.addWidget(button, row, column)
                else:
                    self.addWidget(button, row, column)

                self._connectButtonClicked(self._insertToDisplay, button)

    def _connectButtonClicked(self, function, button):
        button.clicked.connect(function)

    def _configSpecialButton(self, button):
        specialButton = button.text()
        if specialButton == "C":
            self._connectButtonClicked(self._clear, button)
        if specialButton in "+*/^":
            self._connectButtonClicked(self._insertOperator, button)
        if specialButton == "=":
            self._connectButtonClicked(self._eq, button)
        if specialButton == "◀":
            self._connectButtonClicked(self.display.backspace, button)
        if specialButton == "-":
            self._connectButtonClicked(self._negativeNumber, button)

    def _insertToDisplay(self, *args):
        if len(args) > 0:
            text = args[0]
        else:
            text = self.sender().text()

        newDisplayValue = self.display.text() + text
        negativeNumber = self._left is None and text == "-"
        if not isValidNumber(newDisplayValue) and not negativeNumber:
            return
        self.display.insert(text)
        self.display.setFocus()

    def _clear(self):
        self._left = None
        self._right = None
        self._operator = None
        self.equation = None
        self.display.clear()

    def _insertOperator(self, *args):
        if len(args) > 0:
            text = args[0]
        else:
            text = self.sender().text()
        displayText = self.display.text()

        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError("Número inválido")
            return

        if self._left is None:
            self._left = float(displayText)

        self._operator = text
        self.equation = f"{self._left} {self._operator} ??"
        self.display.setFocus()

    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showError("Você não digitou nada")
            return
        if self._left is None:
            return

        self._right = float(displayText)
        self.equation = f"{self._left} {self._operator} {self._right}"
        result = "error"
        try:
            if "^" in self.equation and self._left is not None:
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError("Não é possível dividir por zero")
        except OverflowError:
            self._showError("Número muito grande")

        self.display.clear()
        self.info.setText(f"{self.equation} = {result}")
        self._left = result
        self._right = None

        if result == "error":
            self._left = None

    def _showError(self, text):
        self.msgBox.setText(text)
        self.msgBox.exec()

    def _negativeNumber(self, *args):
        displayText = self.display.text()
        length = len(displayText)
        if self._left is None and "-" not in displayText and length == 0:
            self._insertToDisplay("-") if len(args) > 0 else self._insertToDisplay
        else:
            self._insertOperator("-")
