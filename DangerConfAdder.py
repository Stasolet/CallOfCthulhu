from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QSizePolicy

from CthulhuCore.ViewShower import ViewInfoChanger, ViewShower, ViewRecordAdder

from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from DangerConfEditor import DangerConfEditor


class DangerConfAdder(ViewRecordAdder):
    add_cell = DangerConfEditor.add_cell
    del_cell = DangerConfEditor.del_cell
    push_slave_changes = DangerConfEditor.push_slave_changes
    slave_combo_update = DangerConfEditor.slave_combo_update

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
        self.worker_id = self.changed_cells["код_категории_вредности"]
        self.push_slave_changes()

