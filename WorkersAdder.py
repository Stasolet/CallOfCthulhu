from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QSizePolicy

from CthulhuCore.ViewShower import ViewInfoChanger, ViewShower, ViewRecordAdder

from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from WorkersEditor import WorkersEditor


class WorkersAdder(ViewRecordAdder):
    add_cell = WorkersEditor.add_cell
    del_cell = WorkersEditor.del_cell
    push_slave_changes = WorkersEditor.push_slave_changes
    slave_combo_update = WorkersEditor.slave_combo_update

    def __init__(self, header, parent: ViewShower):
        super().__init__(header, parent)
        self.combo_change_idx["название_параметра"] = {}
        self.worker_id = None
        self.way_layout = QVBoxLayout()
        push_btn = self.main_layout.takeAt(self.main_layout.count() - 1).widget()
        self.slave_combo_config = {"название_параметра": ("параметры", "*", "название_параметра", "код_параметра")}
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(lambda e: self.add_cell(-1))
        self.main_layout.addWidget(add_btn)

        self.main_layout.addLayout(self.way_layout)
        self.main_layout.addWidget(push_btn)

    def push_changes(self):
        super().push_changes()
        self.worker_id = self.changed_cells["табельный_номер"]
        self.push_slave_changes()

