from random import choice
from datetime import date


class BriefService:

    WEATHER_MESSAGES = {
        "Clear": [
            "Солнце! Бери темные очки.",
            "Кайфовая погода, рекомендую погулять.",
            "На улице ясно. Отличный день!",
            "Небо чистое. Наслаждайся теплом."
        ],

        "Clouds": [
            "Облачно, но без осадков. Комфортно.",
            "Солнце спряталось. Идеально для прогулки.",
            "Не жарко. Самое то побегать.",
            "Пасмурно, но день будет супер!"
        ],

        "Rain": [
            "Дождик! Твой зонт заждался.",
            "Капает. Обувай непромокаемые кеды.",
            "Свежесть после дождя — кайф.",
            "Дождь не помеха хорошему дню!"
        ],

        "Snow": [
            "Красота! Снаружи сказочный снегопад.",
            "Снег валит. Утепляйся по полной!",
            "Время лепить снеговика. Одевайся теплее.",
            "Свежий снег. На улице супер!"
        ],

        "Thunderstorm": [
            "Гроза! Уютно чиллим дома.",
            "Гремит. Отличный повод для сериала.",
            "Молнии! Пережди этот замес в тепле.",
            "Штормит. Дома теплее и безопаснее."
        ],

        "Mist": [
            "Туман. На улице Silent Hill.",
            "Вокруг молоко. Будь аккуратнее на дороге.",
            "Загадочный туман.",
            "Видимость слабая, зато очень атмосферно."
        ],

        "Fog": [
            "Туман. На улице Silent Hill.",
            "Вокруг молоко. Будь аккуратнее на дороге.",
            "Загадочный туман.",
            "Видимость слабая, зато очень атмосферно."
        ]
    }

    def __init__(self, weather_service, schedule_service):
        self.weather_service = weather_service
        self.schedule_service = schedule_service

    def generate_brief(self):

        parts = []

        weather = self.weather_service.get_weather()

        if weather:

            weather_type = weather["weather"][0]["main"]

            if weather_type in self.WEATHER_MESSAGES:
                parts.append(
                    choice(
                        self.WEATHER_MESSAGES[weather_type]
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
                event["time"]
                for event in work_events
            )

            finish = max(
                event["time"]
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
                "Свободный день. Можно заняться тем, что давно откладывал."
            )

        return " ".join(parts)
