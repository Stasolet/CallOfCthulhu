from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QSizePolicy, QScrollArea, QGridLayout, QLabel

from CthulhuCore.ViewShower import ViewInfoChanger, ViewShower, ViewRecordAdder


slave_combo_config = {"название_параметра": ("параметры", "*", "название_параметра", "код_параметра")}


class DangerConfEditor(ViewInfoChanger):
    def __init__(self, header, info, parent: ViewShower):
        super().__init__(header, info, parent)
        self.way_layout = QVBoxLayout()
        push_btn = self.main_layout.takeAt(self.main_layout.count() - 1).widget()

        self.worker_id = info[0]
        self.slave_combo_config = {"название_параметра": ("параметры", "*", "название_параметра", "код_параметра")}
        self.combo_change_idx["название_параметра"] = {}
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(lambda e: self.add_cell(-1))
        self.main_layout.addWidget(add_btn)

        way = self.db.execute(f"SELECT код_параметра, название_параметра, нижний_допустимый_порог, верхний_допустимый_порог FROM `подчинённые_допустимые_значения_параметров_view` where `код_категории_вредности` = {self.worker_id}")
        for pos, point in enumerate(way, start=-1):
            param_name = str(point[1])
            self.combo_change_idx["название_параметра"][param_name] = point[0]
            self.add_cell(pos, param_name, point[2], point[3])

        self.main_layout.addLayout(self.way_layout)
        self.main_layout.addWidget(push_btn)

    def add_cell(self, pos: int, txt="", dnw_val="", up_val=""):
        """Вставляет ячейку ниже активирующей кнопки для вставки на уровне надо передать ::pos:: = -1"""

        cell = QHBoxLayout()
        edi = QLineEdit()
        edi.setText(txt)

        dwn_val_edt = QLineEdit()
        dwn_val_edt.setText(str(dnw_val))
        up_val_edt = QLineEdit(str(up_val))

        add_btn = QPushButton("Добавить")
        del_btn = QPushButton("Удалить")

        cmb = QComboBox()
        cmb.addItem(txt)

        edi.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        cmb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dwn_val_edt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        up_val_edt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        add_btn.clicked.connect(lambda e, c=cell: self.add_cell(c.pos))
        del_btn.clicked.connect(lambda e, c=cell: self.del_cell(c.pos))

        edi.editingFinished.connect(lambda c=cmb, t=edi.text:
                                    self.slave_combo_update("название_параметра", c, t()))  # le-kostyl
        cell.pos = pos
        cell.addWidget(edi)
        cell.addWidget(cmb)
        cell.addWidget(dwn_val_edt)
        cell.addWidget(up_val_edt)
        cell.addWidget(add_btn)
        cell.addWidget(del_btn)
        for i in range(pos + 1, self.way_layout.count()):
            cell_to_move = self.way_layout.itemAt(i)
            cell_to_move.pos += 1
        cell.pos += 1  # для вставки ниже активированной кнопки

        self.way_layout.insertLayout(cell.pos, cell)

    def slave_combo_update(self, c_name: str, c: QComboBox, text: str):  # grand le-kostyl
        tmp = self.combo_config
        self.combo_config = self.slave_combo_config
        self.combo_update(c_name, c, text)
        self.combo_config = tmp

    def del_cell(self, pos):
        cell: QVBoxLayout
        cell = self.way_layout.takeAt(pos)
        for i in range(cell.count()):
            w = cell.takeAt(0).widget()
            w.deleteLater()
        cell.deleteLater()

        for i in range(pos, self.way_layout.count()):
            cell_to_move = self.way_layout.itemAt(i)
            cell_to_move.pos -= 1

    def push_slave_changes(self):
        params = []
        kakoito_set = set()
        try:
            for i in range(self.way_layout.count()):
                cell = self.way_layout.itemAt(i)
                w = cell.itemAt(1).widget()
                param = w.currentText()
                if param:
                    if param in kakoito_set:
                        raise KeyError
                    kakoito_set.add(param)
                    param_id = self.combo_change_idx["название_параметра"][param]
                    dwn_w = cell.itemAt(2).widget()
                    up_w = cell.itemAt(3).widget()
                    dwn_val = dwn_w.text()
                    up_val = up_w.text()
                    if not dwn_val:
                        dwn_val = 0
                    if not up_val:
                        up_val = 0
                    params.append((self.worker_id, param_id, dwn_val, up_val))


            query = f" insert into `допустимые_значения_параметров` values(%s, %s, %s, %s)"
            self.db.execute("delete from `допустимые_значения_параметров` where код_категории_вредности = %s", (self.worker_id,))
            self.db.executemany(query, params)
            self.db.commit()
        except KeyError as er:
            from PyQt5.QtWidgets import QErrorMessage
            error_widget = QErrorMessage()
            error_widget.showMessage(f"Дубликат параметра")
            error_widget.exec()

    def push_changes(self):
        self.push_slave_changes()
        super().push_changes()

