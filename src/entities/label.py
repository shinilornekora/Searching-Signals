from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

def makeLabel(text):
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet('font-size: 18px;')

    return label