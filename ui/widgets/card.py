from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QFrame,
    QGraphicsOpacityEffect
)


class Card(QFrame):
    def __init__(self, title, content):
        super().__init__()

        self.setObjectName("card")

        layout = QVBoxLayout(self)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        content_label = QLabel(content)
        content_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(content_label)

        self.opacity = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(0)
