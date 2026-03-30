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
        layout.setAlignment(Qt.AlignTop)
        self.current_row = 1
        self.rows = []

        self._init_headers()

    def _init_headers(self):
        headers = ["Element", "Estimate", "  Fit  ", "Add to Iterlist", "Delete Element"]

        for col, text in enumerate(headers):
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label, 0, col)

    def add_row(self, model: Elements):
        row = self.current_row

        group = ElementRow(model)

        delete_button = QPushButton("X")
        delete_button.clicked.connect(lambda _, g=group: self.remove_row(g))

        self.layout.addWidget(group.element, row, 0)
        self.layout.addWidget(group.estimate, row, 1)
        self.layout.addWidget(group.fit, row, 2, alignment=Qt.AlignCenter)
        self.layout.addWidget(group.iterlist, row, 3, alignment=Qt.AlignCenter)
        self.layout.addWidget(delete_button, row, 4)

        self.rows.append(group)
        self.current_row += 1

    def remove_row(self, group):
        self.rows.remove(group)
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        self._init_headers()

        self.current_row = 1
        for group in self.rows:
            delete_button = QPushButton("X")
            delete_button.clicked.connect(lambda _, g=group: self.remove_row(g))

            self.layout.addWidget(group.element, self.current_row, 0)
            self.layout.addWidget(group.estimate, self.current_row, 1)
            self.layout.addWidget(group.fit, self.current_row, 2, alignment=Qt.AlignCenter)
            self.layout.addWidget(group.iterlist, self.current_row, 3, alignment=Qt.AlignCenter)
            self.layout.addWidget(delete_button, self.current_row, 4)

            self.current_row += 1

    def to_dict(self):
        return [group.get() for group in self.rows]