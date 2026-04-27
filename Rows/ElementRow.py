from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
)
from NumberValidator import NumericInput
from Rows.BaseRow import BaseRow
from Models.Elements import Elements

class ElementRow(BaseRow):
    def __init__(self, model: Elements):
        super().__init__()
        self.model= model


        self.element = QLabel(model.element)
        self.estimate = NumericInput(str(model.estimate))
        self.fit = QCheckBox()
        self.fit.setChecked(model.fit)
        self.iterlist = QCheckBox()
        self.iterlist.setChecked(model.iterlist)

        self.estimate.editingFinished.connect(self.update_estimate)
        self.fit.stateChanged.connect(lambda state: setattr(self.model, 'fit', bool(state)))
        self.iterlist.stateChanged.connect(lambda state: setattr(self.model, 'iterlist', bool(state)))


    def get(self):
        return {
            "element": self.element.text(),
            "estimate": self.estimate.text(),
            "fit": self.fit.isChecked(),
            "iterlist": self.iterlist.isChecked(),
        }
    
    def update_estimate(self):
        self.model.estimate = float(self.estimate.text())
    
    
    def set(self, element, estimate, fit, iterlist):
        self.model.element = element
        self.model.estimate = estimate
        self.model.fit = bool(fit)
        self.model.iterlist = bool(iterlist)