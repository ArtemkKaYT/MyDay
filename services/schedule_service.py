import json
from pathlib import Path
from datetime import date


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
            repeat="none"
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
            "repeat": repeat
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

    def get_events_by_date(self, target_date):

        events = self.load_schedule()

        return [
            event
            for event in events
            if event["date"] == target_date
        ]
