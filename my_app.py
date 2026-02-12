import sys
from PySide6.QtCore import (
    QEvent, 
    Qt, 
    QRegularExpression as QRegExp, # check if it's needed, no need for numbers but chem elems might need it
    QEvent,
    QPoint,
)
from PySide6.QtGui import QRegularExpressionValidator as QRegExpValidator, QDoubleValidator
from PySide6.QtWidgets import (
    QApplication, 
    QVBoxLayout, 
    QWidget, 
    QHBoxLayout, 
    QLineEdit, 
    QPushButton, 
    QCheckBox,
    QLabel,
    QToolTip,
)
import pyqtgraph as pg
import numpy as np

import NumberValidator
import FieldGroup

import matplotlib.pyplot as plt

uiclass, baseclass = pg.Qt.loadUiType("plot.ui")

class Elements:
    def __init__(self, id, element, estimate, fit = False, iterlist = False):
        self.id = id
        self.element = element
        self.estimate = estimate
        self.fit = fit
        self.iterlist = iterlist
    
class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Might need to use some external plotting tool and insert it 
        # here before plotting, e.g., matplotlib or pyqtgraph

        # In  the future let the user choose the data file for plotting
        data = np.loadtxt("plot1", usecols=(0, 1))
        self.widget.plot(data[:, 0], data[:, 1])
        
        self.scroll_layout = QVBoxLayout(self.tab2_scrollAreaWidgetContents) # inside a scroll element
        self.scroll_layout2 = QVBoxLayout(self.simpleParams)
        self.elementWidgets = []
        self.elements = []
        self.addElementButton.clicked.connect(self.add_element)
        self.saveConfButton.clicked.connect(self.save_data_to_file)

        self.scroll_layout2.addStretch()
        self.initiate_fields(self.scroll_layout2)
        
        

        self.scroll_layout.addStretch()

    def initiate_fields(self, layout):
        self.fields = {}

        for name in ["res", "vr", "vsini", "vmic", "vmac", "teff", "logg", "metal"]:
            if name == "res":
                fg = FieldGroup.FieldGroup(name, with_checkbox=False)
            else:   
                fg = FieldGroup.FieldGroup(name)
            
            self.fields[name] = fg
            layout.takeAt(layout.count()-1)
            layout.addWidget(fg)
            layout.addStretch()



    def add_element(self):
        new_elem = Elements(len(self.elements)+1, "", 0.0)
        self.elements.append(new_elem)
        print(self.elements[0].estimate, "elements")
        self.add_element_widget(new_elem)

    def add_element_widget(self, element):
        self.scroll_layout.takeAt(self.scroll_layout.count()-1)

        elementWidget = QWidget()
        self.scroll_layout.addWidget(elementWidget)

        elementLayout = QHBoxLayout(elementWidget)

        el = QLineEdit()
        est = QLineEdit()
        #self.number_validation(est) 
        fit = QCheckBox()
        iter = QCheckBox()

        NumberValidator.NumericInput(est)

        self.add_elements_to_layout(elementLayout, [el, est, fit, iter])
        
        # changes in fields are also saved to elements object, makes it easier to deal with them later
        el.textChanged.connect(lambda text, e=element: setattr(e, "element", text)) 
        est.textChanged.connect(lambda text, e=element: setattr(e, "estimate", float(text.replace(",", ".")))) 
        fit.stateChanged.connect(lambda state, e=element: setattr(e, "fit", bool(state))) 
        iter.stateChanged.connect(lambda state, e=element: setattr(e, "iterlist", bool(state))) 


        self.elementWidgets.append((el, est, fit, iter))
        self.scroll_layout.addStretch()
        print(self.elementWidgets[0][0].text())      # How to access first element's name
        print(self.elementWidgets[0][2].isChecked()) # How to access first element's fit checkbox

    
    def add_elements_to_layout(self, layout, elements):
        for e in elements:
            layout.addWidget(e)
        

        
    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in (
            Qt.Key_Enter,
            Qt.Key_Return,
        ):
            self.focusNextPrevChild(True)
        return super().event(event)

    def save_data_to_file(self,):
        self.elements
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
