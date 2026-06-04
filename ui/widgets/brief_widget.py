"""
@file theme_meneger.py
@brief Module of MyDay project.
"""
from ui.widgets.type_writer_label import TypeWriterLabel
from services.brief_service import BriefService


class BriefWidget(TypeWriterLabel):  # Виджет с анимированным выводом сводки дня
    def __init__(self, brief_service: BriefService):  # Принимает сервис для генерации текста
        self.brief_service = brief_service

        brief_text = self.brief_service.generate_brief()

        super().__init__(brief_text)
        self.setObjectName("briefLabel")
        self.setWordWrap(True)

    def start_animation(self):  # Запускает анимацию печати текста
        self.start()
