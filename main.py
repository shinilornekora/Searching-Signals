from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from src.widgets.functional import init as makeFunctionalLayout
from src.widgets.static import init as makeStaticLayout
from PyQt5.QtGui import QIcon
from sys import exit, argv

def makeLayout(layout):
    makeStaticLayout(layout)
    makeFunctionalLayout(layout)

def init():
    app = QApplication(argv)
    layout = QVBoxLayout()
    window = QWidget()

    window.resize(760, 300)
    window.move(500, 500)
    window.setWindowIcon(QIcon('./loop.png'))
    window.setWindowTitle('Поиск сигналов')

    makeLayout(layout)

    window.setLayout(layout)
    window.setStyleSheet('background-color: white;')
    window.show()

    exit(app.exec())

if __name__ == '__main__':
    init()