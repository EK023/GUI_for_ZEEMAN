import numpy as np
from matplotlib.widgets import SpanSelector
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PySide6.QtWidgets import (
    QWidget
)

from PySide6.QtCore import (
    Qt, Signal
)

from Controllers.RangeController import RangeController

class CustomToolbar(NavigationToolbar):
    toolitems = [
        ('Home', 'Reset view', 'home', 'home'),
        ('Pan', 'Pan axes', 'move', 'pan'),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
    ]

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

class PlotInteractionController(QWidget):
    openWaveRanges = Signal()
    DEFAULT_COLOR = (0.12, 0.5, 0.71, 0.3)
    ACTIVE_COLOR  = (0.12, 0.5, 0.71, 0.7)

    def __init__(self, plot_widget, graph_ranges):
        super().__init__()
        self.plot_widget = plot_widget
        self.graph_ranges = graph_ranges
        self.controllers = []
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
        self.openWaveRanges.emit()
        
        while self.plot_widget.layout().count():
            item = self.plot_widget.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.plot_widget.layout().addWidget(self.sc)
        self.plot_widget.layout().addWidget(NavigationToolbar(self.sc, self.plot_widget))

        self.activeController = None
        self.isDragging = False
        self.sc.fig.canvas.mpl_connect("button_release_event", lambda e: setattr(self, "isDragging", False))

        self.span = SpanSelector(
            self.sc.axes,
            self.onselect,
            "horizontal",
            useblit=False,
            grab_range=20, # Check if that helps anything....
            props=dict(alpha=0.3, facecolor="tab:blue"), # can change color 
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
             # If you select range then it activeController is practically immediately overridden to None and that breaks the logic
            return
        self.isDragging = True
        self.openWaveRanges.emit()
        if self.activeController is not None:
            self.reset_patch_colors()
            self.activeController.updatePatch(xmin, xmax)
            return

        # Otherwise → create a new range
        self.add_range(xmin, xmax)
    
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
        selected = None
        self.reset_patch_colors()

        # First: find which controller was picked
        for controller in self.controllers:
            if controller.containsPatch(patch):
                selected = controller
                break

        if selected:
            self.activeController = selected
            selected.patch.set_facecolor(self.ACTIVE_COLOR)
            selected.patch.set_edgecolor("tab:blue")

            self.span.extents = (selected.model.min, selected.model.max)
            self.span.set_active(True)

            selected.widget.min.setText(str(selected.model.min))
            selected.widget.max.setText(str(selected.model.max))
        else:
            self.activeController = None
            self.span.set_active(False)

        self.sc.draw_idle()

    def reset_patch_colors(self):
        for controller in self.controllers:
            controller.patch.set_facecolor(self.DEFAULT_COLOR)
            controller.patch.set_edgecolor("none")

    def remove_controller(self, controller):
        if self.activeController is controller:
            self.activeController = None
            self.span.set_active(False)
            self.span.extents = (0, 0)
            self.reset_patch_colors()

        controller.patch.remove()
        controller.widget.setParent(None)

        if controller in self.controllers:
            self.controllers.remove(controller)

        self.sc.draw_idle()

    def add_range(self, min_val, max_val, active=True):
        controller = RangeController(self.sc.axes, self.graph_ranges, min_val, max_val)
        controller.set_delete_callback(self.remove_controller)
        self.controllers.append(controller)
        if active:
            self.activeController = controller

    def clear_controllers(self):
        for controller in self.controllers:
            self.remove_controller(controller)

    def load_from_conf(self, range_list):
        self.controllers = []
        for min_val, max_val in range_list:
            controller = RangeController(self.sc.axes, self.graph_ranges, min_val, max_val)
            controller.set_delete_callback(self.remove_controller)
            self.controllers.append(controller)

    def get_ranges(self):
        return [controller.get() for controller in self.controllers]

    