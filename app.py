import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from db.initdb import init_db
from ui.HomeUI import HomeUI
from ui.LoginUI import LoginUI
from ui.RegisterUI import RegisterUI
from ui.SettingsUI import SettingUI
from ui.RedirectUI import RedirectUI
def switch_ui(current_ui, next_ui, redir):
    """
    Switches the current UI to the next UI.
    :param current_ui: The current UI instance.
    :param next_ui: The next UI instance to switch to.
    :param redir: The redirecting UI instance to show briefly.
    """
    if redir is None:
        next_ui.move(current_ui.pos())
        current_ui.hide()
        next_ui.show()
        return
    redir.move(current_ui.pos())
    next_ui.move(redir.pos())
    current_ui.hide()
    redir.show()
    QTimer.singleShot(1000, lambda: hide_redirect_and_show_next(redir, next_ui))

def hide_redirect_and_show_next(redir, next_ui):
    """
    Hides the redirect UI and shows the next UI.
    :param redir: The redirecting UI to hide.
    :param next_ui: The next UI to show.
    """
    redir.hide()
    next_ui.show()

def main():
    app = QApplication(sys.argv)
    init_db()
    home_ui = HomeUI()
    login_ui = LoginUI()
    register_ui = RegisterUI()
    redirect_ui = RedirectUI()
    settings_ui = SettingUI()
    home_ui.login_signal.connect(lambda: switch_ui(home_ui, login_ui, None))
    home_ui.register_signal.connect(lambda: switch_ui(home_ui, register_ui, None))
    home_ui.setting_signal.connect(lambda: switch_ui(home_ui, settings_ui, None))
    login_ui.login_signal.connect(lambda: switch_ui(login_ui, home_ui, redirect_ui))
    login_ui.register_signal.connect(lambda: switch_ui(login_ui, register_ui, redirect_ui))
    register_ui.register_signal.connect(lambda: switch_ui(register_ui, login_ui, redirect_ui))
    settings_ui.back_home.connect(lambda: switch_ui(settings_ui, home_ui, None))
    
    home_ui.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
    
