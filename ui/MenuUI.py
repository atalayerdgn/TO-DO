from qfluentwidgets import (
    FluentWindow, CardWidget, TitleLabel, BodyLabel, TransparentToolButton, LineEdit,
    ComboBox, TextEdit, PrimaryPushButton, CheckBox, FlowLayout,
    InfoBar, MessageBox, Dialog, ScrollArea, FluentIcon as FIF
)
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QSizePolicy, QSpacerItem, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize

class TaskCard(CardWidget):
    """Custom task card component with interactive elements"""
    edit_requested = pyqtSignal(object)
    delete_requested = pyqtSignal(object)

    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.setFixedHeight(80)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        self.priority_indicator = TransparentToolButton(self)
        self.priority_indicator.setIconSize(QSize(12, 12))
        self.priority_indicator.setFixedSize(24, 24)
        self.update_priority_color()
        self.checkbox = CheckBox(self.task['name'], self)
        self.checkbox.setChecked(self.task['completed'])
        self.desc_label = BodyLabel(self.task['description'], parent=self)
        self.desc_label.setStyleSheet("color: #666;")
        self.category_tag = BodyLabel(self.task['category'], parent=self)
        self.update_category_style()
        action_layout = QHBoxLayout()
        self.edit_btn = TransparentToolButton(FIF.EDIT, parent=self)
        self.delete_btn = TransparentToolButton(FIF.DELETE, parent=self)
        action_layout.addWidget(self.edit_btn)
        action_layout.addWidget(self.delete_btn)
        action_layout.setSpacing(10)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.checkbox)
        left_layout.addWidget(self.desc_label)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.category_tag, 0, Qt.AlignRight)
        right_layout.addLayout(action_layout)

        layout.addWidget(self.priority_indicator)
        layout.addLayout(left_layout)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(right_layout)

    def setup_connections(self):
        self.checkbox.stateChanged.connect(self.update_task_status)
        self.delete_btn.clicked.connect(lambda: self.delete_requested.emit(self))
        self.edit_btn.clicked.connect(lambda: self.edit_requested.emit(self))

    def update_task_status(self):
        self.task['completed'] = self.checkbox.isChecked()
        self.setStyleSheet("background-color: #f5f5f5;" if self.task['completed'] else "")

    def update_priority_color(self):
        colors = {
            'High': '#ff4040',
            'Medium': '#ffaa15',
            'Low': '#20b2aa'
        }
        self.priority_indicator.setStyleSheet(
            f"color: {colors.get(self.task['priority'], 'gray')};"
        )

    def update_category_style(self):
        self.category_tag.setStyleSheet(
            """
            padding: 4px 8px;
            border-radius: 4px;
            background-color: rgba(0, 120, 212, 0.1);
            color: #0078D4;
            """
        )

