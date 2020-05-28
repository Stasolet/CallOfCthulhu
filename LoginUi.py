from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QPushButton

from CtulhuCore.DbWrapper import db_wrapper
from MainUi import MainUi


class LoginUi(QWidget):
    def __init__(self):
        super().__init__()
        self.main_lay = QVBoxLayout()
        self.login_lay = QFormLayout()
        self.btn_lay = QHBoxLayout()
        self.main_lay.addLayout(self.login_lay)
        self.main_lay.addLayout(self.btn_lay)

        self.log_edt = QLineEdit()
        self.pas_edt = QLineEdit()
        self.pas_edt.setEchoMode(QLineEdit.Password)

        self.login_lay.addRow("Логин", self.log_edt)
        self.login_lay.addRow("Пароль", self.pas_edt)

        self.close_btn = QPushButton("Закрыть")
        self.enter_btn = QPushButton("Войти")

        self.enter_btn.clicked.connect(self.login)

        self.btn_lay.addWidget(self.enter_btn)
        self.btn_lay.addWidget(self.close_btn)

        self.setLayout(self.main_lay)
        self.w = MainUi()

    def login(self):
        try:
            db_wrapper.connect(host="localhost",
                               user=self.log_edt.text(),
                               passwd=self.pas_edt.text(),
                               database="пассажироперевозочная",
                               use_pure=True)
        except Exception as err:
            msg = None
            if err.args[0] == 1045:
                msg = "Не правильный логин или пароль"
            if err.args[0] == 2003:
                msg = "Сервер недоступен"

            if msg:
                from PyQt5.QtWidgets import QErrorMessage
                error = QErrorMessage()
                error.showMessage(msg)
                error.exec()
        else:
            self.w.show()
            self.hide()