from qfluentwidgets import (
    FluentWindow, PushButton, SubtitleLabel, HyperlinkButton, TitleLabel,
    FluentIcon as FIF, ComboBox, LineEdit, TextEdit, CheckBox, InfoBar,
    CardWidget, IconWidget, SearchLineEdit, TabBar, SegmentedWidget,
    ToggleButton, SwitchButton, DatePicker, MessageBox, setTheme, Theme
)
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
    QSizePolicy, QScrollArea, QSplitter, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QColor, QFont
from db.tasks import add_task, delete_task_db
from ui.LoginUI import get_current_user
from utils.config import APP_NAME, DEFAULT_FONT

class MenuUI(FluentWindow):
    """
    Enhanced task manager interface with improved user experience and additional features.
    """
    backtohome_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - Task Manager")
        self.resize(1200, 800)
        self.tasks = []
        self.current_view = "all"
        self.is_darkmode = False
        self.init_ui()
        self.setup_connections()
        self.load_tasks()

    def init_ui(self):
        """
        Initializes the enhanced user interface of the task manager window.
        """
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        header_layout = QHBoxLayout()
        user_info_layout = QHBoxLayout()
        user_icon = IconWidget(FIF.PEOPLE, self)
        user_icon.setFixedSize(28, 28)
        self.user_label = QLabel(f"Logged in as: {get_current_user()}", self)
        user_info_layout.addWidget(user_icon)
        user_info_layout.addWidget(self.user_label)
        header_layout.addStretch(1)
        header_layout.addLayout(user_info_layout)
        
        main_layout.addLayout(header_layout)
        self.tab_bar = TabBar(self)
        self.tab_bar.addTab("all", "All Tasks")
        self.tab_bar.addTab("today", "Today") 
        self.tab_bar.addTab("important", "Important")
        self.tab_bar.addTab("completed", "Completed")
        main_layout.addWidget(self.tab_bar)

        self.content_splitter = QSplitter(Qt.Horizontal, self)
        left_panel = CardWidget(self)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(10)
        
        form_title = SubtitleLabel("Add New Task", self)
        form_title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(form_title)
        title_layout = QHBoxLayout()
        title_icon = IconWidget(FIF.EDIT, self)
        title_icon.setFixedSize(20, 20)
        title_layout.addWidget(title_icon)
        title_layout.addWidget(QLabel("Task Title:"))
        left_layout.addLayout(title_layout)
        
        self.task_input = LineEdit(self)
        self.task_input.setPlaceholderText("Enter task title")
        self.task_input.setClearButtonEnabled(True)
        left_layout.addWidget(self.task_input)
        desc_layout = QHBoxLayout()
        desc_icon = IconWidget(FIF.FONT, self)
        desc_icon.setFixedSize(20, 20)
        desc_layout.addWidget(desc_icon)
        desc_layout.addWidget(QLabel("Description:"))
        left_layout.addLayout(desc_layout)
        
        self.desc_input = TextEdit(self)
        self.desc_input.setPlaceholderText("Task details...")
        self.desc_input.setMaximumHeight(100)
        left_layout.addWidget(self.desc_input)
        date_layout = QHBoxLayout()
        date_icon = IconWidget(FIF.CALENDAR, self)
        date_icon.setFixedSize(20, 20)
        date_layout.addWidget(date_icon)
        date_layout.addWidget(QLabel("Due Date:"))
        left_layout.addLayout(date_layout)
        
        self.date_picker = DatePicker(self)
        self.date_picker.setDate(QDate.currentDate())
        left_layout.addWidget(self.date_picker)
        
        priority_layout = QHBoxLayout()
        priority_icon = IconWidget(FIF.FLAG, self)
        priority_icon.setFixedSize(20, 20)
        priority_layout.addWidget(priority_icon)
        priority_layout.addWidget(QLabel("Priority:"))
        left_layout.addLayout(priority_layout)
        
        self.priority_combo = ComboBox(self)
        self.priority_combo.addItems(["High", "Medium", "Low"])
        self.priority_combo.setCurrentText("Medium")
        left_layout.addWidget(self.priority_combo)
        
        category_layout = QHBoxLayout()
        category_icon = IconWidget(FIF.TAG, self)
        category_icon.setFixedSize(20, 20)
        category_layout.addWidget(category_icon)
        category_layout.addWidget(QLabel("Category:"))
        left_layout.addLayout(category_layout)
        
        self.category_combo = ComboBox(self)
        self.category_combo.addItems(["Work", "Personal", "Shopping", "Health", "Education", "Other"])
        self.category_combo.setCurrentText("Work")
        left_layout.addWidget(self.category_combo)
        important_layout = QHBoxLayout()
        self.important_check = SwitchButton("Mark as Important", self)
        important_layout.addWidget(self.important_check)
        left_layout.addLayout(important_layout)
        
        left_layout.addSpacing(10)
        self.add_btn = PushButton("Add Task", self)
        self.add_btn.setIcon(FIF.ADD)
        left_layout.addWidget(self.add_btn)
        self.reset_btn = PushButton("Clear Form", self)
        self.reset_btn.setIcon(FIF.CANCEL)
        left_layout.addWidget(self.reset_btn)
        left_layout.addStretch(1)
        right_panel = QWidget(self)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)
        
        search_layout = QHBoxLayout()
        self.search_box = SearchLineEdit(self)
        self.search_box.setPlaceholderText("Search tasks...")
        search_layout.addWidget(self.search_box)
        
        self.filter_combo = ComboBox(self)
        self.filter_combo.addItems(["All Categories", "Work", "Personal", "Shopping", "Health", "Education", "Other"])
        self.filter_combo.setCurrentText("All Categories")
        search_layout.addWidget(self.filter_combo)
        
        right_layout.addLayout(search_layout)
        
        self.task_scroll = QScrollArea(self)
        self.task_scroll.setWidgetResizable(True)
        self.task_scroll.setFrameShape(QFrame.NoFrame)
        
        self.task_container = QWidget(self)
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setAlignment(Qt.AlignTop)
        self.task_layout.setSpacing(10)
        
        self.task_scroll.setWidget(self.task_container)
        right_layout.addWidget(self.task_scroll)
        self.content_splitter.addWidget(left_panel)
        self.content_splitter.addWidget(right_panel)
        self.content_splitter.setSizes([300, 700])
        
        main_layout.addWidget(self.content_splitter)
        status_layout = QHBoxLayout()
        self.task_count_label = QLabel("0 tasks", self)
        self.logout_btn = PushButton("Logout", self)
        self.logout_btn.setIcon(FIF.RETURN)
        self.theme_switch = SwitchButton("Dark Mode", self)
        
        status_layout.addWidget(self.task_count_label)
        status_layout.addStretch(1)
        status_layout.addWidget(self.theme_switch)
        status_layout.addWidget(self.logout_btn)
        
        main_layout.addLayout(status_layout)
        
        central_widget.setObjectName("menuInterface")
        self.addSubInterface(central_widget, FIF.MENU, "Task Manager")

    def setup_connections(self):
        """
        Sets up the signal-slot connections for all interactive elements.
        """
        self.add_btn.clicked.connect(self.add_task)
        self.reset_btn.clicked.connect(self.reset_form)
        self.logout_btn.clicked.connect(self.navigate_back)
        self.tab_bar.currentChanged.connect(self.filter_by_tab)
        self.search_box.textChanged.connect(self.filter_tasks)
        self.filter_combo.currentTextChanged.connect(self.filter_tasks)
        self.theme_switch.checkedChanged.connect(self.toggle_theme)

    def load_tasks(self):
        """
        Load tasks from database - placeholder for actual implementation
        """
        self.update_task_count()

    def update_task_count(self):
        """
        Update the task count display in the status bar
        """
        task_count = len(self.tasks)
        self.task_count_label.setText(f"{task_count} task{'s' if task_count != 1 else ''}")

    def reset_form(self):
        """
        Clear all form fields
        """
        self.task_input.clear()
        self.desc_input.clear()
        self.date_picker.setDate(QDate.currentDate())
        self.priority_combo.setCurrentText("Medium")
        self.category_combo.setCurrentText("Work")
        self.important_check.setChecked(False)
        
        InfoBar.success(
            "Form Reset",
            "The form has been cleared",
            duration=2000,
            parent=self
        )

    def add_task(self):
        """
        Add a new task with enhanced validation and visual feedback
        """
        current_user = get_current_user()
        title = self.task_input.text().strip()
        if not title:
            InfoBar.error(
                "Validation Error",
                "Task title cannot be empty!",
                parent=self
            )
            self.task_input.setFocus()
            return
            
        description = self.desc_input.toPlainText().strip()
        priority = self.priority_combo.currentText()
        category = self.category_combo.currentText()
        
        try:
            due_date = self.date_picker.getDate().toString("yyyy-MM-dd")
        except Exception as e:
            due_date = QDate.currentDate().toString("yyyy-MM-dd")
            
        is_important = self.important_check.isChecked()
        priority_color = {
            "High": "#ef5350",    
            "Medium": "#ffb74d",  
            "Low": "#42a5f5"      
        }.get(priority, "#9e9e9e")
        task_card = CardWidget(self)
        task_layout = QVBoxLayout(task_card)
        task_layout.setContentsMargins(10, 10, 10, 10)
        task_layout.setSpacing(5)
        header_layout = QHBoxLayout()
        status_icon = IconWidget(FIF.CHECKBOX, self)
        status_icon.setFixedSize(24, 24)
        title_label = QLabel(title, self)
        title_label.setFont(QFont(DEFAULT_FONT, 12, QFont.Bold))
        important_icon = IconWidget(FIF.PIN, self)
        important_icon.setFixedSize(24, 24)
        important_icon.setVisible(is_important)
        
        header_layout.addWidget(status_icon)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(important_icon)
        
        task_layout.addLayout(header_layout)
        meta_layout = QHBoxLayout()
        category_layout = QHBoxLayout()
        category_icon = IconWidget(FIF.TAG, self)
        category_icon.setFixedSize(16, 16)
        category_label = QLabel(category, self)
        category_layout.addWidget(category_icon)
        category_layout.addWidget(category_label)
        priority_layout = QHBoxLayout()
        priority_icon = IconWidget(FIF.FLAG, self)
        priority_icon.setFixedSize(16, 16)
        priority_label = QLabel(priority, self)
        priority_layout.addWidget(priority_icon)
        priority_layout.addWidget(priority_label)
        date_layout = QHBoxLayout()
        date_icon = IconWidget(FIF.CALENDAR, self)
        date_icon.setFixedSize(16, 16)
        date_label = QLabel(due_date, self)
        date_layout.addWidget(date_icon)
        date_layout.addWidget(date_label)
        
        meta_layout.addLayout(category_layout)
        meta_layout.addStretch(1)
        meta_layout.addLayout(priority_layout)
        meta_layout.addStretch(1)
        meta_layout.addLayout(date_layout)
        
        task_layout.addLayout(meta_layout)
        if description:
            desc_label = QLabel(description, self)
            desc_label.setWordWrap(True)
            task_layout.addWidget(desc_label)
        actions_layout = QHBoxLayout()
        complete_btn = PushButton("Complete", self)
        complete_btn.setIcon(FIF.CHECKBOX)
        edit_btn = PushButton("Edit", self)
        edit_btn.setIcon(FIF.EDIT)
        delete_btn = PushButton("Delete", self)
        delete_btn.setIcon(FIF.DELETE)
        
        actions_layout.addWidget(complete_btn)
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        
        task_layout.addLayout(actions_layout)
        
        task_card.setStyleSheet(f"background-color: {priority_color};")
        
        def complete_task():
            status_icon.setIcon(FIF.COMPLETED)
            task_card.setStyleSheet("background-color: #2e7d32;")
            
            try:
                pass
            except Exception as e:
                print(f"Error marking task as completed: {e}")
            
            InfoBar.success(
                "Task Completed",
                f"Task '{title}' marked as completed",
                duration=2000,
                parent=self
            )
            
        def edit_task():
            self.task_input.setText(title)
            self.desc_input.setText(description)
            self.priority_combo.setCurrentText(priority)
            self.category_combo.setCurrentText(category)
            
            try:
                date_obj = QDate.fromString(due_date, "yyyy-MM-dd")
                self.date_picker.setDate(date_obj)
            except Exception as e:
                self.date_picker.setDate(QDate.currentDate())
                
            self.important_check.setChecked(is_important)
            
            self.delete_task_internal(task_card)
            
            InfoBar.info(
                "Edit Task",
                f"Editing task '{title}'",
                duration=2000,
                parent=self
            )
            
        def delete_task_action():
            msg_box = MessageBox(
                parent=self,
                title="Confirm Deletion",
                content=f"Are you sure you want to delete task '{title}'?"
            )
            msg_box.yesButton.setText("Delete")
            msg_box.cancelButton.setText("Cancel")
            
            if msg_box.exec_():
                self.delete_task_internal(task_card)
                delete_task_db(username=current_user, task=description)
                InfoBar.success(
                    "Task Deleted",
                    f"Task '{title}' was deleted",
                    duration=2000,
                    parent=self
                )
        
        complete_btn.clicked.connect(complete_task)
        edit_btn.clicked.connect(edit_task)
        delete_btn.clicked.connect(delete_task_action)
        
        self.task_layout.insertWidget(0, task_card)
        self.tasks.append(task_card)
        
        add_task(current_user, description)
        
        self.update_task_count()
        
        self.reset_form()
        
        InfoBar.success(
            "Task Added",
            f"New task '{title}' added successfully!",
            duration=2000,
            parent=self
        )

    def delete_task_internal(self, task_widget):
        """
        Delete a task widget from the UI
        """
        self.task_layout.removeWidget(task_widget)
        task_widget.deleteLater()
        
        if task_widget in self.tasks:
            self.tasks.remove(task_widget)
            
        self.update_task_count()

    def filter_by_tab(self, index):
        """
        Filter tasks based on the selected tab
        """
        if index == 0:
            tab_text = "All Tasks"
            self.current_view = "all"
        elif index == 1:
            tab_text = "Today"
            self.current_view = "today"
        elif index == 2:
            tab_text = "Important"
            self.current_view = "important"
        elif index == 3:
            tab_text = "Completed"
            self.current_view = "completed"
            
        self.filter_tasks()
        
        InfoBar.info(
            "View Changed",
            f"Showing {tab_text.lower()} tasks",
            duration=2000,
            parent=self
        )

    def filter_tasks(self):
        """
        Filter tasks based on search text, category filter, and current tab view
        """
        search_text = self.search_box.text().lower()
        category_filter = self.filter_combo.currentText()
        
        for i in range(self.task_layout.count()):
            widget = self.task_layout.itemAt(i).widget()
            if widget is None:
                continue
                
            show_widget = True
            
            if search_text:
                widget_text = widget.findChild(QLabel).text().lower()
                if search_text not in widget_text:
                    show_widget = False
            
            if category_filter != "All Categories" and show_widget:
                found_category = False
                for child in widget.findChildren(QLabel):
                    if category_filter == child.text():
                        found_category = True
                        break
                
                if not found_category:
                    show_widget = False
            
            if self.current_view != "all" and show_widget:
                if self.current_view == "today":
                    today = QDate.currentDate().toString("yyyy-MM-dd")
                    found_today = False
                    for child in widget.findChildren(QLabel):
                        if today == child.text():
                            found_today = True
                            break
                    
                    if not found_today:
                        show_widget = False
                        
                elif self.current_view == "important":
                    important_icon = widget.findChild(IconWidget)
                    if important_icon and not important_icon.isVisible():
                        show_widget = False
                        
                elif self.current_view == "completed":
                    pass
            
            widget.setVisible(show_widget)
        
        InfoBar.info(
            "Tasks Filtered",
            f"Filter applied: {category_filter} | Search: {search_text or 'None'} | View: {self.current_view}",
            duration=2000,
            parent=self
        )

    def toggle_theme(self, is_dark):
        """
        Toggle between light and dark themes
        """
        self.is_darkmode = is_dark
        theme_name = "Dark" if is_dark else "Light"
        
        try:
            if is_dark:
                setTheme(Theme.DARK)
            else:
                setTheme(Theme.LIGHT)
        except Exception as e:
            print(f"Error changing theme: {e}")
        
        InfoBar.success(
            "Theme Changed",
            f"Switched to {theme_name} mode",
            duration=2000,
            parent=self
        )

    def navigate_back(self):
        """
        Navigate back to home screen
        """
        self.hide()
        self.backtohome_signal.emit()
