from datetime import date
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QSpinBox,
    QLayout
)
from PyQt6.QtCore import QDate
from ui.widgets.card import Card
from services.schedule_service import ScheduleService


class ScheduleWidget(Card):
    def __init__(self, schedule_service: ScheduleService):
        self.schedule_service = schedule_service

        schedule_container = QWidget()
        schedule_layout = QVBoxLayout(schedule_container)
        schedule_layout.setContentsMargins(0, 0, 0, 0)

        schedule_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        self.schedule_text = QLabel()
        self.schedule_text.setWordWrap(True)
        self.schedule_text.setObjectName("cardText")

        self.add_event_button = QPushButton("+ Добавить событие")
        self.add_event_button.clicked.connect(self.toggle_event_form)

        schedule_layout.addWidget(self.schedule_text)
        schedule_layout.addWidget(self.add_event_button)

        self.event_form = QWidget()
        form_layout = QVBoxLayout(self.event_form)

        self.event_title = QLineEdit()
        self.event_title.setPlaceholderText("Название события")

        self.event_type = QComboBox()
        self.event_type.addItems([
            "Учеба",
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

        self.repeat_type = QComboBox()
        self.repeat_type.addItems([
            "Не повторять",
            "Дни",
            "Недели",
            "Месяцы"
        ])

        self.repeat_interval = QSpinBox()
        self.repeat_interval.setMinimum(1)
        self.repeat_interval.setMaximum(365)
        self.repeat_interval.setValue(1)
        self.repeat_interval.hide()

        def toggle_interval(text):
            if text == "Не повторять":
                self.repeat_interval.hide()
            else:
                self.repeat_interval.show()

        self.repeat_type.currentTextChanged.connect(toggle_interval)

        save_button = QPushButton("Сохранить событие")
        save_button.clicked.connect(self.save_event)

        form_layout.addWidget(self.event_title)
        form_layout.addWidget(self.event_type)
        form_layout.addWidget(self.start_time)
        form_layout.addWidget(self.end_time)
        form_layout.addWidget(self.event_date)
        form_layout.addWidget(self.repeat_type)
        form_layout.addWidget(self.repeat_interval)
        form_layout.addWidget(save_button)

        self.event_form.hide()
        schedule_layout.addWidget(self.event_form)

        super().__init__("Расписание", body_widget=schedule_container)

        self.load_schedule()

    def load_schedule(self):

        events = self.schedule_service.get_events_by_date(str(date.today()))

        if not events:

            self.schedule_text.setText(
                "Сегодня событий нет"
            )
            return

        lines = []

        for event in events:

            icon = {
                "Учеба": "📚",
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
            repeat_type=self.repeat_type.currentText(),
            repeat_interval=self.repeat_interval.value()
        )

        self.load_schedule()

        self.event_title.clear()

        self.start_time.clear()

        self.end_time.clear()

        self.event_form.hide()
