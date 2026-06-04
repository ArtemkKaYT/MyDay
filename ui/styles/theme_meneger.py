def get_weather_theme(weather_main: str) -> str:  # Возвращает CSS стиль в зависимости от погоды
    THEMES = {  # Словарь с цветовыми схемами для типов погоды
        "Clear": {
            "bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1A263E, stop:0.5 #11141A, stop:1 #2D2214)",
            "card": "#161A24",
            "accent": "#FBBF24"
        },
        "Rain": {
            "bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1A2433, stop:0.6 #0F131A, stop:1 #141A24)",
            "card": "#161B24",
            "accent": "#60A5FA"
        },
        "Snow": {
            "bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2E3138, stop:0.6 #16171A, stop:1 #252830)",
            "card": "#1E2026",
            "accent": "#E2E8F0"
        },
        "Thunderstorm": {
            "bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1A122B, stop:0.6 #090611, stop:1 #0F0F12)",
            "card": "#130F1C",
            "accent": "#A855F7"
        },
        "Clouds": {
            "bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #242427, stop:0.6 #121214, stop:1 #1C1C1F)",
            "card": "#18181B",
            "accent": "#A1A1AA"
        },
        "Default_Mist": {
            "bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #131C1A, stop:0.6 #0A0F0D, stop:1 #121715)",
            "card": "#121816",
            "accent": "#2DD4BF"
        }
    }

    # Для тумана используем Default_Mist
    if weather_main in ["Mist", "Fog", "Haze", "Smoke"]:
        cfg = THEMES["Default_Mist"]
    else:
        cfg = THEMES.get(weather_main, THEMES["Clouds"])

    return f"""  # Формируем строку со стилями CSS
        QWidget {{
            background-color: {cfg['bg']};
            color: #E2E8F0;
            font-size: 14px;
            font-family: "Segoe UI", sans-serif;
        }}

        QScrollArea QWidget {{
            background-color: transparent;
        }}

        #timeLabel {{
            font-size: 32px;
            font-weight: 800;
            color: #FFFFFF;
        }}

        #dateLabel {{
            font-size: 16px;
            color: #71717A;
        }}

        #briefLabel {{
            font-size: 15px;
            padding: 18px;
            background-color: {cfg['card']};
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
        }}

        #card {{
            background-color: {cfg['card']};
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 20px;
        }}

        #cardTitle {{
            font-size: 16px;
            font-weight: 700;
            color: #FFFFFF;
        }}

        #cardText {{
            color: #A1A1AA;
        }}

        #weatherIcon {{
            font-size: 38px;
            background-color: transparent;
        }}

        #weatherTemp {{
            font-size: 24px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: transparent;
        }}

        #weatherStatus {{
            font-size: 13px;
            color: {cfg['accent']};
            background-color: transparent;
        }}

        #eventIcon {{
            font-size: 16px;
            background-color: transparent;
        }}

        #eventTime {{
            font-size: 14px;
            font-weight: 600;
            color: #71717A; /* Приглушенный серый для времени */
            background-color: transparent;
            min-width: 90px; /* Чтобы время всегда занимало одинаковую ширину */
        }}

        #eventTitle {{
            font-size: 15px;
            font-weight: 500;
            color: #FFFFFF; /* Белый для самого события */
            background-color: transparent;
        }}

        #noEventsLabel {{
            color: #71717A;
            font-style: italic;
            padding: 8px 0;
        }}

        #noteRow {{
            background-color: #1E1E24; /* Чуть светлее фона карточки */
            border: 1px solid #2D2D34;
            border-radius: 8px;
        }}

        #noteText {{
            font-size: 14px;
            color: #E4E4E7;
            background-color: transparent;
        }}

        QCheckBox#noteCheckBox {{
            spacing: 0px;
            background-color: transparent;
        }}

        QCheckBox#noteCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid #52525B;
            border-radius: 5px;
            background-color: transparent;
        }}

        QCheckBox#noteCheckBox::indicator:hover {{
            border-color: #A1A1AA;
        }}

        QCheckBox#noteCheckBox::indicator:checked {{
            background-color: #10B981;
            border-color: #10B981;
        }}

        #noNotesLabel {{
            color: #71717A;
            font-style: italic;
            padding: 8px 0;
        }}

        QPushButton {{
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #E2E8F0;
            padding: 10px 16px;
            border-radius: 12px;
            font-weight: 600;
        }}

        QPushButton:hover {{
            background-color: rgba(255, 255, 255, 0.08);
            border: 1px solid #E2E8F0;
        }}

        QPushButton:pressed {{
            background-color: rgba(0, 0, 0, 0.2);
        }}

        QListWidget::item {{
            background-color: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.03);
            padding: 12px;
            margin-bottom: 6px;
            border-radius: 10px;
        }}

        QLineEdit, QComboBox, QDateEdit, QSpinBox {{
            background-color: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 8px 12px;
            color: white;
        }}

        QLineEdit:focus, QComboBox:focus {{
            border: 1px solid {cfg['accent']};
        }}

        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 8px;
        }}
        QScrollBar::handle:vertical {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            min-height: 40px;
        }}

        #weatherSettingsBtn {{
            background-color: transparent;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            color: #71717A;
            padding: 2px;
        }}

        #weatherSettingsBtn:hover {{
            color: #FFFFFF;
            background-color: #27272A;
        }}
    """
