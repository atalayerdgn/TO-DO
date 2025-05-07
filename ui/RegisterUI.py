from qfluentwidgets import (
    FluentWindow, FluentIcon as FIF, SubtitleLabel, LineEdit, 
    PushButton, PasswordLineEdit, pyqtSignal, CardWidget, 
    TitleLabel, InfoBar, IconWidget, TransparentToolButton,
    CheckBox
)
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from utils.RegisterUtils import RegisterUtils
from utils.config import APP_NAME, DEFAULT_FONT
from utils.widgets import CustomBannerWidget


class RegisterUI(FluentWindow, RegisterUtils):
    """
    Enhanced registration interface with improved user experience.
    """
    register_signal = pyqtSignal()
    back_home = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Initializes the RegisterUI class.
        """
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - Registration")
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.init_ui()
        
    def init_ui(self):
        """
        Initializes the user interface of the register window with an improved layout and design.
        """
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        banner = CustomBannerWidget(self)
        banner.setTitle("Create Your Account")
        banner.setContent("Sign up to start managing your tasks effectively")
        banner.setBackgroundColor(QColor(76, 175, 80))
        main_layout.addWidget(banner)
        
        content_layout = QHBoxLayout()
        
        register_card = CardWidget(self)
        register_card.setFixedWidth(600)
        register_form_layout = QVBoxLayout(register_card)
        register_form_layout.setContentsMargins(30, 30, 30, 30)
        register_form_layout.setSpacing(15)
        
        header_layout = QHBoxLayout()
        title_icon = IconWidget(FIF.ADD, self)
        title_icon.setFixedSize(48, 48)
        title = TitleLabel("Join Us Today", self)
        title.setFont(QFont(DEFAULT_FONT, 18, QFont.Bold))
        header_layout.addWidget(title_icon)
        header_layout.addWidget(title)
        header_layout.addStretch(1)
        register_form_layout.addLayout(header_layout)
        
        subtitle = SubtitleLabel("Create an account to organize your tasks", self)
        register_form_layout.addWidget(subtitle)
        register_form_layout.addSpacing(20)
        
        username_layout = QHBoxLayout()
        username_icon = IconWidget(FIF.PEOPLE, self)
        username_icon.setFixedSize(24, 24)
        self.username_input = LineEdit(self)
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setClearButtonEnabled(True)
        username_layout.addWidget(username_icon)
        username_layout.addWidget(self.username_input)
        register_form_layout.addLayout(username_layout)
        
        username_req = QLabel("Username must be at least 4 characters", self)
        username_req.setStyleSheet("color: gray; font-size: 11px;")
        register_form_layout.addWidget(username_req)
        
        email_layout = QHBoxLayout()
        email_icon = IconWidget(FIF.MAIL, self)
        email_icon.setFixedSize(24, 24)
        self.email_input = LineEdit(self)
        self.email_input.setPlaceholderText("Your email address")
        self.email_input.setClearButtonEnabled(True)
        email_layout.addWidget(email_icon)
        email_layout.addWidget(self.email_input)
        register_form_layout.addLayout(email_layout)
        
        email_req = QLabel("Please enter a valid email address", self)
        email_req.setStyleSheet("color: gray; font-size: 11px;")
        register_form_layout.addWidget(email_req)
        
        password_layout = QHBoxLayout()
        password_icon = IconWidget(FIF.CERTIFICATE, self)
        password_icon.setFixedSize(24, 24)
        self.password_input = PasswordLineEdit(self)
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setClearButtonEnabled(True)
        password_layout.addWidget(password_icon)
        password_layout.addWidget(self.password_input)
        register_form_layout.addLayout(password_layout)
        
        password_req = QLabel("Password must be at least 6 characters", self)
        password_req.setStyleSheet("color: gray; font-size: 11px;")
        register_form_layout.addWidget(password_req)
        
        terms_layout = QHBoxLayout()
        self.terms_checkbox = CheckBox("I agree to the Terms of Service and Privacy Policy", self)
        terms_layout.addWidget(self.terms_checkbox)
        register_form_layout.addLayout(terms_layout)
        
        register_form_layout.addSpacing(20)
        
        register_button = PushButton("Create Account", self)
        register_button.setIcon(FIF.ACCEPT)
        register_button.clicked.connect(self.onregister)
        register_form_layout.addWidget(register_button)
        
        login_layout = QHBoxLayout()
        login_text = QLabel("Already have an account?", self)
        login_link = TransparentToolButton("Sign In", self)
        login_link.clicked.connect(self.navigate_to_login)
        login_layout.addWidget(login_text)
        login_layout.addWidget(login_link)
        login_layout.addStretch(1)
        register_form_layout.addLayout(login_layout)
        
        content_layout.addWidget(register_card, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(content_layout)
        main_layout.addStretch(1)
        
        back_button = PushButton("Back to Home", self)
        back_button.setIcon(FIF.HOME)
        back_button.clicked.connect(self.navigate_back)
        main_layout.addWidget(back_button, alignment=Qt.AlignLeft)
        
        central_widget.setObjectName("registerInterface")
        self.addSubInterface(central_widget, FIF.ADD, "Register")
    
    def navigate_back(self):
        """Navigate back to home screen"""
        self.hide()
        self.back_home.emit()
    
    def navigate_to_login(self):
        """Navigate to login screen"""
        self.register_signal.emit()
    
    def onregister(self):
        """
        Handles the register button click event with improved validation.
        """
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not username:
            InfoBar.error(
                "Validation Error",
                "Please enter a username",
                parent=self
            )
            self.username_input.setFocus()
            return
            
        if len(username) < 4:
            InfoBar.error(
                "Validation Error",
                "Username must be at least 4 characters long",
                parent=self
            )
            self.username_input.setFocus()
            return
        
        if not email:
            InfoBar.error(
                "Validation Error",
                "Please enter your email address",
                parent=self
            )
            self.email_input.setFocus()
            return
            
        if "@" not in email or "." not in email:
            InfoBar.error(
                "Validation Error",
                "Please enter a valid email address",
                parent=self
            )
            self.email_input.setFocus()
            return
            
        if not password:
            InfoBar.error(
                "Validation Error",
                "Please create a password",
                parent=self
            )
            self.password_input.setFocus()
            return
            
        if len(password) < 6:
            InfoBar.error(
                "Validation Error",
                "Password must be at least 6 characters long",
                parent=self
            )
            self.password_input.setFocus()
            return
            
        if not self.terms_checkbox.isChecked():
            InfoBar.warning(
                "Terms & Conditions",
                "Please agree to the Terms of Service and Privacy Policy",
                parent=self
            )
            return
        
        InfoBar.info(
            "Creating Account",
            "Please wait while we create your account...",
            duration=2000,
            parent=self
        )
        
        registration_result = self.handle_register(username, email, password)
        
        if registration_result == 1:
            InfoBar.success(
                "Registration Successful",
                "Your account has been created successfully!",
                duration=3000,
                parent=self
            )
            self.register_signal.emit()
        else:
            error_messages = {
                0: "An error occurred during registration. Please try again.",
                -1: "Username already exists. Please choose a different username.",
                -2: "Email already registered. Please use a different email or log in.",
                -3: "Invalid input. Please check your information and try again."
            }
            
            error_message = error_messages.get(registration_result, "Registration failed. Please try again.")
            
            InfoBar.error(
                "Registration Failed",
                error_message,
                parent=self
            )
