import json
import uuid
from pathlib import Path
from datetime import date


class NotesService:

    def __init__(self, file_path="data/notes.json"):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def load_notes(self):

        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_notes(self, notes):

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                notes,
                file,
                ensure_ascii=False,
                indent=4
            )

    def add_note(self, text):

        notes = self.load_notes()

        new_note = {
            "id": str(uuid.uuid4()),
            "text": text,
            "created_at": str(date.today())
        }

        notes.append(new_note)

        self.save_notes(notes)

    def delete_note(self, note_id):

        notes = self.load_notes()

        notes = [
            note
            for note in notes
            if note["id"] != note_id
        ]

        self.save_notes(notes)

    def get_notes(self):

        return self.load_notes()

    def clear_notes(self):

        self.save_notes([])
