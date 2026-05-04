from PySide6.QtWidgets import QToolButton, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout
from PySide6.QtCore import Qt, Signal

class WaveRangePage(QWidget):
    request_add_range = Signal()
    request_new_group = Signal()
    request_delete = Signal(QWidget)
    
    def __init__(self, is_master = False):
        super().__init__()
        self.is_wave_layer = True
        
        self.page_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        contents_widget = QWidget()
        self.ranges_layout = QVBoxLayout(contents_widget)
        self.ranges_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area.setWidget(contents_widget)
        self.page_layout.addWidget(self.scroll_area)
        
        self.btn_layout = QHBoxLayout()
        self.add_btn = QToolButton(text="Add range")
        self.add_grp_btn = QToolButton(text="+ Group")
        self.delete_grp_btn = QToolButton(text="- Group")
       
        self.btn_layout.addWidget(self.add_btn)
        self.btn_layout.addWidget(self.add_grp_btn)
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.delete_grp_btn)

        if is_master:
            self.delete_grp_btn.setEnabled(False)

        self.page_layout.addLayout(self.btn_layout)

        self.add_btn.clicked.connect(self.request_add_range)
        self.add_grp_btn.clicked.connect(self.request_new_group)
        self.delete_grp_btn.clicked.connect(lambda: self.request_delete.emit(self))
