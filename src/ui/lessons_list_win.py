from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from main_page import *
from lesson_win import Lesson_page


class Lessons_page(QWidget):    
    def __init__(self,stack=None, lesson_page=None):
        super().__init__()
        self.stack = None
        self.pg_lesson = None
        self.stack = stack
        self.pg_lesson = lesson_page

        self.pg_lessons = QtWidgets.QWidget()
        self.pg_lessons.setObjectName("pg_lessons")
        self.main_lessons_layout = QtWidgets.QGridLayout(self.pg_lessons)
        self.main_lessons_layout.setObjectName("main_lessons_layout")
        
        self.lb_lessons = QtWidgets.QLabel(self.pg_lessons)
        self.lb_lessons.setText("Уроки")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.lb_lessons.setSizePolicy(sizePolicy)
        self.lb_lessons.setMinimumSize(QtCore.QSize(0, 50))
        self.lb_lessons.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_lessons.setProperty("type", "title")
        
        self.lb_lessons.setObjectName("lb_lessons")
        self.main_lessons_layout.addWidget(self.lb_lessons, 0, 0, 1, 1)
        self.lessons_tab_widget = QtWidgets.QTabWidget(self.pg_lessons)
        self.lessons_tab_widget.setMinimumSize(QtCore.QSize(660, 300))
        self.lessons_tab_widget.setObjectName("lessons_tab_widget")
        
        self.main_lessons_layout.addWidget(self.lessons_tab_widget, 2, 0, 1, 1)
        self.lb_choice = QtWidgets.QLabel(self.pg_lessons)
        self.lb_choice.setText("Виберіть курс:")
        self.lb_choice.setSizePolicy(sizePolicy)
        self.lb_choice.setMinimumSize(QtCore.QSize(0, 50))
        self.lb_choice.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_choice.setProperty("type", "page_section")
        self.lb_choice.setObjectName("lb_choice")
        self.main_lessons_layout.addWidget(self.lb_choice, 1, 0, 1, 1)

        self.add_new_tab("Перша вкладка", [
        ("Розділ 1", [
            {"title": "Вступ до Python", "labels": ("Math", "Beginner"), "description": "Опис уроку 1"},
            {"title": "Умовні оператори", "labels": ("IT", "Intermediate"), "description": "Опис уроку 2"},
            {"title": "Цикли for та while", "labels": ("Math", "Advanced"), "description": "Опис уроку 3"}
        ]),
        ("Python Basics", [
            {"Функції": "Урок 4", "labels": ("Math", "Beginner"), "description": "Опис уроку 4"},
            {"Класи та обʼєкти": "Урок 5", "labels": ("IT", "Advanced"), "description": "Опис уроку 5"}
        ])
    ])
        self.add_new_tab("Python Basics", [
        ("Розділ 1", [
            {"title": "Алгоритми сортування", "labels": ("Math", "Beginner"), "description": "Опис уроку 1"},
            {"title": "Рекурсія", "labels": ("IT", "Intermediate"), "description": "Опис уроку 2"},
            {"title": "Списки та словники", "labels": ("Math", "Advanced"), "description": "Опис уроку 3"}
        ]),
        ("Розділ 2", [
            {"title": "Модулі та пакети", "labels": ("Math", "Beginner"), "description": "Опис уроку 4"},
            {"title": "Урок 5", "labels": ("IT", "Advanced"), "description": "Опис уроку 5"}
        ])
    ])

        self.setLayout(self.main_lessons_layout)


    def create_card(self, title_text="Назва", labels_text=("TextLabel1", "TextLabel2"), desc_text="Опис"):
        card = QtWidgets.QWidget()
        card.setFixedSize(QtCore.QSize(360, 330))
        card.setProperty("type", "card")
        card_layout = QtWidgets.QVBoxLayout(card)
        title = QtWidgets.QLabel(title_text)
        title.setProperty("type","lb_name_lesson")
        # Мітки 
        labels = QtWidgets.QHBoxLayout()
        for text in labels_text:
            lb_subject = QtWidgets.QLabel(text)
            lb_subject.setProperty("type","lb_name_course")
            lb_subject.setMinimumSize(QtCore.QSize(165, 50))
            lb_subject.setMaximumSize(QtCore.QSize(165, 50))
            labels.addWidget(lb_subject)
        
        lb_description = QtWidgets.QLabel(desc_text)
        lb_description.setProperty("type","lb_description")
        
        stacked_widget = QtWidgets.QStackedWidget()
        stacked_widget.setMaximumSize(QtCore.QSize(16777215, 75))
        stacked_widget.setProperty("type","w_pg")

        page_start = QtWidgets.QWidget()
        page_start.setProperty("type","w_pg")
        layout_start = QtWidgets.QGridLayout(page_start)

        btn_start = QtWidgets.QPushButton("Start Course")
        btn_start.setMinimumSize(QtCore.QSize(310, 50))
        btn_start.setProperty("type","start_continue")
        
        layout_start.addWidget(btn_start, 0, 0, 1, 1)

        page_start.setLayout(layout_start)

        page_continue = QtWidgets.QWidget()
        layout_continue = QtWidgets.QGridLayout(page_continue)

        btn_continue = QtWidgets.QPushButton("Continue")
        btn_continue.setMinimumSize(QtCore.QSize(310, 50))
        btn_continue.setProperty("type","start_continue")

        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setMinimumSize(QtCore.QSize(310, 20))
        progress_bar.setMaximum(100)
        progress_bar.setValue(10)
        
        layout_continue.setContentsMargins(0, 0, 0, 0)
        layout_continue.addWidget(btn_continue, 0, 0, 1, 1)
        layout_continue.addWidget(progress_bar, 1, 0, 1, 1)

        page_continue.setLayout(layout_continue)
        page_continue.setProperty("type","w_pg")

        stacked_widget.addWidget(page_start)
        stacked_widget.addWidget(page_continue)

        def switch_to_continue():
            stacked_widget.setCurrentWidget(page_continue)

        def open_lesson_page():
            print(f"Клік по уроці: {title_text}")
            self.pg_lesson.set_lesson_data(title_text)
            self.stack.setCurrentWidget(self.pg_lesson)
        
        btn_start.clicked.connect(switch_to_continue)
        btn_continue.clicked.connect(open_lesson_page)

        card_layout.addWidget(title)
        card_layout.addLayout(labels)
        card_layout.addWidget(lb_description)
        card_layout.addWidget(stacked_widget)
        return card

    def create_section(self, section_title="Розділ", cards_data=None):
        section_widget = QtWidgets.QWidget()
        section_layout = QtWidgets.QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)
        
        section_label = QtWidgets.QLabel(section_title)
        section_label.setProperty("type", "card")
        section_layout.addWidget(section_label)

        cards_container = QtWidgets.QWidget()
        cards_layout = QtWidgets.QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(10)  
        cards_layout.setAlignment(QtCore.Qt.AlignLeft) 

        if cards_data:
            for card_info in cards_data:
                title = card_info.get("title", "Назва")
                labels = card_info.get("labels", ("Label1", "Label2"))
                desc = card_info.get("description", "Опис")
                card = self.create_card(title, labels, desc)
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
        scroll_area_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_area_widget)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(15)
        if sections_data:
            for section_title, num_cards in sections_data:
                section_widget = self.create_section(section_title, num_cards)
                scroll_layout.addWidget(section_widget)
        scroll_area.setWidget(scroll_area_widget)
        tab_layout = QtWidgets.QVBoxLayout(new_tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area)
        self.lessons_tab_widget.addTab(new_tab, name)
    
    def set_lesson_tab_by_name(self, lesson_name):
        print(f"Пошук уроку у вкладках: {lesson_name}")
        tab_count = self.lessons_tab_widget.count()
        found_index = -1
        for i in range(tab_count):
            tab_label = self.lessons_tab_widget.tabText(i)
            if isinstance(tab_label, str):
                if tab_label.lower() == lesson_name.lower():
                    found_index = i
                    break
        if found_index != -1:
            self.lessons_tab_widget.setCurrentIndex(found_index)
        else:
            print("Вкладку не знайдено")