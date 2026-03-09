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
        self._min = min_val
        self._max = max_val

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

    def get(self):
        return {
            "min": self._min,
            "max": self._max
        }