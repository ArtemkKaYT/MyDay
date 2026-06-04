"""
Модуль сервиса для генерации ежедневной сводки (Brief Service).

Этот модуль предоставляет функциональность для создания персональной
ежедневной сводки, которая включает:

- Приветствие в зависимости от времени суток
- Мотивирующее сообщение о текущей погоде
- Информацию о предстоящих событиях дня
- Интеллектуальные советы на основе расписания

Сервис объединяет данные из сервисов погоды и расписания
для создания единой информативной сводки.

Пример:
    Использование BriefService::

        from services.brief_service import BriefService
        from services.weather_service import WeatherService
        from services.schedule_service import ScheduleService

        weather_service = WeatherService()
        schedule_service = ScheduleService()
        
        brief_service = BriefService(weather_service, schedule_service)
        svodka = brief_service.generate_brief()
        print(svodka)
"""

from random import choice
from datetime import date, datetime
from config import WEATHER_MESSAGES


class BriefService:
    """
    Сервис для генерации персональной ежедневной сводки.

    Этот класс создаёт информативное текстовое резюме дня на основе
    времени суток, информации о погоде и расписания событий пользователя.

    Атрибуты:
        weather_service (WeatherService): Сервис для получения данных о погоде.
        schedule_service (ScheduleService): Сервис для получения данных о расписании.
    """

    def __init__(self, weather_service, schedule_service):
        """
        Инициализация BriefService.

        Аргументы:
            weather_service (WeatherService): Экземпляр сервиса погоды.
            schedule_service (ScheduleService): Экземпляр сервиса расписания.
        """
        self.weather_service = weather_service
        self.schedule_service = schedule_service

    def generate_brief(self):
        """
        Сгенерировать ежедневную сводку.

        Формирует текстовую сводку дня, объединяя приветствие
        в зависимости от времени суток, информацию о погоде,
        и краткое описание событий из расписания на сегодня.

        Возвращает:
            str: Сформированная сводка дня на русском языке.
        """
        parts = []

        current_hour = datetime.now().hour

        # Определяем время суток для приветствия
        if 6 <= current_hour < 12:
            parts.append("Доброе утро!")

        elif 12 <= current_hour < 18:
            parts.append("Добрый день!")

        elif 18 <= current_hour < 24:
            parts.append("Добрый вечер!")

        else:
            parts.append("Доброй ночи!")

        # Добавляем мотивирующее сообщение о погоде
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

        # Получаем события на сегодня
        events = self.schedule_service.get_events_by_date(
            today
        )

        # Фильтруем события по типам
        study_events = [
            event
            for event in events
            if event["type"] == "Учеба"
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

        # Добавляем информацию об учебе
        if study_events:

            parts.append(
                f"Сегодня {len(study_events)} учебных занятия."
            )

        # Добавляем информацию о работе
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

        # Добавляем информацию о спорте
        if sport_events:

            parts.append(
                "Сегодня есть тренировка. Не забудь позаниматься!"
            )

        # Сценарии для пустого расписания
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
