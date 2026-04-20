from Rows.RangeRow import RangeRow
from Models.SelectedRange import SelectedRange

class RangeController:
    def __init__(self, axes, layout, xmin, xmax):
        self.model = SelectedRange(xmin, xmax)

        self.patch = axes.axvspan(
            xmin, xmax,
            alpha=0.2,
            picker=True,
            color="tab:blue"
        )

        layout.takeAt(layout.count()-1)
        self.widget = RangeRow(self.model)
        layout.addWidget(self.widget)
        layout.addStretch()

        self.model.changed.connect(self.updatePatch)

        self.widget.deleteRequest.connect(self._handle_delete)

        self._delete_callback = None

    def updatePatch(self, new_min, new_max):
        rounded_min = round(new_min, 2)
        rounded_max = round(new_max, 2)

        self.patch.set_x(new_min) 
        self.patch.set_width(new_max - new_min)

        self.widget.min.setText(str(rounded_min))
        self.widget.max.setText(str(rounded_max))
        
        self.model.set_silent(rounded_min, rounded_max)
        self.patch.figure.canvas.draw_idle()

    def containsPatch(self, patch):
        return patch is self.patch
    
    def set_delete_callback(self, callback):
        self._delete_callback = callback

    def _handle_delete(self):
        if self._delete_callback:
            self._delete_callback(self)

    @property 
    def xmin(self): 
        return self.model.min 
    @property 
    def xmax(self): 
        return self.model.max

    def get(self):
        return [self.model.min, self.model.max]

    
