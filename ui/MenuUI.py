from qfluentwidgets import (
    FluentWindow, PushButton, SubtitleLabel, HyperlinkButton, TitleLabel,
    FluentIcon as FIF, ComboBox, LineEdit, TextEdit, CheckBox, InfoBar
)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal

class MenuUI(FluentWindow):
    backtohome_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Manager")
        self.resize(800, 600)

        self.tasks = []

        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(20)
        self.title = TitleLabel("📝 Manage Your Tasks")
        self.subtitle = SubtitleLabel("Add, view and organize your tasks efficiently")
        self.task_input = LineEdit(self)
        self.task_input.setPlaceholderText("Task title")
        self.desc_input = TextEdit(self)
        self.desc_input.setPlaceholderText("Description...")
        self.priority_combo = ComboBox(self)
        self.priority_combo.addItems(["High", "Medium", "Low"])
        self.priority_combo.setCurrentText("Medium")
        self.category_combo = ComboBox(self)
        self.category_combo.addItems(["Work", "Personal", "Shopping", "Other"])
        self.category_combo.setCurrentText("Work")
        self.add_btn = PushButton("➕ Add Task", self)
        self.logout_btn = HyperlinkButton(text="Logout", url="", icon=FIF.LAYOUT)
        self.logout_btn.mousePressEvent = lambda event: self.backtohome_signal.emit()
        self.task_area = QWidget(self)
        self.task_layout = QVBoxLayout(self.task_area)
        self.task_layout.setSpacing(10)
        self.task_layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.task_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_input)
        layout.addWidget(QLabel("Priority:"))
        layout.addWidget(self.priority_combo)
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_combo)
        layout.addWidget(self.add_btn)
        layout.addWidget(QLabel("Your Tasks:"))
        layout.addWidget(self.task_area)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.logout_btn, alignment=Qt.AlignRight)
        central_widget.setObjectName("menuInterface")
        self.addSubInterface(central_widget, FIF.MENU, "Task Manager")

    def setup_connections(self):
        self.add_btn.clicked.connect(self.add_task)
        self.logout_btn.clicked.connect(self.backtohome_signal.emit)

    def add_task(self):
        title = self.task_input.text().strip()
        if not title:
            InfoBar.error("Error", "Task title cannot be empty!", self)
            return

        description = self.desc_input.toPlainText().strip()
        priority = self.priority_combo.currentText()
        category = self.category_combo.currentText()

        task_text = f"✅ {title} | {priority} | {category}\n{description}"
        task_label = QLabel(task_text, self)
        task_label.setWordWrap(True)
        task_label.setStyleSheet("background: #f1f1f1; padding: 10px; border-radius: 6px;")
        self.task_layout.addWidget(task_label)

        self.tasks.append(task_label)

        self.task_input.clear()
        self.desc_input.clear()
        InfoBar.success("Success", "Task added successfully!", self)
