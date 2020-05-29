from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout


class StatisticUi(QWidget):
    """Отчёты на основании процедур за месяц и за день"""
    def __init__(self):
        super().__init__()

        self.resize(500, 500)

        self.workers_btn = QPushButton("Управление персоналом")
        self.monitor_btn = QPushButton("Мониторинг рабочих")
        self.danger_conf_btn = QPushButton("Категории вредности")
        self.params_btn = QPushButton("Измеряемые параметры")

        self.active_btn = QPushButton("Активные устройства")

        # self.workers_btn.clicked.connect(lambda: self.slave_widgets.append(WorkersUi()))
        # self.danger_conf_btn.clicked.connect(lambda: self.slave_widgets.append(DangerConfUi()))
        # self.monitor_btn.clicked.connect(lambda: self.slave_widgets.append(OrdersUi()))
        # self.params_btn.clicked.connect(lambda: self.slave_widgets.append(ParamsUi()))
        #
        # self.active_btn.clicked.connect(lambda: self.slave_widgets.append(StatisticUi()))

        self.bx = QVBoxLayout()
        self.bx.addWidget(self.workers_btn)
        self.bx.addWidget(self.danger_conf_btn)
        self.bx.addWidget(self.monitor_btn)
        self.bx.addWidget(self.params_btn)
        self.bx.addWidget(self.active_btn)

        self.setLayout(self.bx)

        self.show()