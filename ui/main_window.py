from PyQt6.QtCore import QTimer, QPropertyAnimation, QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from ui.widgets.header_widget import HeaderWidget
from ui.widgets.brief_widget import BriefWidget
from ui.widgets.weather_widget import WeatherWidget
from ui.widgets.schedule_widget import ScheduleWidget
from ui.widgets.notes_widget import NotesWidget

from services.weather_service import WeatherService
from services.schedule_service import ScheduleService
from services.notes_service import NotesService
from services.brief_service import BriefService

from ui.styles.theme_meneger import get_weather_theme


class WeatherFetchWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, weather_service):
        super().__init__()
        self.weather_service = weather_service

    def run(self):
        data = self.weather_service.get_weather()
        if data:
            self.finished.emit(data)


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

        self.setStyleSheet(get_weather_theme("Clouds"))

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(24, 24, 24, 24)
        scroll_layout.setSpacing(16)

        # Header widget
        self.header_widget = HeaderWidget()
        scroll_layout.addWidget(self.header_widget)

        # Brief widget
        self.brief_widget = BriefWidget(self.brief_service)
        scroll_layout.addWidget(self.brief_widget)

        # Weather widget
        self.weather_widget = WeatherWidget(self.weather_service)
        scroll_layout.addWidget(self.weather_widget)

        # Schedule widget
        self.schedule_widget = ScheduleWidget(self.schedule_service)
        scroll_layout.addWidget(self.schedule_widget)

        # Notes widget
        self.notes_widget = NotesWidget(self.notes_service)
        scroll_layout.addWidget(self.notes_widget)

        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        root.addWidget(scroll_area)

        self.start_animations()

    def load_weather_theme_async(self):
        self.weather_worker = WeatherFetchWorker(self.weather_service)
        
        self.weather_worker.finished.connect(self.on_weather_loaded)
        
        self.weather_worker.start()

    def on_weather_loaded(self, weather_data):
        try:
            weather_main = weather_data["weather"][0]["main"]
            
            new_style = get_weather_theme(weather_main)
            
            self.setStyleSheet(new_style)
            
        except (KeyError, IndexError):
            pass

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
