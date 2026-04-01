from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QLineEdit, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal

class MultiSelectPopup(QWidget):

    elementToggled = Signal(str, bool)

    def __init__(self, elements, parent=None, max_height=300):
        super().__init__(parent, Qt.Popup)
        self.setWindowFlags(Qt.Popup)
        self.setLayout(QVBoxLayout())
        self.checkboxes = {}
        self.all_elements = elements

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.layout().addWidget(self.search_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.scroll_area)

        container = QFrame()
        scroll_layout = QVBoxLayout(container)
        container.setLayout(scroll_layout)
        self.scroll_area.setWidget(container)

        for el in elements:
            cb = QCheckBox(el)
            cb.stateChanged.connect(lambda state, el=el: self.on_toggled(el, state))
            scroll_layout.addWidget(cb)
            self.checkboxes[el] = cb
        
        scroll_layout.addStretch()

        self.scroll_area.setMaximumHeight(max_height)


        self.search_bar.textChanged.connect(self.filter_elements)

    def on_toggled(self, element, state):       
        state = Qt.CheckState(state) == Qt.Checked
        if state:
            self.elementToggled.emit(element, state)
        else:
            self.elementToggled.emit(element, state)
    
    def filter_elements(self, text):
        text = text.lower()

        for el, cb in self.checkboxes.items():
            cb.setVisible(text in el.lower())

class DropDownMenu(QWidget):

    # Need to decide where the app is exactly when its used, maybe even let user conf the file location
    def __init__(self, elementButton, elements):
        super().__init__()
        self.elementButton = elementButton

        # elements = ["H", "He", "Li", "Be", "B", "C"]
        self.popup = MultiSelectPopup(elements, self)

        self.elementButton.clicked.connect(self.show_popup)

    def show_popup(self):
        pos = self.elementButton.mapToGlobal(self.elementButton.rect().bottomLeft())
        self.popup.move(pos)
        self.popup.show()