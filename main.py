import sys
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGraphicsOpacityEffect
)


class TypeWriterLabel(QLabel):
    def __init__(self, text="", speed=30):
        super().__init__()

        self.full_text = text
        self.current_text = ""
        self.index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)

        self.speed = speed

    def start(self):
        self.current_text = ""
        self.index = 0
        self.timer.start(self.speed)

    def update_text(self):
        if self.index < len(self.full_text):
            self.current_text += self.full_text[self.index]
            self.setText(self.current_text)
            self.index += 1
        else:
            self.timer.stop()


class Card(QFrame):
    def __init__(self, title, content):
        super().__init__()

        self.setObjectName("card")

        layout = QVBoxLayout(self)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        content_label = QLabel(content)
        content_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(content_label)

        self.opacity = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(0)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            background-color: #1E1E1E;
            color: white;
            font-size: 14px;
        }

        #timeLabel {
            font-size: 36px;
            font-weight: bold;
        }

        #dateLabel {
            color: #AAAAAA;
            font-size: 16px;
            margin-bottom: 20px;
        }

        #briefLabel {
            font-size: 18px;
            padding: 15px;
            background-color: #252526;
            border-radius: 12px;
            margin-bottom: 10px;
        }

        #card {
            background-color: #252526;
            border-radius: 15px;
            padding: 10px;
        }

        #cardTitle {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 8px;
        }
    """)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())