from PyQt5.QtGui import QFont, QColor

class COLORS:
    """Color constants used throughout the application"""
    PRIMARY = "#2196F3"
    PRIMARY_LIGHT = "#E3F2FD"
    PRIMARY_DARK = "#1976D2"
    SECONDARY = "#FF9800"
    SECONDARY_LIGHT = "#FFF3E0"
    SUCCESS = "#4CAF50"
    SUCCESS_LIGHT = "#E8F5E9"
    WARNING = "#FFC107"
    WARNING_LIGHT = "#FFF8E1"
    ERROR = "#F44336"
    ERROR_LIGHT = "#FFEBEE"
    GRAY_DARK = "#333333"
    GRAY = "#666666"
    GRAY_LIGHT = "#999999"
    GRAY_LIGHTER = "#CCCCCC"
    BACKGROUND = "#F7F8FA"
    WHITE = "#FFFFFF"
    
    TEXT_PRIMARY = "#0F1D35"
    TEXT_SECONDARY = "#858A94"
    
    BG_PRIMARY = "#FFFFFF"
    BG_SECONDARY = "#F7F8FA"
    
    BORDER_LIGHT = "#E5E7EB"
    BORDER_MEDIUM = "#D1D5DB"
    
    TAG_BG = "#F3F4F6"
    TAG_TEXT = "#858A94"
    
    METADATA_TEXT = "#858A94"

class FONTS:
    """Font constants used throughout the application"""
    H1 = QFont("Inter", 24, QFont.Bold)
    H2 = QFont("Inter", 20, QFont.Bold)
    H3 = QFont("Inter", 18, QFont.Bold)
    H4 = QFont("Inter", 16, QFont.Bold)
    TITLE = QFont("Inter", 16, QFont.Bold)
    SUBTITLE = QFont("Inter", 14)
    BODY = QFont("Inter", 12)
    BODY_SMALL = QFont("Inter", 11)
    SMALL = QFont("Inter", 10)
    TINY = QFont("Inter", 8)
    TAB = QFont("Inter", 14)
    BUTTON = QFont("Inter", 13, QFont.DemiBold)

class STYLES:
    """Style constants used throughout the application"""
    PRIMARY_BUTTON = f"""
        QPushButton {{
            background-color: {COLORS.PRIMARY};
            color: white;
            border: none;
            border-radius: 18px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #1976D2;
        }}
        QPushButton:pressed {{
            background-color: #0D47A1;
        }}
    """
    
    BUTTON_SECONDARY = f"""
        QPushButton {{
            background-color: transparent;
            color: {COLORS.PRIMARY};
            border: 1px solid {COLORS.PRIMARY};
            border-radius: 18px;
            padding: 8px 16px;
        }}
        QPushButton:hover {{
            background-color: {COLORS.PRIMARY_LIGHT};
        }}
        QPushButton:pressed {{
            background-color: #BBDEFB;
        }}
    """
    
    CARD = """
        QFrame {
            background-color: white;
            border-radius: 12px;
            border: 1px solid #E0E0E0;
        }
    """
    
    TAB_BUTTON = """
        QPushButton {
            background-color: transparent;
            border: none;
            padding: 8px 16px;
            color: #858A94;
            border-radius: 20px;
        }
        QPushButton:checked {
            color: #566CD2;
            background-color: #DDE2F6;
            font-weight: 600;
        }
        QPushButton:hover:!checked {
            background-color: #F7F8FA;
        }
    """
    
    FILTER_BUTTON = """
        QPushButton {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 20px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #F7F8FA;
            border-color: #D1D5DB;
        }
    """
    
    CHECKBOX = """
        QCheckBox {
            color: #0F1D35;
        }
        QCheckBox::indicator:checked {
            background-color: #566CD2;
            border-color: #566CD2;
        }
    """ 