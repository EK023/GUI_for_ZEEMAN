from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox
)
from PySide6.QtCore import Qt

class MultiSelectPopup(QWidget):
    def __init__(self, elements, parent=None):
        super().__init__(parent, Qt.Popup)
        self.setWindowFlags(Qt.Popup)
        self.setLayout(QVBoxLayout())
        self.checkboxes = {}

        for el in elements:
            cb = QCheckBox(el)
            cb.stateChanged.connect(lambda state, el=el: self.on_toggled(el, state))
            self.layout().addWidget(cb)
            self.checkboxes[el] = cb

    def on_toggled(self, element, state):
        if state == Qt.Checked:
            print(f"Add {element}")
        else:
            print(f"Remove {element}")

class DropDownMenu(QWidget):
    def __init__(self, elementButton):
        super().__init__()
        self.elementButton = elementButton
        elements = ["H", "He", "Li", "Be", "B", "C"]
        self.popup = MultiSelectPopup(elements, self)

        self.elementButton.clicked.connect(self.show_popup)

    def show_popup(self):
        pos = self.elementButton.mapToGlobal(self.elementButton.rect().bottomLeft())
        self.popup.move(pos)
        self.popup.show()