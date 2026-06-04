"""
Модуль для создания карточки (Card) с заголовком и телом.

Этот модуль содержит Card - базовый виджет для создания
визуальных карточек с заголовком, содержимым и эффектами анимации.

Пример:
    Использование Card::

        from ui.widgets.card import Card

        card = Card(
            title="Мой заголовок",
            body_text="Содержимое карточки"
        )
        card.show()
"""

from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGraphicsOpacityEffect,
)


class Card(QFrame):
    """
    Базовый виджет карточки для отображения контента.

    Этот класс создаёт визуальную карточку с заголовком, опциональным
    заголовком справа и телом (текст или кастомный виджет).
    Включает эффект прозрачности для анимации появления.

    Атрибуты:
        opacity (QGraphicsOpacityEffect): Эффект прозрачности для анимации
    """

    def __init__(self,
                 title,
                 body_text="",
                 body_widget=None,
                 header_right=None,
                 parent=None
                 ):
        """
        Инициализация Card.

        Создаёт карточку с заголовком и опциональным телом (текст или виджет).

        Аргументы:
            title (str): Заголовок карточки.
            body_text (str, optional): Текст содержимого. Используется если
                body_widget не указан. По умолчанию пустая строка.
            body_widget (QWidget, optional): Кастомный виджет для размещения
                в теле карточки. Имеет приоритет над body_text.
            header_right (QWidget, optional): Виджет для размещения справа
                в заголовке (например, кнопка настроек).
            parent (QWidget, optional): Родительский виджет.
        """
        super().__init__(parent)

        self.setObjectName("card")

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(10)

        # Создаём заголовок
        header = QHBoxLayout()
        header.setSpacing(10)

        # Добавляем текст заголовка
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        header.addWidget(title_label)
        header.addStretch()

        # Добавляем виджет справа в заголовок если указан
        if header_right is not None:
            header.addWidget(header_right)

        root.addLayout(header)

        # Добавляем тело карточки (виджет или текст)
        if body_widget is not None:
            root.addWidget(body_widget)
        else:
            content_label = QLabel(body_text)
            content_label.setWordWrap(True)
            content_label.setObjectName("cardText")
            root.addWidget(content_label)

        # Устанавливаем эффект прозрачности для анимации появления
        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(0)
