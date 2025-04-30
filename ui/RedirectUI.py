from qfluentwidgets import FluentWindow, SubtitleLabel, FluentIcon as FIF
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer

class RedirectUI(FluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface for the redirecting screen.
        :return: None
        """
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        self.subtitle_label = SubtitleLabel("Redirecting.", self)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.subtitle_label)

        central_widget.setObjectName("redirectInterface")
        self.addSubInterface(central_widget, FIF.ACCEPT, "Redirecting...")
        self.dots_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_redirect_text)
        self.timer.start(350)

    def update_redirect_text(self):
        """
        Updates the redirecting text with dots.
        :return: None
        """
        self.dots_count = (self.dots_count + 1) % 4
        dots = '.' * self.dots_count
        self.subtitle_label.setText(f"Redirecting{dots}")
