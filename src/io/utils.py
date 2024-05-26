import sys
from PyQt5.QtWidgets import QFileDialog

def openFileExplorerAndReturnFileName(parent=None):
    options = QFileDialog.Options()
    result = QFileDialog.getOpenFileName(parent, "Open File", "", "PDF Files (*.pdf)", options=options)
    return result[0]