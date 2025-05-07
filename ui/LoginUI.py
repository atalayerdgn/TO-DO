from qfluentwidgets import (
    FluentWindow, FluentIcon as FIF, SubtitleLabel, LineEdit, PushButton, 
    PasswordLineEdit, pyqtSignal, CardWidget, TitleLabel, InfoBar,
    IconWidget, TransparentToolButton
)
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from utils.LoginUtils import LoginUtils
from utils.config import APP_NAME, DEFAULT_FONT
from utils.widgets import CustomBannerWidget

current_user = None

class LoginUI(FluentWindow, LoginUtils):
    """
    This class represents the login interface of the application.
    """
    login_signal = pyqtSignal()
    register_signal = pyqtSignal()
    back_home = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - Login")
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.init_ui()
    
    def init_ui(self):
        """
        Initializes the user interface of the login window with an improved layout and design.
        """
        central_widget = QFrame(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        banner = CustomBannerWidget(self)
        banner.setTitle("Welcome Back")
        banner.setContent("Sign in to access your tasks")
        banner.setBackgroundColor(QColor(0, 128, 128))
        main_layout.addWidget(banner)
        
        content_layout = QHBoxLayout()
        
        login_card = CardWidget(self)
        login_card.setFixedWidth(500)
        login_form_layout = QVBoxLayout(login_card)
        login_form_layout.setContentsMargins(30, 30, 30, 30)
        login_form_layout.setSpacing(15)
        
        title_icon = IconWidget(FIF.PEOPLE, self)
        title_icon.setFixedSize(48, 48)
        title = TitleLabel("Login to Your Account", self)
        title.setFont(QFont(DEFAULT_FONT, 18, QFont.Bold))
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(title_icon)
        header_layout.addWidget(title)
        header_layout.addStretch(1)
        login_form_layout.addLayout(header_layout)
        
        subtitle = SubtitleLabel("", self)
        login_form_layout.addWidget(subtitle)
        login_form_layout.addSpacing(20)
        
        username_layout = QHBoxLayout()
        username_icon = IconWidget(FIF.PEOPLE, self)
        username_icon.setFixedSize(24, 24)
        self.username_input = LineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setClearButtonEnabled(True)
        username_layout.addWidget(username_icon)
        username_layout.addWidget(self.username_input)
        login_form_layout.addLayout(username_layout)
        
        email_layout = QHBoxLayout()
        email_icon = IconWidget(FIF.MAIL, self)
        email_icon.setFixedSize(24, 24)
        self.email_input = LineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.email_input.setClearButtonEnabled(True)
        email_layout.addWidget(email_icon)
        email_layout.addWidget(self.email_input)
        login_form_layout.addLayout(email_layout)
        
        password_layout = QHBoxLayout()
        password_icon = IconWidget(FIF.CERTIFICATE, self)
        password_icon.setFixedSize(24, 24)
        self.password_input = PasswordLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setClearButtonEnabled(True)
        password_layout.addWidget(password_icon)
        password_layout.addWidget(self.password_input)
        login_form_layout.addLayout(password_layout)
        
        login_form_layout.addSpacing(20)
        
        login_button = PushButton("Sign In", self)
        login_button.setIcon(FIF.CHEVRON_RIGHT)
        login_button.clicked.connect(self.login_click)
        login_form_layout.addWidget(login_button)
        
        register_layout = QHBoxLayout()
        register_text = QLabel("Don't have an account?", self)
        register_button = TransparentToolButton("Register Now", self)
        register_button.clicked.connect(self.register_signal.emit)
        register_layout.addWidget(register_text)
        register_layout.addWidget(register_button)
        register_layout.addStretch(1)
        login_form_layout.addLayout(register_layout)
        
        content_layout.addWidget(login_card, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(content_layout)
        main_layout.addStretch(1)
        
        back_button = PushButton("Back to Home", self)
        back_button.setIcon(FIF.HOME)
        back_button.clicked.connect(self.navigateBack)
        main_layout.addWidget(back_button, alignment=Qt.AlignLeft)
        
        central_widget.setObjectName("loginInterface")
        self.addSubInterface(central_widget, FIF.ACCEPT, "Login")
    
    def navigateBack(self):
        """Navigate back to home screen"""
        self.hide()
        self.back_home.emit()
    
    def login_click(self):
        """
        Handles the login button click event with improved validation.
        It retrieves the input values and calls the handle_login method from LoginUtils.
        """
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not username:
            InfoBar.error(
                "Validation Error",
                "Please enter your username",
                parent=self
            )
            self.username_input.setFocus()
            return
        
        if not email:
            InfoBar.error(
                "Validation Error",
                "Please enter your email",
                parent=self
            )
            self.email_input.setFocus()
            return
            
        if not password:
            InfoBar.error(
                "Validation Error",
                "Please enter your password",
                parent=self
            )
            self.password_input.setFocus()
            return
        
        global current_user
        current_user = username
        
        InfoBar.info(
            "Logging in",
            "Please wait while we verify your credentials...",
            duration=2000,
            parent=self
        )
        
        val = self._on_login_clicked(username, email, password)
        if val:
            InfoBar.success(
                "Login Successful",
                f"Welcome back, {username}!",
                duration=3000,
                parent=self
            )
            self.login_signal.emit()
        else:
            InfoBar.error(
                "Login Failed",
                "Invalid username, email, or password. Please try again.",
                parent=self
            )
            self.password_input.clear()

def get_current_user():
    """
    Returns the current user.
    :return: str
    """
    return current_user
