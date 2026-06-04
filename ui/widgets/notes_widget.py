"""
Модуль виджета для работы с заметками (Notes Widget).

Этот модуль содержит NotesWidget - визуальный компонент для создания,
отображения и удаления заметок с персистентным хранилищем.

Пример:
    Использование NotesWidget::

        from ui.widgets.notes_widget import NotesWidget
        from services.notes_service import NotesService

        notes_service = NotesService()
        widget = NotesWidget(notes_service)
        widget.show()
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


class NotesWidget(Card):
    """
    Виджет для отображения и управления заметками.

    Этот класс предоставляет интерфейс для создания, просмотра и удаления
    заметок. Заметки хранятся в JSON файле и отображаются в виде списка.

    Атрибуты:
        notes_service (NotesService): Сервис для управления заметками
        notes_list_container (QWidget): Контейнер для списка заметок
        note_form (QWidget): Форма для добавления новой заметки
        note_input (QLineEdit): Поле ввода для текста заметки
    """

    def __init__(self, notes_service: NotesService):
        """
        Инициализация NotesWidget.

        Создаёт виджет с кнопкой добавления заметки и формой для ввода.

        Аргументы:
            notes_service (NotesService): Экземпляр сервиса для работы с заметками.
        """
        self.notes_service = notes_service

        # Создаём контейнер для заметок
        notes_container = QWidget()
        notes_layout = QVBoxLayout(notes_container)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        notes_layout.setSpacing(10)
        notes_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        # Создаём контейнер для списка заметок
        self.notes_list_container = QWidget()
        self.notes_list_layout = QVBoxLayout(self.notes_list_container)
        self.notes_list_layout.setContentsMargins(0, 0, 0, 0)
        self.notes_list_layout.setSpacing(6)

        # Кнопка для добавления заметки
        self.add_note_button = QPushButton("+ Добавить заметку")
        self.add_note_button.clicked.connect(self.toggle_note_form)

        notes_layout.addWidget(self.notes_list_container)
        notes_layout.addWidget(self.add_note_button)

        # Создаём форму для добавления заметки
        self.note_form = QWidget()
        form_layout = QVBoxLayout(self.note_form)
        form_layout.setContentsMargins(0, 4, 0, 0)
        form_layout.setSpacing(6)

        # Поле ввода для текста заметки
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Введите заметку")

        # Добавляем заметку при нажатии Enter
        self.note_input.returnPressed.connect(self.add_note)

        # Кнопка сохранения
        save_button = QPushButton("Сохранить заметку")
        save_button.clicked.connect(self.add_note)

        form_layout.addWidget(self.note_input)
        form_layout.addWidget(save_button)

        # Скрываем форму по умолчанию
        self.note_form.hide()
        notes_layout.addWidget(self.note_form)

        # Инициализируем родительский класс Card
        super().__init__("Заметки", body_widget=notes_container)
        
        # Загружаем заметки
        self.load_notes()

    def toggle_note_form(self):
        """
        Переключить видимость формы добавления заметки.

        Показывает форму если она скрыта, или скрывает если она видна.
        """
        self.note_form.setVisible(not self.note_form.isVisible())

    def clear_notes_layout(self):
        """
        Очистить список заметок.

        Удаляет все виджеты заметок из макета списка.
        """
        while self.notes_list_layout.count():
            item = self.notes_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_notes(self):
        """
        Загрузить и отобразить все заметки из сервиса.

        Получает все заметки из хранилища и создаёт визуальные элементы
        для каждой заметки с чекбоксом для удаления.
        """
        self.clear_notes_layout()
        notes = self.notes_service.get_notes()

        # Если заметок нет, показываем сообщение
        if not notes:
            no_notes_label = QLabel("Заметок пока нет")
            no_notes_label.setObjectName("noNotesLabel")
            self.notes_list_layout.addWidget(no_notes_label)
            return

        # Создаём визуальный элемент для каждой заметки
        for note in notes:
            row_widget = QWidget()
            row_widget.setObjectName("noteRow")
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(10, 8, 10, 8)
            row_layout.setSpacing(10)

            # Чекбокс для удаления заметки
            checkbox = QCheckBox()
            checkbox.setObjectName("noteCheckBox")
            checkbox.clicked.connect(lambda _, note_id=note["id"]: self.delete_note(note_id))

            # Текст заметки
            text_label = QLabel(note["text"])
            text_label.setObjectName("noteText")
            text_label.setWordWrap(True)

            row_layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignVCenter)
            row_layout.addWidget(text_label, stretch=1, alignment=Qt.AlignmentFlag.AlignVCenter)

            self.notes_list_layout.addWidget(row_widget)

    def add_note(self):
        """
        Добавить новую заметку из поля ввода.

        Получает текст из поля ввода, добавляет его в сервис,
        перезагружает список и очищает форму.
        """
        text = self.note_input.text().strip()
        if not text:
            return

        self.notes_service.add_note(text)
        self.load_notes()
        self.note_input.clear()
        self.note_form.hide()

    def delete_note(self, note_id):
        """
        Удалить заметку по идентификатору.

        Аргументы:
            note_id (str): ID заметки для удаления.
        """
        self.notes_service.delete_note(note_id)
        self.load_notes()
