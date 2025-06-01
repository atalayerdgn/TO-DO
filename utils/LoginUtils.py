from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QDialog, QWidget
from qfluentwidgets import (
    SubtitleLabel, LineEdit, PushButton, InfoBar, InfoBarPosition, PasswordLineEdit
)
from db.user import verify_user, get_mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint

class LoginUtils(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.verification_code = None

    def _on_login_clicked(self,username, email, password):
        """
        Handles the login button click event.
        :param username: The username of the user.
        :param email: The email address of the user.
        :param password: The password of the user.
        """
        if not self._verify_credentials(username,email,password):
            InfoBar.error(
                title="Error",
                content="Invalid credentials.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        email = get_mail(username)
        if not email:
            InfoBar.error(
                title="Error",
                content="Invalid email address.",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        self.verification_code = self._generate_verification_code()
        if self._send_email(email, self.verification_code):
            InfoBar.success(
                title="Success",
                content=f"succesfully sent code at {email} ",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return self._prompt_verification_code()
        else:
            InfoBar.error(
                title="Error",
                content="Failed to send verification code.",
                parent=self,
                position=InfoBarPosition.TOP
            )

    def _verify_credentials(self,login,email,password) -> bool:
        """check if the credentials are valid."""
        return verify_user(login, email, password)

    def _generate_verification_code(self) -> str:
        """generate a random 6-digit verification code."""
        return str(randint(100000, 999999))

    def _send_email(self, recipient_email: str, code: str) -> bool:
        """send an email with the verification code.
        recipient_email: The email address to send the code to.
        code: The verification code to send.
        """
        try:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "atalayerdgnn@gmail.com"
            sender_password = ""
            subject = "Giriş Doğrulama Kodunuz"
            body = f"Giriş işleminizi tamamlamak için doğrulama kodunuz: {code}"

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())

            return True
        except Exception as e:
            print(f"E-posta gönderme hatası: {e}")
            return False

    def _prompt_verification_code(self):
        """
        Kullanıcıdan doğrulama kodunu girmesini ister.
        Eğer kod doğruysa giriş işlemini tamamlar.
        Eğer kod yanlışsa hata mesajı gösterir.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Verification Code")
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)

        code_input = LineEdit(dialog)
        code_input.setPlaceholderText("Code")
        layout.addWidget(code_input)

        submit_button = PushButton("Verify", dialog)
        layout.addWidget(submit_button)

        def verify():
            entered_code = code_input.text().strip()
            if entered_code == self.verification_code:
                InfoBar.success(
                    title="Success",
                    content="Code verified successfully.",
                    parent=dialog,
                    position=InfoBarPosition.TOP
                )
                dialog.accept()
            else:
                InfoBar.error(
                    title="Error",
                    content="Invalid code. Please try again.",
                    parent=dialog,
                    position=InfoBarPosition.TOP
                )

        submit_button.clicked.connect(verify)
        dialog.exec_()
        return dialog.result() == QDialog.Accepted
