from datetime import datetime
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel


class HeaderWidget(QWidget):  # Виджет с часами и датой в шапке
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.time_label = QLabel()
        self.time_label.setObjectName("timeLabel")

        self.date_label = QLabel()
        self.date_label.setObjectName("dateLabel")

        layout.addWidget(self.time_label)
        layout.addWidget(self.date_label)
        layout.addStretch()

        self.setup_clock()

    def setup_clock(self):  # Запускает таймер для обновления времени
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_time)
        self.clock_timer.start(1000)
        self.update_time()

    def update_time(self):  # Обновляет время и дату каждую секунду
        now = datetime.now()

        self.time_label.setText(now.strftime("%H:%M"))

        months = [
            "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ]
        weekdays = [
            "Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота", "Воскресенье"
        ]

        self.date_label.setText(
            f"{weekdays[now.weekday()]}, {now.day} {months[now.month - 1]}"
        )
