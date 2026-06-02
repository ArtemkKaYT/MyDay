from PyQt6.QtCore import QTimer, QPropertyAnimation
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from ui.widgets.header_widget import HeaderWidget
from ui.widgets.brief_widget import BriefWidget
from ui.widgets.weather_widget import WeatherWidget
from ui.widgets.schedule_widget import ScheduleWidget
from ui.widgets.notes_widget import NotesWidget

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

        # Header widget
        self.header_widget = HeaderWidget()
        root.addWidget(self.header_widget)

        # Brief widget
        self.brief_widget = BriefWidget(self.brief_service)
        root.addWidget(self.brief_widget)

        # Weather widget
        self.weather_widget = WeatherWidget(self.weather_service)
        root.addWidget(self.weather_widget)

        # Schedule widget
        self.schedule_widget = ScheduleWidget(self.schedule_service)
        root.addWidget(self.schedule_widget)

        # Notes widget
        self.notes_widget = NotesWidget(self.notes_service)
        root.addWidget(self.notes_widget)

        root.addStretch()

        self.start_animations()

    def start_animations(self):
        QTimer.singleShot(300, self.brief_widget.start_animation)

        cards = [self.weather_widget, self.schedule_widget, self.notes_widget]

        for index, card in enumerate(cards):
            def show_card(c=card):
                animation = QPropertyAnimation(c.graphicsEffect(), b"opacity")
                animation.setDuration(700)
                animation.setStartValue(0)
                animation.setEndValue(1)
                animation.start()
                self.animations.append(animation)

            QTimer.singleShot(1200 + index * 350, show_card)
