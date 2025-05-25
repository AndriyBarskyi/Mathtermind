from PyQt5 import QtWidgets, QtCore
from src.services import AuthService

class RegisterPage(QtWidgets.QWidget):
    back_to_login = QtCore.pyqtSignal()  

    def __init__(self):
        super().__init__()

        self.setObjectName("pg_register")
        self.setMinimumSize(800, 600)
        
        self.label_title = QtWidgets.QLabel("Реєстрація")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.input_username = QtWidgets.QLineEdit()
        self.input_username.setPlaceholderText("Ім'я користувача")
        self.input_username.setProperty("type", "settings")
        self.input_username.setMinimumSize(QtCore.QSize(200, 50))
        self.input_username.setMaximumSize(QtCore.QSize(400, 50))

        self.input_email = QtWidgets.QLineEdit()
        self.input_email.setPlaceholderText("Електронна адреса користувача")
        self.input_email.setProperty("type", "settings")
        self.input_email.setMinimumSize(QtCore.QSize(200, 50))
        self.input_email.setMaximumSize(QtCore.QSize(400, 50))


        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setPlaceholderText("Пароль")
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password.setProperty("type", "settings")
        self.input_password.setMinimumSize(QtCore.QSize(200, 50))
        self.input_password.setMaximumSize(QtCore.QSize(400, 50))

        self.input_confirm = QtWidgets.QLineEdit()
        self.input_confirm.setPlaceholderText("Повторіть пароль")
        self.input_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_confirm.setProperty("type", "settings")
        self.input_confirm.setMinimumSize(QtCore.QSize(200, 50))
        self.input_confirm.setMaximumSize(QtCore.QSize(400, 50))

        self.btn_register = QtWidgets.QPushButton("Зареєструватися")
        self.btn_register.clicked.connect(self.register_user)
        self.btn_register.setProperty("type", "start_continue")
        self.btn_register.setMinimumSize(QtCore.QSize(200, 50))
        self.btn_register.setMaximumSize(QtCore.QSize(400, 50))

        self.btn_back = QtWidgets.QPushButton("← Назад до входу")
        self.btn_back.clicked.connect(self.back_to_login.emit)
        self.btn_back.setProperty("type", "register")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(15)
        layout.addWidget(self.label_title)
        layout.addWidget(self.input_username)
        layout.addWidget(self.input_email)
        layout.addWidget(self.input_password)
        layout.addWidget(self.input_confirm)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.btn_back)

    def register_user(self):
        username = self.input_username.text()
        email = self.input_email.text()
        password = self.input_password.text()
        confirm_password = self.input_confirm.text()

        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Паролі не співпадають")
            return

        auth_service = AuthService()
        success, message = auth_service.register_user(username, password, email)

        if success:
            QtWidgets.QMessageBox.information(self, "Успіх", "Користувача успішно зареєстровано. Тепер ви можете увійти.")
            self.back_to_login.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", message)
