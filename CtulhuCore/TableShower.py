from PyQt5.QtWidgets import QScrollArea, QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QLineEdit, QPushButton, QGridLayout, QSizePolicy, QRadioButton, QButtonGroup, QMessageBox


from CtulhuCore.DbWrapper import db_wrapper


class TableShower(QWidget):
    """класс визуализации таблицы из бд, с возможностью изменения и добавления данных в неё"""
    def __init__(self, source: str, key_fields: list = None, editable=True, deletable=True, parent=None):
        super().__init__(parent=parent)
        self.editable = editable
        self.deletable = deletable
        self.slave_widgets = []
        self.source = source
        self.key_fields = key_fields
        self.header = None
        self.db = db_wrapper
        self.record_editor = TableInfoChanger
        self.record_adder = TableRecordAdder

        self.content_widget = QWidget()
        self.table = QScrollArea()
        self.table.setWidget(self.content_widget)
        self.table.setWidgetResizable(True)
        self.table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.content_layout = QGridLayout()
        self.content_widget.setLayout(self.content_layout)

        self.head_layout = QVBoxLayout()
        self.footer_layout = QVBoxLayout()
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.head_layout)
        self.main_layout.addWidget(self.table)
        self.main_layout.addLayout(self.footer_layout)
        self.setLayout(self.main_layout)

        if self.editable:
            self.add_record_btn = QPushButton("ДОБАВИТЬ")
            self.footer_layout.addWidget(self.add_record_btn)
            self.add_record_btn.clicked.connect(lambda state: self.record_adder(self.header, self).show())

        self.build_filter_ui()

        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.content_update)
        self.head_layout.addWidget(refresh_btn)

        self.content()
        self.resize(1000, 100)  # потому что я так хочу иначе слишком узко получается some magic
        # я не знаю почему но при таких числах всё хорошо выглядит

    def build_filter_ui(self):
        self.filter_layout = QVBoxLayout()
        self.head_layout.addLayout(self.filter_layout)
        self.filters = {}
        cur = self.db.execute(f"desc {self.source}")
        for col in cur:
            t = col[1]  # col_type
            f = {"type": None, "value": None}
            if t.find("int") != -1 or t.find("float") != -1 or t == "double" or t.startswith("decimal"):
                f["type"] = "number"
            elif t.find("char") != -1:
                f["type"] = "string"
            elif t.find("date") != -1 or t.find("time") != -1:
                f["type"] = "datetime"

            self.filters[col[0]] = f  # col_name
        for f in self.filters.keys():
            f_conf = self.filters[f]
            if f_conf["type"] in {"number", "string", "datetime"}:
                cell = QHBoxLayout()
                cell_name = QLabel(str(f))
                cell.addWidget(cell_name)
                if f_conf["type"] == "number" or f_conf["type"] == "datetime":
                    less_lbl = QLabel("больше")
                    less_edt = QLineEdit()

                    great_lbl = QLabel("меньше")
                    great_edt = QLineEdit()

                    grp = QButtonGroup()
                    and_radio = QRadioButton("И")
                    and_radio.setChecked(True)
                    or_radio = QRadioButton("ИЛИ")
                    grp.addButton(and_radio, 0)
                    grp.addButton(or_radio, 1)

                    f_conf["value"] = (less_edt, great_edt, grp)

                    cell.addWidget(less_lbl)
                    cell.addWidget(less_edt)
                    cell.addWidget(great_lbl)
                    cell.addWidget(great_edt)
                    cell.addWidget(and_radio)
                    cell.addWidget(or_radio)
                elif f_conf["type"] == "string":
                    l1 = QLabel("содержит")
                    edit = QLineEdit()

                    f_conf["value"] = edit

                    cell.addWidget(l1)
                    cell.addWidget(edit)

                self.filter_layout.addLayout(cell)

    def content(self) -> None:
        """Отображение непосредственно данных"""
        query = f"SELECT * FROM {self.source}"

        filter_query = self.get_filter_query()
        if filter_query:
            query += " WHERE " + filter_query

        all_path = self.db.execute(query)
        data = [all_path.column_names] + all_path.fetchall()  # если отделить заголовок сложно верстать
        self.header = all_path.column_names
        rows = len(data)
        cols = len(data[0])
        for i in range(rows):
            for j in range(cols):
                lbl = QLabel(str(data[i][j]))
                self.content_layout.addWidget(lbl, i, j)

        if self.editable:
            for i in range(1, rows):
                btn = QPushButton("Изменить запись")
                btn.clicked.connect(lambda state, num=i: self.record_editor(data[0], data[num], self).show())
                self.content_layout.addWidget(btn, i, cols)
            cols += 1

        if self.deletable:
            for i in range(1, rows):
                btn = QPushButton("Удалить запись")
                btn.clicked.connect(lambda state, num=i: self.del_record_quest(data[0], data[num]))
                self.content_layout.addWidget(btn, i, cols)
            cols += 1

    def content_update(self) -> None:
        """Обновление данных при принятии изменений"""
        for i in reversed(range(self.content_layout.count())):  # Скопипасченное шайтан колдунство для очистки
            widget_to_remove = self.content_layout.itemAt(i).widget()
            widget_to_remove.setParent(None)
            widget_to_remove.deleteLater()
        self.content()

    def del_record_quest(self, header, data):
        qwe = set(self.key_fields)
        i = 0
        del_query = []
        while qwe:
            if header[i] in qwe:
                del_query.append(f"`{header[i]}` = {data[i]}")
                qwe.remove(header[i])
            i += 1
        del_query = ','.join(del_query)
        del_d = QMessageBox()
        del_d.setIcon(QMessageBox.Question)
        del_d.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        del_d.setText(f"Удалить запись {del_query}")
        dialog_res = del_d.exec()
        if dialog_res == QMessageBox.Ok:
            self.db.execute(f"delete from {self.source} where {del_query}")
            self.db.commit()
            self.content_update()

    def get_filter_query(self):
        filter_query = []
        for f in self.filters.keys():
            f_conf = self.filters[f]
            q = None
            if f_conf["type"] == "number" or f_conf["type"] == "datetime":
                q = f"`{f}`"
                values = f_conf["value"]
                grt_val = values[0].text()
                les_val = values[1].text()

                if f_conf["type"] == "datetime":
                    grt_val = f'"{grt_val}"' if grt_val else grt_val
                    les_val = f'"{les_val}"' if les_val else les_val

                if grt_val:

                    if les_val:  # 1 1
                        or_flag = values[2].checkedId()
                        if not or_flag:
                            q += f" BETWEEN {grt_val} AND {les_val}"
                        else:
                            q += f" >= {grt_val} OR `{f}` <= {les_val}"

                    else:  # 1 0
                        q += f" >= {grt_val} "
                elif les_val:  # 0 1
                    q += f"<= {les_val}"
                else:  # 0 0
                    q = None

            elif f_conf["type"] == "string":
                if f_conf["value"].text():
                    q = f"`{f}` LIKE \"%{f_conf['value'].text()}%\""

            if q:
                filter_query.append(q)
        filter_query = " AND ".join(filter_query)
        return filter_query


