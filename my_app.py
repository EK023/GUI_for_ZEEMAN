import sys
from PySide6.QtCore import (
    QEvent, 
    Qt, 
    QRegularExpression as QRegExp, # check if it's needed, no need for numbers but chem elems might need it
    QEvent,
)
from PySide6.QtWidgets import (
    QApplication, 
    QVBoxLayout,
    QLineEdit,
)
import pyqtgraph as pg
import numpy as np

from Elements import Elements
from SimpleFieldGroup import SimpleFieldGroup
from ElementFieldGroup import ElementFieldGroup

import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

uiclass, baseclass = pg.Qt.loadUiType("plot.ui")

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

    
class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Might need to use some external plotting tool and insert it 
        # here before plotting, e.g., matplotlib or pyqtgraph
        self.plot_widget = QVBoxLayout(self.widget)
        # In  the future let the user choose the data file for plotting
        data = np.loadtxt("plot1", usecols=(0, 1))

        self.graph_ranges = QVBoxLayout(self.scrollAreaWidgetContents)
        # from https://matplotlib.org/stable/gallery/widgets/span_selector.html
        

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        x = data[:, 0]
        y = data[:, 1]
        self.x = x
        self.y = y

        self.sc.axes.plot(x, y)
        self.sc.axes.set_xlim(x.min(), x.max())
        self.sc.axes.set_ylim(y.min(), y.max())
        self.plot_widget.addWidget(self.sc)
        self.plot_widget.addWidget(NavigationToolbar(self.sc, self))

        def onselect(xmin, xmax):
            indmin, indmax = np.searchsorted(self.x, (xmin, xmax))
            indmax = min(len(self.x) - 1, indmax)

            region_x = self.x[indmin:indmax]

            if len(region_x) >= 2:
                self.graph_ranges.addWidget(QLineEdit(f"Selected range: {region_x[0]:.2f} - {region_x[-1]:.2f}"))

        self.span = SpanSelector(
            self.sc.axes,
            onselect,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:blue"), # can change color 
            interactive=True,
            drag_from_anywhere=True
        )

        
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
        group = ElementFieldGroup(element)
        self.scroll_layout.addWidget(group)
        self.scroll_layout.addStretch()
    
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
