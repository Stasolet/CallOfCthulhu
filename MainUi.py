from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from WorkersUi import WorkersUi
from DangerConfUi import DangerConfUi
from ParamsUi import ParamsUi
from MonitorUi import MonitorUi
from StatisticUi import StatisticUi


class MainUi(QWidget):
    def __init__(self):
        super().__init__()
        self.slave_widgets = []

        self.resize(500, 500)

        self.workers_btn = QPushButton("Управление персоналом")
        self.params_btn = QPushButton("Измеряемые параметры")
        self.danger_conf_btn = QPushButton("Категории вредности")
        self.monitor_btn = QPushButton("Мониторинг рабочих")

        self.statistic_btn = QPushButton("Статистика")

        self.workers_btn.clicked.connect(lambda: self.slave_widgets.append(WorkersUi()))
        self.danger_conf_btn.clicked.connect(lambda: self.slave_widgets.append(DangerConfUi()))
        self.params_btn.clicked.connect(lambda: self.slave_widgets.append(ParamsUi()))
        self.monitor_btn.clicked.connect(lambda: self.slave_widgets.append(MonitorUi()))

        self.statistic_btn.clicked.connect(lambda: self.slave_widgets.append(StatisticUi()))

        self.bx = QVBoxLayout()
        self.bx.addWidget(self.workers_btn)
        self.bx.addWidget(self.danger_conf_btn)
        self.bx.addWidget(self.params_btn)
        self.bx.addWidget(self.monitor_btn)
        self.bx.addWidget(self.statistic_btn)

        self.setLayout(self.bx)


if __name__ == '__main__':
    from CthulhuCore.DbWrapper import db_wrapper

    db_wrapper.connect(host="localhost",
                       user="1422",
                       passwd="1422",
                       database="cthulhudb",
                       use_pure=True)
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    w = MainUi()
    w.show()
    sys.exit((app.exec_()))