class TableInfoChanger(QWidget):
    """Класс для изменения записей в таблице, визуализированной TableShower

    исходные значения полей берёт из родительского TableShower, после изменений вызывает обновление родителя
    каждая ячейка представленна в виде Layout, информация о которых хранится в cell_index"""
    def __init__(self, header, info, parent: TableShower):
        super().__init__()
        parent.slave_widgets.append(self)
        self.source = parent.source
        self.db = parent.db
        self.key_fields = parent.key_fields
        self.p_content_up = parent.content_update
        self.changed_cells = {}
        self.old_data = dict(zip(header, info))
        self.main_layout = QVBoxLayout()
        self.cell_index = {}
        for h, i in zip(header, info):
            cell_layout = QHBoxLayout()
            cell_head = QLabel(str(h))
            cell_info = QLineEdit()
            cell_info.setText(str(i))
            cell_info.editingFinished.connect(lambda name=h, new_info_func=cell_info.text:
                                              self.changed_cells.__setitem__(name, new_info_func()))
            cell_layout.addWidget(cell_head)
            cell_layout.addWidget(cell_info)
            self.cell_index[str(h)] = cell_layout
            self.main_layout.addLayout(cell_layout)
        accept_btn = QPushButton("Подтвердить изменения")
        accept_btn.clicked.connect(self.push_changes)
        self.main_layout.addWidget(accept_btn)
        self.setLayout(self.main_layout)

    def push_changes(self):
        """отправляет изменения обратно в базу данных

        собирает запрос, поочерёдно сравнивая значения в изменённых ячейках и собриает в единый запрос"""
        params, query = self.get_set_query()

        # формирование части запроса для определения изменяемого кортежа
        query += " WHERE "
        key_fields_values = [self.old_data[field] for field in self.key_fields]
        key_query = [f"`{k}` = {v}" for k, v in zip(self.key_fields, key_fields_values)]
        query += " and ".join(key_query)
        if params:
            self.db.execute(f"UPDATE {self.source} SET {query} ", params=params)
            self.db.commit()
            self.p_content_up()
            self.close()

    def get_set_query(self):
        """формирует последовательность вида: поле1 = значение1, полеN = значениеN, ... на основе изменённых полей"""
        query = []
        params = []
        for field_name in self.changed_cells.keys():
            if self.changed_cells[field_name] != str(self.old_data[field_name]):
                query.append(f" `{field_name}` = %s")
                params.append(self.changed_cells[field_name])
        query = ",".join(query)
        return params, query


class TableRecordAdder(TableInfoChanger):
    def __init__(self, header, parent: TableShower):
        super().__init__(header=header, info=[""] * len(header), parent=parent)

    def push_changes(self):
        params, query = self.get_set_query()
        if params:
            self.db.execute(f"insert into {self.source} SET {query} ", params=params)
            self.db.commit()
            self.p_content_up()
            self.close()


if __name__ == '__main__':
    db_wrapper.connect(host="localhost",
                       user="root",
                       passwd="111222333",
                       database="пассажироперевозочная",
                       use_pure=True)

    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    drive = TableShower("`водитель`", ["Табельный номер"], deletable=True)
    drive.show()
    sys.exit((app.exec_()))

