from PyQt5.QtWidgets import QWidget, QHBoxLayout
from src.handlers import exportHandler, importHandler, selectHandler
from src.entities.button import makeButton 
from src.entities.select import makeSelect

def init(layout):
    functionalWidget = QWidget()
    functionalLayout = QHBoxLayout()

    importButton = makeButton(importHandler, "Импортировать данные")
    exportButton = makeButton(exportHandler, "Экспортировать XML")
    selectBlueprintType = makeSelect(selectHandler, ["Укажите тип чертежа", "Чертеж - Ж/Д станция"])

    functionalLayout.addWidget(importButton)
    functionalLayout.addWidget(exportButton)
    functionalLayout.addWidget(selectBlueprintType)
    functionalWidget.setLayout(functionalLayout)

    layout.addWidget(functionalWidget)