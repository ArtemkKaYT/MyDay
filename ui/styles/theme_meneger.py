def get_weather_theme(weather_main: str) -> str:
    THEMES = {
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

    if weather_main in ["Mist", "Fog", "Haze", "Smoke"]:
        cfg = THEMES["Default_Mist"]
    else:
        cfg = THEMES.get(weather_main, THEMES["Clouds"])

    return f"""
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
    """
