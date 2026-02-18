import sys
from PySide6.QtCore import (
    QEvent, 
    Qt, 
    QRegularExpression as QRegExp, # check if it's needed, no need for numbers but chem elems might need it
    QEvent,
    QPoint,
)
from PySide6.QtWidgets import (
    QApplication, 
    QVBoxLayout, 
)
import pyqtgraph as pg
import numpy as np

from Elements import Elements
from SimpleFieldGroup import SimpleFieldGroup
from ElementFieldGroup import ElementFieldGroup

import matplotlib.pyplot as plt

uiclass, baseclass = pg.Qt.loadUiType("plot.ui")


    
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
                fg = SimpleFieldGroup(name, with_checkbox=False)
            else:   
                fg = SimpleFieldGroup(name)
            
            self.fields[name] = fg
            layout.takeAt(layout.count()-1)
            layout.addWidget(fg)
            layout.addStretch()

    def collect_values(self):
        results = {}

        for name, field in self.fields.items():
            results[name] = field.get()

        
        for i, element in enumerate(self.elements):
            results[f"element_{i}"] = element.get()

        return results


    def add_element(self):
        new_elem = Elements("", 0.0)
        self.elements.append(new_elem)
        # print(self.elements[0].estimate, "elements")
        self.add_element_widget(new_elem)

    def add_element_widget(self, element):
        self.scroll_layout.takeAt(self.scroll_layout.count()-1)

        # elementLayout = QHBoxLayout(elementWidget)

        # el = QLineEdit()
        # est = NumericInput()
        # fit = QCheckBox()
        # iter = QCheckBox()

        # self.add_elements_to_layout(elementLayout, [el, est, fit, iter])
        
        # # changes in fields are also saved to elements object, makes it easier to deal with them later
        # el.textChanged.connect(lambda text, e=element: setattr(e, "element", text)) 
        # est.textChanged.connect(lambda text, e=element: setattr(e, "estimate", float(text.replace(",", ".")))) 
        # fit.stateChanged.connect(lambda state, e=element: setattr(e, "fit", bool(state))) 
        # iter.stateChanged.connect(lambda state, e=element: setattr(e, "iterlist", bool(state))) 


        # self.elementWidgets.append((el, est, fit, iter))
        group = ElementFieldGroup(element)
        self.scroll_layout.addWidget(group)
        self.scroll_layout.addStretch()
        # print(self.elementWidgets[0][0].text())      # How to access first element's name
        # print(self.elementWidgets[0][2].isChecked()) # How to access first element's fit checkbox

    
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
        print(self.collect_values())
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
