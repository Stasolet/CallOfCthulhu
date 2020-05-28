import sys
from PyQt5.QtWidgets import QApplication

from LoginUi import LoginUi

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login = LoginUi()
    login.show()

    sys.exit((app.exec_()))

