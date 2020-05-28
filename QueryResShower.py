from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, \
    QLabel, QGridLayout, QSizePolicy


class QueryResShower(QWidget):
    """Класс для визуализации двумерного массива информации без возможности изменения"""

    def __init__(self, data):
        super().__init__()
        self.content_widget = QWidget()
        self.table = QScrollArea()
        self.table.setWidget(self.content_widget)
        self.table.setWidgetResizable(True)
        self.table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.content_layout = QGridLayout()
        self.content_widget.setLayout(self.content_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.table)
        self.setLayout(self.main_layout)

        width = len(data[0])
        for i in range(len(data)):
            for j in range(width):
                lbl = QLabel(str(data[i][j]))
                self.content_layout.addWidget(lbl, i, j)

