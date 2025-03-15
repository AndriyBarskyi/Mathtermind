from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from src.ui.theme import ThemeManager

from src.ui.graphs import *
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.pg_main = QtWidgets.QWidget(self)
        self.pg_main.setObjectName("pg_main")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.pg_main)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.w_pg_main1 = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg_main1.sizePolicy().hasHeightForWidth())
        self.w_pg_main1.setSizePolicy(sizePolicy)
        self.w_pg_main1.setMinimumSize(QtCore.QSize(900, 335))
        self.w_pg_main1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        
        # Use theme manager for card background
        self.w_pg_main1.setStyleSheet(f"""
            QWidget {{
                border-radius: 25px;
                background-color: {ThemeManager.get_color('card_background')};
            }}
        """)
        

        self.w_pg_main1.setObjectName("w_pg_main1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.w_pg_main1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lb_con_view = QtWidgets.QLabel(self.w_pg_main1)
        self.lb_con_view.setText("Продовжити перегляд")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.lb_con_view.setSizePolicy(sizePolicy)
        self.lb_con_view.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lb_con_view.setFont(font)
        
        # Use theme manager for label text color
        self.lb_con_view.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        self.lb_con_view.setObjectName("lb_con_view")
        self.gridLayout_2.addWidget(self.lb_con_view, 0, 1, 1, 1)
        self.scrollArea_5 = QtWidgets.QScrollArea(self.w_pg_main1)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(-329, 0, 1816, 250))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_5)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        
        for i in range(1, 10):  # віджети для курсів
            widget = QtWidgets.QWidget(self.scrollAreaWidgetContents_5)
            widget.setMinimumSize(QtCore.QSize(250, 0))
            widget.setMaximumSize(QtCore.QSize(250, 16777215))
            
            # Use theme manager for card styling
            widget.setStyleSheet(f"""
                QWidget {{
                    border-radius: 25px;
                    border: 1px solid {ThemeManager.get_color('border_color')};
                    background-color: {ThemeManager.get_color('card_background')};
                }}
            """)
            
            widget.setObjectName(f"w_pg1_les{i}")
            vertical_layout = QtWidgets.QVBoxLayout(widget)
            vertical_layout.setObjectName(f"verticalLayout_{i}")
            lb_n = QtWidgets.QLabel(widget)
            
            # Use theme manager for label styling
            lb_n.setStyleSheet(f"""
                border: none;
                background-color: transparent;
                color: {ThemeManager.get_color('primary_text')};
                font: 75 14pt "MS Shell Dlg 2";
            """)
            
            lb_n.setObjectName(f"lb_n_les{i}")
            vertical_layout.addWidget(lb_n)
            lb_name_course = QtWidgets.QLabel(widget)
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
            lb_name_course.setSizePolicy(size_policy)
            lb_name_course.setMinimumSize(QtCore.QSize(0, 50))
            lb_name_course.setMaximumSize(QtCore.QSize(16777215, 50))
            
            # Use theme manager for course name label
            lb_name_course.setStyleSheet(f"""
                border-radius: 25px;
                background-color: {ThemeManager.get_color('accent_primary')};
                color: white;
                border: none;
            """)
            
            lb_name_course.setObjectName(f"lb_name_course{i}")
            vertical_layout.addWidget(lb_name_course)
            lb_description = QtWidgets.QLabel(widget)
            
            # Use theme manager for description label
            lb_description.setStyleSheet(f"""
                border: none;
                background-color: transparent;
                color: {ThemeManager.get_color('secondary_text')};
                font: 75 10pt "MS Shell Dlg 2";
            """)
            
            lb_description.setObjectName(f"lb_description{i}")
            vertical_layout.addWidget(lb_description)
            pb = QtWidgets.QProgressBar(widget)
            
            # Use theme manager for progress bar
            pb.setStyleSheet(f"""
                QProgressBar {{
                    border-radius: 8px;
                    background-color: {ThemeManager.get_color('input_background')};
                    color: {ThemeManager.get_color('primary_text')};
                }}
                QProgressBar::chunk {{
                    background-color: {ThemeManager.get_color('accent_primary')};
                    border-radius: 8px;
                }}
            """)
            
            pb.setProperty("value", 24)
            pb.setObjectName(f"pb_les{i}")
            vertical_layout.addWidget(pb)
            self.horizontalLayout_17.addWidget(widget)

        self.horizontalLayout_21.addLayout(self.horizontalLayout_17)
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.gridLayout_2.addWidget(self.scrollArea_5, 1, 1, 1, 1)
        self.btn_next = QtWidgets.QPushButton(self.w_pg_main1)
        
        # Use theme manager for next button
        self.btn_next.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {ThemeManager.get_color('border_color')};
                background-color: {ThemeManager.get_color('button_background')};
                border-radius: 20px;
                width: 40px;
                height: 40px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.get_color('button_hover_background')};
            }}
        """)
        
        self.btn_next.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icon/next.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_next.setIcon(icon9)
        self.btn_next.setIconSize(QtCore.QSize(30, 30))
        self.btn_next.setObjectName("btn_next")
        self.gridLayout_2.addWidget(self.btn_next, 1, 2, 1, 1)
        self.btn_prev = QtWidgets.QPushButton(self.w_pg_main1)
        
        # Use theme manager for prev button
        self.btn_prev.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {ThemeManager.get_color('border_color')};
                background-color: {ThemeManager.get_color('button_background')};
                border-radius: 20px;
                width: 40px;
                height: 40px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.get_color('button_hover_background')};
            }}
        """)
        
        self.btn_prev.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icon/previous.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_prev.setIcon(icon10)
        self.btn_prev.setIconSize(QtCore.QSize(30, 30))
        self.btn_prev.setObjectName("btn_prev")
        self.gridLayout_2.addWidget(self.btn_prev, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.w_pg_main1, 1, 0, 1, 1)
        self.w_pg_main2 = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg_main2.sizePolicy().hasHeightForWidth())
        self.w_pg_main2.setSizePolicy(sizePolicy)
        self.w_pg_main2.setMinimumSize(QtCore.QSize(851, 341))
        
        # Use theme manager for card background
        self.w_pg_main2.setStyleSheet(f"""
            QWidget {{
                border-radius: 25px;
                background-color: {ThemeManager.get_color('card_background')};
            }}
        """)
        
        self.w_pg_main2.setObjectName("w_pg_main2")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.w_pg_main2)
        self.gridLayout_14.setObjectName("gridLayout_14")       

        self.lb_my_courses = QtWidgets.QLabel(self.w_pg_main2)
        self.lb_my_courses.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_my_courses.setText("Курси")
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lb_my_courses.setFont(font)
        
        # Use theme manager for label text color
        self.lb_my_courses.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        self.lb_my_courses.setObjectName("lb_my_courses")
        self.gridLayout_14.addWidget(self.lb_my_courses, 0, 0, 1, 2)

        for i in range(1, 9):
            circular_progress = QtWidgets.QFrame(self.w_pg_main2)
            circular_progress.setMinimumSize(QtCore.QSize(125, 125))
            circular_progress.setMaximumSize(QtCore.QSize(125, 125))
            circular_progress.setFrameShape(QtWidgets.QFrame.StyledPanel)
            circular_progress.setFrameShadow(QtWidgets.QFrame.Raised)
            circular_progress.setObjectName(f"circular_progress_{i}")
            row = (i - 1) // 4 + 1  
            col = (i - 1) % 4       
            self.gridLayout_14.addWidget(circular_progress, row, col, 1, 1)
            
            # Use theme manager for circular progress
            circular_progress.setStyleSheet(f"""
                QWidget {{
                    border-radius: 25px;
                    background-color: {ThemeManager.get_color('accent_primary')};
                }}
            """)
            
            pg1_course = QtWidgets.QLabel(self.w_pg_main2)
            pg1_course.setObjectName(f"pg1_course{i}")
            pg1_course.setMinimumSize(QtCore.QSize(100, 20))
            pg1_course.setMaximumSize(QtCore.QSize(100, 20))
            pg1_course.setText("курс")
            
            # Use theme manager for course label
            pg1_course.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
            
            self.gridLayout_14.addWidget(pg1_course, row + 1, col, 1, 1)  
            


        self.gridLayout_4.addWidget(self.w_pg_main2, 2, 0, 1, 1)
        self.w_pg_main3 = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg_main3.sizePolicy().hasHeightForWidth())
        self.w_pg_main3.setSizePolicy(sizePolicy)
        self.w_pg_main3.setMinimumSize(QtCore.QSize(312, 340))
        self.w_pg_main3.setMaximumSize(QtCore.QSize(500, 16777215))
        
        # Use theme manager for card background
        self.w_pg_main3.setStyleSheet(f"""
            QWidget {{
                border-radius: 25px;
                background-color: {ThemeManager.get_color('card_background')};
            }}
        """)
        
        self.w_pg_main3.setObjectName("w_pg_main3")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.w_pg_main3)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.lb_activity = QtWidgets.QLabel(self.w_pg_main3)
        self.lb_activity.setMinimumSize(QtCore.QSize(0, 50))
        self.lb_activity.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_activity.setText("Активність")
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lb_activity.setFont(font)
        
        # Use theme manager for label text color
        self.lb_activity.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        self.lb_activity.setObjectName("lb_activity")
        self.gridLayout_13.addWidget(self.lb_activity, 0, 0, 1, 1)
        self.graph1 = QtWidgets.QWidget(self.w_pg_main3)
        self.graph1.setObjectName("graph1")
        self.gridLayout_13.addWidget(self.graph1, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.w_pg_main3, 2, 1, 1, 1)
        self.w_pg_main4 = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg_main4.sizePolicy().hasHeightForWidth())
        self.w_pg_main4.setSizePolicy(sizePolicy)
        self.w_pg_main4.setMaximumSize(QtCore.QSize(500, 16777215))
        
        # Use theme manager for card background
        self.w_pg_main4.setStyleSheet(f"""
            QWidget {{
                border-radius: 25px;
                background-color: {ThemeManager.get_color('card_background')};
            }}
        """)
        
        self.w_pg_main4.setObjectName("w_pg_main4")
        self.gridLayout_26 = QtWidgets.QGridLayout(self.w_pg_main4)
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.label_12 = QtWidgets.QLabel(self.w_pg_main4)
        self.label_12.setText("Можливо цікавить")
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_12.setFont(font)
        
        # Use theme manager for label text color
        self.label_12.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        self.label_12.setObjectName("label_12")
        self.gridLayout_26.addWidget(self.label_12, 0, 0, 1, 1)
        self.graph1_2 = QtWidgets.QWidget(self.w_pg_main4)
        self.graph1_2.setMinimumSize(QtCore.QSize(0, 275))
        self.graph1_2.setObjectName("graph1_2")
        self.gridLayout_26.addWidget(self.graph1_2, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.w_pg_main4, 1, 1, 1, 1)
        self.lb_main = QtWidgets.QLabel(self.pg_main)
        self.lb_main.setText("Головна")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lb_main.setFont(font)
        
        # Use theme manager for main label text color
        self.lb_main.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        self.lb_main.setObjectName("lb_main")
        self.gridLayout_4.addWidget(self.lb_main, 0, 0, 1, 1)
        self.setLayout(self.gridLayout_4)
        
        # Connect signals
        self.btn_next.clicked.connect(self.scroll_right)
        self.btn_prev.clicked.connect(self.scroll_left)
        
    def update_theme_styles(self):
        """Update all component styles when theme changes"""
        # Update main cards
        for widget_name in ['w_pg_main1', 'w_pg_main2', 'w_pg_main3', 'w_pg_main4']:
            widget = getattr(self, widget_name)
            widget.setStyleSheet(f"""
                QWidget {{
                    border-radius: 25px;
                    background-color: {ThemeManager.get_color('card_background')};
                }}
            """)
        
        # Update labels
        for label_name in ['lb_con_view', 'lb_my_courses', 'lb_activity', 'label_12', 'lb_main']:
            if hasattr(self, label_name):
                label = getattr(self, label_name)
                label.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        # Update navigation buttons
        for btn_name in ['btn_next', 'btn_prev']:
            btn = getattr(self, btn_name)
            btn.setStyleSheet(f"""
                QPushButton {{
                    border: 1px solid {ThemeManager.get_color('border_color')};
                    background-color: {ThemeManager.get_color('button_background')};
                    border-radius: 20px;
                    width: 40px;
                    height: 40px;
                }}
                QPushButton:hover {{
                    background-color: {ThemeManager.get_color('button_hover_background')};
                }}
            """)
        
        # Update course cards in carousel (scroll area)
        for i in range(1, 10):
            widget_name = f"w_pg1_les{i}"
            # Find the widget in the scroll area
            for child in self.scrollAreaWidgetContents_5.children():
                if child.objectName() == widget_name:
                    # Update the card background
                    child.setStyleSheet(f"""
                        QWidget {{
                            border-radius: 25px;
                            border: 1px solid {ThemeManager.get_color('border_color')};
                            background-color: {ThemeManager.get_color('card_background')};
                        }}
                    """)
                    
                    # Update all labels in the card
                    for label in child.findChildren(QtWidgets.QLabel):
                        if "lb_name_course" in label.objectName():
                            # Course name label with accent background
                            label.setStyleSheet(f"""
                                border-radius: 25px;
                                background-color: {ThemeManager.get_color('accent_primary')};
                                color: white;
                                padding: 8px;
                            """)
                        elif "lb_n" in label.objectName():
                            # Lesson number label
                            label.setStyleSheet(f"""
                                border: none;
                                background-color: transparent;
                                color: {ThemeManager.get_color('primary_text')};
                                font: 75 14pt "MS Shell Dlg 2";
                            """)
                        else:
                            # Other labels
                            label.setStyleSheet(f"""
                                border: none;
                                background-color: transparent;
                                color: {ThemeManager.get_color('secondary_text')};
                            """)
                    
                    # Update all buttons in the card
                    for button in child.findChildren(QtWidgets.QPushButton):
                        button.setStyleSheet(ThemeManager.get_button_style('primary'))
        
        # Update course cards in the second carousel if it exists
        if hasattr(self, 'scrollAreaWidgetContents_6'):
            for i in range(1, 10):
                widget_name = f"w_pg1_course{i}"
                # Find the widget in the scroll area
                for child in self.scrollAreaWidgetContents_6.children():
                    if child.objectName() == widget_name:
                        # Update the card background
                        child.setStyleSheet(f"""
                            QWidget {{
                                border-radius: 25px;
                                border: 1px solid {ThemeManager.get_color('border_color')};
                                background-color: {ThemeManager.get_color('card_background')};
                            }}
                        """)
                        
                        # Update all labels in the card
                        for label in child.findChildren(QtWidgets.QLabel):
                            if "lb_course_name" in label.objectName():
                                # Course name label
                                label.setStyleSheet(f"""
                                    color: {ThemeManager.get_color('primary_text')};
                                    font: 75 14pt "MS Shell Dlg 2";
                                    background-color: transparent;
                                """)
                            else:
                                # Other labels
                                label.setStyleSheet(f"""
                                    color: {ThemeManager.get_color('secondary_text')};
                                    background-color: transparent;
                                """)
                        
                        # Update all buttons in the card
                        for button in child.findChildren(QtWidgets.QPushButton):
                            button.setStyleSheet(ThemeManager.get_button_style('primary'))
        
        # Update activity widgets if they exist
        for widget_name in ['w_pg1_act1', 'w_pg1_act2', 'w_pg1_act3']:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.setStyleSheet(f"""
                    QWidget {{
                        border-radius: 25px;
                        border: 1px solid {ThemeManager.get_color('border_color')};
                        background-color: {ThemeManager.get_color('card_background')};
                    }}
                """)
                
                # Update all labels in the widget
                for label in widget.findChildren(QtWidgets.QLabel):
                    if "lb_title" in label.objectName():
                        label.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
                    else:
                        label.setStyleSheet(f"color: {ThemeManager.get_color('secondary_text')};")
        
    def scroll_left(self):
        """Scroll the course cards to the left"""
        self.scrollArea_5.horizontalScrollBar().setValue(
            self.scrollArea_5.horizontalScrollBar().value() - 300)
        
    def scroll_right(self):
        """Scroll the course cards to the right"""
        self.scrollArea_5.horizontalScrollBar().setValue(
            self.scrollArea_5.horizontalScrollBar().value() + 300)
    
        