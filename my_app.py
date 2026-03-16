import sys
from unittest.mock import patch
from PySide6.QtCore import (
    QEvent, 
    Qt, 
    QRegularExpression as QRegExp, # check if it's needed, no need for numbers but chem elems might need it
    QEvent,
)
from PySide6.QtWidgets import (
    QApplication, 
    QVBoxLayout,
    QFileDialog,
)
import json

import pyqtgraph as pg
import numpy as np

from Elements import Elements
from SimpleFieldGroup import SimpleFieldGroup
from ElementFieldGroup import ElementFieldGroup
from PlotController import PlotInteractionController


from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


uiclass, baseclass = pg.Qt.loadUiType("plot.ui")

class MainWindow(uiclass, baseclass):
    
    def selectFile(self):
            global filename
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Choose a data file",
                "",
                "All Files (*);;Data Files (*.csv *.txt *.json)"
            )
            if filename:
                
                self.fileName = filename
                self.plotInteraction.loadData(filename, self.selectPlottingFileButton)
                

                
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Might need to use some external plotting tool and insert it 
        # here before plotting, e.g., matplotlib or pyqtgraph
        self.graph_ranges = QVBoxLayout(self.scrollAreaWidgetContents)

        self.controllers = []
        self.plot_widget = QVBoxLayout(self.widget)
        #self.plotInteraction = PlotInteractionController(self.widget.layout(), self.graph_ranges, self.controllers)
        self.plotInteraction = PlotInteractionController(self.plot_widget, self.graph_ranges, self.controllers)
    
        # In  the future let the user choose the data file for plotting
        self.selectPlottingFileButton.clicked.connect(self.selectFile)

        # loadAndPlotData(self, "plot1")
        
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
        print(self.controllers, "controllers in collect values")
        for name, field in self.fields.items():
            results[name] = field.get()    
        for i, element in enumerate(self.elements):
            results[f"element_{i}"] = element.get()
        for i, controller in enumerate(self.controllers):
            print(controller.get(), "controller get", controller.xmin, controller.xmax)

            results[f"range_{i}"] = controller.get()
        
        print(filename, "filename in collect values")
        results["file"] = filename


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
    
    def show_save_file_dialog(self,values):
        file_name, _ = QFileDialog.getSaveFileName(window, 'Save File', '', 'Text Files (*.txt);;All Files (*)')

        if file_name:
            with open(file_name, 'w') as file:
                file.write(json.dumps(values))
            print(f'Saved file: {file_name}')

    def save_data_to_file(self,):
        values = self.collect_values()
        print(values, "values in save data to file")
        self.show_save_file_dialog(values)
    

        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
