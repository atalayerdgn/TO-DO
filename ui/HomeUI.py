from qfluentwidgets import FluentWindow, PushButton, SubtitleLabel, FluentIcon, HyperlinkButton
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

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
        self.setWindowTitle("Home")
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface of the home window.
        It creates a central widget with a vertical layout, adds a subtitle label,
        """
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        subtitle_label = SubtitleLabel("To-do Application\n Written By Atalay Erdogan", self)
        gitlinkbutton = HyperlinkButton(FluentIcon.LINK, "https://github.com/atalayerdgn", 'Github')
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        main_layout.addWidget(gitlinkbutton, alignment=Qt.AlignCenter)
        login_button = PushButton("Login", self)
        login_button.clicked.connect(self.login_signal.emit)
        main_layout.addWidget(login_button)
        register_button = PushButton("Register", self)
        register_button.clicked.connect(self.register_signal.emit)
        main_layout.addWidget(register_button)
        setting_button = PushButton("Settings", self)
        setting_button.clicked.connect(self.setting_signal.emit)
        main_layout.addWidget(setting_button)
        central_widget.setObjectName("homeInterface")
        self.addSubInterface(central_widget, FluentIcon.HOME, "Home")
