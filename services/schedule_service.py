import json
from pathlib import Path
from datetime import date, datetime


class ScheduleService:

    def __init__(self, file_path="data/schedule.json"):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def load_schedule(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def save_schedule(self, schedule):
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

        schedule = self.load_schedule()

        if 0 <= index < len(schedule):
            schedule.pop(index)
            self.save_schedule(schedule)

    def get_events(self):

        return self.load_schedule()

    def should_show_event(self, event, target_date_obj):

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
