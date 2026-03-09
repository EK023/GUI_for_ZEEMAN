from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLineEdit,
)
from NumberValidator import NumericInput
from BaseFieldGroup import BaseFieldGroup
from Elements import Elements

class ElementFieldGroup(BaseFieldGroup):
    def __init__(self, model: Elements):
        super().__init__()
        self.model= model


        self.element = QLineEdit(model.element) # In future maybe another validator for chem el
        self.estimate = NumericInput(str(model.estimate))
        self.fit = QCheckBox()
        self.fit.setChecked(model.fit)
        self.iterlist = QCheckBox()
        self.iterlist.setChecked(model.iterlist)


        layout = QHBoxLayout(self)
        layout.addWidget(self.element)
        layout.addWidget(self.estimate)
        layout.addWidget(self.fit)
        layout.addWidget(self.iterlist)

        self.element.textChanged.connect(lambda text: setattr(self.model, 'element', text))
        self.estimate.textChanged.connect(lambda text: setattr(self.model, 'estimate', float(text.replace(",", "."))))
        self.fit.stateChanged.connect(lambda state: setattr(self.model, 'fit', bool(state)))
        self.iterlist.stateChanged.connect(lambda state: setattr(self.model, 'iterlist', bool(state)))


    def get(self):
        return {
            "element": self.element.text(),
            "estimate": self.estimate.text(),
            "fit": self.fit.isChecked(),
            "iterlist": self.iterlist.isChecked(),
        }