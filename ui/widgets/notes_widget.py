from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QInputDialog
)
from ui.widgets.card import Card
from services.notes_service import NotesService


class NotesWidget(Card):
    def __init__(self, notes_service: NotesService):
        self.notes_service = notes_service

        notes_container = QWidget()
        notes_layout = QVBoxLayout(notes_container)
        notes_layout.setContentsMargins(0, 0, 0, 0)

        self.notes_list = QListWidget()
        notes_layout.addWidget(self.notes_list)

        super().__init__("Заметки", body_widget=notes_container)

        self.load_notes()

    def load_notes(self):

        self.notes_list.clear()

        notes = self.notes_service.get_notes()

        for note in notes:
            self.notes_list.addItem(
                note["text"]
            )

    def add_note(self):

        text, ok = QInputDialog.getText(
            self,
            "Добавить заметку",
            "Введите заметку:"
        )

        if ok and text.strip():

            self.notes_service.add_note(
                text.strip()
            )

            self.load_notes()
