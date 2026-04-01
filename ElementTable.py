from PySide6.QtCore import (
    Qt, 
)
from PySide6.QtWidgets import (
    QPushButton,
    QLabel,
)

from Models.Elements import Elements
from Rows.ElementRow import ElementRow

class ElementTable:
    def __init__(self, layout):
        self.layout = layout
        # layout.setAlignment(Qt.AlignTop)
        self.current_row = 1
        self.rows = {}

        self._init_headers()

    def _init_headers(self):
        headers = ["Element", "Estimate", "Fit", "Iter"]

        for col, text in enumerate(headers):
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label, 0, col)

    def add_element(self, model: Elements):
        element = model.element

        if element in self.rows:
            return
        row = self.current_row

        group = ElementRow(model)

        self.layout.addWidget(group.element, row, 0)
        self.layout.addWidget(group.estimate, row, 1)
        self.layout.addWidget(group.fit, row, 2, alignment=Qt.AlignCenter)
        self.layout.addWidget(group.iterlist, row, 3, alignment=Qt.AlignCenter)

        self.rows[element] = group
        self.current_row += 1

    def remove_element(self, element):
        if element not in self.rows:
            return

        del self.rows[element]

        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        self._init_headers()

        self.current_row = 1
        for group in self.rows.values():
            self.layout.addWidget(group.element, self.current_row, 0)
            self.layout.addWidget(group.estimate, self.current_row, 1)
            self.layout.addWidget(group.fit, self.current_row, 2, alignment=Qt.AlignCenter)
            self.layout.addWidget(group.iterlist, self.current_row, 3, alignment=Qt.AlignCenter)

            self.current_row += 1

    def to_dict(self):
        return [group.get() for group in self.rows]