"""
Модуль сервиса для работы с заметками (Notes Service).

Этот модуль предоставляет функциональность управления заметками, включая:

- Создание и сохранение заметок
- Удаление заметок по идентификатору
- Загрузку всех сохранённых заметок
- Очистку всех заметок
- Персистентное хранилище на базе JSON файлов

Заметки хранятся в JSON формате с уникальными ID и датой создания.

Пример:
    Использование NotesService::

        from services.notes_service import NotesService

        notes_service = NotesService()
        
        # Добавить заметку
        notes_service.add_note("Купить молоко")
        
        # Получить все заметки
        all_notes = notes_service.get_notes()
        
        # Удалить заметку по ID
        notes_service.delete_note("note_id")
"""

import json
import uuid
from pathlib import Path
from datetime import date


class NotesService:
    """
    Сервис для управления заметками пользователя.

    Этот класс обеспечивает функциональность создания, удаления,
    загрузки и сохранения заметок. Заметки хранятся в JSON файле
    с автоматическим генерированием уникальных ID для каждой заметки.

    Атрибуты:
        file_path (Path): Путь к JSON файлу для хранения заметок.
    """

    def __init__(self, file_path="data/notes.json"):
        """
        Инициализация NotesService.

        Создаёт JSON файл хранилища, если он не существует.

        Аргументы:
            file_path (str, optional): Путь к JSON файлу. По умолчанию
                'data/notes.json'.
        """
        self.file_path = Path(file_path)

        # Создаём файл и директорию, если они не существуют
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def load_notes(self):
        """
        Загрузить все заметки из JSON файла.

        Возвращает:
            list: Список всех заметок. Каждая заметка содержит
                ключи 'id', 'text' и 'created_at'.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_notes(self, notes):
        """
        Сохранить заметки в JSON файл.

        Аргументы:
            notes (list): Список заметок для сохранения.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                notes,
                file,
                ensure_ascii=False,
                indent=4
            )

    def add_note(self, text):
        """
        Добавить новую заметку.

        Создаёт новую заметку с уникальным ID (UUID),
        текстом и датой создания, затем сохраняет её в файл.

        Аргументы:
            text (str): Текст заметки.
        """
        notes = self.load_notes()

        new_note = {
            "id": str(uuid.uuid4()),
            "text": text,
            "created_at": str(date.today())
        }

        notes.append(new_note)

        self.save_notes(notes)

    def delete_note(self, note_id):
        """
        Удалить заметку по идентификатору.

        Находит и удаляет заметку с указанным ID.

        Аргументы:
            note_id (str): ID заметки для удаления.
        """
        notes = self.load_notes()

        notes = [
            note
            for note in notes
            if note["id"] != note_id
        ]

        self.save_notes(notes)

    def get_notes(self):
        """
        Получить все заметки.

        Возвращает:
            list: Список всех сохранённых заметок.
        """
        return self.load_notes()

    def clear_notes(self):
        """
        Удалить все заметки.

        Очищает хранилище заметок полностью.
        """
        self.save_notes([])
