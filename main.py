import sys
from PyQt6.QtWidgets import QApplication  # Главный класс приложения, управляет циклом событий

from ui.main_window import MainWindow  # Класс главного окна


def main():
    app = QApplication(sys.argv)  # Создаёт объект приложения (обязательный шаг)

    window = MainWindow()  # Создаёт экземпляр главного окна
    window.show()  # Отображает окно на экране

    sys.exit(app.exec())  # Запускает главный цикл обработки событий


if __name__ == "__main__":
    main()
