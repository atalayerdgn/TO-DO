from qfluentwidgets import (
    FluentWindow, PushButton, SubtitleLabel, FluentIcon as FIF, HyperlinkButton,
    TitleLabel, CardWidget, TransparentToolButton, InfoBar,
    IconWidget, SwitchButton
)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon
from utils.config import APP_NAME, APP_VERSION, APP_AUTHOR, GITHUB_URL, DEFAULT_FONT
from utils.widgets import CustomBannerWidget

class HomeUI(FluentWindow):
    """
    This class represents the home interface of the application.
    It inherits from FluentWindow and sets up the main window with buttons for login and registration.
    """
    login_signal = pyqtSignal()
    register_signal = pyqtSignal()
    setting_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - v{APP_VERSION}")
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface of the home window with an improved layout and design.
        """
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        banner = CustomBannerWidget(self)
        banner.setTitle(APP_NAME)
        banner.setContent(f"Task management application by {APP_AUTHOR}")
        banner.setImage("")
        main_layout.addWidget(banner)
        
        title_layout = QHBoxLayout()
        app_icon = IconWidget(FIF.CHECKBOX, self)
        app_icon.setFixedSize(64, 64)
        title_layout.addWidget(app_icon)
        
        title_container = QVBoxLayout()
        title = TitleLabel(APP_NAME, self)
        title.setFont(QFont(DEFAULT_FONT, 24, QFont.Bold))
        subtitle = SubtitleLabel(f"Version {APP_VERSION}", self)
        title_container.addWidget(title)
        title_container.addWidget(subtitle)
        title_layout.addLayout(title_container)
        title_layout.addStretch(1)
        
        main_layout.addLayout(title_layout)
        main_layout.addSpacing(20)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        login_card = CardWidget(self)
        login_layout = QVBoxLayout(login_card)
        login_icon = IconWidget(FIF.PEOPLE, self)
        login_icon.setFixedSize(48, 48)
        login_title = SubtitleLabel("Login", self)
        login_title.setAlignment(Qt.AlignCenter)
        login_description = QLabel("Access your tasks and continue where you left off", self)
        login_description.setWordWrap(True)
        login_description.setAlignment(Qt.AlignCenter)
        login_button = PushButton("Login Now", self)
        login_button.clicked.connect(self.login_signal.emit)
        login_button.setMinimumWidth(200)
        
        login_layout.addWidget(login_icon, alignment=Qt.AlignCenter)
        login_layout.addWidget(login_title)
        login_layout.addWidget(login_description)
        login_layout.addStretch(1)
        login_layout.addWidget(login_button, alignment=Qt.AlignCenter)
        login_layout.setContentsMargins(20, 20, 20, 20)
        cards_layout.addWidget(login_card)
        
        register_card = CardWidget(self)
        register_layout = QVBoxLayout(register_card)
        register_icon = IconWidget(FIF.ADD, self)
        register_icon.setFixedSize(48, 48)
        register_title = SubtitleLabel("Register", self)
        register_title.setAlignment(Qt.AlignCenter)
        register_description = QLabel("Create a new account to start organizing your tasks", self)
        register_description.setWordWrap(True)
        register_description.setAlignment(Qt.AlignCenter)
        register_button = PushButton("Sign Up", self)
        register_button.clicked.connect(self.register_signal.emit)
        register_button.setMinimumWidth(200)
        
        register_layout.addWidget(register_icon, alignment=Qt.AlignCenter)
        register_layout.addWidget(register_title)
        register_layout.addWidget(register_description)
        register_layout.addStretch(1)
        register_layout.addWidget(register_button, alignment=Qt.AlignCenter)
        register_layout.setContentsMargins(20, 20, 20, 20)
        cards_layout.addWidget(register_card)
        
        main_layout.addLayout(cards_layout)
        
        bottom_layout = QHBoxLayout()
        
        settings_button = PushButton("Settings", self)
        settings_button.setIcon(FIF.SETTING)
        settings_button.clicked.connect(self.setting_signal.emit)
        
        github_link = HyperlinkButton(FIF.GITHUB, GITHUB_URL, "GitHub", self)
        
        bottom_layout.addWidget(settings_button)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(github_link)
        
        main_layout.addStretch(1)
        main_layout.addLayout(bottom_layout)
        
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Dark Mode:", self)
        theme_switch = SwitchButton(self)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(theme_switch)
        theme_layout.addStretch(1)
        
        main_layout.addLayout(theme_layout)
        
        def on_theme_changed(checked):
            InfoBar.success(
                "Theme Changed",
                "Dark mode enabled" if checked else "Light mode enabled",
                duration=3000,
                parent=self
            )
        
        theme_switch.checkedChanged.connect(on_theme_changed)
        
        central_widget.setObjectName("homeInterface")
        self.addSubInterface(central_widget, FIF.HOME, "Home")
