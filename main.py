import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styles.dark_theme import DARK_THEME


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet(DARK_THEME)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
