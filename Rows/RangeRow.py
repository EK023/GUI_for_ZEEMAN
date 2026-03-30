from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Signal

from NumberValidator import NumericInput
from Rows.BaseRow import BaseRow
from Models.SelectedRange import SelectedRange

class RangeRow(BaseRow):

    deleteRequest = Signal()

    def __init__(self, model=SelectedRange):
        super().__init__()
        self.model = model

        self.min = NumericInput(str(model.min))
        self.max = NumericInput(str(model.max))
        self.delete_button = QPushButton("X")
        self.delete_button.setMaximumWidth(20)

        layout = QHBoxLayout(self)
        layout.addWidget(self.min)
        layout.addWidget(self.max)
        layout.addWidget(self.delete_button)

        self.delete_button.clicked.connect(self.deleteRequest.emit)

        self.min.textChanged.connect(lambda text: setattr(self.model, 'min', float(text.replace(",", "."))))
        self.max.textChanged.connect(lambda text: setattr(self.model, 'max', float(text.replace(",", "."))))

    def get(self):
        return [self.min.text(), self.max.text()]