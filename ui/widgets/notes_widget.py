"""
@file theme_meneger.py
@brief Module of MyDay project.
"""
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QLayout
)
from PyQt6.QtCore import Qt
from ui.widgets.card import Card
from services.notes_service import NotesService


class NotesWidget(Card):  # Виджет для отображения и управления заметками
    def __init__(self, notes_service: NotesService):  # Принимает сервис заметок
        self.notes_service = notes_service

        notes_container = QWidget()
        notes_layout = QVBoxLayout(notes_container)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        notes_layout.setSpacing(10)
        notes_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        self.notes_list_container = QWidget()
        self.notes_list_layout = QVBoxLayout(self.notes_list_container)
        self.notes_list_layout.setContentsMargins(0, 0, 0, 0)
        self.notes_list_layout.setSpacing(6)

        self.add_note_button = QPushButton("+ Добавить заметку")
        self.add_note_button.clicked.connect(self.toggle_note_form)

        notes_layout.addWidget(self.notes_list_container)
        notes_layout.addWidget(self.add_note_button)

        self.note_form = QWidget()
        form_layout = QVBoxLayout(self.note_form)
        form_layout.setContentsMargins(0, 4, 0, 0)
        form_layout.setSpacing(6)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Введите заметку")

        self.note_input.returnPressed.connect(self.add_note)

        save_button = QPushButton("Сохранить заметку")
        save_button.clicked.connect(self.add_note)

        form_layout.addWidget(self.note_input)
        form_layout.addWidget(save_button)

        self.note_form.hide()
        notes_layout.addWidget(self.note_form)

        super().__init__("Заметки", body_widget=notes_container)
        self.load_notes()

    def toggle_note_form(self):  # Показывает/скрывает форму добавления заметки
        self.note_form.setVisible(not self.note_form.isVisible())

    def clear_notes_layout(self):  # Очищает список заметок
        while self.notes_list_layout.count():
            item = self.notes_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_notes(self):  # Загружает и отображает все заметки из сервиса
        self.clear_notes_layout()
        notes = self.notes_service.get_notes()

        if not notes:
            no_notes_label = QLabel("Заметок пока нет")
            no_notes_label.setObjectName("noNotesLabel")
            self.notes_list_layout.addWidget(no_notes_label)
            return

        for note in notes:
            row_widget = QWidget()
            row_widget.setObjectName("noteRow")
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(10, 8, 10, 8)
            row_layout.setSpacing(10)

            checkbox = QCheckBox()
            checkbox.setObjectName("noteCheckBox")
            checkbox.clicked.connect(lambda _, note_id=note["id"]: self.delete_note(note_id))

            text_label = QLabel(note["text"])
            text_label.setObjectName("noteText")
            text_label.setWordWrap(True)

            row_layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignVCenter)
            row_layout.addWidget(text_label, stretch=1, alignment=Qt.AlignmentFlag.AlignVCenter)

            self.notes_list_layout.addWidget(row_widget)

    def add_note(self):  # Добавляет новую заметку из поля ввода
        text = self.note_input.text().strip()
        if not text:
            return

        self.notes_service.add_note(text)
        self.load_notes()
        self.note_input.clear()
        self.note_form.hide()

    def delete_note(self, note_id):  # Удаляет заметку по ID
        self.notes_service.delete_note(note_id)
        self.load_notes()
