import sys
from PyQt5.QtWidgets import QFileDialog

def openFileExplorer(parent=None):
    options = QFileDialog.Options()
    file_name = QFileDialog.getOpenFileName()
    if file_name:
        print(file_name)