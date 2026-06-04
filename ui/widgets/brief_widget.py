"""
Модуль виджета для отображения ежедневной сводки (Brief Widget).

Этот модуль содержит BriefWidget, который отображает персональную
ежедневную сводку с анимированным эффектом печати текста.

Пример:
    Использование BriefWidget::

        from ui.widgets.brief_widget import BriefWidget
        from services.brief_service import BriefService

        brief_service = BriefService(weather_service, schedule_service)
        widget = BriefWidget(brief_service)
        widget.show()
"""

from ui.widgets.type_writer_label import TypeWriterLabel
from services.brief_service import BriefService


class BriefWidget(TypeWriterLabel):
    """
    Виджет для отображения ежедневной сводки с анимацией печати.

    Этот класс наследуется от TypeWriterLabel и отображает
    персональную ежедневную сводку с эффектом печати текста.

    Атрибуты:
        brief_service (BriefService): Сервис для генерации текста сводки.
    """

    def __init__(self, brief_service: BriefService):
        """
        Инициализация BriefWidget.

        Аргументы:
            brief_service (BriefService): Экземпляр сервиса для генерации сводки.
        """
        self.brief_service = brief_service

        # Генерируем текст сводки
        brief_text = self.brief_service.generate_brief()

        # Инициализируем родительский класс с текстом
        super().__init__(brief_text)
        self.setObjectName("briefLabel")
        self.setWordWrap(True)

    def start_animation(self):
        """
        Запустить анимацию печати текста сводки.

        Начинает воспроизведение эффекта печатания текста символ за символом.
        """
        self.start()
