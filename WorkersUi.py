from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from CthulhuCore.ViewShower import ViewShower,ViewInfoChanger,ViewRecordAdder
from WorkersEditor import WorkersEditor
from WorkersEditor import WorkersEditor
from WorkersAdder import WorkersAdder
worker_combo_config = {"категория_вредности": ("категории_вредности", "*", "название_категории_вредности","код_категории_вредности")}


class WorkersUi(ViewShower):

    def __init__(self):
        super().__init__("`работники_view`", ["табельный_номер"], "`работники`")
        self.record_editor = WorkersEditor
        self.record_adder = WorkersAdder
        WorkersEditor.combo_config = worker_combo_config
        WorkersAdder.combo_config = worker_combo_config

        # self.record_editor = type("OrderEditor", (ViewInfoChanger,), {"combo_config": worker_combo_config})
        # self.record_adder = type("OrderAdder", (ViewRecordAdder,), {"combo_config": worker_combo_config})
        # self.replacement_btn.clicked.connect(lambda: ViewShower("`корректировки_view`",
        #                                                          ["табельный_номер", "код_параметра"],"`корректировки`").show())

        self.show()

