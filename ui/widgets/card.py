"""
@file theme_meneger.py
@brief Module of MyDay project.
"""
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGraphicsOpacityEffect,
)


class Card(QFrame):  # Карточка с заголовком, телом и эффектом прозрачности
    def __init__(self,  # Создает карточку с возможностью кастомного виджета или текста
                 title,
                 body_text="",
                 body_widget=None,
                 header_right=None,
                 parent=None
                 ):
        super().__init__(parent)

        self.setObjectName("card")

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(10)

        header = QHBoxLayout()
        header.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        header.addWidget(title_label)
        header.addStretch()

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

        # Эффект для анимации появления
        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(0)
