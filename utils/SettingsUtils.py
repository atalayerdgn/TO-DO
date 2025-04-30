from PyQt5.QtCore import QSettings

class SettingUtils:
    @staticmethod
    def saveSettings(theme: str, language: str):
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("theme", theme)
        settings.setValue("language", language)

    @staticmethod
    def loadSettings():
        settings = QSettings("MyCompany", "MyApp")
        theme = settings.value("theme", "Light", type=str)
        language = settings.value("language", "tr", type=str)
        return theme, language
