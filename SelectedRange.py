# class SelectedRange:
#     def __init__(self, min, max):
#         self.min = min
#         self.max = max

#     def get(self):
#         return {
#             [self.min, self.max]
#         }

from PySide6.QtCore import QObject, Signal

class SelectedRange(QObject):
    changed = Signal(float, float)

    def __init__(self, min_val=0.0, max_val=0.0):
        super().__init__()
        self._min = round(min_val, 2)
        self._max = round(max_val, 2)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self._min = value
        self.changed.emit(self._min, self._max)

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value
        self.changed.emit(self._min, self._max)

    def set_silent(self, new_min, new_max):
        self.blockSignals(True)
        self._min = new_min
        self._max = new_max
        self.blockSignals(False)


    def get(self):
        return {
            "min": self._min,
            "max": self._max
        }