class MenuUI(FluentWindow):
    """Main application interface for task management"""
    backtohome_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tasks = []
        self.setWindowTitle("Smart Todo")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 600)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(40, 30, 40, 30)
        self.main_layout.setSpacing(20)
        header_layout = QHBoxLayout()
        self.title_label = TitleLabel("My Tasks", self)
        self.filter_combo = ComboBox(self)
        self.filter_combo.addItems(['All', 'Work', 'Personal', 'Shopping', 'Other'])
        self.search_input = LineEdit(self)
        self.search_input.setPlaceholderText("Search tasks...")
        self.search_input.setClearButtonEnabled(True)

        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.filter_combo, 0, Qt.AlignRight)
        header_layout.addWidget(self.search_input, 0, Qt.AlignRight)
        self.task_form = CardWidget(self)
        self.task_form.setFixedHeight(180)
        form_layout = QGridLayout(self.task_form)
        form_layout.setContentsMargins(20, 20, 20, 20)

        self.task_input = LineEdit(self)
        self.task_input.setPlaceholderText("Task title")
        self.desc_input = TextEdit(self)
        self.desc_input.setPlaceholderText("Description")
        self.priority_combo = ComboBox(self)
        self.priority_combo.addItems(['High', 'Medium', 'Low'])
        self.category_combo = ComboBox(self)
        self.category_combo.addItems(['Work', 'Personal', 'Shopping', 'Other'])
        self.add_btn = PrimaryPushButton("Add Task", self)

        form_layout.addWidget(QLabel("Title:"), 0, 0)
        form_layout.addWidget(self.task_input, 0, 1)
        form_layout.addWidget(QLabel("Priority:"), 0, 2)
        form_layout.addWidget(self.priority_combo, 0, 3)
        form_layout.addWidget(QLabel("Description:"), 1, 0)
        form_layout.addWidget(self.desc_input, 1, 1, 1, 3)
        form_layout.addWidget(QLabel("Category:"), 2, 0)
        form_layout.addWidget(self.category_combo, 2, 1)
        form_layout.addWidget(self.add_btn, 2, 3)

        # Task list display
        self.scroll_area = ScrollArea(self)
        self.scroll_widget = QWidget()
        self.flow_layout = FlowLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # Logout button
        self.logout_btn = PrimaryPushButton("Logout", self)

        # Main layout assembly
        self.main_layout.addLayout(header_layout)
        self.main_layout.addWidget(self.task_form)
        self.main_layout.addWidget(TitleLabel("Task List", self))
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.logout_btn, 0, Qt.AlignRight)

        central_widget.setObjectName("menuInterface")
        self.addSubInterface(central_widget, 'VIEW', "Tasks")

    def setup_connections(self):
        self.add_btn.clicked.connect(self.add_task)
        self.logout_btn.clicked.connect(self.backtohome_signal.emit)
        self.filter_combo.currentIndexChanged.connect(self.apply_filters)
        self.search_input.textChanged.connect(self.apply_filters)

    def apply_filters(self):
        current_filter = self.filter_combo.currentText()
        search_text = self.search_input.text().lower()
        for card in self.tasks:
            category_match = (current_filter == 'All' or card.task['category'] == current_filter)
            search_match = (search_text in card.task['name'].lower() or 
                            search_text in card.task['description'].lower())
            card.setVisible(category_match and search_match)

    def add_task(self):
        name = self.task_input.text().strip()
        if not name:
            InfoBar.error("Error", "Task title cannot be empty!", self)
            return

        task_data = {
            'name': name,
            'description': self.desc_input.toPlainText(),
            'priority': self.priority_combo.currentText(),
            'category': self.category_combo.currentText(),
            'completed': False
        }
        self._add_task_card(task_data)
        self.task_input.clear()
        self.desc_input.clear()
        InfoBar.success("Success", "Task added successfully!", self)

    def _add_task_card(self, task_data):
        card = TaskCard(task_data, self)
        card.delete_requested.connect(self.delete_task)
        card.edit_requested.connect(self.edit_task_dialog)
        self.flow_layout.addWidget(card)
        self.tasks.append(card)

    def delete_task(self, card):
        confirm = MessageBox("Confirm Delete", "Are you sure you want to delete this task?", self)
        if confirm.exec_() == QDialog.Accepted:
            self.flow_layout.removeWidget(card)
            card.deleteLater()
            self.tasks.remove(card)

    def edit_task_dialog(self, card):
        dialog = Dialog("Edit Task", card, self)
        container = QWidget(dialog)
        layout = QVBoxLayout(container)

        title_edit = LineEdit(container)
        title_edit.setText(card.task['name'])
        desc_edit = TextEdit(container)
        desc_edit.setText(card.task['description'])

        priority_combo = ComboBox(container)
        priority_combo.addItems(['High', 'Medium', 'Low'])
        priority_combo.setCurrentText(card.task['priority'])

        category_combo = ComboBox(container)
        category_combo.addItems(['Work', 'Personal', 'Shopping', 'Other'])
        category_combo.setCurrentText(card.task['category'])

        layout.addWidget(QLabel("Title:"))
        layout.addWidget(title_edit)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(desc_edit)
        layout.addWidget(QLabel("Priority:"))
        layout.addWidget(priority_combo)
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(category_combo)

        button_layout = QHBoxLayout()
        save_btn = PrimaryPushButton("Save", container)
        save_btn.clicked.connect(lambda: self._save_edit(card, title_edit, desc_edit, priority_combo, category_combo, dialog))
        cancel_btn = PrimaryPushButton("Cancel", container)
        cancel_btn.clicked.connect(dialog.close)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)

        dialog.addWidget(container)
        dialog.exec_()

    def _save_edit(self, card, title_edit, desc_edit, priority_combo, category_combo, dialog):
        card.task.update({
            'name': title_edit.text(),
            'description': desc_edit.toPlainText(),
            'priority': priority_combo.currentText(),
            'category': category_combo.currentText()
        })
        card.checkbox.setText(card.task['name'])
        card.desc_label.setText(card.task['description'])
        card.update_priority_color()
        card.category_tag.setText(card.task['category'])
        card.update_category_style()
        dialog.close()
