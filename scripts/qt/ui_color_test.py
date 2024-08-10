import os
import sys

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QDialog

UI_FILE = f"{os.path.dirname(__file__)}/ui/transcription_main_window.ui"

class TranscriptorMain(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        self.cbox_model_type.addItems(
            ['tiny', 'base', 'small', 'medium', 'large'])

        self.btn_audio_file_browser.clicked.connect(
            self._btn_audio_file_browser)

        self._setup_or_transcription_toggle(0)

    def _btn_audio_file_browser(self) -> None:
        """ Prompts dialog for searching audio file on disk."""
        file_path, filter = QFileDialog.getOpenFileName(self, "Get Audio")

    def _setup_or_transcription_toggle(self, switch: int = 0) -> None:
        """ Allows the gui to be set between the setup and transcription state
        by disabling and enabling parts of the gui"""

        # print("switch", switch)

        def setup_section_toggle(switch: bool):
            self.ledit_audio_file_path.setEnabled(switch)
            self.btn_audio_file_browser.setEnabled(switch)
            self.ledit_export_dir_path.setEnabled(switch)
            self.btn_export_dir_browser.setEnabled(switch)
            self.cbox_model_type.setEnabled(switch)
            self.chkbox_eng_only.setEnabled(switch)
            self.label_audio_file_path.setEnabled(switch)
            self.label_export_dir_path.setEnabled(switch)
            self.label_model_type.setEnabled(switch)

        def transcription_section_toggle(switch: bool):
            self.ptedit_transcription.setEnabled(switch)
            self.btn_transcription_confirm.setEnabled(switch)
            self.btn_transcription_cancel.setEnabled(switch)
            self.label_transcription.setEnabled(switch)

        if switch == 0: # setup state
            setup_section_toggle(True)
            transcription_section_toggle(False)
        elif switch == 1: # transcription state
            setup_section_toggle(False)
            transcription_section_toggle(True)
        else: # ignore if switch is not 0 or 1
            pass


if __name__ == "__main__":
    from pathlib import Path
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('qss/dark.qss').read_text())

    window = TranscriptorMain()
    window.show()
    sys.exit(app.exec_())
