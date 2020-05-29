from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from CthulhuCore.TableShower import TableShower


class ParamsUi(TableShower):

    def __init__(self):
        super().__init__("`параметры`", ["код_параметра"])
        self.show()
