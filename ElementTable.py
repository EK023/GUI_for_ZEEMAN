from PySide6.QtCore import (
    Qt, Signal
)
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
)

from Models.Elements import Elements
from Rows.ElementRow import ElementRow

class ElementTable(QWidget):
    elementRemoved = Signal(str)

    def __init__(self, layout):
        super().__init__()
        self.layout = layout
        # layout.setAlignment(Qt.AlignTop)
        self.current_row = 1
        self.rows = {}

        self._init_headers()

    def _init_headers(self):
        headers = ["Element", "Estimate", "  Fit  ", "  Iter  "]
        self.layout.setRowStretch(999, 1)
        for col, text in enumerate(headers):
            label = QLabel(text)
            self.layout.addWidget(label, 0, col )

        # self.layout.

    def add_element(self, model: Elements):
        element = model.element

        if element in self.rows:
            return
        row = self.current_row

        group = ElementRow(model)

        delete_button = QPushButton("X")
        delete_button.setMaximumWidth(20)
        delete_button.clicked.connect(lambda _, e=element: self.remove_element(e))

        self.layout.addWidget(group.element, row, 0)
        self.layout.addWidget(group.estimate, row, 1)
        self.layout.addWidget(group.fit, row, 2, alignment=Qt.AlignCenter)
        self.layout.addWidget(group.iterlist, row, 3, alignment=Qt.AlignCenter)
        self.layout.addWidget(delete_button, row, 4)

        self.rows[element] = group
        self.current_row += 1

    def remove_element(self, element):
        if element not in self.rows:
            return

        del self.rows[element]
        self.elementRemoved.emit(element)

        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        self._init_headers()

        self.current_row = 1
        for group in self.rows.values():
            delete_button = QPushButton("X")
            delete_button.setMaximumWidth(20)
            delete_button.clicked.connect(lambda _, e=group: self.remove_element(e.element.text()))
            self.layout.addWidget(group.element, self.current_row, 0)
            self.layout.addWidget(group.estimate, self.current_row, 1)
            self.layout.addWidget(group.fit, self.current_row, 2, alignment=Qt.AlignCenter)
            self.layout.addWidget(group.iterlist, self.current_row, 3, alignment=Qt.AlignCenter)
            self.layout.addWidget(delete_button, self.current_row, 4 )

            self.current_row += 1

    def to_dict(self):
        return [group.get() for group in self.rows]