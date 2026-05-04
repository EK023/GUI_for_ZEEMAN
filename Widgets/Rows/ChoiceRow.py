from PySide6.QtWidgets import QLabel, QComboBox

from Widgets.Rows.BaseRow import BaseRow

class ChoiceRow(BaseRow):
    def __init__(self, name, layout, row, choices):
        super().__init__(name)
        self.label = QLabel(name)
        self.combo = QComboBox()
        self.combo.addItems(choices)

        layout.addWidget(self.label, row, 0)
        layout.addWidget(self.combo, row, 1)

    def get(self):
        return self.combo.currentText()
    
    def set(self, selection):
        index = self.combo.findText(selection)
        if index != -1:
            self.combo.setCurrentIndex(index)
