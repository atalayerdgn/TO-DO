from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTimeEdit
from qfluentwidgets import (
    InfoBar, InfoBarPosition, TimeEdit
)
from db.user import add_user
import re

class RegisterUtils(QWidget):
    def __init__(self, parent=None):
        super().__init__()

    def is_valid_email(self, email) -> bool:
        """checks if the email is valid.
        :param email: The email address to check.
        :return: True if the email is valid, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def handle_register(self, username: str, email: str, password: str):
        """
        Handles the registration process.
        :param username: The username of the user.
        :param email: The email address of the user.
        :param password: The password of the user.
        :return: 1 if the registration is successful, None otherwise.
        """
        if not self.is_valid_email(email):
            InfoBar.error(
                title="Geçersiz E-posta",
                content="Lütfen geçerli bir e-posta adresi girin.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        if not username or not password or not email:
            InfoBar.error(
                title="Eksik Bilgi",
                content="Lütfen tüm alanları doldurun.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        success = add_user(username, email, password)
        if success:
            InfoBar.success(
                title="Kayıt Başarılı",
                content="Kayıt işlemi başarıyla tamamlandı.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return 1
        else:
            InfoBar.warning(
                title="Kayıt Hatası",
                content="Bu kullanıcı adı zaten kayıtlı.",
                parent=self,
                position=InfoBarPosition.TOP
            )
