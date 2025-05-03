from qfluentwidgets import (
    FluentWindow, FluentIcon as FIF, ComboBox,
    IconWidget, pyqtSignal, PushButton
)
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from utils.SettingsUtils import SettingUtils
from qfluentwidgets import Theme, setTheme


class SettingUI(FluentWindow):
    """FluentWindow üzerinde çalışacak tema ve dil ayarları arayüzü."""

    themeChanged = pyqtSignal(str)
    languageChanged = pyqtSignal(str)
    back_home = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(1200, 800)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()

    def initUI(self):
        current_theme, current_lang = SettingUtils.loadSettings()
        self.centralWidget = QFrame(self)
        layout = QVBoxLayout(self.centralWidget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        theme_layout = QHBoxLayout()
        theme_layout.setAlignment(Qt.AlignCenter)
        self.themeIcon = IconWidget(FIF.PALETTE, self)
        theme_layout.addWidget(self.themeIcon)
        self.themeCombo = ComboBox(self)
        self.themeCombo.addItems(["Light", "Dark", "System"])
        self.themeCombo.setFixedWidth(200)
        index_theme = self.themeCombo.findText(current_theme)
        if index_theme != -1:
            self.themeCombo.setCurrentIndex(index_theme)
        theme_layout.addWidget(self.themeCombo)
        layout.addLayout(theme_layout)
        lang_layout = QHBoxLayout()
        lang_layout.setAlignment(Qt.AlignCenter)
        self.langIcon = IconWidget(FIF.LANGUAGE, self)
        lang_layout.addWidget(self.langIcon)
        self.langCombo = ComboBox(self)
        self.langCombo.addItem("Türkçe", "tr")
        self.langCombo.addItem("English", "en")
        self.langCombo.setFixedWidth(200)
        if current_lang == "en":
            self.langCombo.setCurrentIndex(1)
        else:
            self.langCombo.setCurrentIndex(0)
        home_button = PushButton("Back To Home", self)
        home_button.clicked.connect(self.back_home.emit)
        home_button.setFixedWidth(200)
        lang_layout.addWidget(home_button)
        lang_layout.addWidget(self.langCombo)
        layout.addLayout(lang_layout)
        self.themeCombo.currentTextChanged.connect(self.onThemeChanged)
        self.langCombo.currentIndexChanged.connect(self.onLanguageChanged)
        self.centralWidget.setObjectName("settingsInterface")
        self.addSubInterface(self.centralWidget, FIF.SETTING, "Settings")
    def onThemeChanged(self, theme_text):
        lang_code = self.langCombo.currentData()
        SettingUtils.saveSettings(theme_text, lang_code)

        if theme_text == "Light":
            setTheme(Theme.LIGHT)
        elif theme_text == "Dark":
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.AUTO)

        self.themeChanged.emit(theme_text)

    def onLanguageChanged(self, index):
        """Dil değiştiğinde ayarları kaydeder ve sinyal yayar."""
        lang_code = self.langCombo.itemData(index)
        current_theme = self.themeCombo.currentText()
        SettingUtils.saveSettings(current_theme, lang_code)
        self.languageChanged.emit(lang_code)
