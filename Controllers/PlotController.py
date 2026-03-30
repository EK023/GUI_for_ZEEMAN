import numpy as np
from matplotlib.widgets import SpanSelector
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PySide6.QtCore import (
    Qt, 
)

from Controllers.RangeController import RangeController

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

class PlotInteractionController:
    def __init__(self, plot_widget, graph_ranges, controllers):
        self.plot_widget = plot_widget
        self.graph_ranges = graph_ranges
        self.controllers = controllers
        self.activeController = None
        self.isDragging = False

    def loadData(self, filename):
        data = np.loadtxt(filename, usecols=(0, 1))
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        x = data[:, 0]
        y = data[:, 1]
        self.x = x
        self.y = y
        self.sc.axes.plot(x, y)
        
        self.sc.axes.set_xlim(x.min(), x.max())
        self.sc.axes.set_ylim(y.min(), y.max())
        
        self.plot_widget.addWidget(self.sc)
        #self.plot_widget.addWidget(NavigationToolbar(self.sc, self.plot_widget))

        self.activeController = None
        self.isDragging = False
        self.sc.fig.canvas.mpl_connect("button_release_event", lambda e: setattr(self, "isDragging", False))

        self.span = SpanSelector(
            self.sc.axes,
            self.onselect,
            "horizontal",
            useblit=False,
            grab_range=20, # Check if that helps anything....
            props=dict(alpha=0.4, facecolor="tab:blue"), # can change color 
            interactive=True,
            handle_props={"mouseover":True},
            drag_from_anywhere=False
        )

        self.sc.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

        self.sc.fig.canvas.mpl_connect('pick_event', self.onPick)
    
    def setupInteractions(self):
        ...
    
    def onselect(self,xmin, xmax):
        if xmin == xmax:
            self.activeController = None
            return
        self.isDragging = True
        # If a range is active → edit it
        if self.isDragging and self.activeController is not None:
            self.activeController.updatePatch(xmin, xmax)
            return

        # Otherwise → create a new range
        controller = RangeController(self.sc.axes, self.graph_ranges, xmin, xmax)
        controller.set_delete_callback(self.remove_controller)
        self.controllers.append(controller)
        self.activeController = controller
    
    # That needs a fix doesn't work at all
    def on_motion(self, event):
        if self.activeController is None:
            return

        xmin = self.activeController.xmin
        xmax = self.activeController.xmax

        # Convert data coords to pixels
        xpix = event.x
        xmin_pix = self.sc.axes.transData.transform((xmin, 0))[0]
        xmax_pix = self.sc.axes.transData.transform((xmax, 0))[0]

        if abs(xpix - xmin_pix) < 8 or abs(xpix - xmax_pix) < 8:
            self.sc.fig.canvas.setCursor(Qt.SizeHorCursor)
        else:
            self.sc.fig.canvas.setCursor(Qt.ArrowCursor)

    def onPick(self, event):
        patch = event.artist
        for controller in self.controllers:
            if controller.containsPatch(patch):
                self.activeController = controller

                controller.patch.set_alpha(0.6)

                self.span.extents = (controller.model.min, controller.model.max)
                self.span.set_active(True)

                controller.widget.min.setText(str(controller.model.min))
                controller.widget.max.setText(str(controller.model.max))

            else:
                controller.patch.set_alpha(0.3)
                controller.patch.set_edgecolor("none")

        self.sc.draw_idle()

    def remove_controller(self, controller):
        controller.patch.remove()

        controller.widget.setParent(None)

        self.controllers.remove(controller)

        self.sc.draw_idle()