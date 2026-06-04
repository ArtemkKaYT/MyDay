"""
Модуль для создания метки с эффектом печатающейся машинки (TypeWriter).

Этот модуль содержит TypeWriterLabel - кастомный виджет метки,
который отображает текст с эффектом печатания символ за символом.

Пример:
    Использование TypeWriterLabel::

        from ui.widgets.type_writer_label import TypeWriterLabel

        label = TypeWriterLabel("Привет, мир!", speed=30)
        label.show()
        label.start()  # Запустить анимацию печати
"""

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel


class TypeWriterLabel(QLabel):
    """
    Метка с эффектом печатания текста.

    Этот класс создаёт QLabel, который выводит текст с эффектом
    печатающейся машинки, добавляя по одному символу на каждый тик таймера.

    Атрибуты:
        full_text (str): Полный текст для отображения
        current_text (str): Текущий выводимый текст
        index (int): Индекс текущего символа
        timer (QTimer): Таймер для управления скоростью печати
        speed (int): Скорость печати в миллисекундах между символами
    """

    def __init__(self, text="", speed=30):
        """
        Инициализация TypeWriterLabel.

        Аргументы:
            text (str, optional): Текст для отображения. По умолчанию пустая строка.
            speed (int, optional): Скорость печати в миллисекундах между символами.
                По умолчанию 30 мс.
        """
        super().__init__()

        self.full_text = text
        self.current_text = ""
        self.index = 0

        # Создаём таймер для управления печатью
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)

        self.speed = speed

    def start(self):
        """
        Запустить анимацию печати текста.

        Сбрасывает текущий текст и индекс, затем запускает таймер
        для начала печатания символов.
        """
        self.current_text = ""
        self.index = 0
        self.timer.start(self.speed)

    def update_text(self):
        """
        Обновить отображаемый текст, добавив один символ.

        Этот метод вызывается таймером каждый тик. Добавляет один символ
        к текущему тексту и обновляет метку. Останавливает таймер когда
        все символы выведены.
        """
        if self.index < len(self.full_text):
            self.current_text += self.full_text[self.index]
            self.setText(self.current_text)
            self.index += 1
        else:
            self.timer.stop()
