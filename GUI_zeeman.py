import sys
from PySide6.QtCore import QEvent, Qt, QEvent
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QToolButton, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout

import numpy as np
import pyqtgraph as pg

from Models.Elements import Elements
from Widgets.Rows.ParameterRow import ParameterRow
from Widgets.Rows.FileSelectRow import FileSelectRow
from Widgets.Rows.ChoiceRow import ChoiceRow
from Controllers.PlotController import PlotInteractionController
from Widgets.ElementTable import ElementTable
from Widgets.Dropdown import DropDownMenu
from Config.Reader import ConfigReader
from Config.Writer import ConfigWriter
from Widgets.WaveRangePage import WaveRangePage
from parameters import params, get_key as get_params_key
from Widgets.ListBuilder import ListBuilderWidget
# from Zeeman import zeeman_python

uiclass, baseclass = pg.Qt.loadUiType("plot.ui")

class MainWindow(uiclass, baseclass):

    
    def selectFile(self, name):
        f, _ = QFileDialog.getOpenFileName(
            self,
            f"Choose a {name} file",
            "",
            "All Files (*);;Data Files (*.csv *.txt *.json)"
        )
        if f:
            return f
                
    def plot_data(self, name=False, filename=False):
        
        if not filename :
            filename = self.selectFile(name)
        if self.fileName:
            self.clear_wave_groups()
            # self.elementTable.clear() # not sure if elements should be cleared as well
        self.fileName = filename
        self.filePathLabel.setText(filename)
        self.plot_controller.loadData(filename)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.rightToolBox.setMinimumWidth(300)
        self.rightToolBox.setMaximumWidth(300)

        self.mainSplitter.setStretchFactor(0, 1) 
        self.mainSplitter.setStretchFactor(1, 0)

        self.plot_controller = PlotInteractionController(self.plotArea)

        self.master_wave_page = WaveRangePage(is_master=True)
        self.rightToolBox.insertItem(1, self.master_wave_page, "Wave ranges")
        self.connect_wave_page_signals(self.master_wave_page)
        
        self.last_active_wave_page = self.master_wave_page
        self.rightToolBox.currentChanged.connect(self.on_toolbox_changed)
        self.plot_controller.switch_layer(self.master_wave_page, initialize=True)

        self.plot_controller.openWaveRanges.connect(self.force_open_wave_page)
        self.plot_controller.newWaveGroupRequested.connect(self.add_new_wave_group)
        
        self.selectPlottingFileButton.clicked.connect(lambda: self.plot_data("spectrum"))

        self.elementWidgets = []
        self.fileName = None
        self.saveConfButton.clicked.connect(self.save_data_to_file)
        self.loadConfButton.clicked.connect(self.load_conf_from_file)
        self.helpButton.clicked.connect(self.show_help_dialog)

        self.initiate_fields(self.page_3.layout())
        self.elementTable = ElementTable(self.elementsContainer.layout())

        self.elementData = self.load_elements("newatom.dat")

        self.elementDropDown = DropDownMenu(self.SelectElements, self.elementData.keys())
        self.elementDropDown.popup.elementToggled.connect(self.handle_element_toggle)

        all_params = ['vr', 'vmic', 'vmac', 'vsini', 'teff', 'logg','metal', 'contpoly'] + list(self.elementData.keys())
        self.iterlist_builder = ListBuilderWidget(all_params)
        self.iterLayout.addWidget(self.iterlist_builder)

        self.elementTable.elementRemoved.connect(self.elementDropDown.popup.uncheck_element)
        self.elementTable.elementAdded.connect(self.elementDropDown.popup.check_element)

    def load_elements(self, filename):
        with open (filename) as f:
            count = int(f.readline())
        data = np.loadtxt(filename, 
                          dtype=[ ("estimates", float), ("elements", "U2")],
                          usecols=(2, 10), skiprows=1, max_rows=count
                          )
        return {el: est for el, est in zip(data["elements"], data["estimates"])}
    
    def connect_wave_page_signals(self, page_widget):
        """Helper to wire up a new WaveRangePage."""
        page_widget.request_add_range.connect(self.manual_add_range)
        page_widget.request_new_group.connect(self.add_new_wave_group)
        page_widget.request_delete.connect(self.delete_wave_group)

        
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
                case "fit": 
                    fg = ParameterRow(display_name, layout, row)  
                case _: #default at the moment 
                    continue   
                  
            self.fields[key] = fg
            layout.addWidget(fg)
        
        layout.setRowStretch(999, 1)

    def collect_values(self):
        results = {}
        for name, field in self.fields.items():
            results[name] = field.get()    

        results['iterlist'] = self.iterlist_builder.get_lists_of_lists()
        results["elements"] = self.elementTable.to_dict()
        results["ranges"] = self.plot_controller.get_ranges()
        
        results["obsspecpath"] = self.fileName
        
        return results
    
    def add_new_wave_group(self):
        existing_waves = sum(1 for i in range(self.rightToolBox.count()) 
                             if getattr(self.rightToolBox.widget(i), "is_wave_layer", False))
        group_name = f"Wave ranges {existing_waves + 1}"
        
        new_page = WaveRangePage()
        self.connect_wave_page_signals(new_page)

        insert_index = self.rightToolBox.currentIndex() + 1
        self.rightToolBox.insertItem(insert_index, new_page, group_name)

        self.rightToolBox.setCurrentIndex(insert_index)

    def update_wave_group_names(self):
        wave_group_count = 1
        for i in range(self.rightToolBox.count()):
            widget = self.rightToolBox.widget(i)
            if getattr(widget, "is_wave_layer", False):
                self.rightToolBox.setItemText(i, f"Wave ranges {wave_group_count}")
                wave_group_count += 1

    def on_toolbox_changed(self, index):
        if index < 0:
            return
            
        current_page = self.rightToolBox.widget(index)
        
        if getattr(current_page, "is_wave_layer", False):
            current_page = self.rightToolBox.widget(index)

            self.plot_controller.switch_layer(current_page)
            self.last_active_wave_page = current_page

    def delete_wave_group(self, page_widget):
        self.plot_controller.delete_layer(page_widget)
        
        for i in range(self.rightToolBox.count()):
            if self.rightToolBox.widget(i) == page_widget:
                self.rightToolBox.removeItem(i)
                self.rightToolBox.setCurrentIndex(i-1)
                break
                
        page_widget.deleteLater()
        self.update_wave_group_names()

    def clear_wave_groups(self):
        for i in reversed(range(self.rightToolBox.count())):
            widget = self.rightToolBox.widget(i)
            if getattr(widget, "is_wave_layer", False) and widget != self.master_wave_page:
                self.plot_controller.delete_layer(widget)
                self.rightToolBox.removeItem(i)
                widget.deleteLater()
            if widget == self.master_wave_page:
                self.plot_controller.active_page_widget = widget
        self.update_wave_group_names()

    
    def force_open_wave_page(self):
        if self.last_active_wave_page:
            # Find the index using the widget object
            idx = self.rightToolBox.indexOf(self.last_active_wave_page)
            if idx != -1 and self.rightToolBox.currentIndex() != idx:
                self.rightToolBox.setCurrentIndex(idx)

    def manual_add_range(self):
        self.plot_controller.add_range(0, 0, active=False)
    
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

        # zeeman_python.run(file_name)

    def save_data_to_file(self,):
        values = self.collect_values()
        self.show_save_file_dialog(values)

    def load_conf_from_file(self):
        filename = self.selectFile("configuration")
        conf_reader = ConfigReader(filename)
        data = conf_reader.read()
        for key, value in data.items():
            if key in self.fields:
                self.fields[key].set(value)

        self.plot_data(filename=data["obsspecpath"])
        self.iterlist_builder.load_from_conf(data["iterlist"])
        self.plot_controller.load_from_conf(data['wave_range_lists'])
        self.elementTable.load_from_conf(data["elements"])

    def show_help_dialog(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Information about the GUI")
        dlg.setText("""
            Editing selected wave ranges from the plot
            is a little odd, easiest way is to edit them 
            from the side
                    
            Good old checklist:
                    
            * put the right file in observed.dat
            * input your initial estimate parameters
            * set the appropriate elements to be fittable
            * set vsini to be fittable or fixed
            * used the right line list in vlines.dat
            * set spectral windows and Itot in zmodel.dat

        """)
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setIcon(QMessageBox.Question)
        dlg.exec()


    
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
