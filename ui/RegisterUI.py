from qfluentwidgets import FluentWindow, FluentIcon as FIF, SubtitleLabel, LineEdit, PushButton, PasswordLineEdit, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget
import os
from PyQt5.QtCore import Qt
from utils.RegisterUtils import RegisterUtils


class RegisterUI(FluentWindow, RegisterUtils):
    register_signal = pyqtSignal()
    def __init__(self, parent=None):
        """
        Initializes the RegisterUI class.
        """
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.init_ui()
    def init_ui(self):
        """
        Initializes the user interface of the register window.
        It creates a central widget with a vertical layout, adds a subtitle label,
        and sets up input fields for username, email, and password.
        """
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        subtitle_label = SubtitleLabel("Register", self)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        self.username_input = LineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedWidth(300)
        self.email_input = LineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedWidth(300)
        self.password_input = PasswordLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedWidth(300)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(self.password_input)
        register_button = PushButton("Register", self)
        register_button.clicked.connect(self.onregister)
        main_layout.addWidget(register_button)
        central_widget.setObjectName("registerInterface")
        self.addSubInterface(central_widget, FIF.ADD, "Register")
    def onregister (self):
        """
        Handles the register button click event.
        It retrieves the input values and calls the handle_register method from RegisterUtils.
        """
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        if self.handle_register(username, email, password) == 1:
            self.register_signal.emit()
