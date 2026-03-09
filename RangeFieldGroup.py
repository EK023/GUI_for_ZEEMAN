from PySide6.QtWidgets import (
    QHBoxLayout,
)

from NumberValidator import NumericInput
from BaseFieldGroup import BaseFieldGroup
from SelectedRange import SelectedRange

class RangeFieldGroup(BaseFieldGroup):
    def __init__(self, model=SelectedRange):
        super().__init__()
        self.model = model

        self.min = NumericInput(str(model.min))
        self.max = NumericInput(str(model.max))

        layout = QHBoxLayout(self)
        layout.addWidget(self.min)
        layout.addWidget(self.max)

        self.min.textChanged.connect(lambda text: setattr(self.model, 'min', float(text.replace(",", "."))))
        self.max.textChanged.connect(lambda text: setattr(self.model, 'max', float(text.replace(",", "."))))

    def get(self):
        return [self.min.text(), self.max.text()]