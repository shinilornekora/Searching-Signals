from PyQt5.QtWidgets import QPushButton

def makeButton(cb, text):
    button = QPushButton(text)
    button.setFixedSize(200, 40)
    button.clicked.connect(cb)
    button.setStyleSheet("""
        QPushButton {
            border: 1px solid gray; 
            border-radius: 5px; 
            background-color: rgba(221, 221, 221, 0.1);
            font-size: 14px;
        }
          
        QPushButton:hover {
            background-color: rgba(221, 221, 221, 0.4);
        }
    """)

    return button