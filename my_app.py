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

# import matplotlib.pyplot as plt

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
        self.elementWidgets = []
        self.elements = []
        self.addElementButton.clicked.connect(self.add_element)

        self.scroll_layout.addStretch()

    def add_element(self):
        new_elem = Elements(len(self.elements)+1, "", 0.0)
        # if len(self.elements) == 0: # For adding labels inside the scroll box, not sure if I want them there
        #     self.add_label_widget()
        self.elements.append(new_elem)
        self.add_element_widget(new_elem)

    def add_label_widget(self):
        self.scroll_layout.takeAt(self.scroll_layout.count()-1)

        i = len(self.elementWidgets)

        elementWidget = QWidget()
        self.scroll_layout.addWidget(elementWidget)

        elementLayout = QHBoxLayout(elementWidget)

        el = QLabel("1")
        # est = QLineEdit(element.estimate)
        fit = QLabel("2")
        iter = QLabel("3")
        # button = QPushButton(f"Edit {i}")

        elementLayout.addWidget(el)
        # elementLayout.addWidget(est)
        elementLayout.addWidget(fit)
        elementLayout.addWidget(iter)

        self.elementWidgets.append((el, fit, iter))
        self.scroll_layout.addStretch()


    # Really buggy input validation, works only if the user inputs letters and 
    # if input valid writes the inserted number twice
    # def attach_number_tooltip(self, line_edit: QLineEdit): 
    #     validator = QDoubleValidator() 
    #     validator.setNotation(QDoubleValidator.StandardNotation) 
    #     line_edit.setValidator(validator) 
    
    #     def event_filter(obj, event): 
    #         if obj is line_edit and event.type() == QEvent.KeyPress: 
    #             before = line_edit.text() 
    #             result = QLineEdit.event(obj, event) 
    #             after = line_edit.text()
    #             if before == after and event.text().isalpha(): 
    #                 QToolTip.showText( line_edit.mapToGlobal(QPoint(0, line_edit.height())), "Numbers only" ) 
    #                 return result 
    #             return False 
    
    #     line_edit.installEventFilter(line_edit) 
    #     line_edit.eventFilter = event_filter
    
    def add_element_widget(self, element):
        # before stretch, remove stretch
        self.scroll_layout.takeAt(self.scroll_layout.count()-1)

        elementWidget = QWidget()
        self.scroll_layout.addWidget(elementWidget)

        elementLayout = QHBoxLayout(elementWidget)

        el = QLineEdit()
        est = QLineEdit()
        #self.attach_number_tooltip(est)
        fit = QCheckBox()
        iter = QCheckBox()

        # reg_ex = QRegExp("[0-9]+((\.|\,)[0-9]+)?")
        # input_validator = QRegExpValidator(reg_ex, est)
        # est.setValidator(input_validator)

        # validator = QDoubleValidator() 
        # validator.setNotation(QDoubleValidator.StandardNotation) 
        # est.setValidator(validator)
        # est.inputRejected.connect(lambda: est.setToolTip("Numbers only"))
        
        el.textChanged.connect(lambda text, e=element: setattr(e, "element", text)) 
        est.textChanged.connect(lambda text, e=element: setattr(e, "estimate", float(text) if text else 0.0)) 
        fit.stateChanged.connect(lambda state, e=element: setattr(e, "fit", bool(state))) 
        iter.stateChanged.connect(lambda state, e=element: setattr(e, "iterlist", bool(state))) 

        elementLayout.addWidget(el)
        elementLayout.addWidget(est)
        elementLayout.addWidget(fit)
        elementLayout.addWidget(iter)

        self.elementWidgets.append((el, est, fit, iter))
        self.scroll_layout.addStretch()
        print(self.elementWidgets[0][0].text())      # How to access first element's name
        print(self.elementWidgets[0][2].isChecked()) # How to access first element's fit checkbox
        
    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in (
            Qt.Key_Enter,
            Qt.Key_Return,
        ):
            self.focusNextPrevChild(True)
        return super().event(event)

    def input_validation(self,):
        pass

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
