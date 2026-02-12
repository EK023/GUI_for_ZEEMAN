
# Copilot generated a class based on this not sure if it works correctly
# def attach_number_validator(self, line_edit: QLineEdit):
#         validator = QDoubleValidator() 
#         validator.setNotation(QDoubleValidator.StandardNotation) 
#         line_edit.setValidator(validator) 

#     # They work as spacers and if you click enter they are automatically removeed, it considers only the dot as real comma
#     # Not sure how big of a problem it is but allows inserting multiple "," every other check works (for example "1,1,1,1" is accepted)
#     def attach_number_tooltip(self, line_edit: QLineEdit): 
#         self.attach_number_validator(line_edit)
    
#         def event_filter(obj, event): 
#             if obj is line_edit and event.type() == QEvent.KeyPress: 
#                 before = line_edit.text() 
#                 result = QLineEdit.event(obj, event) 
#                 after = line_edit.text()
#                 if before == after and not event.text().isnumeric(): 
#                     QToolTip.showText( line_edit.mapToGlobal(QPoint(0, line_edit.height())), "Numbers only" ) 
#                     return result 
#                 elif after.count(",") + after.count(".") > 1: 
#                     QToolTip.showText( line_edit.mapToGlobal(QPoint(0, line_edit.height())), "Only one comma allowed" ) 
#                     line_edit.setText(before)
#                 return True 
    
#         line_edit.installEventFilter(line_edit) 
#         line_edit.eventFilter = event_filter


from PySide6.QtWidgets import QLineEdit, QToolTip
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import QEvent, QPoint


class NumericInput(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

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
