from PyQt5 import QtGui

class ThemeManager:
    """
    Centralized theme management for the application.
    Handles color schemes and theme switching.
    """
    
    # Theme constants
    LIGHT_THEME = "light"
    DARK_THEME = "dark"
    
    # Current theme
    _current_theme = LIGHT_THEME
    
    # Theme color definitions
    _themes = {
        LIGHT_THEME: {
            # Background colors
            "app_background": "rgb(243, 246, 250)",
            "sidebar_background": "rgb(255, 255, 255)",
            "content_background": "rgb(255, 255, 255)",
            "card_background": "rgb(255, 255, 255)",
            "input_background": "rgb(230, 230, 230)",
            "button_background": "rgb(230, 230, 230)",
            "button_hover_background": "rgb(220, 220, 220)",
            
            # Text colors
            "primary_text": "rgb(15, 29, 53)",  # #0F1D35
            "secondary_text": "rgb(133, 138, 148)",  # #858A94
            "button_text": "rgb(15, 29, 53)",
            
            # Border colors
            "border_color": "rgb(229, 231, 235)",  # #E5E7EB
            "border_hover_color": "rgb(209, 213, 219)",  # #D1D5DB
            
            # Accent colors
            "accent_primary": "rgb(86, 108, 210)",  # #566CD2
            "accent_secondary": "rgb(221, 226, 246)",  # #DDE2F6
            "accent_tertiary": "rgb(243, 244, 246)",  # #F3F4F6
            
            # Status colors
            "success": "rgb(34, 197, 94)",  # #22C55E
            "warning": "rgb(234, 179, 8)",  # #EAB308
            "error": "rgb(239, 68, 68)",  # #EF4444
            "info": "rgb(59, 130, 246)",  # #3B82F6
        },
        
        DARK_THEME: {
            # Background colors
            "app_background": "rgb(17, 24, 39)",  # #111827
            "sidebar_background": "rgb(31, 41, 55)",  # #1F2937
            "content_background": "rgb(31, 41, 55)",  # #1F2937
            "card_background": "rgb(55, 65, 81)",  # #374151
            "input_background": "rgb(75, 85, 99)",  # #4B5563
            "button_background": "rgb(75, 85, 99)",  # #4B5563
            "button_hover_background": "rgb(107, 114, 128)",  # #6B7280
            
            # Text colors
            "primary_text": "rgb(255, 255, 255)",  # #FFFFFF
            "secondary_text": "rgb(156, 163, 175)",  # #9CA3AF
            "button_text": "rgb(255, 255, 255)",
            
            # Border colors
            "border_color": "rgb(75, 85, 99)",  # #4B5563
            "border_hover_color": "rgb(107, 114, 128)",  # #6B7280
            
            # Accent colors
            "accent_primary": "rgb(96, 165, 250)",  # #60A5FA
            "accent_secondary": "rgb(59, 130, 246)",  # #3B82F6
            "accent_tertiary": "rgb(55, 65, 81)",  # #374151
            
            # Status colors
            "success": "rgb(34, 197, 94)",  # #22C55E
            "warning": "rgb(234, 179, 8)",  # #EAB308
            "error": "rgb(239, 68, 68)",  # #EF4444
            "info": "rgb(59, 130, 246)",  # #3B82F6
        }
    }
    
    @classmethod
    def get_color(cls, color_name):
        """Get a color from the current theme."""
        return cls._themes[cls._current_theme].get(color_name, "#000000")
    
    @classmethod
    def set_theme(cls, theme_name):
        """Set the current theme."""
        if theme_name in cls._themes:
            cls._current_theme = theme_name
            return True
        return False
    
    @classmethod
    def get_current_theme(cls):
        """Get the current theme name."""
        return cls._current_theme
    
    @classmethod
    def is_dark_mode(cls):
        """Check if the current theme is dark mode."""
        return cls._current_theme == cls.DARK_THEME
    
    @classmethod
    def get_theme_stylesheet(cls):
        """Generate a stylesheet for the current theme."""
        theme = cls._themes[cls._current_theme]
        
        return f"""
        /* Global Styles */
        QWidget {{
            font-family: Inter;
            color: {theme["primary_text"]};
        }}

        /* Main Window */
        QMainWindow {{
            background-color: {theme["app_background"]};
        }}

        /* Central Widget */
        QWidget#centralwidget {{
            background-color: {theme["app_background"]};
        }}

        /* Sidebar */
        QWidget#sidebarContainer {{
            background-color: {theme["sidebar_background"]};
            border-right: 1px solid {theme["border_color"]};
        }}

        /* Sidebar Buttons */
        QWidget#sidebarContainer QPushButton {{
            background-color: {theme["sidebar_background"]};
            color: {theme["primary_text"]};
            border-radius: 25px;
            font-size: 18px;
            min-height: 50px;
            max-height: 100px;
            min-width: 50px;
        }}

        QWidget#sidebarContainer QPushButton:hover {{
            background-color: {theme["button_hover_background"]};
        }}

        QWidget#sidebarContainer QPushButton:checked {{
            font-weight: bold;
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                            stop:0.034 {theme["accent_primary"]}, 
                                            stop:0.039 {theme["sidebar_background"]});
            color: {theme["accent_primary"]};
        }}

        /* Header Container */
        QWidget#headerContainer {{
            background-color: {theme["app_background"]};
        }}

        /* Search Input */
        QLineEdit {{
            background-color: {theme["input_background"]};
            color: {theme["primary_text"]};
            border-radius: 15px;
            padding: 5px 10px;
        }}

        /* Search Button */
        QPushButton#searchButton {{
            background-color: {theme["button_background"]};
            color: {theme["primary_text"]};
            border-radius: 15px;
        }}

        /* Points Button */
        QPushButton#pointsButton {{
            background-color: {theme["app_background"]};
            color: {theme["primary_text"]};
            border-radius: 15px;
        }}

        /* User Button */
        QPushButton#userButton {{
            background-color: {theme["button_background"]};
            color: {theme["primary_text"]};
            border-radius: 15px;
        }}

        /* Content Area */
        QScrollArea {{
            background-color: {theme["app_background"]};
            border: none;
        }}

        QWidget#scrollAreaContent {{
            background-color: {theme["app_background"]};
        }}

        /* Stacked Widget Pages */
        QStackedWidget {{
            background-color: {theme["app_background"]};
        }}

        QWidget#pg_main, QWidget#pg_courses, QWidget#pg_lessons, 
        QWidget#pg_progress, QWidget#pg_settings {{
            background-color: {theme["app_background"]};
        }}
        
        /* Standard Buttons */
        QPushButton {{
            background-color: {theme["button_background"]};
            color: {theme["primary_text"]};
            border-radius: 15px;
            padding: 5px 10px;
            min-height: 30px;
        }}
        
        QPushButton:hover {{
            background-color: {theme["button_hover_background"]};
        }}
        
        /* Primary Action Buttons */
        QPushButton[class="primary"] {{
            background-color: {theme["accent_primary"]};
            color: white;
            border-radius: 25px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        
        QPushButton[class="primary"]:hover {{
            background-color: {theme["accent_secondary"]};
            color: {theme["accent_primary"]};
        }}
        
        /* Card Widgets */
        QWidget[class="with_border"], QFrame[frameShape="6"] {{
            background-color: {theme["card_background"]};
            border-radius: 25px;
            border: 1px solid {theme["border_color"]};
        }}
        
        /* Labels */
        QLabel {{
            color: {theme["primary_text"]};
        }}
        
        QLabel[class="secondary"] {{
            color: {theme["secondary_text"]};
        }}
        
        /* Checkboxes */
        QCheckBox {{
            color: {theme["primary_text"]};
        }}
        
        QCheckBox::indicator {{
            border: 2px solid {theme["border_color"]};
            background-color: {theme["card_background"]};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {theme["accent_primary"]};
            border-color: {theme["accent_primary"]};
        }}
        
        /* Dashboard Cards */
        QWidget#w_pg_main1, QWidget#w_pg_main2, QWidget#w_pg_main3, QWidget#w_pg_main4 {{
            background-color: {theme["card_background"]};
            border-radius: 25px;
            border: 1px solid {theme["border_color"]};
        }}
        
        /* Course and Lesson Cards */
        QWidget[class="course_card"], QWidget[class="lesson_card"] {{
            background-color: {theme["card_background"]};
            border-radius: 25px;
            border: 1px solid {theme["border_color"]};
        }}
        
        /* Card Descriptions */
        QLabel[class="description"] {{
            color: {theme["secondary_text"]};
        }}
        
        /* Navigation Buttons */
        QPushButton#btn_next, QPushButton#btn_prev {{
            background-color: {theme["button_background"]};
            border: 1px solid {theme["border_color"]};
            border-radius: 20px;
        }}
        
        QPushButton#btn_next:hover, QPushButton#btn_prev:hover {{
            background-color: {theme["button_hover_background"]};
        }}
        """
    
    @classmethod
    def get_card_style(cls):
        """Get card style for course and lesson cards."""
        theme = cls._themes[cls._current_theme]
        
        return f"""
            QFrame {{
                background-color: {theme["card_background"]};
                border-radius: 25px;
                border: 1px solid {theme["border_color"]};
            }}
            QFrame:hover {{
                border: 1px solid {theme["border_hover_color"]};
            }}
            QLabel {{
                color: {theme["primary_text"]};
                background-color: transparent;
                border: none;
            }}
            QLabel[class="metadata"], QLabel[class="secondary"] {{
                color: {theme["secondary_text"]};
            }}
        """
    
    @classmethod
    def get_button_style(cls, button_type='default'):
        """Get the style for buttons based on type"""
        if button_type == 'primary':
            return f"""
                QPushButton {{
                    background-color: {cls.get_color('accent_primary')};
                    color: white;
                    border-radius: 18px;
                    padding: 0 16px;
                }}
                QPushButton:hover {{
                    background-color: {cls.get_color('accent_primary_hover')};
                }}
            """
        elif button_type == 'secondary':
            return f"""
                QPushButton {{
                    background-color: transparent;
                    border: 1px solid {cls.get_color('accent_primary')};
                    color: {cls.get_color('accent_primary')};
                    border-radius: 18px;
                    padding: 0 16px;
                }}
                QPushButton:hover {{
                    background-color: {cls.get_color('accent_secondary')};
                }}
            """
        else:  # default
            return f"""
                QPushButton {{
                    background-color: {cls.get_color('button_background')};
                    color: {cls.get_color('primary_text')};
                    border-radius: 18px;
                    padding: 0 16px;
                }}
                QPushButton:hover {{
                    background-color: {cls.get_color('button_hover_background')};
                }}
            """
    
    @classmethod
    def get_start_button_style(cls):
        """Get the style for start buttons"""
        return f"""
            QPushButton {{
                background-color: {cls.get_color('accent_primary')};
                color: white;
                border-radius: 18px;
                padding: 0 16px;
            }}
            QPushButton:hover {{
                background-color: {cls.get_color('accent_primary_hover')};
            }}
        """
    
    @classmethod
    def get_input_style(cls):
        """Get input field style."""
        theme = cls._themes[cls._current_theme]
        
        return f"""
            QLineEdit {{
                background-color: {theme["input_background"]};
                color: {theme["primary_text"]};
                border-radius: 15px;
                padding: 5px 10px;
                border: 1px solid {theme["border_color"]};
            }}
            QLineEdit:focus {{
                border: 2px solid {theme["accent_primary"]};
            }}
        """ 