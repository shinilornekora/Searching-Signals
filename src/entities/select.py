from PyQt5.QtWidgets import QComboBox

def makeSelect(cb, items):
    select = QComboBox()
    
    select.currentIndexChanged.connect(cb)
    select.addItems(items)
    select.setFixedSize(220, 40)
    select.setStyleSheet("""
        QComboBox {
            padding: 5px 15px;
            border: 1px solid gray;
            border-radius: 5px;
            font-size: 14px;
        }

        QComboBox:hover {
            background-color: rgba(221, 221, 221, 0.4);
        }
        
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: darkgray;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }

        QComboBox::down-arrow {
            image: url('./arrow.png');
            width: 10px;
            height: 10px;
        }

        QComboBox QAbstractItemView {
            width: calc(100% - 12px);
            border: 1px solid darkgray;
            selection-background-color: azure;
            selection-color: black;
            padding: 10px;
        }
    """)

    return select