from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel


class TypeWriterLabel(QLabel):  # Виджет с анимацией печати текста
    def __init__(self, text="", speed=30):  # Принимает текст и скорость печати
        super().__init__()

        self.full_text = text
        self.current_text = ""
        self.index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)

        self.speed = speed

    def start(self):  # Запускает анимацию печати
        self.current_text = ""
        self.index = 0
        self.timer.start(self.speed)

    def update_text(self):  # Добавляет один символ за тик таймера
        if self.index < len(self.full_text):
            self.current_text += self.full_text[self.index]
            self.setText(self.current_text)
            self.index += 1
        else:
            self.timer.stop()
