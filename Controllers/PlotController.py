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
    ACTIVE_COLOR  = (0.12, 0.5, 0.71, 0.5)
    EDGE_THRESHOLD = 6 # pixels

    def __init__(self, plot_widget, graph_ranges):
        super().__init__()
        self.plot_widget = plot_widget
        self.graph_ranges = graph_ranges
        self.controllers = []
        self.activeController = None
        self.dragMode = None
        self.isDragging = False
        self.clicked_empty_space = False

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
        self.toolbar = NavigationToolbar(self.sc, self.plot_widget)
        self.plot_widget.layout().addWidget(self.toolbar)

        self.activeController = None
        self.isDragging = False
        self.sc.fig.canvas.mpl_connect("button_release_event", lambda e: setattr(self, "isDragging", False))
        self.sc.fig.canvas.mpl_connect("button_press_event", self.on_press)

        self.span = SpanSelector(
            self.sc.axes,
            self.onselect,
            "horizontal",
            useblit=False,
            grab_range=self.EDGE_THRESHOLD, # Check if that helps anything....
            props=dict(facecolor=self.ACTIVE_COLOR), # can change color 
            interactive=True,
            handle_props={"mouseover":True},
            drag_from_anywhere=False
        )

        self.sc.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def on_press(self, event):
        self.ignoreNextSelect = False

        if event.dblclick:
            self.ignoreNextSelect = True
            return
        
        if event.x is None or event.xdata is None or event.inaxes != self.sc.axes:
            return
        
        xpix = event.x
        clicked_controller = None
        edge_hit = False

        # 1. Check if we clicked on the RESIZE EDGE of ANY existing controller
        for controller in self.controllers:
            cmin_pix = self.sc.axes.transData.transform((controller.xmin, 0))[0]
            cmax_pix = self.sc.axes.transData.transform((controller.xmax, 0))[0]
            
            if abs(xpix - cmin_pix) <= self.EDGE_THRESHOLD or abs(xpix - cmax_pix) <= self.EDGE_THRESHOLD:
                clicked_controller = controller
                edge_hit = True
                break

        # 2. If not an edge, check if we clicked dead-center INSIDE ANY existing controller
        if not clicked_controller:
            for controller in self.controllers:
                if controller.xmin <= event.xdata <= controller.xmax:
                    clicked_controller = controller
                    break

        if clicked_controller is not None:
            # Activate the controller we just hit
            self.clicked_empty_space = False
            self.set_active_controller(clicked_controller)
            
            if edge_hit:
                self.dragMode = "edit"
            else:
                self.dragMode = "create" 
            return

        # 3. Clicked completely empty space
        self.clicked_empty_space = True
        self.clear_selection()
        self.dragMode = "create"

    def set_active_controller(self, controller):
        if self.activeController == controller:
            return
            
        self.reset_patch_colors()
        self.activeController = controller
        
        controller.patch.set_facecolor(self.ACTIVE_COLOR)
        controller.patch.set_edgecolor("tab:blue")

        # Give the span selector the exact dimensions to take over for dragging
        self.span.extents = (controller.model.min, controller.model.max)
        self.span.set_active(True)

        if hasattr(controller, 'widget') and controller.widget:
            controller.widget.min.setText(str(controller.model.min))
            controller.widget.max.setText(str(controller.model.max))

        self.sc.draw_idle()
    
    def setupInteractions(self):
        ...
    
    def onselect(self, xmin, xmax):
        if getattr(self, "ignoreNextSelect", False):
            self.ignoreNextSelect = False
            return

        if xmin == xmax:
            if self.clicked_empty_space:
                self.clear_selection()
            elif self.activeController is not None:
                # If user just single-clicked the center, SpanSelector internally collapses to 0, here we restore it
                self.span.extents = (self.activeController.model.min, self.activeController.model.max)
                self.span.set_active(True)
            return
        
        
        if self.range_exists(xmin, xmax):
            return

        self.openWaveRanges.emit()

        if self.dragMode == "edit" and self.activeController is not None:
            self.reset_patch_colors()
            self.activeController.updatePatch(xmin, xmax)
            self.activeController.patch.set_facecolor(self.ACTIVE_COLOR)
            self.activeController.patch.set_edgecolor("tab:blue")
            return

        self.reset_patch_colors()
        self.add_range(xmin, xmax)
        self.activeController.patch.set_facecolor(self.ACTIVE_COLOR)
        self.activeController.patch.set_edgecolor("tab:blue")

    def range_exists(self, xmin, xmax, tol=1e-6):
        for controller in self.controllers:
            cmin, cmax = controller.get()
            if abs(cmin - xmin) < tol and abs(cmax - xmax) < tol:
                return True
        return False
    
    def clear_selection(self):
        self.activeController = None
        self.span.extents = (0, 0)
        self.reset_patch_colors()
        self.sc.fig.canvas.setCursor(Qt.ArrowCursor)
        self.sc.draw_idle()
    
    def on_motion(self, event):
        # doesn't interfere with matplotlib's pan or zoom tools
        if self.sc.widgetlock.locked():
            return
        
        if self.activeController is None or event.x is None or event.inaxes != self.sc.axes:
            if self.activeController is not None and self.activeController.patch.get_linewidth() != 0:
                self.sc.fig.canvas.setCursor(Qt.ArrowCursor)
                self.activeController.patch.set_linewidth(0)
                self.sc.draw_idle()
            return

        xmin = self.activeController.xmin
        xmax = self.activeController.xmax

        xpix = event.x
        xmin_pix = self.sc.axes.transData.transform((xmin, 0))[0]
        xmax_pix = self.sc.axes.transData.transform((xmax, 0))[0]

        near_left = abs(xpix - xmin_pix) <= self.EDGE_THRESHOLD
        near_right = abs(xpix - xmax_pix) <= self.EDGE_THRESHOLD

        if near_left or near_right:
            if self.activeController.patch.get_linewidth() != 3:
                self.sc.fig.canvas.setCursor(Qt.SizeHorCursor)
                self.activeController.patch.set_linewidth(3)
                self.sc.draw_idle()

        else:
            if self.activeController.patch.get_linewidth() != 0:
                self.sc.fig.canvas.setCursor(Qt.ArrowCursor)
                self.activeController.patch.set_linewidth(0)
                self.sc.draw_idle()

    def reset_patch_colors(self):
        for controller in self.controllers:
            controller.patch.set_facecolor(self.DEFAULT_COLOR)
            controller.patch.set_edgecolor("none")

    def remove_controller(self, controller):
        if self.activeController is controller:
            self.clear_selection()

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

    