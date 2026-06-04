"""
Модуль сервиса расписания (Schedule Service) для приложения MyDay.

Этот модуль предоставляет функциональность управления расписанием и событиями, включая:

- Создание, чтение, обновление и удаление событий
- Поддержка повторяющихся событий (ежедневно, еженедельно, ежемесячно)
- Фильтрацию событий по дате с учётом логики повторений
- Персистентное хранилище на базе JSON файлов

Класс ScheduleService управляет всеми операциями, связанными с расписанием,
и обрабатывает паттерны повторения событий для гибкого планирования.

Пример:
    Использование ScheduleService::

        from services.schedule_service import ScheduleService

        service = ScheduleService()
        service.add_event(
            title='Встреча',
            start_time='14:00',
            end_time='15:00',
            event_type='Работа'
        )
        events = service.get_events_by_date('2024-06-04')

Атрибуты:
    ScheduleService: Основной класс сервиса управления расписанием
"""

import json
from pathlib import Path
from datetime import date, datetime


class ScheduleService:
    """
    Сервис для управления событиями и операциями расписания.

    Этот класс обеспечивает полный функционал работы с событиями,
    включая создание, удаление, загрузку, сохранение и поиск событий.
    Поддерживает повторяющиеся события с различными паттернами повторения
    (ежедневно, еженедельно, ежемесячно).

    События хранятся в JSON формате и включают поддержку:
    - Названия события, даты и времени
    - Категоризации события (Работа, Учеба, Спорт и т.д.)
    - Паттернов повторения и интервалов

    Атрибуты:
        file_path (Path): Путь к JSON файлу для хранения событий
    """

    def __init__(self, file_path="data/schedule.json"):
        """
        Инициализация ScheduleService с JSON файлом хранилища.

        Создаёт файл хранилища и директории, если они не существуют.

        Аргументы:
            file_path (str, optional): Путь к JSON файлу. По умолчанию
                'data/schedule.json'.
        """
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def load_schedule(self):
        """
        Загрузить все события из JSON файла хранилища.

        Возвращает:
            list: Список всех событий. Возвращает пустой список если
                  JSON файл некорректен или повреждён.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def save_schedule(self, schedule):
        """
        Сохранить события в JSON файл хранилища.

        Аргументы:
            schedule (list): Список словарей событий для сохранения.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                schedule,
                file,
                ensure_ascii=False,
                indent=4
            )

    def add_event(
            self,
            title,
            start_time,
            end_time,
            event_type,
            event_date=None,
            repeat_type=None,
            repeat_interval=None
    ):
        """
        Добавить новое событие в расписание.

        Создаёт новое событие с указанными параметрами и сохраняет
        его в файл хранилища.

        Аргументы:
            title (str): Название/описание события.
            start_time (str): Время начала события в формате HH:MM.
            end_time (str): Время завершения события в формате HH:MM.
            event_type (str): Категория события (например, 'Работа', 'Учеба', 'Спорт').
            event_date (str, optional): Дата события в формате YYYY-MM-DD.
                По умолчанию используется текущая дата.
            repeat_type (str, optional): Паттерн повторения. Может быть:
                - 'Не повторять' (без повторения, по умолчанию)
                - 'Дни' (ежедневно)
                - 'Недели' (еженедельно)
                - 'Месяцы' (ежемесячно)
            repeat_interval (int, optional): Интервал повторения
                (например, 2 означает каждые 2 дня/недели/месяца).

        Пример:
            Добавление повторяющегося события работы::

                service.add_event(
                    title='Встреча с командой',
                    start_time='10:00',
                    end_time='11:00',
                    event_type='Работа',
                    repeat_type='Недели',
                    repeat_interval=1
                )
        """
        schedule = self.load_schedule()

        if event_date is None:
            event_date = str(date.today())

        new_event = {
            "title": title,
            "date": event_date,
            "start_time": start_time,
            "end_time": end_time,
            "type": event_type,
            "repeat_type": repeat_type,
            "repeat_interval": repeat_interval
        }

        schedule.append(new_event)

        self.save_schedule(schedule)

    def delete_event(self, index):
        """
        Удалить событие по его индексу в расписании.

        Аргументы:
            index (int): Нулевой индекс события для удаления.

        Возвращает:
            None
        """
        schedule = self.load_schedule()

        if 0 <= index < len(schedule):
            schedule.pop(index)
            self.save_schedule(schedule)

    def get_events(self):
        """
        Получить все события в расписании.

        Возвращает:
            list: Список всех словарей событий.
        """
        return self.load_schedule()

    def should_show_event(self, event, target_date_obj):
        """
        Определить, должно ли событие отображаться в указанную дату.

        Проверяет, появляется ли событие с правилами повторения
        в целевую дату. Обрабатывает непрерывные, ежедневные,
        еженедельные и ежемесячные паттерны повторения.

        Аргументы:
            event (dict): Словарь события с информацией о дате и повторении.
            target_date_obj (date): Дата для проверки.

        Возвращает:
            bool: True если событие должно отображаться в target_date_obj,
                  False в противном случае.

        Примечание:
            - Для ежемесячного повторения проверяется совпадение дня
            - Дни считаются от даты начала события
        """
        try:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            return False

        if target_date_obj < event_date:
            return False

        repeat_type = event.get("repeat_type") or "Не повторять"
        interval = event.get("repeat_interval")
        interval = int(interval) if interval is not None else 1

        delta_days = (target_date_obj - event_date).days

        if repeat_type == "Не повторять":
            return event_date == target_date_obj

        elif repeat_type == "Дни":
            return delta_days % interval == 0

        elif repeat_type == "Недели":
            return delta_days % (interval * 7) == 0

        elif repeat_type == "Месяцы":
            delta_months = (target_date_obj.year
                            - event_date.year) * 12 + (target_date_obj.month
                                                       - event_date.month)
            return delta_months % interval == 0 and target_date_obj.day == event_date.day

        return False

    def get_events_by_date(self, target_date):
        """
        Получить все события на конкретную дату, включая повторяющиеся.

        Получает события, которые приходятся на указанную дату,
        учитывая паттерны повторяющихся событий. Результаты сортируются
        по времени начала.

        Аргументы:
            target_date (str): Дата в формате YYYY-MM-DD.

        Возвращает:
            list: Список словарей событий для целевой даты,
                  отсортированные по start_time. Возвращает пустой список если
                  формат даты некорректен.

        Пример:
            Получение событий на сегодня::

                from datetime import date
                today = str(date.today())
                events = service.get_events_by_date(today)
                for event in events:
                    print(f"{event['title']}: {event['start_time']}")
        """
        try:
            target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            return []

        all_events = self.load_schedule()
        filtered_events = []

        for event in all_events:
            if self.should_show_event(event, target_date_obj):
                filtered_events.append(event)

        filtered_events.sort(key=lambda x: x.get("start_time", ""))

        return filtered_events
