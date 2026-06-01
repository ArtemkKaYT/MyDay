from datetime import date
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QInputDialog,
    QMessageBox,
)

from ui.widgets.card import Card
from ui.widgets.type_writer_label import TypeWriterLabel

from services.weather_service import WeatherService
from services.schedule_service import ScheduleService
from services.notes_service import NotesService
from services.brief_service import BriefService


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.weather_service = WeatherService()
        self.schedule_service = ScheduleService()
        self.notes_service = NotesService()

        self.brief_service = BriefService(
            self.weather_service,
            self.schedule_service
        )

        self.setWindowTitle("MyDay")
        self.resize(720, 860)

        self.animations = []

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # Верхняя строка: время и дата
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        self.time_label = QLabel()
        self.time_label.setObjectName("timeLabel")

        self.date_label = QLabel()
        self.date_label.setObjectName("dateLabel")

        top_row.addWidget(self.time_label)
        top_row.addWidget(self.date_label)
        top_row.addStretch()

        root.addLayout(top_row)

        # Brief
        brief_text = self.brief_service.generate_brief()
        
        self.brief = TypeWriterLabel(brief_text)
        self.brief.setObjectName("briefLabel")
        self.brief.setWordWrap(True)

        root.addWidget(self.brief)

        # Погода
        weather_body = QWidget()
        weather_layout = QHBoxLayout(weather_body)
        weather_layout.setContentsMargins(0, 0, 0, 0)
        weather_layout.setSpacing(14)

        self.weather_icon = QLabel("☀️")
        self.weather_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_icon.setFont(QFont("Segoe UI", 28))

        self.weather_text = QLabel("+18°C\nЯсно")
        self.weather_text.setWordWrap(True)
        self.weather_text.setObjectName("cardText")

        weather_layout.addWidget(self.weather_icon)
        weather_layout.addWidget(self.weather_text)

        self.weather_card = Card("Погода", body_widget=weather_body)
        root.addWidget(self.weather_card)

        # Расписание
        self.schedule_text = QLabel(
            "• Учёба: 08:30–11:50\n"
            "• Работа: сегодня нет\n"
            "• Спорт: 19:00–20:30"
        )
        self.schedule_text.setWordWrap(True)
        self.schedule_text.setObjectName("cardText")

        self.schedule_button = QPushButton("Составить расписание")
        self.schedule_button.clicked.connect(self.compose_schedule)

        self.schedule_card = Card(
            "Расписание",
            body_widget=self.schedule_text,
            header_right=self.schedule_button,
        )
        root.addWidget(self.schedule_card)

        # Заметки
        self.notes_list = QListWidget()

        self.load_notes()

        self.notes_card = Card("Заметки", body_widget=self.notes_list)
        root.addWidget(self.notes_card)

        # Кнопка добавить заметку
        self.add_note_button = QPushButton("Добавить заметку")
        self.add_note_button.clicked.connect(self.add_note)

        root.addWidget(self.add_note_button)

        root.addStretch()

        self.setup_clock()
        self.start_animations()

        self.load_weather()

        self.load_schedule()

    def setup_clock(self):
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_time)
        self.clock_timer.start(1000)
        self.update_time()

    def update_time(self):
        from datetime import datetime

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

    def start_animations(self):
        QTimer.singleShot(300, self.brief.start)

        cards = [self.weather_card, self.schedule_card, self.notes_card]

        for index, card in enumerate(cards):
            def show_card(c=card):
                animation = QPropertyAnimation(c.graphicsEffect(), b"opacity")
                animation.setDuration(700)
                animation.setStartValue(0)
                animation.setEndValue(1)
                animation.start()
                self.animations.append(animation)

            QTimer.singleShot(1200 + index * 350, show_card)

    def add_note(self):

        text, ok = QInputDialog.getText(
            self,
            "Добавить заметку",
            "Введите заметку:"
        )

        if ok and text.strip():

            self.notes_service.add_note(
                text.strip()
            )

            self.load_notes()

    def compose_schedule(self):
        QMessageBox.information(
            self,
            "Составить расписание",
            "Эта функция пока недоступна."
        )
    
    def load_weather(self):

        weather = self.weather_service.get_weather()

        if not isinstance(weather, dict):
            self.weather_text.setText(
                "Не удалось получить погоду"
            )
            return

        try:

            temp = round(weather["main"]["temp"])
            status = weather["weather"][0]["description"]

            self.weather_text.setText(
                f"{temp}°C\n{status.capitalize()}"
            )

            weather_type = weather["weather"][0]["main"]

            self.update_weather_icon(weather_type)

        except (KeyError, TypeError):
            self.weather_text.setText(
                "Ошибка данных погоды"
            )

    def update_weather_icon(self, weather_type):

        icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Snow": "❄️",
            "Thunderstorm": "⛈️"
        }

        self.weather_icon.setText(
            icons.get(weather_type, "🌤️")
        )
    
    def load_notes(self):

        self.notes_list.clear()

        notes = self.notes_service.get_notes()

        for note in notes:
            self.notes_list.addItem(
                note["text"]
            )
    
    def load_schedule(self):

        events = self.schedule_service.get_events_by_date(
                                str(date.today())
                            )

        if not events:

            self.schedule_text.setText(
                "Сегодня событий нет"
            )
            return

        lines = []

        for event in events:

            lines.append(
                f"{event['time']} • "
                f"{event['title']} "
                f"({event['type']})"
            )

        self.schedule_text.setText(
            "\n".join(lines)
        )
