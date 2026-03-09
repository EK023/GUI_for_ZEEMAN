from RangeFieldGroup import RangeFieldGroup
from SelectedRange import SelectedRange

class RangeController:
    def __init__(self, axes, layout, xmin, xmax):
        self.model = SelectedRange(xmin, xmax)

        # Create patch
        self.patch = axes.axvspan(
            xmin, xmax,
            alpha=0.2,
            picker=True,
            color="tab:blue"
        )

        # Create UI widget
        self.widget = RangeFieldGroup(self.model)
        layout.addWidget(self.widget)

        # Sync model → patch
        self.model.changed.connect(self.updatePatch)

    def updatePatch(self, new_min, new_max):
        self.patch.set_x(new_min) 
        self.patch.set_width(new_max - new_min)
        # self.model.min = new_min
        # self.model.max = new_max
        self.patch.figure.canvas.draw_idle()

    def containsPatch(self, patch):
        return patch is self.patch

    @property 
    def xmin(self): 
        return self.model.min 
    @property 
    def xmax(self): 
        return self.model.max

    
