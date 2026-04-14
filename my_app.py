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

import numpy as np

import pyqtgraph as pg

from Models.Elements import Elements
from Rows.ParameterRow import ParameterRow
from Rows.FileSelectRow import FileSelectRow
from Rows.ChoiceRow import ChoiceRow
from Controllers.PlotController import PlotInteractionController
from ElementTable import ElementTable
from Dropdown import DropDownMenu
from Config.Reader import ConfigReader
from Config.Writer import ConfigWriter
from parameters import params, get_key as get_params_key

uiclass, baseclass = pg.Qt.loadUiType("plot.ui")

class MainWindow(uiclass, baseclass):

    
    def selectFile(self):
        f, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a data file",
            "",
            "All Files (*);;Data Files (*.csv *.txt *.json)"
        )
        if f:
            return f
    
    def selectFileAndPlot(self):
        filename = self.selectFile()
        self.fileName = filename
        self.filePathLabel.setText(filename)
        self.plotInteraction.loadData(filename)
                
    def plot_data(self, filename):
        self.fileName = filename
        self.filePathLabel.setText(filename)
        self.plotInteraction.loadData(filename)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.rightPanel.setMinimumWidth(250)
        self.rightPanel.setMaximumWidth(250)

        self.page_3.setMinimumWidth(250)
        self.page_3.setMaximumWidth(250)

        self.mainSplitter.setStretchFactor(0, 1) 
        self.mainSplitter.setStretchFactor(1, 0)

        self.controllers = []
        self.plotInteraction = PlotInteractionController(self.plotArea, self.waveRangeContents.layout(), self.controllers)

        self.plotInteraction.openWaveRanges.connect(lambda: self.rightPanel.setCurrentWidget(self.page_2))

        self.addRangeButton.clicked.connect(lambda: self.plotInteraction.add_range(0, 0, active=False))
        
        self.selectPlottingFileButton.clicked.connect(self.selectFileAndPlot)

        self.elementWidgets = []
        # self.addElementButton.clicked.connect(lambda: self.elementTable.add_row(Elements("",0.0)))
        self.saveConfButton.clicked.connect(self.save_data_to_file)
        self.loadConfButton.clicked.connect(self.load_conf_from_file)

        self.initiate_fields(self.page_3.layout())
        self.elementTable = ElementTable(self.elementsContainer.layout())

        self.elementData = self.load_elements("newatom.dat")

        self.elementDropDown = DropDownMenu(self.SelectElements, self.elementData.keys())

        self.elementDropDown.popup.elementToggled.connect(self.handle_element_toggle)

        self.elementTable.elementRemoved.connect(self.elementDropDown.popup.uncheck_element)

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
        for row, meta in enumerate(params):
            display_name = meta["display"]
            key = get_params_key(meta)
            row_type = meta["type"]
            
            match row_type:
                case "int":
                    fg = ParameterRow(display_name, layout, row, with_checkbox=False)
                case "bool":
                    fg = ParameterRow(display_name, layout, row, with_text=False, with_checkbox=True)
                case "file":
                    fg = FileSelectRow(display_name, layout, row, folder=meta.get("folder", False)) # False is the fallback if there is no Folder
                case "choice":
                    fg = ChoiceRow(display_name, layout, row, meta.get("options"))
                case _: #default at the moment 
                    fg = ParameterRow(display_name, layout, row)     
                  
            self.fields[key] = fg
            layout.addWidget(fg)
        
        layout.setRowStretch(999, 1)

    def collect_values(self):
        results = {}
        for name, field in self.fields.items():
            results[name] = field.get()    

        results["elements"] = self.elementTable.to_dict() # Probably want to use that in a better way
        for i, controller in enumerate(self.controllers):
            results[f"range_{i}"] = controller.get()
        
        results["obsspecpath"] = self.fileName
        
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
        file_name, _ = QFileDialog.getSaveFileName(window, 'Save File', '','All Files (*) ;;Text Files (*.txt)') # can change default file formats

        if file_name:
            self.config_writer = ConfigWriter(file_name, values)

    def save_data_to_file(self,):
        values = self.collect_values()
        print(values, "values in save data to file")
        self.show_save_file_dialog(values)

    def merge_ranges(self, ranges):
        if not ranges:
            return []

        merged = []
        current_min, current_max = ranges[0]

        for min_val, max_val in ranges[1:]:
            if min_val == current_max:
                # extend current range
                current_max = max_val
            else:
                merged.append([current_min, current_max])
                current_min, current_max = min_val, max_val

        merged.append([current_min, current_max])
        return merged
    
    def merge_element_data(self, elements, iterlist):
        iter_set = set(iterlist[0]) if iterlist else set()

        return [
            [el, est, fit, int(el in iter_set)]
            for el, est, fit in elements
        ]

    def load_conf_from_file(self):
        filename = self.selectFile()
        conf_reader = ConfigReader(filename)
        data = conf_reader.read()
        print(data)
         # contpoly has a weird thing at the moment, need to fix that
        for key, value in data.items():
            if key in self.fields:
                self.fields[key].set(value)
        self.plot_data(data["obsspecpath"])

        # Unite the split up wave ranges back to one big one if there are any
        merged_wave_ranges = self.merge_ranges(data['wave_range_lists'])
        self.plotInteraction.load_from_conf(merged_wave_ranges)

        merged_elements = self.merge_element_data(data["elements"], data["iterlist"])
        self.elementTable.load_from_conf(merged_elements)

    
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
