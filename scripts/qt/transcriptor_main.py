import os
import sys

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication


UI_FILE = f"{os.path.dirname(__file__)}/ui/main.ui"

class TranscriptorMain(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        self.button_file_browser.clicked.connect(self.buttonFileBrowser)
        self.button_dir_browser.clicked.connect(self.buttonDirBrowser)
        self.button_transcribe.clicked.connect(self.buttonTranscribe)

        self.cbox_model_type.addItems(['tiny', 'base', 'small', 'medium', 'large'])
        self.model_type = self.cbox_model_type.currentText()

        self.cbox_model_type.activated.connect(self.cboxModelType)
        self._initGui()
        self._evaluateParams()