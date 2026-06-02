import sys
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.styles.dark_theme import DARK_THEME


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
