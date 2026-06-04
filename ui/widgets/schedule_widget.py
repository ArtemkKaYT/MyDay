"""
Модуль виджета для работы с расписанием (Schedule Widget).

Этот модуль содержит ScheduleWidget - визуальный компонент для создания,
отображения и управления событиями в расписании.

Пример:
    Использование ScheduleWidget::

        from ui.widgets.schedule_widget import ScheduleWidget
        from services.schedule_service import ScheduleService

        schedule_service = ScheduleService()
        widget = ScheduleWidget(schedule_service)
        widget.show()
"""

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
    """
    Виджет для отображения и управления расписанием событий.

    Этот класс предоставляет интерфейс для создания, просмотра и удаления
    событий в расписании. Поддерживает повторяющиеся события и различные
    категории (Учеба, Работа, Спорт, Другое).

    Атрибуты:
        schedule_service (ScheduleService): Сервис для управления расписанием
        events_list_container (QWidget): Контейнер для списка событий
        event_form (QWidget): Форма для добавления нового события
        event_title (QLineEdit): Поле для названия события
        event_type (QComboBox): Выбор категории события
        start_time (QLineEdit): Время начала события
        end_time (QLineEdit): Время завершения события
        event_date (QDateEdit): Дата события
        repeat_type (QComboBox): Тип повторения события
        repeat_interval (QSpinBox): Интервал повторения
    """

    def __init__(self, schedule_service: ScheduleService):
        """
        Инициализация ScheduleWidget.

        Создаёт виджет с кнопкой добавления события и формой для ввода.

        Аргументы:
            schedule_service (ScheduleService): Экземпляр сервиса для работы с расписанием.
        """
        self.schedule_service = schedule_service

        # Создаём контейнер для расписания
        schedule_container = QWidget()
        schedule_layout = QVBoxLayout(schedule_container)
        schedule_layout.setContentsMargins(0, 0, 0, 0)

        schedule_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        # Создаём контейнер для списка событий
        self.events_list_container = QWidget()
        self.events_layout = QVBoxLayout(self.events_list_container)
        self.events_layout.setContentsMargins(0, 0, 0, 0)
        self.events_layout.setSpacing(8)

        # Кнопка для добавления события
        self.add_event_button = QPushButton("+ Добавить событие")
        self.add_event_button.clicked.connect(self.toggle_event_form)

        schedule_layout.addWidget(self.events_list_container)
        schedule_layout.addWidget(self.add_event_button)

        # Создаём форму для добавления события
        self.event_form = QWidget()
        form_layout = QVBoxLayout(self.event_form)
        form_layout.setContentsMargins(0, 8, 0, 0)
        form_layout.setSpacing(8)

        # Поле для названия события
        self.event_title = QLineEdit()
        self.event_title.setPlaceholderText("Название события")

        # Выбор категории события
        self.event_type = QComboBox()
        self.event_type.addItems([
            "Учеба",
            "Работа",
            "Спорт",
            "Другое"
        ])

        # Поля для времени
        time_row = QWidget()
        time_layout = QHBoxLayout(time_row)
        time_layout.setContentsMargins(0, 0, 0, 0)
        time_layout.setSpacing(8)

        self.start_time = QLineEdit()
        self.start_time.setPlaceholderText("08:30")

        self.end_time = QLineEdit()
        self.end_time.setPlaceholderText("10:00")

        # Выбор даты события
        self.event_date = QDateEdit()
        self.event_date.setCalendarPopup(True)
        self.event_date.setDate(QDate.currentDate())

        # Настройки повторения события
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
            """Показывает интервал если выбран повторяющийся тип."""
            if text == "Не повторять":
                self.repeat_interval.hide()
            else:
                self.repeat_interval.show()

        self.repeat_type.currentTextChanged.connect(toggle_interval)

        # Кнопка сохранения события
        save_button = QPushButton("Сохранить событие")
        save_button.clicked.connect(self.save_event)

        # Добавляем элементы в строку времени
        time_layout.addWidget(self.start_time)
        time_layout.addWidget(self.end_time)

        # Добавляем элементы в строку повторения
        repeat_layout.addWidget(self.repeat_type)
        repeat_layout.addWidget(self.repeat_interval)

        # Добавляем все элементы в форму
        form_layout.addWidget(self.event_title)
        form_layout.addWidget(self.event_type)
        form_layout.addWidget(time_row)
        form_layout.addWidget(self.event_date)
        form_layout.addWidget(repeat_row)
        form_layout.addWidget(save_button)

        # Скрываем форму по умолчанию
        self.event_form.hide()
        schedule_layout.addWidget(self.event_form)

        # Инициализируем родительский класс Card
        super().__init__("Расписание", body_widget=schedule_container)

        # Загружаем события
        self.load_schedule()

    def clear_events_layout(self):
        """
        Очистить список событий.

        Удаляет все виджеты событий из макета списка.
        """
        while self.events_layout.count():
            item = self.events_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_schedule(self):
        """
        Загрузить и отобразить события на сегодня.

        Получает события на текущую дату из сервиса и создаёт визуальные
        элементы для каждого события с иконками категорий.
        """
        self.clear_events_layout()

        events = self.schedule_service.get_events_by_date(str(date.today()))

        # Если событий нет, показываем сообщение
        if not events:
            no_events_label = QLabel("Сегодня событий нет")
            no_events_label.setObjectName("noEventsLabel")
            self.events_layout.addWidget(no_events_label)
            return

        # Создаём визуальный элемент для каждого события
        for event in events:
            # Выбираем иконку в зависимости от типа события
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

            # Иконка события
            icon_label = QLabel(icon)
            icon_label.setObjectName("eventIcon")

            # Время события
            time_label = QLabel(f"{event['start_time']} – {event['end_time']}")
            time_label.setObjectName("eventTime")

            # Название события
            title_label = QLabel(event["title"])
            title_label.setObjectName("eventTitle")
            title_label.setWordWrap(True)

            row_layout.addWidget(icon_label)
            row_layout.addWidget(time_label)
            row_layout.addWidget(title_label, stretch=1)

            self.events_layout.addWidget(row_widget)

    def toggle_event_form(self):
        """
        Переключить видимость формы добавления события.

        Показывает форму если она скрыта, или скрывает если она видна.
        """
        if self.event_form.isVisible():
            self.event_form.hide()
        else:
            self.event_form.show()

    def save_event(self):
        """
        Сохранить новое событие и обновить список.

        Получает данные из формы, добавляет событие в сервис,
        перезагружает список и очищает форму.
        """
        title = self.event_title.text().strip()

        if not title:
            return

        # Добавляем событие в сервис
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

        # Перезагружаем список и очищаем форму
        self.load_schedule()

        self.event_title.clear()
        self.start_time.clear()
        self.end_time.clear()
        self.event_form.hide()
