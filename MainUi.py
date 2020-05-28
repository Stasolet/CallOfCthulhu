from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

from AutoUi import AutoUi
from DriverUi import DriverUi
from OrdersUi import OrdersUi
from PathUi import PathUi
from StatisticUi import StatisticUi


class MainUi(QWidget):
    def __init__(self):
        super().__init__()
        self.slave_widgets = []

        self.resize(500, 500)

        self.drive_btn = QPushButton("Управление персоналом")
        self.auto_btn = QPushButton("Управление автопарком")
        self.orders_btn = QPushButton("Управление рейсами")
        self.path_btn = QPushButton("Управлнение маршрутами")
        self.statistic_btn = QPushButton("Статистика")

        self.drive_btn.clicked.connect(lambda: self.slave_widgets.append(DriverUi()))
        self.auto_btn.clicked.connect(lambda: self.slave_widgets.append(AutoUi()))
        self.orders_btn.clicked.connect(lambda: self.slave_widgets.append(OrdersUi()))
        self.path_btn.clicked.connect(lambda: self.slave_widgets.append(PathUi()))
        self.statistic_btn.clicked.connect(lambda: self.slave_widgets.append(StatisticUi()))

        self.bx = QVBoxLayout()
        self.bx.addWidget(self.drive_btn)
        self.bx.addWidget(self.auto_btn)
        self.bx.addWidget(self.orders_btn)
        self.bx.addWidget(self.path_btn)
        self.bx.addWidget(self.statistic_btn)

        self.setLayout(self.bx)

