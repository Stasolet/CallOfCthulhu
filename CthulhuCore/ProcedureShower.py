from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSizePolicy

from CthulhuCore.DbWrapper import db_wrapper
from CthulhuCore.QueryResShower import QueryResShower


class ProcedureShower(QWidget):
    def __init__(self, procedure_name, arg: list = None):
        super().__init__()

        self.slave = []
        self.procedure_name = procedure_name
        self.db = db_wrapper
        self.args = arg
        self.combo_arg = {}
        self.args_value_getters = []
        self.combo_substitution_idx = {}

        self.main_layout = QVBoxLayout()
        self.input_layout = QVBoxLayout()
        self.res_layout = QVBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.res_layout)
        self.setLayout(self.main_layout)

        show_res = QPushButton("Показать")
        show_res.clicked.connect(self.content)
        self.main_layout.addWidget(show_res)
        if arg:
            for i in arg:
                cell = QHBoxLayout()
                cell_name = QLabel()
                cell.addWidget(cell_name)
                if type(i) is tuple:
                    arg_name = i[0]
                    cell_name.setText(str(arg_name))
                    cell_comb_search = QLineEdit()
                    cell_val = QComboBox()
                    cell_comb_search.editingFinished.connect(lambda combo_name=arg_name,
                                                                    combo=cell_val,
                                                                    t=cell_comb_search:
                                                             self.combo_update(combo_name, combo, t.text()))
                    cell.addWidget(cell_comb_search)

                    cell_comb_search.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
                    cell_val.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                    self.args_value_getters.append(lambda c_name=arg_name, c=cell_val:
                                                   self.combo_get(c_name, c))
                    self.combo_arg[arg_name] = i[1]
                    self.combo_substitution_idx[arg_name] = {}
                    self.combo_update(arg_name, cell_val, "")  # изначальное заполнение всеми возможными
                else:
                    cell_name.setText(str(i))
                    cell_val = QLineEdit()
                    self.args_value_getters.append(cell_val.text)

                cell.addWidget(cell_val)
                self.input_layout.addLayout(cell)

    def combo_update(self, combo_name, combo, text):
        results = self.db.execute(f"""SELECT {self.combo_arg[combo_name]["substitution"]}, 
                                    {self.combo_arg[combo_name]["comb_info"]}
                                    from {self.combo_arg[combo_name]["src"]} 
                                    where {self.combo_arg[combo_name]["comb_info"]} LIKE '%{text}%';""")
        combo.clear()
        for i in results:
            combo_text = " ".join(i[1:])  # за счёт этой части можно кидать несколько полей
            self.combo_substitution_idx[combo_name][combo_text] = i[0]
            combo.addItem(combo_text)

    def combo_get(self, combo_name, c: QComboBox):
        if c.currentText():
            return self.combo_substitution_idx[combo_name][c.currentText()]

    def content(self):
        args = [getter() for getter in self.args_value_getters]
        cur = self.db.callproc(self.procedure_name, args)
        data = next(cur.stored_results())
        data = [data.column_names] + data.fetchall()
        c = QueryResShower(data)
        self.slave.append(c)
        c.show()

