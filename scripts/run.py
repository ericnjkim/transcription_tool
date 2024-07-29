import sys

from scripts.qt.transcriptor_main import TranscriptorMain
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
# set style
window = TranscriptorMain()
window.show()
sys.exit(app.exec_())
