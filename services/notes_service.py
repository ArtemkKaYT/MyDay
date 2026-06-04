"""
@file theme_meneger.py
@brief Module of MyDay project.
"""
import json
import uuid
from pathlib import Path
from datetime import date


class NotesService:  # Сервис для работы с заметками

    def __init__(self, file_path="data/notes.json"):  # Инициализация с указанием пути к файлу
        self.file_path = Path(file_path)

        # Создаем файл, если его нет
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def load_notes(self):  # Загружает заметки из JSON файла
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_notes(self, notes):  # Сохраняет заметки в JSON файл
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                notes,
                file,
                ensure_ascii=False,
                indent=4
            )

    def add_note(self, text):  # Добавляет новую заметку с уникальным ID
        notes = self.load_notes()

        new_note = {
            "id": str(uuid.uuid4()),
            "text": text,
            "created_at": str(date.today())
        }

        notes.append(new_note)

        self.save_notes(notes)

    def delete_note(self, note_id):  # Удаляет заметку по ID
        notes = self.load_notes()

        notes = [
            note
            for note in notes
            if note["id"] != note_id
        ]

        self.save_notes(notes)

    def get_notes(self):  # Возвращает список всех заметок
        return self.load_notes()

    def clear_notes(self):  # Удаляет все заметки
        self.save_notes([])
