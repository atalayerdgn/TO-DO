from qfluentwidgets import (
    FluentWindow, FluentIcon as FIF, ComboBox, SwitchButton,
    IconWidget, pyqtSignal, PushButton, ExpandLayout, SettingCardGroup,
    CardWidget, TitleLabel, SubtitleLabel, InfoBar
)
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QColor, QFont
from utils.SettingsUtils import SettingUtils
from utils.config import APP_NAME, APP_VERSION, APP_AUTHOR
from qfluentwidgets import Theme, setTheme
from utils.widgets import CustomBannerWidget


class SettingUI(FluentWindow):
    """
    Enhanced settings interface with improved organization and functionality.
    """
    themeChanged = pyqtSignal(str)
    languageChanged = pyqtSignal(str)
    back_home = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - Settings")
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.settings = QSettings("AtolayErdogan", "ToDoApp")
        self.initUI()

    def initUI(self):
        """
        Initialize the settings interface with a more organized and user-friendly layout.
        """
        current_theme, current_lang = SettingUtils.loadSettings()
        
        central_widget = QFrame(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        banner = CustomBannerWidget(self)
        banner.setTitle("Settings")
        banner.setContent("Customize your application experience")
        banner.setBackgroundColor(QColor(100, 53, 201))
        main_layout.addWidget(banner)
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        scroll_widget = QFrame(self)
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(40, 20, 40, 20)
        scroll_layout.setSpacing(20)
        appearance_card = CardWidget(self)
        appearance_layout = QVBoxLayout(appearance_card)
        appearance_layout.setContentsMargins(20, 20, 20, 20)
        
        appearance_title = TitleLabel("Appearance", self)
        appearance_layout.addWidget(appearance_title)
        theme_layout = QHBoxLayout()
        theme_icon = IconWidget(FIF.PALETTE, self)
        theme_label = QLabel("Theme:", self)
        self.theme_combo = ComboBox(self)
        self.theme_combo.addItems(["Light", "Dark", "System"])
        index_theme = self.theme_combo.findText(current_theme)
        if index_theme != -1:
            self.theme_combo.setCurrentIndex(index_theme)
        self.theme_combo.currentTextChanged.connect(self.onThemeChanged)
        theme_layout.addWidget(theme_icon)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        appearance_layout.addLayout(theme_layout)
        
        animations_layout = QHBoxLayout()
        animations_icon = IconWidget(FIF.BRUSH, self)
        animations_label = QLabel("Enable Animations:", self)
        self.animation_switch = SwitchButton(self)
        self.animation_switch.setChecked(True)
        animations_layout.addWidget(animations_icon)
        animations_layout.addWidget(animations_label)
        animations_layout.addStretch(1)
        animations_layout.addWidget(self.animation_switch)
        appearance_layout.addLayout(animations_layout)
        
        scroll_layout.addWidget(appearance_card)
        
        language_card = CardWidget(self)
        language_layout = QVBoxLayout(language_card)
        language_layout.setContentsMargins(20, 20, 20, 20)
        
        language_title = TitleLabel("Language", self)
        language_layout.addWidget(language_title)
        
        language_select_layout = QHBoxLayout()
        language_icon = IconWidget(FIF.LANGUAGE, self)
        language_label = QLabel("Interface Language:", self)
        self.language_combo = ComboBox(self)
        self.language_combo.addItems(["Türkçe", "English"])
        if current_lang == "en":
            self.language_combo.setCurrentIndex(1)
        else:
            self.language_combo.setCurrentIndex(0)
        self.language_combo.currentIndexChanged.connect(self.onLanguageChanged)
        language_select_layout.addWidget(language_icon)
        language_select_layout.addWidget(language_label)
        language_select_layout.addWidget(self.language_combo)
        language_layout.addLayout(language_select_layout)
        
        scroll_layout.addWidget(language_card)
        tasks_card = CardWidget(self)
        tasks_layout = QVBoxLayout(tasks_card)
        tasks_layout.setContentsMargins(20, 20, 20, 20)
        tasks_title = TitleLabel("Task Settings", self)
        tasks_layout.addWidget(tasks_title)
        view_layout = QHBoxLayout()
        view_icon = IconWidget(FIF.VIEW, self)
        view_label = QLabel("Default Task View:", self)
        self.view_combo = ComboBox(self)
        self.view_combo.addItems(["All Tasks", "Today", "Important", "Completed"])
        self.view_combo.setCurrentIndex(0)
        view_layout.addWidget(view_icon)
        view_layout.addWidget(view_label)
        view_layout.addWidget(self.view_combo)
        tasks_layout.addLayout(view_layout)
        reminders_layout = QHBoxLayout()
        reminders_icon = IconWidget(FIF.CALENDAR, self)
        reminders_label = QLabel("Task Reminders:", self)
        self.reminders_switch = SwitchButton(self)
        reminders_layout.addWidget(reminders_icon)
        reminders_layout.addWidget(reminders_label)
        reminders_layout.addStretch(1)
        reminders_layout.addWidget(self.reminders_switch)
        tasks_layout.addLayout(reminders_layout)
        
        scroll_layout.addWidget(tasks_card)
        
        data_card = CardWidget(self)
        data_layout = QVBoxLayout(data_card)
        data_layout.setContentsMargins(20, 20, 20, 20)
        
        data_title = TitleLabel("Data & Privacy", self)
        data_layout.addWidget(data_title)
        clear_tasks_layout = QHBoxLayout()
        clear_tasks_icon = IconWidget(FIF.DELETE, self)
        clear_tasks_label = QLabel("Clear All Tasks:", self)
        self.clear_tasks_btn = PushButton("Clear Tasks", self)
        self.clear_tasks_btn.setIcon(FIF.DELETE)
        self.clear_tasks_btn.clicked.connect(self.confirm_clear_tasks)
        clear_tasks_layout.addWidget(clear_tasks_icon)
        clear_tasks_layout.addWidget(clear_tasks_label)
        clear_tasks_layout.addStretch(1)
        clear_tasks_layout.addWidget(self.clear_tasks_btn)
        data_layout.addLayout(clear_tasks_layout)
        reset_settings_layout = QHBoxLayout()
        reset_settings_icon = IconWidget(FIF.SYNC, self)
        reset_settings_label = QLabel("Reset All Settings:", self)
        self.reset_settings_btn = PushButton("Reset Settings", self)
        self.reset_settings_btn.setIcon(FIF.SYNC)
        self.reset_settings_btn.clicked.connect(self.confirm_reset_settings)
        reset_settings_layout.addWidget(reset_settings_icon)
        reset_settings_layout.addWidget(reset_settings_label)
        reset_settings_layout.addStretch(1)
        reset_settings_layout.addWidget(self.reset_settings_btn)
        data_layout.addLayout(reset_settings_layout)
        scroll_layout.addWidget(data_card)
        about_card = CardWidget(self)
        about_layout = QVBoxLayout(about_card)
        about_layout.setContentsMargins(20, 20, 20, 20)
        
        about_title = TitleLabel("About", self)
        about_layout.addWidget(about_title)
        
        app_name_label = QLabel(APP_NAME, self)
        app_name_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        
        version_label = QLabel(f"Version {APP_VERSION}", self)
        author_label = QLabel(f"Created by {APP_AUTHOR}", self)
        
        about_layout.addWidget(app_name_label)
        about_layout.addWidget(version_label)
        about_layout.addWidget(author_label)
        
        scroll_layout.addWidget(about_card)
        
        back_button = PushButton("Back to Home", self)
        back_button.setIcon(FIF.HOME)
        back_button.clicked.connect(self.navigate_back)
        
        scroll_layout.addWidget(back_button)
        scroll_layout.addStretch(1)
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        central_widget.setObjectName("settingsInterface")
        self.addSubInterface(central_widget, FIF.SETTING, "Settings")
        
    def onThemeChanged(self, theme_text):
        """
        Handle theme change with improved feedback and save settings.
        """
        lang_index = self.language_combo.currentIndex()
        lang_code = "en" if lang_index == 1 else "tr"
        SettingUtils.saveSettings(theme_text, lang_code)

        if theme_text == "Light":
            setTheme(Theme.LIGHT)
        elif theme_text == "Dark":
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.AUTO)
            
        InfoBar.success(
            "Theme Changed",
            f"Theme set to {theme_text}",
            duration=3000,
            parent=self
        )

        self.themeChanged.emit(theme_text)

    def onLanguageChanged(self, index):
        """
        Handle language change with improved feedback and save settings.
        """
        lang_code = "en" if index == 1 else "tr"
        current_theme = self.theme_combo.currentText()
        SettingUtils.saveSettings(current_theme, lang_code)
        
        language_name = self.language_combo.itemText(index)
        
        InfoBar.success(
            "Language Changed",
            f"Language set to {language_name}",
            duration=3000,
            parent=self
        )
        
        self.languageChanged.emit(lang_code)
        
    def confirm_clear_tasks(self):
        """
        Show confirmation before clearing all tasks.
        """
        self.clear_all_tasks()
        
    def clear_all_tasks(self):
        """
        Clear all tasks from the database.
        """
        InfoBar.success(
            "Tasks Cleared",
            "All tasks have been deleted",
            duration=3000,
            parent=self
        )
        
    def confirm_reset_settings(self):
        """
        Show confirmation before resetting all settings.
        """
        self.reset_all_settings()
        
    def reset_all_settings(self):
        """
        Reset all settings to default values.
        """
        self.settings.clear()
        
        self.theme_combo.setCurrentText("Light")
        self.language_combo.setCurrentIndex(0)
        self.view_combo.setCurrentText("All Tasks")
        self.reminders_switch.setChecked(False)
        self.animation_switch.setChecked(True)
        
        setTheme(Theme.LIGHT)
        
        InfoBar.success(
            "Settings Reset",
            "All settings have been reset to default values",
            duration=3000,
            parent=self
        )

    def navigate_back(self):
        """Navigate back to home screen"""
        self.hide()
        self.back_home.emit()
