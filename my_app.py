import sys
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import (
    QApplication, 
    QVBoxLayout, 
    QWidget, 
    QHBoxLayout, 
    QLineEdit, 
    QPushButton, 
    QCheckBox,
    QLabel,
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
        # self.plot_graph = pg.PlotWidget()
        # self.setCentralWidget(self.plot_graph)
        data = np.loadtxt("plot1", usecols=(0, 1))
        # time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        self.widget.plot(data[:, 0], data[:, 1])

        
        self.scroll_layout = QVBoxLayout(self.tab2_scrollAreaWidgetContents) # inside a scroll element
        self.elementWidgets = []
        self.elements = []
        # for i, contact in enumerate(Elements): # if there are previous values to load from somewhere can use this
        #     contactWidget = QWidget()
        #     layout.addWidget(contactWidget)
        #     contactLayout = QHBoxLayout(contactWidget)
        #     edit = QLineEdit(contact.element)
        #     pushButton = QPushButton(f"Edit {i}")
        #     contactLayout.addWidget(edit)
        #     contactLayout.addWidget(pushButton)
        #     self.elementWidgets.append((edit, pushButton)) 

        # a "spacer" at the bottom, in case there are not enough contact 
        # widgets to vertically fill the scroll area
        self.addElementButton = QPushButton("Add Element")
        self.scroll_layout.addWidget(self.addElementButton)
        self.addElementButton.clicked.connect(self.add_element)

        self.scroll_layout.addStretch()

    def add_element(self):
        new_elem = Elements(len(self.elements)+1, "", 0.0)
        if len(self.elements) == 0:
            self.add_label_widget()
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

        # add stretch back
        self.scroll_layout.addStretch()
    
    def add_element_widget(self, element):
        # before stretch, remove stretch
        self.scroll_layout.takeAt(self.scroll_layout.count()-1)

        i = len(self.elementWidgets)

        elementWidget = QWidget()
        self.scroll_layout.addWidget(elementWidget)

        elementLayout = QHBoxLayout(elementWidget)

        el = QLineEdit(element.element)
        # est = QLineEdit(element.estimate)
        fit = QCheckBox()
        iter = QCheckBox()
        # button = QPushButton(f"Edit {i}")

        elementLayout.addWidget(el)
        # elementLayout.addWidget(est)
        elementLayout.addWidget(fit)
        elementLayout.addWidget(iter)

        self.elementWidgets.append((el, fit, iter))

        # add stretch back
        self.scroll_layout.addStretch()
    
    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in (
            Qt.Key_Enter,
            Qt.Key_Return,
        ):
            self.focusNextPrevChild(True)
        return super().event(event)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

# from random import randint

# import pyqtgraph as pg
# from PyQt6 import QtCore, QtWidgets

# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Temperature vs time dynamic plot
#         self.plot_graph = pg.PlotWidget()
#         self.setCentralWidget(self.plot_graph)
#         self.plot_graph.setBackground("w")
#         pen = pg.mkPen(color=(255, 0, 0))
#         self.plot_graph.setTitle("Temperature vs Time", color="b", size="20pt")
#         styles = {"color": "red", "font-size": "18px"}
#         self.plot_graph.setLabel("left", "Temperature (°C)", **styles)
#         self.plot_graph.setLabel("bottom", "Time (min)", **styles)
#         self.plot_graph.addLegend()
#         self.plot_graph.showGrid(x=True, y=True)
#         self.plot_graph.setYRange(20, 40)
#         self.time = list(range(10))
#         self.temperature = [randint(20, 40) for _ in range(10)]
#         # Get a line reference
#         self.line = self.plot_graph.plot(
#             self.time,
#             self.temperature,
#             name="Temperature Sensor",
#             pen=pen,
#             symbol="+",
#             symbolSize=15,
#             symbolBrush="b",
#         )
#         # Add a timer to simulate new temperature measurements
#         self.timer = QtCore.QTimer()
#         self.timer.setInterval(300)
#         self.timer.timeout.connect(self.update_plot)
#         self.timer.start()

#     def update_plot(self):
#         self.time = self.time[1:]
#         self.time.append(self.time[-1] + 1)
#         self.temperature = self.temperature[1:]
#         self.temperature.append(randint(20, 40))
#         self.line.setData(self.time, self.temperature)

# app = QtWidgets.QApplication([])
# main = MainWindow()
# main.show()
# app.exec()