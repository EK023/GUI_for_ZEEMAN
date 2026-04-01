from PySide6.QtWidgets import QLineEdit, QToolTip
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import QEvent, QPoint

class NumericInput(QLineEdit):
    def __init__(self, nr=0.0, parent=None):
        super().__init__(parent)
        self.setText(str(nr))

        # Set up the validator
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.setValidator(validator)

        # Install event filter on itself
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self and event.type() == QEvent.KeyPress:
            before = self.text()
            result = super().event(event)
            after = self.text()
            if before == after and not event.text().isnumeric():
                QToolTip.showText(
                    self.mapToGlobal(QPoint(0, self.height())),
                    "Numbers only"
                )
                return result
            if after.count(",") + after.count(".") > 1:
                QToolTip.showText(
                    self.mapToGlobal(QPoint(0, self.height())),
                    "Only one comma allowed"
                )
                self.setText(before)
                return True

            return True

        return super().eventFilter(obj, event)

    def value(self):
        text = self.text().replace(",", ".")
        return float(text) if text else None
