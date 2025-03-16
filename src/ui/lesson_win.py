from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget
from graphs import *
#from listw import *
class Page6(QWidget):
    def __init__(self):
        super().__init__()
        self.pg_lesson = QtWidgets.QWidget()
        self.pg_lesson.setObjectName("pg_lesson")
        self.gridLayout_45 = QtWidgets.QGridLayout(self.pg_lesson)
        self.gridLayout_45.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_45.setObjectName("gridLayout_45")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.pg_lesson)
        self.scrollArea_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 1399, 746))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.gridLayout_44 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_44.setObjectName("gridLayout_44")
        self.widget_13 = QVideoWidget(self.scrollAreaWidgetContents_3)
        self.widget_13.setMinimumSize(QtCore.QSize(800, 350))
        self.widget_13.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.widget_13.setObjectName("widget_13")
        self.gridLayout_44.addWidget(self.widget_13, 1, 0, 2, 1)
        self.widget_22 = QtWidgets.QWidget(self.scrollAreaWidgetContents_3)
        self.widget_22.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.widget_22.setObjectName("widget_22")
        self.gridLayout_52 = QtWidgets.QGridLayout(self.widget_22)
        self.gridLayout_52.setContentsMargins(-1, 25, -1, 25)
        self.gridLayout_52.setObjectName("gridLayout_52")
        self.label = QtWidgets.QLabel(self.widget_22)
        self.label.setObjectName("label")
        self.gridLayout_52.addWidget(self.label, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.widget_22)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 25))
        self.progressBar.setStyleSheet("QProgressBar {\n"
"                border: 2px solid #f3f3f3;\n"
"                border-radius: 8px; /* Закруглення всієї панелі */\n"
"                background-color: #f3f3f3;\n"
"                height: 10px; /* Висота прогрес-бару */\n"
"            }\n"
"QProgressBar::chunk {\n"
"                background: qlineargradient(\n"
"                    x1: 0, y1: 0, x2: 1, y2: 1,\n"
"                    stop: 0 #6c9dfd,\n"
"                    stop: 1 #8fb4ff\n"
"                ); /* Градієнт заповнення */\n"
"                border-radius: 6px; /* Закруглення заповненого сегменту */\n"
"            }")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_52.addWidget(self.progressBar, 1, 0, 1, 1)
        self.gridLayout_44.addWidget(self.widget_22, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_2.setMinimumSize(QtCore.QSize(0, 50))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_2.setObjectName("label_2")
        self.gridLayout_44.addWidget(self.label_2, 3, 0, 1, 1)
        self.scrollArea_8 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_3)
        self.scrollArea_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollArea_8.setObjectName("scrollArea_8")
        self.scrollAreaWidgetContents_8 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_8.setGeometry(QtCore.QRect(0, 0, 570, 498))
        self.scrollAreaWidgetContents_8.setObjectName("scrollAreaWidgetContents_8")
        self.gridLayout_51 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_8)
        self.gridLayout_51.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_51.setObjectName("gridLayout_51")
        self.widget_23 = QtWidgets.QWidget(self.scrollAreaWidgetContents_8)
        self.widget_23.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.widget_23.setObjectName("widget_23")
        self.gridLayout_50 = QtWidgets.QGridLayout(self.widget_23)
        self.gridLayout_50.setContentsMargins(11, -1, -1, -1)
        self.gridLayout_50.setObjectName("gridLayout_50")
        self.listWidget = QtWidgets.QListWidget(self.widget_23)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout_50.addWidget(self.listWidget, 0, 0, 1, 1)
        self.gridLayout_51.addWidget(self.widget_23, 0, 0, 1, 1)
        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_8)
        self.gridLayout_44.addWidget(self.scrollArea_8, 2, 1, 3, 1)
        self.scrollArea_7 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_3)
        self.scrollArea_7.setMinimumSize(QtCore.QSize(800, 0))
        self.scrollArea_7.setMaximumSize(QtCore.QSize(700, 16777215))
        self.scrollArea_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollArea_7.setObjectName("scrollArea_7")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 800, 290))
        self.scrollAreaWidgetContents_6.setMinimumSize(QtCore.QSize(800, 0))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.gridLayout_49 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_49.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_49.setObjectName("gridLayout_49")
        self.widget_18 = QtWidgets.QWidget(self.scrollAreaWidgetContents_6)
        self.widget_18.setMinimumSize(QtCore.QSize(800, 290))
        self.widget_18.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.widget_18.setObjectName("widget_18")
        self.gridLayout_46 = QtWidgets.QGridLayout(self.widget_18)
        self.gridLayout_46.setObjectName("gridLayout_46")
        self.tabWidget = QtWidgets.QTabWidget(self.widget_18)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_48 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_48.setObjectName("gridLayout_48")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_47 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_47.setObjectName("gridLayout_47")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_46.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_49.addWidget(self.widget_18, 0, 0, 1, 1)
        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_6)
        self.gridLayout_44.addWidget(self.scrollArea_7, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_3.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        
        self.label_3.setObjectName("label_3")
        self.gridLayout_44.addWidget(self.label_3, 0, 0, 1, 1)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_45.addWidget(self.scrollArea_4, 0, 0, 1, 1)
        self.setLayout(self.gridLayout_45)



        """self.listWidget.setStyleSheet(
            QListWidget {
                border: none;
                background: #f5f5f5;
                border-radius: 15px;
                padding: 10px;
            }
            QListWidget::item {
                margin: 5px;
            }
            QListWidget::item:selected {
                background: #e0e0e0;
                border-radius: 10px;
            }
        )

        items = [
            ("Introduction to AI", "10 min 30 sec"),
            ("Natural Language Processing Basics", "12 min 50 sec"),
            ("Image Generation using AI", "45 min 11 sec"),
            ("Text Generation using AI", "20 min 21 sec"),
            ("Understanding Neural Networks", "45 min 10 sec"),
            ("Machine Learning Fundamentals", "25 min 43 sec"),
            ("Sentiment Analysis with AI", "24 min 19 sec"),
            ("Ethical Considerations in AI", "30 min 50 sec"),
        ]

        for title, duration in items:
            item = QListWidgetItem(self.listWidget)
            widget = CustomListItem(title, duration)
            item.setSizeHint(widget.sizeHint())
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)"""