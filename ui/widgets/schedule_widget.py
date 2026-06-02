from datetime import date
from PyQt6.QtWidgets import (
    QHBoxLayout,
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

        self.events_list_container = QWidget()
        self.events_layout = QVBoxLayout(self.events_list_container)
        self.events_layout.setContentsMargins(0, 0, 0, 0)
        self.events_layout.setSpacing(8)

        self.add_event_button = QPushButton("+ Добавить событие")
        self.add_event_button.clicked.connect(self.toggle_event_form)

        schedule_layout.addWidget(self.events_list_container)
        schedule_layout.addWidget(self.add_event_button)

        self.event_form = QWidget()
        form_layout = QVBoxLayout(self.event_form)
        form_layout.setContentsMargins(0, 8, 0, 0)
        form_layout.setSpacing(8)

        self.event_title = QLineEdit()
        self.event_title.setPlaceholderText("Название события")

        self.event_type = QComboBox()
        self.event_type.addItems([
            "Учеба",
            "Работа",
            "Спорт",
            "Другое"
        ])

        time_row = QWidget()
        time_layout = QHBoxLayout(time_row)
        time_layout.setContentsMargins(0, 0, 0, 0)
        time_layout.setSpacing(8)

        self.start_time = QLineEdit()
        self.start_time.setPlaceholderText("08:30")

        self.end_time = QLineEdit()
        self.end_time.setPlaceholderText("10:00")

        self.event_date = QDateEdit()
        self.event_date.setCalendarPopup(True)
        self.event_date.setDate(QDate.currentDate())

        repeat_row = QWidget()
        repeat_layout = QHBoxLayout(repeat_row)
        repeat_layout.setContentsMargins(0, 0, 0, 0)
        repeat_layout.setSpacing(8)

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

        time_layout.addWidget(self.start_time)
        time_layout.addWidget(self.end_time)

        repeat_layout.addWidget(self.repeat_type)
        repeat_layout.addWidget(self.repeat_interval)

        form_layout.addWidget(self.event_title)
        form_layout.addWidget(self.event_type)
        form_layout.addWidget(time_row)
        form_layout.addWidget(self.event_date)
        form_layout.addWidget(repeat_row)
        form_layout.addWidget(save_button)

        self.event_form.hide()
        schedule_layout.addWidget(self.event_form)

        super().__init__("Расписание", body_widget=schedule_container)

        self.load_schedule()

    def clear_events_layout(self):
        while self.events_layout.count():
            item = self.events_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_schedule(self):
        self.clear_events_layout()

        events = self.schedule_service.get_events_by_date(str(date.today()))

        if not events:
            no_events_label = QLabel("Сегодня событий нет")
            no_events_label.setObjectName("noEventsLabel")
            self.events_layout.addWidget(no_events_label)
            return

        for event in events:
            icon = {
                "Учеба": "📚",
                "Работа": "💼",
                "Спорт": "🏋️",
                "Другое": "📌"
            }.get(event["type"], "📌")

            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 4, 0, 4)
            row_layout.setSpacing(12)

            icon_label = QLabel(icon)
            icon_label.setObjectName("eventIcon")
            
            time_label = QLabel(f"{event['start_time']} – {event['end_time']}")
            time_label.setObjectName("eventTime")
            
            title_label = QLabel(event["title"])
            title_label.setObjectName("eventTitle")
            title_label.setWordWrap(True)

            row_layout.addWidget(icon_label)
            row_layout.addWidget(time_label)
            row_layout.addWidget(title_label, stretch=1)

            self.events_layout.addWidget(row_widget)

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
