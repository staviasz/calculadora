import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from mainWindow import MainWindow
from display import Display
from infoLabel import Info
from buttons import ButtonGrid
from consts import WINDOW_ICON_PATH
from styles import setupTheme

if __name__ == "__main__":
    # Criando aplicação
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    # Definição de icone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info Label
    info = Info("2 + 2 = 4")
    window.addWidgetVLayout(info)

    # Display
    display = Display()
    window.addWidgetVLayout(display)

    # GridButton
    buttonGrid = ButtonGrid(display)
    window.vLayout.addLayout(buttonGrid)

    # Executando
    window.adjustFixedSize()
    window.show()
    app.exec()
