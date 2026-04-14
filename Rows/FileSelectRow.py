from PySide6.QtWidgets import (
    QHBoxLayout,
    QFileDialog,
    QPushButton,
    QLabel,
)
from Rows.BaseRow import BaseRow

import os

class FileSelectRow(BaseRow):
    def __init__(self, name, layout, row, filename  = "not selected", folder = False):
        super().__init__(name)

        self.parameter = name
        self.button = QPushButton(name)
        self.button.clicked.connect(self.selectFile if not folder else self.selectDirectory)
        self.fileName = filename
        shortenedFilename = filename.split("/")[-1]
        self.filePath = QLabel(shortenedFilename if len(shortenedFilename) < 20 else shortenedFilename[0:17] + "...")

        layout.addWidget(self.button, row , 0)
        layout.addWidget(self.filePath, row, 1, 1, 2)

    def get(self):
        return self.fileName 
    
    def set(self, filename):
        self.fileName = filename
        shortenedFilename = filename.split("/")[-1]
        self.filePath.setText(shortenedFilename if len(shortenedFilename) < 20 else shortenedFilename[0:17] + "...")
    
    def selectFile(self):
            global filename
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Choose a data file",
                "",
                "All Files (*);;Data Files (*.csv *.txt *.json)"
            )
            if filename:
                self.fileName = filename
                shortenedFilename = filename.split("/")[-1]
                self.filePath.setText(shortenedFilename if len(shortenedFilename) < 20 else shortenedFilename[0:17] + "...")
    
    def selectDirectory(self):
            global directory
            directory = QFileDialog.getExistingDirectory(
                self,
                "Choose a directory",
                ""
            )
            if directory:
                self.fileName = directory
                shortenedDirectory = directory.split("/")[-1]
                self.filePath.setText(shortenedDirectory if len(shortenedDirectory) < 20 else shortenedDirectory[0:17] + "...")