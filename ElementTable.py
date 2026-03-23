from PySide6.QtCore import (
    Qt, 
)
from PySide6.QtWidgets import (
    QLabel,
)

from Elements import Elements
from ElementFieldGroup import ElementFieldGroup

class ElementTable:
    def __init__(self, layout):
        self.layout = layout
        layout.setAlignment(Qt.AlignTop)
        self.current_row = 1
        self.rows = []

        self._init_headers()

    def _init_headers(self):
        headers = ["Element", "Estimate", "  Fit  ", "Add to Iterlist"]

        for col, text in enumerate(headers):
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label, 0, col)

    def add_row(self, model: Elements):
        row = self.current_row

        group = ElementFieldGroup(model)

        self.layout.addWidget(group.element, row, 0)
        self.layout.addWidget(group.estimate, row, 1)
        self.layout.addWidget(group.fit, row, 2, alignment=Qt.AlignCenter)
        self.layout.addWidget(group.iterlist, row, 3, alignment=Qt.AlignCenter)

        self.rows.append(group)
        self.current_row += 1