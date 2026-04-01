from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
)
from NumberValidator import NumericInput
from Rows.BaseRow import BaseRow

class ParameterRow(BaseRow):
    def __init__(self, name, layout, row, text=0.0, checkbox=False,  with_text=True, with_checkbox=True):
        super().__init__(name)

        self.label = QLabel(name)
        self.input = NumericInput(text) if with_text else None

        if with_checkbox:
            self.checkbox = QCheckBox()
        self.checkbox.setChecked(checkbox) if with_checkbox else None

        layout.addWidget(self.label, row, 0)

        if with_text:
            layout.addWidget(self.input, row, 1)

        if hasattr(self, 'checkbox'):
            layout.addWidget(self.checkbox, row, 2)

    def get(self):
        return {
            "enabled": self.checkbox.isChecked() if hasattr(self, 'checkbox') else None,
            "value": self.input.text(),
        }