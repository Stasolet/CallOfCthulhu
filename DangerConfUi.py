from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from CthulhuCore.ViewShower import ViewShower,ViewInfoChanger,ViewRecordAdder
from WorkersEditor import WorkersEditor
from DangerConfEditor import DangerConfEditor
from DangerConfAdder import DangerConfAdder
worker_combo_config = None


class DangerConfUi(ViewShower):

    def __init__(self):
        super().__init__("`категории_вредности`", ["код_категории_вредности"], "категории_вредности")
        self.record_editor = DangerConfEditor
        self.record_adder = DangerConfAdder
        DangerConfEditor.combo_config = worker_combo_config
        DangerConfAdder.combo_config = worker_combo_config

        # self.record_editor = type("OrderEditor", (ViewInfoChanger,), {"combo_config": worker_combo_config})
        # self.record_adder = type("OrderAdder", (ViewRecordAdder,), {"combo_config": worker_combo_config})
        # self.replacement_btn.clicked.connect(lambda: ViewShower("`корректировки_view`",
        #                                                          ["табельный_номер", "код_параметра"],"`корректировки`").show())

        self.show()
