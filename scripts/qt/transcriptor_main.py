import os
import sys
from datetime import datetime

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication

from scripts.core.functions_transcriptor import transcribe, write_file
from scripts.core.functions_gui_state_save import save_ui_state, read_ui_state
from scripts.core.classes import UiState

UI_FILE = f"{os.path.dirname(__file__)}/ui/transcription_main_window_02.ui"

""" currently written with a push type method of having parameters update upon 
certain parameters being interacted with but could potentially be much
cleaner to work with a pull type method of only grabbing the parameter values
when they are queried for.
"""

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

    def closeEvent(self, event):
        """ Upon closing the gui, the current ui state is written out so the
        settings are remembered for the next time the gui is called.
        """
        param_dict = self._evaluate_params()
        ui_state = UiState(
            audio_file_path=param_dict["audio_file_path"],
            export_dir_path=param_dict["export_dir_path"],
            model_type=param_dict["cbox_model_type"],
            eng_only=param_dict["chkbox_eng_toggle"],
        )
        save_ui_state(ui_state)

    def _evaluate_params(self) -> dict:
        """ This runs whenever we need to access the current param values."""
        # rename the qt params when you can
        model_type = self.cbox_model_type.currentText()
        if self.chkbox_eng_only.isChecked() and model_type != "large":
            model_type += ".en"

        param_dict = {
            "audio_file_path": self.ledit_audio_file_path.text(),
            "export_dir_path": self.ledit_export_dir_path.text(),
            "model_type": model_type,
            # these two are for storing the raw value in the ui state json
            "cbox_model_type": self.cbox_model_type.currentText(),
            "chkbox_eng_toggle": self.chkbox_eng_only.isChecked(),
        }
        return param_dict

    def _btn_audio_file_browser(self) -> None:
        """ Prompts dialog for searching audio file on disk."""
        param_dict = self._evaluate_params()
        file_path, filter = QFileDialog.getOpenFileName(
            self, "Get Audio", param_dict["audio_file_path"])
        if file_path:
            self.ledit_audio_file_path.setText(file_path)

    def _btn_export_dir_browser(self) -> None:
        """ Prompts dialog for searching the export directory on disk."""
        param_dict = self._evaluate_params()
        dir_path = QFileDialog.getExistingDirectory(
            self, "Export Directory", param_dict["export_dir_path"])
        if dir_path:
            self.ledit_export_dir_path.setText(dir_path)

    def _btn_transcribe(self) -> None:
        """ Transcribes audio file and sets the transcription text window with
        the returned text.
        """
        param_dict = self._evaluate_params()
        transcribed_text = transcribe(
            param_dict["audio_file_path"],
            param_dict["model_type"])

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
        param_dict = self._evaluate_params()
        export_dir_path = param_dict["export_dir_path"]

        write_file(
            export_dir_path=export_dir_path,
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
    app = QApplication(sys.argv)
    # set style
    window = TranscriptorMain()
    window.show()
    sys.exit(app.exec_())
