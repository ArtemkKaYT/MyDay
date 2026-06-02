from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QLineEdit,
    QLayout
)
from PyQt6.QtCore import Qt
from ui.widgets.card import Card
from services.notes_service import NotesService


class NotesWidget(Card):
    def __init__(self, notes_service: NotesService):
        self.notes_service = notes_service

        notes_container = QWidget()
        notes_layout = QVBoxLayout(notes_container)
        notes_layout.setContentsMargins(0, 0, 0, 0)

        notes_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        self.notes_list = QListWidget()

        self.notes_list.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.notes_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.notes_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        notes_layout.addWidget(self.notes_list)

        self.add_note_button = QPushButton(
            "+ Добавить заметку"
        )
        self.add_note_button.clicked.connect(
            self.toggle_note_form
        )

        notes_layout.addWidget(
            self.add_note_button
        )

        self.note_form = QWidget()
        form_layout = QVBoxLayout(self.note_form)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText(
            "Введите заметку"
        )

        save_button = QPushButton(
            "Сохранить заметку"
        )
        save_button.clicked.connect(
            self.add_note
        )

        form_layout.addWidget(
            self.note_input
        )
        form_layout.addWidget(
            save_button
        )

        self.note_form.hide()

        notes_layout.addWidget(
            self.note_form
        )

        super().__init__("Заметки", body_widget=notes_container)

        self.load_notes()
    
    def toggle_note_form(self):

        if self.note_form.isVisible():
            self.note_form.hide()
        else:
            self.note_form.show()
        
        self.adjustSize()
        if self.window():
            self.window().adjustSize()

    def load_notes(self):

        self.notes_list.clear()

        notes = self.notes_service.get_notes()

        for note in notes:
            self.notes_list.addItem(
                note["text"]
            )
        
        self.update_list_height()
    
    def update_list_height(self):

        if self.notes_list.count() == 0:
            self.notes_list.setFixedHeight(0)
            return

        total_height = 0
        for i in range(self.notes_list.count()):
            total_height += self.notes_list.sizeHintForRow(i)

        total_height += self.notes_list.frameWidth() * 2 + 12

        self.notes_list.setFixedHeight(total_height)
        
        self.adjustSize()
        if self.window():
            self.window().adjustSize()

    def add_note(self):

            text = self.note_input.text().strip()
            if not text:
                return

            self.notes_service.add_note(text)
            self.load_notes()
            self.note_input.clear()
            self.note_form.hide()
