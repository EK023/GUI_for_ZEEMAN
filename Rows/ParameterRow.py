from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
)
from NumberValidator import NumericInput
from Rows.BaseRow import BaseRow

class ParameterRow(BaseRow):
    def __init__(self, name, layout, row, text=0, checkbox=False,  with_text=True, with_checkbox=True):
        super().__init__(name)
        self.label = QLabel(name)

        self.input = NumericInput(text) if with_text else None

        
        self.checkbox = QCheckBox() if with_checkbox else None
        if self.checkbox:
            self.checkbox.setChecked(checkbox)

        layout.addWidget(self.label, row, 0)

        if self.input:
            layout.addWidget(self.input, row, 1)

        if self.checkbox:
            layout.addWidget(self.checkbox, row, 2)

    def get(self):
        return {
            "enabled": self.checkbox.isChecked() if self.checkbox else None,
            "value": self.input.text() if self.input else None,
        }
    
    def set(self, value, enabled):
        if self.input:
            self.input.setText(str(value))
        if self.checkbox:
            self.checkbox.setChecked(enabled)