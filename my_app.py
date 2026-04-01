import sys
from PySide6.QtCore import (
    QEvent, 
    Qt, 
    QEvent,
)
from PySide6.QtWidgets import (
    QApplication, 
    QFileDialog,
)
import json
import numpy as np

import pyqtgraph as pg

from Models.Elements import Elements
from Rows.ParameterRow import ParameterRow
from Controllers.PlotController import PlotInteractionController
from ElementTable import ElementTable
from Dropdown import DropDownMenu


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
                self.filePathLabel.setText(filename)
                self.plotInteraction.loadData(filename)
                
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.controlScrollArea.setMinimumWidth(250)
        self.controlScrollArea.setMaximumWidth(250)

        self.mainSplitter.setStretchFactor(0, 1) 
        self.mainSplitter.setStretchFactor(1, 0)

        self.controllers = []
        self.plotInteraction = PlotInteractionController(self.plotArea.layout(), self.waveRangeContents.layout(), self.controllers)
        
        self.selectPlottingFileButton.clicked.connect(self.selectFile)

        self.elementWidgets = []
        # self.addElementButton.clicked.connect(lambda: self.elementTable.add_row(Elements("",0.0)))
        self.saveConfButton.clicked.connect(self.save_data_to_file)

        self.paramsGroup.layout().addStretch()
        self.initiate_fields(self.paramsGroup.layout())
        self.elementTable = ElementTable(self.elementsContainer.layout())

        self.elementData = self.load_elements("newatom.dat")

        self.elementDropDown = DropDownMenu(self.SelectElements, self.elementData.keys())

        self.elementDropDown.popup.elementToggled.connect(self.handle_element_toggle)

    def load_elements(self, filename):
        with open (filename) as f:
            count = int(f.readline())
        data = np.loadtxt(filename, 
                          dtype=[ ("estimates", float), ("elements", "U2")],
                          usecols=(2, 10), skiprows=1, max_rows=count
                          )
        return {el: est for el, est in zip(data["elements"], data["estimates"])}
        
    def handle_element_toggle(self, element, checked):
        if checked:
            self.elementTable.add_element(Elements(element, self.elementData[element]))
        else:
            self.elementTable.remove_element(element)


    def initiate_fields(self, layout):
        self.fields = {}

        for name in ["res", "vr", "vsini", "vmic", "vmac", "teff", "logg", "metal"]:
            if name == "res":
                fg = ParameterRow(name, with_checkbox=False)
            else:   
                fg = ParameterRow(name)
            
            self.fields[name] = fg
            layout.takeAt(layout.count()-1)
            layout.addWidget(fg)
            layout.addStretch()

    

    def collect_values(self):
        results = {}
        print(self.controllers, "controllers in collect values")
        for name, field in self.fields.items():
            results[name] = field.get()    

        results["elements"] = self.elementTable.to_dict() # Probably want to use that in a better way
        for i, controller in enumerate(self.controllers):
            print(controller.get(), "controller get", controller.xmin, controller.xmax)

            results[f"range_{i}"] = controller.get()
        
        print(filename, "filename in collect values")
        results["file"] = filename


        return results
        
    
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
