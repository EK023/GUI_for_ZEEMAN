from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
)
from NumberValidator import NumericInput
from BaseFieldGroup import BaseFieldGroup

class SimpleFieldGroup(BaseFieldGroup):
    def __init__(self, name, with_checkbox=True):
        super().__init__(name)

        self.label = QLabel(name)
        self.input = NumericInput()

        if with_checkbox:
            self.checkbox = QCheckBox()

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)

        if hasattr(self, 'checkbox'):
            layout.addWidget(self.checkbox)

    def get(self):
        return {
            "enabled": self.checkbox.isChecked() if hasattr(self, 'checkbox') else None,
            "value": self.input.text(),
        }