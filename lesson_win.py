from PyQt5.QtWidgets import QWidget, QScrollArea,QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QDrag,QPixmap,QIcon
from graphs import *
from tasks import *
class LessonItem(QWidget):
    def __init__(self, title, duration, status="incomplete"):
        super().__init__()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("background-color: transparent;")
        duration_label = QLabel(duration)
        duration_label.setStyleSheet("color: gray; background-color: transparent;")
        text_layout = QVBoxLayout()
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(duration_label)
        check_label = QLabel()
        check_label.setFixedWidth(30)
        check_label.setAlignment(Qt.AlignCenter)
        check_label.setStyleSheet("background-color: transparent;")

        if status == "done":
            check_label.setFixedSize(30, 30)
            check_label.setPixmap(QPixmap("blue_icon/check_mark.PNG").scaled(check_label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
        else:
            check_label.setText("")

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(text_layout)
        main_layout.addStretch()
        main_layout.addWidget(check_label)
        main_layout.setContentsMargins(10, 5, 10, 5)

        self.setLayout(main_layout)

        # Залежний від статусу фон
        bg_color = {
            "done": "#e0ffe0",     
            "active": "#e6f0ff",    
            "incomplete": "#ffffff" 
        }.get(status, "#ffffff")

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                padding: 6px;
                border-radius: 8px;
            }}
            QLabel {{
                background-color: transparent;
            }}
            QWidget:hover {{
                background-color: #dcdcdc;
            }}
        """)

class Lesson_page(QWidget):
    def __init__(self):
        self.lesson_data = {  # Приклад даних уроків
            "Вступ до Python": {
                "theory": "Основи Python. Змінні, типи даних...",
                "test_question": "Що таке змінна в Python?",
                "test_options": ["Область пам'яті для зберігання даних", "Функція", "Клас"],
                "test_answer": "Область пам'яті для зберігання даних",
                "true_false_question": "Python - компілюється.",
                "true_false_answer": False,
                "input_question": "Обчисліть: 2 + 2 = ?",
                "input_answer": "4",
                "blank_question": " Заповніть пропуск, щоб вираз був істинним: x _ 5",
                "blank_question_part2": "= 10",
                "blank_answer": "+",
                "code_question": "Використовуючи надані фрагменти коду, напишіть програму, яка виводить на екран числа від 0 до 4.",
                "code_snippets": ["print()", "for i in range():"],
                "code_required": ["print()"],
                "formula_question": "Вкажіть степінь, до якої потрібно піднести x, щоб отримати y: y = x ** ?",
                "fix_error_question": "Виправте помилку в коді:",
                "fix_error_code": "prin('Hello')",
                "fix_error_fixes": ["print("],
                "drag_and_drop_question": "З'єднайте визначення з терміном:",
                "drag_and_drop_descriptions": ["Зберігання даних", "Послідовність команд", "Шаблон для об'єктів"],
                "drag_and_drop_words": ["Змінна", "Програма", "Клас"],
                "drag_and_drop_answers": ["Змінна", "Програма", "Клас"],
            },
            "Умовні оператори": {
                "theory": "Умовні оператори (if, elif, else) використовуються для виконання коду залежно від умови.",
                "test_question": "Який оператор використовується для перевірки умови?",
                "test_options": ["for", "while", "if"],
                "test_answer": "if",
                "true_false_question": "Блок 'else' завжди виконується.",
                "true_false_answer": False,
                "input_question": "Яке ключове слово використовується для альтернативної умови?",
                "input_answer": "elif",
                "blank_question": "if x _ 0:",
                "blank_question_part2": "",
                "blank_answer": ">",
                "code_question": "Використовуючи надані фрагменти коду, напишіть програму, яка виводить на екран числа від 0 до 4.",
                "code_snippets": ["if:", "else:", "elif:", "print()"],
                "code_required": ["if:", "else:", "print()"],
                "formula_question": "Немає", 
                "fix_error_question": "Виправте:",
                "fix_error_code": "if x = 5:\n    print('Ok')",
                "fix_error_fixes": ["if x == 5:"],
                "drag_and_drop_question": "З'єднайте оператор з описом:",
                "drag_and_drop_descriptions": ["Якщо умова істинна", "Інакше", "Інакше якщо"],
                "drag_and_drop_words": ["if", "else", "elif"],
                "drag_and_drop_answers": ["if", "else", "elif"],
            },
            "Цикли for та while": {
                "theory": "Цикли for і while використовуються для повторення блоку коду.",
                "test_question": "Який цикл використовується для ітерації по послідовності?",
                "test_options": ["if", "for", "while"],
                "test_answer": "for",
                "true_false_question": "Цикл 'while' завжди виконується хоча б один раз.",
                "true_false_answer": False,
                "input_question": "Яке ключове слово використовується для виходу з циклу?",
                "input_answer": "break",
                "blank_question": "for i in _(5):",
                "blank_question_part2": "",
                "blank_answer": "range",
                "code_snippets": ["for i in range():", "while :", "break", "continue"],
                "code_required": ["for i in range():", "break"],
                "formula_question": "Немає",
                "fix_error_question": "Виправте:",
                "fix_error_code": "for i in range[5]:\n    print(i)",
                "fix_error_fixes": ["for i in range(5):"],
                "drag_and_drop_question": "З'єднайте цикл з описом:",
                "drag_and_drop_descriptions": ["Повторення для кожного елемента", "Повторення поки умова істинна"],
                "drag_and_drop_words": ["for", "while"],
                "drag_and_drop_answers": ["for", "while"],
            },

        }

        super().__init__()
        #task_window = TaskWindow()
        self.pg_lesson = QtWidgets.QWidget()
        self.pg_lesson.setObjectName("pg_lesson")
        
        self.main_grid_layout = QtWidgets.QGridLayout(self.pg_lesson)
        self.main_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_grid_layout.setObjectName("main_grid_layout")
        
        self.main_scroll_area = QtWidgets.QScrollArea(self.pg_lesson)
        self.main_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_scroll_area.setWidgetResizable(True)
        self.main_scroll_area.setObjectName("main_scroll_area")
        self.main_scroll_content = QtWidgets.QWidget()

        self.main_scroll_content.setMinimumSize(QtCore.QSize(1399, 746))
        self.main_scroll_content.setMaximumSize(QtCore.QSize(2000, 2000))

        self.main_scroll_content.setObjectName("main_scroll_content")
        self.main_content_layout = QtWidgets.QGridLayout(self.main_scroll_content)
        self.main_content_layout.setObjectName("main_content_layout")
        """self.video_widget = QVideoWidget(self.main_scroll_content)
        self.video_widget.setMinimumSize(QtCore.QSize(1000, 350))
        self.video_widget.setMaximumSize(QtCore.QSize(16777215, 350))
        self.video_widget.setProperty("type","w_pg")
        self.video_widget.setObjectName("video_widget")
        self.main_content_layout.addWidget(self.video_widget, 1, 0, 2, 1)"""
        self.main_content_layout.setColumnStretch(0, 3)
        
        self.progress_section_widget = QtWidgets.QWidget(self.main_scroll_content)
        self.progress_section_widget.setMaximumSize(QtCore.QSize(400, 200))
        self.progress_section_widget.setProperty("type","w_pg")
        self.progress_section_widget.setObjectName("progress_section_widget")
        self.progress_layout = QtWidgets.QGridLayout(self.progress_section_widget)
        self.progress_layout.setContentsMargins(-1, 25, -1, 25)
        self.progress_layout.setObjectName("progress_layout")
        
        self.course_title_lb = QtWidgets.QLabel(self.progress_section_widget)
        self.course_title_lb.setObjectName("course_title_lb")
        self.course_title_lb.setProperty("type","page_section")
        self.progress_layout.addWidget(self.course_title_lb, 0, 0, 1, 1)
        
        self.lesson_progress_bar = QtWidgets.QProgressBar(self.progress_section_widget)
        self.lesson_progress_bar.setMinimumSize(QtCore.QSize(0, 25))
        self.lesson_progress_bar.setProperty("value", 24)
        self.lesson_progress_bar.setObjectName("lesson_progress_bar")
        self.progress_layout.addWidget(self.lesson_progress_bar, 1, 0, 1, 1)
        self.main_content_layout.addWidget(self.progress_section_widget, 1, 1, 1, 1)
        
        self.lesson_title_lb = QtWidgets.QLabel(self.main_scroll_content)
        self.lesson_title_lb.setMinimumSize(QtCore.QSize(1000, 50))
        self.lesson_title_lb.setMaximumSize(QtCore.QSize(16777215, 100))
        self.lesson_title_lb.setObjectName("lesson_title_lb")
        self.main_content_layout.addWidget(self.lesson_title_lb, 1, 0, 2, 1)
        
        self.lessons_list_scroll_area = QtWidgets.QScrollArea(self.main_scroll_content)
        self.lessons_list_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lessons_list_scroll_area.setWidgetResizable(True)
        self.lessons_list_scroll_area.setObjectName("lessons_list_scroll_area")
        
        self.lessons_list_scroll_content = QtWidgets.QWidget()
        self.lessons_list_scroll_content.setMaximumSize(QtCore.QSize(400, 16777215))
        self.lessons_list_scroll_content.setGeometry(QtCore.QRect(0, 0, 570, 498))
        self.lessons_list_scroll_content.setObjectName("lessons_list_scroll_content")

        self.lessons_list_scroll_layout = QtWidgets.QGridLayout(self.lessons_list_scroll_content)
        self.lessons_list_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.lessons_list_scroll_content.setMaximumSize(QtCore.QSize(400, 16777215))
        self.lessons_list_scroll_layout.setObjectName("lessons_list_scroll_layout")

        self.lessons_list_container = QtWidgets.QWidget(self.lessons_list_scroll_content)
        self.lessons_list_container.setProperty("type","w_pg")
        self.lessons_list_container.setObjectName("lessons_list_container")
        
        self.lessons_list_layout = QtWidgets.QGridLayout(self.lessons_list_container)
        self.lessons_list_layout.setContentsMargins(11, -1, -1, -1)
        self.lessons_list_layout.setObjectName("lessons_list_layout")
        
        self.list_widget = QtWidgets.QListWidget()
        #список
        lessons = [
            ("Вступ до Python", "12 min 30 sec", "done"),
            ("Умовні оператори", "12 min 30 sec", "done"),
            ("Цикли for та while", "45 min 11 sec", "active"),
            ("Функції", "20 min 21 sec", "incomplete"),
            ("Класи та обʼєкти", "12 min 30 sec", "done"),
            ("Алгоритми сортування", "45 min 11 sec", "active"),
            ("Рекурсія", "20 min 21 sec", "incomplete"),
            ("Списки та словники", "12 min 30 sec", "done"),
            ("Модулі та пакети", "45 min 11 sec", "active"),
            ("Text Generation", "20 min 21 sec", "incomplete"),
            ("Intro to Neural Nets", "32 min 14 sec", "incomplete")
        ]

        for title, duration, status in lessons:
            item = QtWidgets.QListWidgetItem()
            widget = LessonItem(title, duration, status)
            item.setSizeHint(widget.sizeHint())

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

        self.list_widget.itemClicked.connect(self.on_item_click)
        self.lessons_list_layout.addWidget(self.list_widget, 0, 0, 1, 1)
        
        self.lessons_list_scroll_layout.addWidget(self.lessons_list_container, 0, 0, 1, 1)
        self.lessons_list_scroll_area.setWidget(self.lessons_list_scroll_content)
        self.main_content_layout.addWidget(self.lessons_list_scroll_area, 2, 1, 3, 1)
        
        self.task_section_scroll_area = QtWidgets.QScrollArea(self.main_scroll_content)
        self.task_section_scroll_area.setMinimumSize(QtCore.QSize(1000, 0))
        self.task_section_scroll_area.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.task_section_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.task_section_scroll_area.setWidgetResizable(True)
        self.task_section_scroll_area.setObjectName("task_section_scroll_area")
        
        self.scroll_task_section_content = QtWidgets.QWidget()
        self.scroll_task_section_content.setGeometry(QtCore.QRect(0, 0, 800, 290))
        self.scroll_task_section_content.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scroll_task_section_content.setMinimumSize(QtCore.QSize(1000, 0))
        self.scroll_task_section_content.setObjectName("scroll_task_section_content")
        
        self.task_scroll_layout = QtWidgets.QGridLayout(self.scroll_task_section_content)
        self.task_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.task_scroll_layout.setObjectName("task_scroll_layout")
        
        self.tab_container_widget = QtWidgets.QWidget()
        self.tab_container_widget.setMinimumSize(QtCore.QSize(1000, 290))
        self.tab_container_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_container_widget.setProperty("type","w_pg")
        self.tab_container_widget.setObjectName("tab_container_widget")
        
        self.task_tabs_layout = QtWidgets.QGridLayout(self.tab_container_widget)
        self.task_tabs_layout.setObjectName("task_tabs_layout")
        
        self.task_tabs = QtWidgets.QTabWidget(self.tab_container_widget)
        self.task_tabs.setMinimumSize(QtCore.QSize(1000, 290))
        self.task_tabs.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.task_tabs.setObjectName("task_tabs")
        
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tab_container_widget.setProperty("type", "w_pg")
        #self.task_tabs.addTab(self.createScrollableTab(task_window.create_theory()), "Теорія")
        #self.task_tabs.addTab(self.createScrollableTab(task_window.create_tasks_tab()),"Всі завдання")

        self.task_tabs_layout.addWidget(self.task_tabs, 0, 0, 1, 1)
        self.task_scroll_layout.addWidget(self.tab_container_widget, 0, 0, 1, 1)
        self.task_section_scroll_area.setWidget(self.scroll_task_section_content)
        self.main_content_layout.addWidget(self.task_section_scroll_area, 4, 0, 1, 1)
        self.title_main_lb = QtWidgets.QLabel(self.main_scroll_content)
        self.title_main_lb.setMinimumSize(QtCore.QSize(1000, 40))
        self.title_main_lb.setMaximumSize(QtCore.QSize(16777215, 40))
        self.title_main_lb.setText("Урок")
        self.title_main_lb.setProperty("type", "title")
        self.title_main_lb.setObjectName("title_main_lb")
        self.main_content_layout.addWidget(self.title_main_lb, 0, 0, 1, 1)
        self.main_scroll_area.setWidget(self.main_scroll_content)
        
        self.main_grid_layout.addWidget(self.main_scroll_area, 0, 0, 1, 1)
        
        self.setLayout(self.main_grid_layout)


    def createScrollableTab(self, inner_widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(inner_widget)
        inner_widget.setProperty("type", "w_pg")
        return scroll_area

    def set_lesson_data(self, lesson_name):
        print(f"Завантажуємо урок: {lesson_name}")
        found_item = None
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            widget = self.list_widget.itemWidget(item)
            if widget.title_label.text() == lesson_name:
                found_item = item
                break

        if found_item:
            self.list_widget.setCurrentItem(found_item)
            self.update_lesson_content(found_item)
            self.update_task_tabs()
        else:
            print(f"Урок з назвою '{lesson_name}' не знайдено у списку.")

    def update_task_tabs(self):
        self.task_tabs.clear() 
        self.task_tabs.addTab(self.createScrollableTab(self.task_window.create_theory()), "Теорія")
        self.task_tabs.addTab(self.createScrollableTab(self.task_window.create_tasks_tab()), "Всі завдання")

    def update_lesson_content(self, item):
        if isinstance(item, QtWidgets.QListWidgetItem):
            selected_lesson_widget = self.list_widget.itemWidget(item)
            if selected_lesson_widget:
                lesson_title = selected_lesson_widget.title_label.text()
                self.lesson_title_lb.setText(lesson_title)
                self.task_window = TaskWindow()
                self.task_window.update_content(self.lesson_data[lesson_title])
                self.update_task_tabs()             
            else:
                print("не вдалося отримати віджет")
        else:
            print("не є в списку ")

    def on_item_click(self, item):
        index = self.list_widget.indexFromItem(item)
        item_text = self.list_widget.itemWidget(item).title_label.text()
        self.lesson_title_lb.setText(item_text)
        self.set_lesson_data(item_text)
    