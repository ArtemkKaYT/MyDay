from random import choice
from datetime import date, datetime
from config import WEATHER_MESSAGES


class BriefService:

    def __init__(self, weather_service, schedule_service):
        self.weather_service = weather_service
        self.schedule_service = schedule_service

    def generate_brief(self):

        parts = []

        current_hour = datetime.now().hour

        if 6 <= current_hour < 12:
            parts.append("Доброе утро!")

        elif 12 <= current_hour < 18:
            parts.append("Добрый день!")

        elif 18 <= current_hour < 24:
            parts.append("Добрый вечер!")

        else:
            parts.append("Доброй ночи!")

        weather = self.weather_service.get_weather()

        if isinstance(weather, dict):

            weather_type = weather["weather"][0]["main"]

            if weather_type in WEATHER_MESSAGES:
                parts.append(
                    choice(
                        WEATHER_MESSAGES[weather_type]
                    )
                )

        today = str(date.today())

        events = self.schedule_service.get_events_by_date(
            today
        )

        study_events = [
            event
            for event in events
            if event["type"] == "Учёба"
        ]

        work_events = [
            event
            for event in events
            if event["type"] == "Работа"
        ]

        sport_events = [
            event
            for event in events
            if event["type"] == "Спорт"
        ]

        if study_events:

            parts.append(
                f"Сегодня {len(study_events)} учебных занятия."
            )

        if work_events:

            start = min(
                event["start_time"]
                for event in work_events
            )

            finish = max(
                event["end_time"]
                for event in work_events
            )

            parts.append(
                f"Работа с {start} до {finish}."
            )

        if sport_events:

            parts.append(
                "Сегодня есть тренировка. Не забудь позаниматься!"
            )

        if not events:

            parts.append(
                "Сегодня расписание свободное."
            )

        if len(events) > 5:

            parts.append(
                "Насыщенный день, не забудь про отдых."
            )

        if len(events) == 0:

            parts.append(
                "Свободный день. Можно заняться тем, что давно откладывал!"
            )

        return " ".join(parts)
