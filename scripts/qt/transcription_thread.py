import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from scripts.core.functions_transcriptor import transcribe


class TranscriptionThread(QThread):
    """ To prevent the heavy operation of transcribing the audio file into text
    freezing the main gui, the transcribe function is ran on a seperate thread.
    """
    output_ready = pyqtSignal(str)

    def __init__(self, audio_file_path, transcriber_model_type):
        super().__init__()
        self.audio_file_path = audio_file_path
        self.transcriber_model_type = transcriber_model_type

    def run(self):
        transcribed_text = transcribe(
            self.audio_file_path,
            self.transcriber_model_type)
        self.output_ready.emit(transcribed_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # set style
    thread = TranscriptionThread(
        "/home/ericnjkim/repo/transcription_tool/_mp3/2023_05_01.mp3",
        "tiny").start()
    print((thread))
    sys.exit(app.exec_())
