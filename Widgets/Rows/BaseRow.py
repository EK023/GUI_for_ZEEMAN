from PySide6.QtWidgets import (
    QWidget,

)

class BaseRow(QWidget):
    def __init__(self, name=None):
        super().__init__()
        self.name = name
        
    def get(self):
        raise NotImplementedError("Subclasses should implement this method")