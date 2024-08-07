import os
import sys
from datetime import datetime

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QDialog

from scripts.core.functions_transcriptor import transcribe, write_file
from scripts.core.functions_gui_state_save import save_ui_state, read_ui_state
from scripts.core.classes import UiState

from scripts.qt.message_dialog import MessageDialog
from scripts.qt.transcription_thread import TranscriptionThread

UI_FILE = f"{os.path.dirname(__file__)}/ui/transcription_main_window_02.ui"

""" currently written with a push type method of having parameters update upon 
certain parameters being interacted with but could potentially be much
cleaner to work with a pull type method of only grabbing the parameter values
when they are queried for.
"""

# wip
# add some cleanup for the ui state class to allow for the +".en" operation more smoothly and confirm it stores bool instead of a string when pulling from a json

class TranscriptorMain(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)
        # setup operations
        self.cbox_model_type.addItems(
            ['tiny', 'base', 'small', 'medium', 'large'])
        self.btn_audio_file_browser.clicked.connect(
            self._btn_audio_file_browser)
        self.btn_export_dir_browser.clicked.connect(
            self._btn_export_dir_browser)
        self.btn_transcribe.clicked.connect(self._btn_transcribe)
        self.btn_transcription_confirm.clicked.connect(
            self._btn_transcription_confirm)
        self.btn_transcription_cancel.clicked.connect(
            self._btn_transcription_cancel)

        self.transcription_thread = TranscriptionThread("", "")
        self.transcription_thread.output_ready.connect(self._on_transcription)

        self._setup_or_transcription_toggle(0)
        self._get_ui_state()
        self.datetime = ""

    def _get_ui_state(self):
        """ When opening the gui, checks for a previous ui state and load it if
        there is.
        """
        ui_state = read_ui_state()
        # print(ui_state)
        self.ledit_audio_file_path.setText(ui_state.audio_file_path)
        self.ledit_export_dir_path.setText(ui_state.export_dir_path)
        self.cbox_model_type.setCurrentText(ui_state.model_type)
        self.chkbox_eng_only.setChecked(ui_state.eng_only)

    def _evaluate_current_ui_state(self) -> UiState:
        """ Turns the gui's current set of parameters into a UiState object."""
        ui_state = UiState(
            audio_file_path=self.ledit_audio_file_path.text(),
            export_dir_path=self.ledit_export_dir_path.text(),
            model_type=self.cbox_model_type.currentText(),
            eng_only=self.chkbox_eng_only.isChecked(),
        )
        return ui_state

    def closeEvent(self, event):
        """ Upon closing the gui, the current ui state is written out so the
        settings are remembered for the next time the gui is called.
        """
        ui_state = self._evaluate_current_ui_state()
        save_ui_state(ui_state)

    def _btn_audio_file_browser(self) -> None:
        """ Prompts dialog for searching audio file on disk."""
        ui_state = self._evaluate_current_ui_state()
        file_path, filter = QFileDialog.getOpenFileName(
            self, "Get Audio", ui_state.audio_file_path)
        if file_path:
            self.ledit_audio_file_path.setText(file_path)

    def _btn_export_dir_browser(self) -> None:
        """ Prompts dialog for searching the export directory on disk."""
        ui_state = self._evaluate_current_ui_state()
        dir_path = QFileDialog.getExistingDirectory(
            self, "Export Directory", ui_state.export_dir_path)
        if dir_path:
            self.ledit_export_dir_path.setText(dir_path)

    def _btn_transcribe(self) -> None:
        """ Transcribes audio file and sets the transcription text window with
        the returned text.
        """
        ui_state = self._evaluate_current_ui_state()
        transcriber_model_type = ui_state.model_type
        # check eng only is a bool
        if ui_state.eng_only: # and ui_state.model_type != "large":
            transcriber_model_type += ".en"

        if not ui_state.check_parameters_valid():
            msg = ("One or more input path not valid."
                   "\nCheck all parameters exist and paths are valid.")
            dlg = MessageDialog(msg)
            dlg.exec()
            return None # end operation early if this condition is met

        self.transcription_thread.audio_file_path = ui_state.audio_file_path
        self.transcription_thread.transcriber_model_type = transcriber_model_type
        self.transcription_thread.start()

    def _on_transcription(self, transcribed_text):
        """ This function is a continuation of hte _btn_transcribe() and is
        split like this so a Qthread can take the load of the transcribe
        function and prevent a gui freeze.
        """
        # adds current datetime to the top of the transcription
        self.datetime = datetime.now().strftime("%Y-%m-%d_%A_%H%M%S")
        transcribed_text = f"{self.datetime}\n\n{transcribed_text}"
        self.ptedit_transcription.setPlainText(transcribed_text)
        self._setup_or_transcription_toggle(1)

    # ___editing the transcription___
    def _btn_transcription_confirm(self) -> None:
        """ Runs the operations for writing out the transcription once the text
        has been checked and confirmed as correct.
        """
        ui_state = self._evaluate_current_ui_state()

        write_file(
            export_dir_path=ui_state.export_dir_path,
            text=self.ptedit_transcription.toPlainText(),
            name=f"Transcription_{self.datetime}")
        # self.ptedit_transcription.clear()
        self._setup_or_transcription_toggle(0)

    def _btn_transcription_cancel(self) -> None:
        """ Runs the operations for writing out the transcription once the text
        has been checked and confirmed as correct.
        """
        self.ptedit_transcription.clear()
        self._setup_or_transcription_toggle(0)

    def _setup_or_transcription_toggle(self, switch: int=0) -> None:
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
