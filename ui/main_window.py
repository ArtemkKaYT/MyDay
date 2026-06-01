from datetime import date
from PyQt6.QtCore import QDate, Qt, QTimer, QPropertyAnimation
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
    QLineEdit,
    QComboBox,
    QDateEdit
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
        self.schedule_text = QLabel()
        self.add_event_button = QPushButton(
            "+ Добавить событие"
        )

        self.add_event_button.clicked.connect(
            self.toggle_event_form
        )
        schedule_container = QWidget()

        schedule_layout = QVBoxLayout(
            schedule_container
        )

        schedule_layout.setContentsMargins(
            0, 0, 0, 0
        )

        schedule_layout.addWidget(
            self.schedule_text
        )

        schedule_layout.addWidget(
            self.add_event_button
        )

        self.schedule_text.setWordWrap(True)
        self.schedule_text.setObjectName("cardText")

        self.schedule_card = Card(
            "Расписание",
            body_widget=schedule_container,
        )
        root.addWidget(self.schedule_card)

        self.event_form = QWidget()

        form_layout = QVBoxLayout(
            self.event_form
        )

        self.event_title = QLineEdit()
        self.event_title.setPlaceholderText(
            "Название события"
        )

        self.event_type = QComboBox()

        self.event_type.addItems([
            "Учёба",
            "Работа",
            "Спорт",
            "Другое"
        ])

        self.start_time = QLineEdit()
        self.start_time.setPlaceholderText("08:30")

        self.end_time = QLineEdit()
        self.end_time.setPlaceholderText("10:00")

        self.event_date = QDateEdit()

        self.event_date.setCalendarPopup(True)
        self.event_date.setDate(QDate.currentDate())

        self.repeat_box = QComboBox()

        self.repeat_box.addItems([
            "Один раз",
            "Ежедневно",
            "Еженедельно",
            "Ежемесячно"
        ])

        save_button = QPushButton(
            "Сохранить событие"
        )

        save_button.clicked.connect(
            self.save_event
        )

        form_layout.addWidget(
            self.event_title
        )

        form_layout.addWidget(
            self.event_type
        )

        form_layout.addWidget(
            self.start_time
        )

        form_layout.addWidget(
            self.end_time
        )

        form_layout.addWidget(
            self.event_date
        )

        form_layout.addWidget(
            self.repeat_box
        )

        form_layout.addWidget(
            save_button
        )

        self.event_form.hide()

        schedule_layout.addWidget(
            self.event_form
        )

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

            icon = {
                "Учёба": "📚",
                "Работа": "💼",
                "Спорт": "🏋️",
                "Другое": "📌"
            }.get(
                event["type"],
                "📌"
            )

            lines.append(
                f"{icon} "
                f"{event['start_time']}"
                f"-"
                f"{event['end_time']}  "
                f"{event['title']}"
            )

        self.schedule_text.setText(
            "\n".join(lines)
        )

    def toggle_event_form(self):

        if self.event_form.isVisible():
            self.event_form.hide()
        else:
            self.event_form.show()
    
    def save_event(self):

        title = self.event_title.text().strip()

        if not title:
            return

        self.schedule_service.add_event(
            title=title,
            start_time=self.start_time.text(),
            end_time=self.end_time.text(),
            event_type=self.event_type.currentText(),
            event_date=self.event_date.date().toString(
                "yyyy-MM-dd"
            ),
            repeat=self.repeat_box.currentText()
        )

        self.load_schedule()

        self.event_title.clear()

        self.start_time.clear()

        self.end_time.clear()

        self.event_form.hide()
