from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QSizePolicy, QScrollArea, QFrame
from PyQt5 import QtWidgets, QtCore, QtGui

class Page3(QWidget):    
    def create_card(self, title_text="Назва", labels_text=("TextLabel1", "TextLabel2"), desc_text="Опис"):
        card = QtWidgets.QWidget()
        card.setMinimumSize(QtCore.QSize(320, 420))
        card.setMaximumSize(QtCore.QSize(320, 420))
        card.setObjectName("courseCard")
        card.setStyleSheet("""
            QWidget#courseCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }
            QWidget#courseCard:hover {
                border-color: #D1D5DB;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            }
        """)
        
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)
    
        title = QtWidgets.QLabel(title_text)
        title.setObjectName("courseTitle")
        title.setStyleSheet("""
            QLabel#courseTitle {
                color: #0F1D35;
                font-weight: 600;
                font-size: 18px;
                min-height: 60px;
                max-height: 60px;
            }
        """)
        
        # Tags
        labels = QtWidgets.QHBoxLayout()
        labels.setSpacing(8)
        for text in labels_text:
            lb_subject = QtWidgets.QLabel(text)
            lb_subject.setObjectName("courseTag")
            lb_subject.setStyleSheet("""
                QLabel#courseTag {
                    background-color: #F3F4F6;
                    color: #858A94;
                    border: none;
                    border-radius: 12px;
                    padding: 4px 12px;
                    font-size: 12px;
                    font-weight: 500;
                    min-height: 24px;
                    max-height: 24px;
                }
            """)
            labels.addWidget(lb_subject)
        
        lb_description = QtWidgets.QLabel(desc_text)
        lb_description.setObjectName("courseDescription")
        lb_description.setStyleSheet("""
            QLabel#courseDescription {
                color: #858A94;
                line-height: 1.5;
                font-size: 14px;
                min-height: 120px;
                max-height: 120px;
            }
        """)
        
        stacked_widget = QtWidgets.QStackedWidget()
        stacked_widget.setMaximumSize(QtCore.QSize(16777215, 75))
        stacked_widget.setStyleSheet("border: none;")

        page_start = QtWidgets.QWidget()
        layout_start = QtWidgets.QGridLayout(page_start)
        layout_start.setContentsMargins(0, 0, 0, 0)

        btn_start = QtWidgets.QPushButton("Start Course")
        btn_start.setObjectName("startButton")
        btn_start.setMinimumSize(QtCore.QSize(288, 36))
        btn_start.setStyleSheet("""
            QPushButton#startButton {
                background-color: #566CD2;
                color: #FFFFFF;
                border: none;
                border-radius: 18px;
                padding: 8px 24px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton#startButton:hover {
                background-color: #4557B9;
            }
        """)
        
        layout_start.addWidget(btn_start, 0, 0, 1, 1)

        page_start.setLayout(layout_start)

        page_continue = QtWidgets.QWidget()
        layout_continue = QtWidgets.QGridLayout(page_continue)
        layout_continue.setContentsMargins(0, 0, 0, 0)
        layout_continue.setSpacing(8)

        btn_continue = QtWidgets.QPushButton("Continue")
        btn_continue.setObjectName("continueButton")
        btn_continue.setMinimumSize(QtCore.QSize(288, 36))
        btn_continue.setStyleSheet("""
            QPushButton#continueButton {
                background-color: #566CD2;
                color: #FFFFFF;
                border: none;
                border-radius: 18px;
                padding: 8px 24px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton#continueButton:hover {
                background-color: #4557B9;
            }
        """)

        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setObjectName("progressBar")
        progress_bar.setMinimumSize(QtCore.QSize(288, 10))
        progress_bar.setStyleSheet("""
            QProgressBar#progressBar {
                border: 2px solid #F3F4F6;
                border-radius: 8px;
                background-color: #F3F4F6;
                height: 10px;
            }
            QProgressBar#progressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #566CD2, stop: 1 #7A8FE6);
                border-radius: 6px;
            }
        """)
        progress_bar.setMaximum(100)
        progress_bar.setValue(1)
        
        layout_continue.addWidget(btn_continue, 0, 0, 1, 1)
        layout_continue.addWidget(progress_bar, 1, 0, 1, 1)

        page_continue.setLayout(layout_continue)

        stacked_widget.addWidget(page_start)
        stacked_widget.addWidget(page_continue)

        def switch_to_continue():
            stacked_widget.setCurrentWidget(page_continue)

        btn_start.clicked.connect(switch_to_continue)
        card_layout.addWidget(title)
        card_layout.addLayout(labels)
        card_layout.addWidget(lb_description)
        card_layout.addWidget(stacked_widget)
        return card

    def create_section(self, section_title="Розділ", num_cards=4):
        section_widget = QtWidgets.QWidget()
        section_layout = QtWidgets.QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(16)
        
        section_label = QtWidgets.QLabel(section_title)
        section_label.setObjectName("section_title")
        section_label.setStyleSheet("""
            QLabel#section_title {
                color: #0F1D35;
                font-weight: 600;
                font-size: 16px;
                margin: 20px 0 10px 0;
            }
        """)
        section_layout.addWidget(section_label)
        
        cards_container = QtWidgets.QWidget()
        cards_layout = QtWidgets.QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(16)
        cards_layout.setAlignment(QtCore.Qt.AlignLeft)
        
        for _ in range(num_cards):
            card = self.create_card()
            cards_layout.addWidget(card)
            
        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        cards_layout.addItem(spacer)

        section_layout.addWidget(cards_container)
        return section_widget

    def add_new_tab(self, name="Нова вкладка", sections_data=None):
        new_tab = QtWidgets.QWidget()
        new_tab.setObjectName(name)
        
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        scroll_area_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_area_widget)
        scroll_layout.setContentsMargins(16, 16, 16, 16)
        scroll_layout.setSpacing(24)
        
        if sections_data:
            for section_title, num_cards in sections_data:
                section_widget = self.create_section(section_title, num_cards)
                scroll_layout.addWidget(section_widget)
                
        scroll_area.setWidget(scroll_area_widget)
        
        tab_layout = QtWidgets.QVBoxLayout(new_tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area)
        
        self.tabWidget_3.addTab(new_tab, name)

    def __init__(self):
        super().__init__()
        self.pg_lessons = QtWidgets.QWidget()
        self.pg_lessons.setObjectName("pg_lessons")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.pg_lessons)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_9.setContentsMargins(16, 16, 16, 16)
        self.gridLayout_9.setSpacing(16)
        
        self.lb_lessons = QtWidgets.QLabel(self.pg_lessons)
        self.lb_lessons.setText("Уроки")
        self.lb_lessons.setObjectName("pageTitle")
        self.lb_lessons.setStyleSheet("""
            QLabel#pageTitle {
                color: #0F1D35;
                font-weight: 600;
                font-size: 24px;
                margin-bottom: 8px;
            }
        """)
        self.gridLayout_9.addWidget(self.lb_lessons, 0, 0, 1, 1)
        
        self.tabWidget_3 = QtWidgets.QTabWidget(self.pg_lessons)
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tabWidget_3.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background: #DDE2F6;
                color: #566CD2;
                border: 1px solid #E5E7EB;
                border-radius: 15px;
                padding: 10px 20px;
                margin-right: 5px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background: #566CD2;
                color: #FFFFFF;
                font-weight: 600;
            }
            QTabBar::tab:hover {
                background: #C5CFEF;
            }
        """)
        self.gridLayout_9.addWidget(self.tabWidget_3, 2, 0, 1, 1)
        
        self.lb_choice = QtWidgets.QLabel(self.pg_lessons)
        self.lb_choice.setText("Виберіть курс:")
        self.lb_choice.setObjectName("subtitle")
        self.lb_choice.setStyleSheet("""
            QLabel#subtitle {
                color: #0F1D35;
                font-weight: 500;
                font-size: 16px;
                margin-bottom: 16px;
            }
        """)
        self.gridLayout_9.addWidget(self.lb_choice, 1, 0, 1, 1)
        
        self.add_new_tab("Перша вкладка", [
            ("Розділ 1", 3),  
            ("Розділ 2", 5), 
            ("Розділ 3", 2)   
        ])

        self.add_new_tab("Друга вкладка", [
            ("Розділ 1", 4),
            ("Розділ 2", 3)
        ])
        
        self.setLayout(self.gridLayout_9)