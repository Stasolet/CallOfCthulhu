from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from CthulhuCore.TableShower import TableShower


class DangerConfUi(QWidget):

    def __init__(self):
        super().__init__()

        self.show_all_btn = QPushButton("Категории вредности")
        self.replacement_btn = QPushButton("Допустимые значения параметров")

        self.show_all_btn.clicked.connect(lambda: TableShower("`категории_вредности`", ["код_категории_вредности"]).show())
        self.replacement_btn.clicked.connect(lambda: TableShower("`допустимые_значения_параметров`",
                                                                 ["код_категории_вредности", "код_параметра"]).show())

        self.box = QVBoxLayout()
        self.box.addWidget(self.show_all_btn)
        self.box.addWidget(self.replacement_btn)

        self.setLayout(self.box)

        self.show()

