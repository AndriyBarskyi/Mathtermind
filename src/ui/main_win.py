from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize

from graphs import MyGraph
from circular_progress import CircularProgress
import pyqtgraph as pg

class Page1(QWidget):
    def __init__(self):
        super().__init__()
        self.pg_main = QtWidgets.QWidget(self)
        self.pg_main.setObjectName("pg_main")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.pg_main)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setContentsMargins(16, 0, 16, 16)
        self.gridLayout_4.setSpacing(12)
        
        # Main title
        self.lb_main = QtWidgets.QLabel(self.pg_main)
        self.lb_main.setText("Головна")
        self.lb_main.setObjectName("pageTitle")
        self.lb_main.setStyleSheet("""
            QLabel#pageTitle {
                color: #0F1D35;
                font-weight: 600;
                font-size: 24px;
                margin-bottom: 4px;
            }
        """)
        self.gridLayout_4.addWidget(self.lb_main, 0, 0, 1, 2)
        
        # Continue viewing section
        self.w_pg_main1 = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg_main1.sizePolicy().hasHeightForWidth())
        self.w_pg_main1.setSizePolicy(sizePolicy)
        self.w_pg_main1.setMinimumSize(QtCore.QSize(0, 280))
        self.w_pg_main1.setMaximumSize(QtCore.QSize(16777215, 280))
        self.w_pg_main1.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E5E7EB;
            }
        """)
        
        self.w_pg_main1.setObjectName("w_pg_main1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.w_pg_main1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(16, 12, 16, 12)
        self.gridLayout_2.setSpacing(12)
        
        self.lb_con_view = QtWidgets.QLabel(self.w_pg_main1)
        self.lb_con_view.setText("Продовжити перегляд")
        self.lb_con_view.setObjectName("sectionTitle")
        self.lb_con_view.setStyleSheet("""
            QLabel#sectionTitle {
                color: #0F1D35;
                font-weight: 600;
                font-size: 18px;
                margin-bottom: 0px;
            }
        """)
        self.gridLayout_2.addWidget(self.lb_con_view, 0, 1, 1, 1)
        
        # Scroll area for courses
        self.scrollArea_5 = QtWidgets.QScrollArea(self.w_pg_main1)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollArea_5.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: #F3F4F6;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #D1D5DB;
                border-radius: 4px;
                min-width: 30px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                height: 0px;
            }
        """)
        
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_5)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_21.setSpacing(16)
        
        # Course cards
        for i in range(1, 10):
            widget = QtWidgets.QWidget(self.scrollAreaWidgetContents_5)
            widget.setFixedSize(QtCore.QSize(250, 200))
            widget.setObjectName(f"courseCard{i}")
            widget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            widget.setStyleSheet("""
                QWidget#courseCard""" + str(i) + """ {
                    background-color: #FFFFFF;
                    border: 1px solid #E5E7EB;
                    border-radius: 16px;
                }
                QWidget#courseCard""" + str(i) + """:hover {
                    border-color: #D1D5DB;
                    border-width: 2px;
                }
            """)
            
            vertical_layout = QtWidgets.QVBoxLayout(widget)
            vertical_layout.setObjectName(f"verticalLayout_{i}")
            vertical_layout.setContentsMargins(16, 12, 16, 12)
            vertical_layout.setSpacing(8)
            
            # Course title
            lb_n = QtWidgets.QLabel(widget)
            lb_n.setObjectName(f"courseTitle{i}")
            lb_n.setText(f"Курс {i}")
            lb_n.setStyleSheet("""
                QLabel {
                    color: #0F1D35;
                    font-weight: 600;
                    font-size: 16px;
                    min-height: 24px;
                    max-height: 24px;
                }
            """)
            vertical_layout.addWidget(lb_n)
            
            # Course tag
            lb_name_course = QtWidgets.QLabel(widget)
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            lb_name_course.setSizePolicy(size_policy)
            lb_name_course.setObjectName(f"courseTag{i}")
            lb_name_course.setText(f"Категорія {i}")
            lb_name_course.setStyleSheet("""
                QLabel {
                    background-color: #F3F4F6;
                    color: #858A94;
                    border: none;
                    border-radius: 12px;
                    padding: 4px 12px;
                    font-size: 12px;
                    font-weight: 500;
                }
            """)
            vertical_layout.addWidget(lb_name_course)
            
            # Course description
            lb_description = QtWidgets.QLabel(widget)
            lb_description.setObjectName(f"courseDescription{i}")
            lb_description.setText(f"Опис курсу {i}. Тут буде короткий опис курсу та його основні особливості.")
            lb_description.setWordWrap(True)
            lb_description.setStyleSheet("""
                QLabel {
                    color: #858A94;
                    line-height: 1.5;
                    font-size: 14px;
                    min-height: 70px;
                    max-height: 70px;
                }
            """)
            vertical_layout.addWidget(lb_description)
            
            # Progress bar
            pb = QtWidgets.QProgressBar(widget)
            pb.setObjectName(f"progressBar{i}")
            pb.setFixedHeight(8)
            pb.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 4px;
                    background-color: #F3F4F6;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #566CD2, stop: 1 #7A8FE6);
                    border-radius: 4px;
                }
            """)
            pb.setTextVisible(False)
            pb.setProperty("value", 10 * i)
            vertical_layout.addWidget(pb)
            
            self.horizontalLayout_21.addWidget(widget)

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.gridLayout_2.addWidget(self.scrollArea_5, 1, 1, 1, 1)
        
        # Navigation buttons
        self.btn_prev = QtWidgets.QPushButton(self.w_pg_main1)
        self.btn_prev.setObjectName("prevButton")
        self.btn_prev.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_prev.setFixedSize(36, 36)
        self.btn_prev.setStyleSheet("""
            QPushButton#prevButton {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
            }
            QPushButton#prevButton:hover {
                background-color: #F3F4F6;
                border-color: #D1D5DB;
                border-width: 2px;
            }
        """)
        self.btn_prev.setText("")
        icon_prev = QtGui.QIcon()
        icon_prev.addPixmap(QtGui.QPixmap("src/ui/assets/icons/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_prev.setIcon(icon_prev)
        self.btn_prev.setIconSize(QtCore.QSize(20, 20))
        self.gridLayout_2.addWidget(self.btn_prev, 1, 0, 1, 1)
        
        self.btn_next = QtWidgets.QPushButton(self.w_pg_main1)
        self.btn_next.setObjectName("nextButton")
        self.btn_next.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_next.setFixedSize(36, 36)
        self.btn_next.setStyleSheet("""
            QPushButton#nextButton {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
            }
            QPushButton#nextButton:hover {
                background-color: #F3F4F6;
                border-color: #D1D5DB;
                border-width: 2px;
            }
        """)
        self.btn_next.setText("")
        icon_next = QtGui.QIcon()
        icon_next.addPixmap(QtGui.QPixmap("src/ui/assets/icons/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_next.setIcon(icon_next)
        self.btn_next.setIconSize(QtCore.QSize(20, 20))
        self.gridLayout_2.addWidget(self.btn_next, 1, 2, 1, 1)
        
        self.gridLayout_4.addWidget(self.w_pg_main1, 1, 0, 1, 1)
        
        # Recommendations section
        self.w_pg_main4 = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg_main4.sizePolicy().hasHeightForWidth())
        self.w_pg_main4.setSizePolicy(sizePolicy)
        self.w_pg_main4.setMinimumSize(QtCore.QSize(300, 280))
        self.w_pg_main4.setMaximumSize(QtCore.QSize(300, 280))
        self.w_pg_main4.setObjectName("recommendationsSection")
        self.w_pg_main4.setStyleSheet("""
            QWidget#recommendationsSection {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }
        """)
        
        self.gridLayout_26 = QtWidgets.QGridLayout(self.w_pg_main4)
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.gridLayout_26.setContentsMargins(16, 12, 16, 12)
        self.gridLayout_26.setSpacing(8)
        
        self.label_12 = QtWidgets.QLabel(self.w_pg_main4)
        self.label_12.setText("Можливо цікавить")
        self.label_12.setObjectName("sectionTitle4")
        self.label_12.setStyleSheet("""
            QLabel#sectionTitle4 {
                color: #0F1D35;
                font-weight: 600;
                font-size: 18px;
                margin-bottom: 0px;
            }
        """)
        self.gridLayout_26.addWidget(self.label_12, 0, 0, 1, 1)
        
        # Recommendations list
        self.recommendations_widget = QtWidgets.QWidget(self.w_pg_main4)
        self.recommendations_widget.setObjectName("recommendations_widget")
        
        recommendations_layout = QtWidgets.QVBoxLayout(self.recommendations_widget)
        recommendations_layout.setContentsMargins(0, 0, 0, 0)
        recommendations_layout.setSpacing(8)
        
        # Add recommendation items
        for i in range(1, 5):
            rec_item = QtWidgets.QWidget()
            rec_item.setObjectName(f"rec_item_{i}")
            rec_item.setFixedHeight(50)
            rec_item.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            rec_item.setStyleSheet("""
                QWidget {
                    background-color: #F9FAFB;
                    border-radius: 8px;
                    border: 1px solid #E5E7EB;
                }
                QWidget:hover {
                    background-color: #F3F4F6;
                    border-color: #D1D5DB;
                    border-width: 2px;
                }
            """)
            
            rec_layout = QtWidgets.QHBoxLayout(rec_item)
            rec_layout.setContentsMargins(10, 6, 10, 6)
            
            # Icon placeholder
            icon_label = QtWidgets.QLabel()
            icon_label.setFixedSize(36, 36)
            icon_label.setStyleSheet("""
                background-color: #DDE2F6;
                border-radius: 18px;
            """)
            rec_layout.addWidget(icon_label)
            
            # Text content
            text_layout = QtWidgets.QVBoxLayout()
            text_layout.setSpacing(0)
            
            title_label = QtWidgets.QLabel(f"Рекомендація {i}")
            title_label.setStyleSheet("""
                font-weight: 600;
                font-size: 14px;
                color: #0F1D35;
            """)
            
            desc_label = QtWidgets.QLabel("Короткий опис рекомендації")
            desc_label.setStyleSheet("""
                font-size: 12px;
                color: #858A94;
            """)
            
            text_layout.addWidget(title_label)
            text_layout.addWidget(desc_label)
            
            rec_layout.addLayout(text_layout)
            rec_layout.addStretch()
            
            recommendations_layout.addWidget(rec_item)
        
        self.gridLayout_26.addWidget(self.recommendations_widget, 1, 0, 1, 1)
        
        self.gridLayout_4.addWidget(self.w_pg_main4, 1, 1, 1, 1)
        
        # Courses section
        self.w_pg_main2 = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg_main2.sizePolicy().hasHeightForWidth())
        self.w_pg_main2.setSizePolicy(sizePolicy)
        self.w_pg_main2.setMinimumSize(QtCore.QSize(0, 280))
        self.w_pg_main2.setMaximumSize(QtCore.QSize(16777215, 280))
        self.w_pg_main2.setObjectName("coursesSection")
        self.w_pg_main2.setStyleSheet("""
            QWidget#coursesSection {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }
        """)
        
        self.gridLayout_14 = QtWidgets.QGridLayout(self.w_pg_main2)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout_14.setContentsMargins(16, 12, 16, 12)
        self.gridLayout_14.setSpacing(16)
        
        self.lb_my_courses = QtWidgets.QLabel(self.w_pg_main2)
        self.lb_my_courses.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lb_my_courses.setText("Курси")
        self.lb_my_courses.setObjectName("sectionTitle2")
        self.lb_my_courses.setStyleSheet("""
            QLabel#sectionTitle2 {
                color: #0F1D35;
                font-weight: 600;
                font-size: 18px;
                margin-bottom: 0px;
            }
        """)
        self.gridLayout_14.addWidget(self.lb_my_courses, 0, 0, 1, 4)
        
        # Course circles with circular progress
        self.circular_progress_widgets = []
        for i in range(1, 9):
            # Create container widget for each course
            course_container = QtWidgets.QWidget(self.w_pg_main2)
            course_container.setObjectName(f"course_container_{i}")
            course_container.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            
            # Create layout for the container
            container_layout = QtWidgets.QVBoxLayout(course_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(4)
            container_layout.setAlignment(Qt.AlignCenter)
            
            # Create frame to hold the circular progress
            circular_frame = QtWidgets.QFrame(course_container)
            circular_frame.setFixedSize(QtCore.QSize(90, 90))
            circular_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
            circular_frame.setObjectName(f"circular_frame_{i}")
            
            # Create layout for the frame
            circular_layout = QtWidgets.QVBoxLayout(circular_frame)
            circular_layout.setContentsMargins(0, 0, 0, 0)
            circular_layout.setAlignment(Qt.AlignCenter)
            
            # Create and add the circular progress widget
            circular_progress = CircularProgress(circular_frame)
            circular_progress.setObjectName(f"circular_progress_{i}")
            circular_progress.setFixedSize(QtCore.QSize(90, 90))
            circular_progress.set_value(i * 10)
            circular_layout.addWidget(circular_progress)
            self.circular_progress_widgets.append(circular_progress)
            
            container_layout.addWidget(circular_frame, 0, Qt.AlignCenter)
            
            # Add course label
            pg1_course = QtWidgets.QLabel(course_container)
            pg1_course.setObjectName(f"pg1_course{i}")
            pg1_course.setText(f"Курс {i}")
            pg1_course.setAlignment(Qt.AlignCenter)
            pg1_course.setStyleSheet("""
                QLabel {
                    color: #0F1D35;
                    font-weight: 500;
                    font-size: 14px;
                }
            """)
            container_layout.addWidget(pg1_course, 0, Qt.AlignCenter)
            
            # Add the container to the grid
            row = (i - 1) // 4 + 1  
            col = (i - 1) % 4       
            self.gridLayout_14.addWidget(course_container, row, col, 1, 1, Qt.AlignCenter)
            
        self.gridLayout_4.addWidget(self.w_pg_main2, 2, 0, 1, 1)
        
        # Activity section
        self.w_pg_main3 = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg_main3.sizePolicy().hasHeightForWidth())
        self.w_pg_main3.setSizePolicy(sizePolicy)
        self.w_pg_main3.setMinimumSize(QtCore.QSize(300, 280))
        self.w_pg_main3.setMaximumSize(QtCore.QSize(300, 280))
        self.w_pg_main3.setObjectName("activitySection")
        self.w_pg_main3.setStyleSheet("""
            QWidget#activitySection {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }
        """)
        
        self.gridLayout_13 = QtWidgets.QGridLayout(self.w_pg_main3)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_13.setContentsMargins(16, 12, 16, 12)
        self.gridLayout_13.setSpacing(8)
        
        self.lb_activity = QtWidgets.QLabel(self.w_pg_main3)
        self.lb_activity.setMinimumSize(QtCore.QSize(0, 24))
        self.lb_activity.setMaximumSize(QtCore.QSize(16777215, 24))
        self.lb_activity.setText("Активність")
        self.lb_activity.setObjectName("sectionTitle3")
        self.lb_activity.setStyleSheet("""
            QLabel#sectionTitle3 {
                color: #0F1D35;
                font-weight: 600;
                font-size: 18px;
                margin-bottom: 0px;
            }
        """)
        self.gridLayout_13.addWidget(self.lb_activity, 0, 0, 1, 1)
        
        # Activity graph
        self.graph1 = QtWidgets.QWidget(self.w_pg_main3)
        self.graph1.setObjectName("graph1")
        self.graph1.setMinimumHeight(210)
        self.gridLayout_13.addWidget(self.graph1, 1, 0, 1, 1)
        
        self.gridLayout_4.addWidget(self.w_pg_main3, 2, 1, 1, 1)
        
        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.pg_main)
        self.setLayout(main_layout)
        
        # Initialize activity graph
        self.activity_layout = QVBoxLayout(self.graph1)
        self.activity_layout.setContentsMargins(0, 0, 0, 0)
        self.activity_plot = pg.PlotWidget() 
        self.activity_plot.setBackground('w')
        self.activity_plot.getAxis('left').setPen(pg.mkPen(color='#D1D5DB', width=1))
        self.activity_plot.getAxis('bottom').setPen(pg.mkPen(color='#D1D5DB', width=1))
        self.activity_plot.showGrid(x=True, y=True, alpha=0.3)
        self.activity_layout.addWidget(self.activity_plot)
        self.activity_chart = MyGraph(self.activity_plot)
        activity_data = [15, 25, 20, 35, 45, 30, 40]
        activity_labels = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        self.activity_chart.plot_bar_chart(activity_data, activity_labels)
        
        # Connect buttons
        self.btn_next.clicked.connect(self.scroll_right)
        self.btn_prev.clicked.connect(self.scroll_left)
        self.scrollArea_5.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
    def scroll_left(self):
        scroll_bar = self.scrollArea_5.horizontalScrollBar()
        scroll_bar.setValue(scroll_bar.value() - 250)
        
    def scroll_right(self):
        scroll_bar = self.scrollArea_5.horizontalScrollBar()
        scroll_bar.setValue(scroll_bar.value() + 250)
    
        