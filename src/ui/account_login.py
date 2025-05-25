from PyQt5 import QtWidgets, QtCore
from src.services import AuthService, SessionManager


class LoginPage(QtWidgets.QWidget):
    login_successful = QtCore.pyqtSignal()  
    goto_register = QtCore.pyqtSignal()     

    def __init__(self):
        super().__init__()

        self.setObjectName("pg_login")
        self.setMinimumSize(800, 600)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.widget = QtWidgets.QWidget()
        self.widget.setMinimumSize(QtCore.QSize(1600, 865))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.widget.setProperty("type", "continue_viewing")
        
        self.label_title = QtWidgets.QLabel("Вхід до системи")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setProperty("type", "title")

        self.input_login = QtWidgets.QLineEdit()
        self.input_login.setPlaceholderText("Логін")
        self.input_login.setProperty("type", "settings")
        self.input_login.setMinimumSize(QtCore.QSize(200, 50))
        self.input_login.setMaximumSize(QtCore.QSize(400, 50))

        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setPlaceholderText("Пароль")
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password.setProperty("type", "settings")
        self.input_password.setFixedSize(QtCore.QSize(200, 50))
        self.input_password.setMaximumSize(QtCore.QSize(400, 50))

        self.btn_login = QtWidgets.QPushButton("Увійти")
        self.btn_login.clicked.connect(self.check_credentials)
        self.btn_login.setProperty("type", "start_continue")
        self.btn_login.setMinimumSize(QtCore.QSize(200, 50))
        self.btn_login.setMaximumSize(QtCore.QSize(400, 2000))

        self.btn_register = QtWidgets.QPushButton("Зареєструватися")
        self.btn_register.setProperty("type", "register")
        self.btn_register.clicked.connect(self.goto_register.emit)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(20)
        layout.addWidget(self.label_title)
        layout.addWidget(self.input_login)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_register)
        

    def check_credentials(self):
        login = self.input_login.text()
        password = self.input_password.text()
        auth_service = AuthService()
        success, session_token, user_data = auth_service.login(login, password)
        if success and user_data:
            SessionManager.set_current_user(user_data)
            self.login_successful.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Невірний логін або пароль")
