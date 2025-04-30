from qfluentwidgets import FluentWindow, FluentIcon as FIF, SubtitleLabel, LineEdit, PushButton, PasswordLineEdit, pyqtSignal
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout
import os
from PyQt5.QtCore import Qt
from utils.LoginUtils import LoginUtils

class LoginUI(FluentWindow ,LoginUtils):
    """
    This class represents the login interface of the application.
    """
    login_signal = pyqtSignal()
    register_signal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.init_ui()
    def init_ui(self):
        """
        Initializes the user interface of the login window.
        It creates a central widget with a vertical layout, adds a subtitle label,
        and sets up input fields for username and password.
        """
        central_widget = QFrame(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        subtitle_label = SubtitleLabel("Login", self)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        self.username_input = LineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedWidth(300)
        self.email_input = LineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedWidth(300)
        self.password_input = PasswordLineEdit(self)
        self.password_input.setFixedWidth(300)
        self.password_input.setPlaceholderText("Password")
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(self.password_input)
        login_button = PushButton("Login", self)
        login_button.clicked.connect(self.login_signal.emit)
        login_button.clicked.connect(self.login_click)
        main_layout.addWidget(login_button)
        register_button = PushButton("Register", self)
        register_button.clicked.connect(self.register_signal.emit)
        central_widget.setObjectName("loginInterface")
        self.addSubInterface(central_widget, FIF.ACCEPT, "Login")
        main_layout.addWidget(register_button)
    def login_click(self):
        """
        Handles the login button click event.
        It retrieves the input values and calls the handle_login method from LoginUtils.
        """
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        self._on_login_clicked(username, email, password)
        