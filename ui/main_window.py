from services.weather_service import WeatherService
from services.schedule_service import ScheduleService
from services.brief_service import BriefService

from ui.widgets.card import Card
from ui.widgets.type_writer_label import TypeWriterLabel
from PyQt6.QtCore import QTimer, QPropertyAnimation
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Личный помощник")
        self.resize(700, 800)

        self.animations = []

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # Время
        self.time_label = QLabel()
        self.time_label.setObjectName("timeLabel")

        # Дата
        self.date_label = QLabel()
        self.date_label.setObjectName("dateLabel")

        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.date_label)

        # Brief
        self.brief = TypeWriterLabel(
            "Добрый вечер, Артём.\n"
            "Сегодня хорошая погода для прогулки.\n"
            "У вас 2 пары и тренировка вечером."
        )

        self.brief.setObjectName("briefLabel")
        self.brief.setWordWrap(True)

        main_layout.addWidget(self.brief)

        # Карточки
        self.weather_card = Card(
            "☀️ Погода",
            "+18°C\nЯсно"
        )

        self.study_card = Card(
            "📚 Учёба",
            "2 пары\n08:30 - 11:50"
        )

        self.work_card = Card(
            "💼 Работа",
            "Сегодня выходной"
        )

        self.sport_card = Card(
            "🏋 Спорт",
            "Сегодня тренировка Full Body"
        )

        self.cards = [
            self.weather_card,
            self.study_card,
            self.work_card,
            self.sport_card
        ]

        for card in self.cards:
            main_layout.addWidget(card)

        main_layout.addStretch()

        self.setup_clock()
        self.start_animations()

    def setup_clock(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def update_time(self):
        from datetime import datetime

        now = datetime.now()

        self.time_label.setText(now.strftime("%H:%M:%S"))

        months = [
            "января", "февраля", "марта",
            "апреля", "мая", "июня",
            "июля", "августа", "сентября",
            "октября", "ноября", "декабря"
        ]

        weekdays = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
            "Воскресенье"
        ]

        date_text = (
            f"{weekdays[now.weekday()]}, "
            f"{now.day} {months[now.month - 1]} "
            f"{now.year}"
        )

        self.date_label.setText(date_text)

    def start_animations(self):

        QTimer.singleShot(500, self.brief.start)

        for index, card in enumerate(self.cards):

            def show_card(c=card):
                animation = QPropertyAnimation(
                    c.graphicsEffect(),
                    b"opacity"
                )

                animation.setDuration(800)
                animation.setStartValue(0)
                animation.setEndValue(1)

                animation.start()

                self.animations.append(animation)

            QTimer.singleShot(
                2500 + index * 500,
                show_card
            )
