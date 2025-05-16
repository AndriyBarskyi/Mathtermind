import random
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QRadioButton, QCheckBox, QLineEdit, QTextEdit,
    QListWidget, QPlainTextEdit, QMessageBox, QScrollArea, QListWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QDrag, QPixmap, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from lesson_win import *


class DraggableLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setProperty("type", "lb_name_course")
        self.setMinimumWidth(100)
        self.setFixedSize(200, 75)

    def mousePressEvent(self, event):
        mime_data = QMimeData()
        mime_data.setText(self.text())

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)


class DropLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setProperty("type", "lb_name_course")
        self.setMinimumWidth(150)
        self.setFixedSize(200, 75)
        self.setAlignment(Qt.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.setText(event.mimeData().text())
        event.acceptProposedAction()


class TaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Типи завдань")
        self.setGeometry(100, 100, 800, 600)
        self.lesson_content = {}  # Для зберігання даних уроку
        main_layout = QVBoxLayout()
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def show_result(self, correct, score=None, total_score=None):
        msg = QMessageBox()
        msg.setWindowIcon(QIcon("icon/logo.png"))
        msg.setWindowTitle("Результат")
        msg.setText(f"Ви отримали {score} балів з {total_score}.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def check_all_tasks(self):
        score = 0
        total_score = 0

        task_points = {
            self.test_task_widget: 2,
            self.true_false_task_widget: 1,
            self.input_task_widget: 3,
            self.fill_in_the_blanks_task_widget: 2,
            self.code_insert_task_widget: 4,
            self.formula_to_plot_task_widget: 0,
            self.fix_error_task_widget: 3,
            self.drag_and_drop_task_widget: 5,
        }

        correct = self.check_test_task()   
        if correct:
            score += task_points[self.test_task_widget]
        total_score += task_points[self.test_task_widget]

        correct = self.check_true_false_task()   
        if correct:
            score += task_points[self.true_false_task_widget]
        total_score += task_points[self.true_false_task_widget]

        correct = self.check_input_task()   
        if correct:
            score += task_points[self.input_task_widget]
        total_score += task_points[self.input_task_widget]

        correct = self.check_fill_in_the_blanks_task()   
        if correct:
            score += task_points[self.fill_in_the_blanks_task_widget]
        total_score += task_points[self.fill_in_the_blanks_task_widget]

        correct = self.check_code_insert_task()   
        if correct:
            score += task_points[self.code_insert_task_widget]
        total_score += task_points[self.code_insert_task_widget]

        score += task_points[self.formula_to_plot_task_widget]  
        total_score += task_points[self.formula_to_plot_task_widget]

        correct = self.check_fix_error_task()   
        if correct:
            score += task_points[self.fix_error_task_widget]
        total_score += task_points[self.fix_error_task_widget]
        
        correct = self.check_drag_and_drop()   
        if correct:
            score += task_points[self.drag_and_drop_task_widget]
        total_score += task_points[self.drag_and_drop_task_widget]
        

        self.show_result(True, score, total_score)
    
    def update_content(self, lesson_content):
        self.lesson_content = lesson_content
        self.update_task_widgets()  
        
    def update_task_widgets(self):
        # Оновлюємо теорію
        if self.stack.count() > 0:
            self.stack.removeWidget(self.stack.widget(0))
        self.stack.insertWidget(0, self.create_theory())
        # Оновлюємо завдання
        if self.stack.count() > 1:
            self.stack.removeWidget(self.stack.widget(1))
        if self.stack.count() > 0:
            self.stack.insertWidget(1, self.create_tasks_tab())
            print(1)
        else:
            self.stack.addWidget(self.create_tasks_tab())
        self.stack.setCurrentIndex(0)

    def create_theory(self):
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Теоретична інформація")
        title.setProperty("type", "title")
        layout.addWidget(title)

        theory_text = QTextEdit()
        theory_text.setReadOnly(True)
        theory = self.lesson_content.get("theory", "Теорія не знайдена")  # теорію з lesson_content
        theory_text.setPlainText(theory)
        layout.addWidget(theory_text)

        widget.setLayout(layout)
        return widget

    def create_tasks_tab(self):

        container = QWidget()
        container.setProperty("type", "w_pg")

        layout = QVBoxLayout(container)

        title = QLabel("Завдання")
        title.setProperty("type", "title")
        layout.addWidget(title)

        self.test_task_widget = self.create_test_task()
        self.true_false_task_widget = self.create_true_false_task()
        self.input_task_widget = self.create_input_task()
        self.fill_in_the_blanks_task_widget = self.create_fill_in_the_blanks_task()
        self.code_insert_task_widget = self.create_code_insert_task()
        self.formula_to_plot_task_widget = self.create_formula_to_plot_task()
        self.fix_error_task_widget = self.create_fix_error_task()
        self.drag_and_drop_task_widget = self.create_drag_and_drop_task()

        self.task_widgets = [
            self.test_task_widget,
            self.true_false_task_widget,
            self.input_task_widget,
            self.fill_in_the_blanks_task_widget,
            self.code_insert_task_widget,
            self.formula_to_plot_task_widget,
            self.fix_error_task_widget,
            self.drag_and_drop_task_widget,
        ]

        for task_widget in self.task_widgets:
            layout.addWidget(task_widget)

        check_all_btn = QPushButton("Перевірити")
        check_all_btn.setProperty("type", "start_continue")
        check_all_btn.setMinimumSize(QSize(250, 50))
        check_all_btn.setMaximumSize(QSize(800, 50))
        check_all_btn.clicked.connect(self.check_all_tasks)
        layout.addWidget(check_all_btn)

        layout.addStretch()
        return container

    def create_test_task(self):
        widget = QWidget()
        widget.setProperty("type", "w_pg")
        layout = QVBoxLayout()

        quest_text = self.lesson_content.get("test_question", "Питання не знайдено")
        quest = QLabel(f"1. {quest_text}")
        quest.setProperty("type", "lb_description")
        layout.addWidget(quest)

        options = self.lesson_content.get("test_options", [])
        self.test_answer = self.lesson_content.get("test_answer", "")
        random.shuffle(options)

        self.test_buttons = []
        for opt in options:
            btn = QRadioButton(opt)
            self.test_buttons.append(btn)
            layout.addWidget(btn)

        widget.setLayout(layout)
        return widget

    def check_test_task(self):
        for btn in self.test_buttons:
            if btn.isChecked() and btn.text() == self.test_answer:
                return True
        return False

    def create_true_false_task(self):
        widget = QWidget()
        widget.setProperty("type", "w_pg")

        quest = QLabel(f"2. {self.lesson_content.get('true_false_question', 'Питання не знайдено')}")
        quest.setProperty("type", "lb_description")

        layout = QVBoxLayout()
        layout.addWidget(quest)
        self.true_false_options = [QRadioButton("Правда"), QRadioButton("Брехня")]
        layout.addWidget(self.true_false_options[0])  # Правда
        layout.addWidget(self.true_false_options[1])  # Брехня
        widget.setLayout(layout)  
        return widget

    def check_true_false_task(self):
        correct_answer = self.lesson_content.get("true_false_answer", False)
        if correct_answer:  
            return self.true_false_options[0].isChecked()
        else:  
            return self.true_false_options[1].isChecked()

    def create_input_task(self):
        widget = QWidget()
        widget.setProperty("type", "w_pg")
        layout = QVBoxLayout()
        quest = QLabel(f"3. {self.lesson_content.get('input_question', 'Питання не знайдено')}")
        quest.setProperty("type", "lb_description")
        
        layout.addWidget(quest)
        self.input_answer = QLineEdit()
        layout.addWidget(self.input_answer)
        widget.setLayout(layout)  
        return widget

    def check_input_task(self):
        return self.input_answer.text().strip() == self.lesson_content.get("input_answer", "")

    def create_fill_in_the_blanks_task(self):
        widget = QWidget()
        widget.setProperty("type", "w_pg")
        main_layout = QVBoxLayout() 
        layout_horizontal = QHBoxLayout()  
        quest1 = QLabel(f"4. {self.lesson_content.get('blank_question', 'Питання не знайдено')}")
        quest1.setProperty("type", "lb_description")

        layout_horizontal.addWidget(quest1)
        self.blank_input = QLineEdit()
        layout_horizontal.addWidget(self.blank_input)
        
        quest2 = QLabel(self.lesson_content.get("blank_question_part2", ""))
        quest2.setProperty("type", "lb_description")
        
        layout_horizontal.addWidget(quest2)
        main_layout.addLayout(layout_horizontal)  
        widget.setLayout(main_layout)  
        return widget

    def check_fill_in_the_blanks_task(self):
        return self.blank_input.text().strip() == self.lesson_content.get("blank_answer", "")

    def create_code_insert_task(self):
        widget = QWidget()
        widget.setProperty("type", "w_pg")
        main_layout = QVBoxLayout()  
        layout_horizontal = QHBoxLayout()  
        quest1 = QLabel(f"5. {self.lesson_content.get('code_question', 'Питання не знайдено')}")
        quest1.setProperty("type", "lb_description")
        main_layout.addWidget(quest1)

        snippets = QListWidget()
        snippets.addItems(self.lesson_content.get("code_snippets", []))
        self.code_area = QPlainTextEdit()

        layout_horizontal.addWidget(snippets)
        layout_horizontal.addWidget(self.code_area)

        main_layout.addLayout(layout_horizontal)  
        widget.setLayout(main_layout)  
        return widget

    def check_code_insert_task(self):
        text = self.code_area.toPlainText()
        required_code = self.lesson_content.get("code_required", [])
        return all(code in text for code in required_code)

    def create_formula_to_plot_task(self):
        widget = QWidget()
        widget.setProperty("type", "w_pg")
        layout = QVBoxLayout()

        self.formula_input = QLineEdit()
        plot_button = QPushButton("Побудувати графік")
        plot_button.setProperty("type", "start_continue")
        plot_button.setMinimumSize(QSize(250, 50))
        plot_button.setMaximumSize(QSize(800, 50))
        plot_button.clicked.connect(self.plot_formula)

        self.canvas = FigureCanvas(Figure(figsize=(15, 9)))
        self.canvas.setFixedSize(800, 500)
        self.ax = self.canvas.figure.add_subplot(111)
        quest = QLabel(f"6. {self.lesson_content.get('formula_question', 'Введіть формулу y = f(x)')}")
        quest.setProperty("type", "lb_description")
        layout.addWidget(quest)
        layout.addWidget(self.formula_input)
        layout.addWidget(plot_button)
        layout.addWidget(self.canvas)

        widget.setLayout(layout)
        return widget

    def plot_formula(self):
        import numpy as np

        formula = self.formula_input.text()
        x = np.linspace(-10, 10, 400)
        try:
            y = eval(formula, {"x": x, "np": np})
            self.ax.clear()
            self.ax.plot(x, y)
            self.canvas.draw()
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Помилка: {e}", ha="center", va="center", wrap=True)
            self.canvas.draw()

    def create_fix_error_task(self):
        widget = QWidget()
        widget.setProperty("type", "w_pg")
        layout = QVBoxLayout()
        quest = QLabel(f"7. {self.lesson_content.get('fix_error_question', 'Виправте помилку:')}")
        quest.setProperty("type", "lb_description")
        layout.addWidget(quest)
        self.fix_code_input = QPlainTextEdit()
        self.fix_code_input.setPlainText(self.lesson_content.get("fix_error_code", ""))
        layout.addWidget(self.fix_code_input)
        widget.setLayout(layout)  
        return widget

    def check_fix_error_task(self):
        required_fixes = self.lesson_content.get("fix_error_fixes", [])
        return all(fix in self.fix_code_input.toPlainText() for fix in required_fixes)

    def create_drag_and_drop_task(self):
        widget = QWidget()
        widget.setProperty("type", "w_pg")
        layout_main = QVBoxLayout()  
        quest = QLabel(f"8. {self.lesson_content.get('drag_and_drop_question', 'Перетягніть слова до визначень:')}")
        quest.setProperty("type", "lb_description")
        layout_main.addWidget(quest)

        descriptions = self.lesson_content.get("drag_and_drop_descriptions", [])
        words = self.lesson_content.get("drag_and_drop_words", [])
        self.drop_labels = []

        drop_layout = QHBoxLayout()
        for desc in descriptions:
            drop_container = QVBoxLayout()

            label_desc = QLabel(desc)
            label_desc.setWordWrap(True)
            label_desc.setAlignment(Qt.AlignCenter)
            label_desc.setProperty("type", "lb_small")
            drop_label = DropLabel()

            drop_container.addWidget(label_desc)
            drop_container.addWidget(drop_label)

            self.drop_labels.append(drop_label)
            drop_layout.addLayout(drop_container)

        drag_layout = QHBoxLayout()
        for word in words:
            drag_layout.addWidget(DraggableLabel(word))

        layout_main.addLayout(drop_layout)
        layout_main.addLayout(drag_layout)
        widget.setLayout(layout_main)  
        return widget

    def check_drag_and_drop(self):
        correct_answers = self.lesson_content.get("drag_and_drop_answers", [])
        return [lbl.text() for lbl in self.drop_labels] == correct_answers

if __name__ == "main":
    app = QApplication(sys.argv)
    window = TaskWindow()
    window.show()
    sys.exit(app.exec_())
                    
