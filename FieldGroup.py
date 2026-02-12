from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QCheckBox,
    QHBoxLayout,
    QLabel,
)
import NumberValidator

class FieldGroup(QWidget):
    def __init__(self, name, with_checkbox=True):
        super().__init__()
        self.name = name

        layout = QHBoxLayout(self)
        self.label = QLabel(name)
        self.input = QLineEdit()

        NumberValidator.NumericInput(self.input)

        if with_checkbox:
            self.checkbox = QCheckBox()
        
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        if hasattr(self, 'checkbox'):
            layout.addWidget(self.checkbox)

    def get(self):
        return {
            "enabled": self.checkbox.isChecked() if hasattr(self, 'checkbox') else None,
            "value": self.input.text(),
        }
