from ui.widgets.type_writer_label import TypeWriterLabel
from services.brief_service import BriefService


class BriefWidget(TypeWriterLabel):
    def __init__(self, brief_service: BriefService):
        self.brief_service = brief_service

        brief_text = self.brief_service.generate_brief()

        super().__init__(brief_text)
        self.setObjectName("briefLabel")
        self.setWordWrap(True)

    def start_animation(self):
        self.start()
