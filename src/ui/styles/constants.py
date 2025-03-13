from PyQt6.QtGui import QFont

class COLORS:
    """Color constants used throughout the application"""
    PRIMARY = "#566CD2"
    PRIMARY_LIGHT = "#DDE2F6"
    PRIMARY_DARK = "#4A5EBF"
    
    SUCCESS = "#10B981"
    SUCCESS_LIGHT = "#ECFDF5"
    
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
    H1 = QFont("Inter", 24, QFont.Weight.Bold)
    H2 = QFont("Inter", 20, QFont.Weight.Bold)
    TITLE = QFont("Inter", 16, QFont.Weight.Bold)
    SUBTITLE = QFont("Inter", 14, QFont.Weight.Bold)
    BODY = QFont("Inter", 13)
    BODY_SMALL = QFont("Inter", 11)
    BUTTON = QFont("Inter", 13, QFont.Weight.DemiBold)
    TAB = QFont("Inter", 14)

class STYLES:
    """Style constants used throughout the application"""
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
    
    PRIMARY_BUTTON = """
        QPushButton {
            background-color: #566CD2;
            color: white;
            border-radius: 18px;
        }
        QPushButton:hover {
            background-color: #4A5EBF;
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