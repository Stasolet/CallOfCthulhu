import datetime

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from CthulhuCore.DbWrapper import db_wrapper


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = []
        super(MplCanvas, self).__init__(self.fig)


class WorkerMonitor(QWidget):
    """отображаются активные устройства и состояния рабочих"""
    def __init__(self, work_id=1, strt=(2020, 5, 1, 8), end=(2020, 5,2, 16)):
        super().__init__()

        morn = datetime.datetime(*strt)
        evn = datetime.datetime(*end)

        qmorn = morn.strftime('%Y-%m-%d %H:%M:%S')
        qevn = evn.strftime('%Y-%m-%d %H:%M:%S')

        self.main_layout = QVBoxLayout()

        qwe = db_wrapper.execute(f"select код_параметра, название_параметра from параметры "
                                 f"where код_параметра"
                                 f" in (SELECT distinct журнал_показаний.код_параметра FROM журнал_показаний where (время_измерения between '{qmorn}' and '{qevn}'));")
        params = qwe.fetchall()

        q = []
        sc = MplCanvas(self, width=15, height=30, dpi=100)
        toolbar = NavigationToolbar(sc, self)
        i = 1
        for param_id, param_name in params:
            qwe = db_wrapper.execute(f"""SELECT date_format(`время_измерения`, '%Y.%m.%H:%i'), avg(значение_параметра)  FROM cthulhudb.журнал_показаний  where (табельный_номер = {work_id})
                                     and (время_измерения between '{qmorn}' and '{qevn}')
                                     and код_параметра = {param_id}
                                     group by date_format(`время_измерения`, '%Y.%m.%H:%i')""")

            res = qwe.fetchall()
            data = pd.DataFrame(res, columns=["время_измерения", "значение_параметра"])

            sc.axes.append(sc.fig.add_subplot(len(params),1,i))
            i+= 1
            sc.axes[-1].plot(data["время_измерения"], data["значение_параметра"])  # данные





        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)
            # self.main_layout.addLayout(layout)
        self.setLayout(layout)

        self.show()