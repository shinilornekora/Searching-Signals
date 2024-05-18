from PyQt5.QtWidgets import QWidget, QVBoxLayout
from src.entities.label import makeLabel

def init(layout):
    textLayout = QVBoxLayout()
    textWidget = QWidget()

    status = makeLabel("Внимание!")
    text = makeLabel("Данные должны быть представлены в формате PDF.")

    textLayout.addWidget(status)
    textLayout.addWidget(text)
    textWidget.setLayout(textLayout)

    layout.addWidget(textWidget)