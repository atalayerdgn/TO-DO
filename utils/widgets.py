from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtProperty
from PyQt5.QtGui import QColor, QFont, QPainter, QLinearGradient
from qfluentwidgets import TitleLabel, BodyLabel, CardWidget
from utils.config import DEFAULT_FONT

class CustomBannerWidget(CardWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._title = ""
        self._content = ""
        self._image_path = ""
        self._bg_color = QColor(0, 120, 215)
        
        self.setFixedHeight(120)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(5)
        
        self.title_label = TitleLabel(self._title)
        self.title_label.setFont(QFont(DEFAULT_FONT, 16, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        
        self.content_label = BodyLabel(self._content)
        self.content_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.content_label)
        layout.addStretch(1)
    
    def setTitle(self, title):
        self._title = title
        self.title_label.setText(title)
    
    def setContent(self, content):
        self._content = content
        self.content_label.setText(content)
    
    def setImage(self, image_path):
        self._image_path = image_path
    
    def setBackgroundColor(self, color):
        if isinstance(color, str):
            self._bg_color = QColor(color)
        else:
            self._bg_color = color
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, self._bg_color)
        gradient.setColorAt(1, self._bg_color.lighter(130))
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 8, 8)
