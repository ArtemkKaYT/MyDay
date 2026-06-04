"""
Модуль виджета заголовка (Header Widget) с часами и датой.

Этот модуль содержит HeaderWidget, который отображает текущие время и дату,
автоматически обновляя их каждую секунду.

Пример:
    Использование HeaderWidget::

        from ui.widgets.header_widget import HeaderWidget

        widget = HeaderWidget()
        widget.show()
"""

from datetime import datetime
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel


class HeaderWidget(QWidget):
    """
    Виджет для отображения текущего времени и даты.

    Этот класс создаёт виджет с двумя метками: одна показывает текущее время
    в формате HH:MM, другая показывает полную дату с названием дня недели.
    Обновляет время каждую секунду автоматически.

    Атрибуты:
        time_label (QLabel): Метка для отображения времени
        date_label (QLabel): Метка для отображения даты и дня недели
        clock_timer (QTimer): Таймер для обновления времени
    """

    def __init__(self):
        """
        Инициализация HeaderWidget.

        Создаёт метки для времени и даты, размещает их в горизонтальный
        макет и запускает таймер для автоматического обновления.
        """
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Создаём метку для времени
        self.time_label = QLabel()
        self.time_label.setObjectName("timeLabel")

        # Создаём метку для даты
        self.date_label = QLabel()
        self.date_label.setObjectName("dateLabel")

        layout.addWidget(self.time_label)
        layout.addWidget(self.date_label)
        layout.addStretch()

        # Инициализируем таймер для обновления времени
        self.setup_clock()

    def setup_clock(self):
        """
        Инициализировать и запустить таймер обновления времени.

        Создаёт таймер, который запускает обновление времени каждую секунду (1000 мс).
        """
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_time)
        self.clock_timer.start(1000)
        self.update_time()

    def update_time(self):
        """
        Обновить отображаемые время и дату.

        Получает текущее время и дату, форматирует их на русском языке
        и обновляет соответствующие метки.
        """
        now = datetime.now()

        # Обновляем время в формате HH:MM
        self.time_label.setText(now.strftime("%H:%M"))

        # Названия месяцев на русском
        months = [
            "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ]

        # Названия дней недели на русском
        weekdays = [
            "Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота", "Воскресенье"
        ]

        # Обновляем дату и день недели
        self.date_label.setText(
            f"{weekdays[now.weekday()]}, {now.day} {months[now.month - 1]}"
        )
