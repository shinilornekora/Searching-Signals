from src.io.utils import openFileExplorerAndReturnFileName
from src.convert.utils import convert2Png
from src.state.images_state import add_images, clear_images, get_images
from src.ml.utils import process_slices

from PyQt5.QtCore import pyqtSlot
from src.Worker import Worker

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

import os

storage = os.path.join(os.path.dirname(__file__), '..', 'temp', 'images') 

import_completed = False

def export_task():
    hor = int(open("meta.txt", "r").readlines()[0])
    wer = int(open("meta.txt", "r").readlines()[1])
    process_slices(get_images(), wer, hor)

class PathHolder():
    def __init__(self) -> None:
        self.path = None
    
    def setPath(self, path):
        self.path = path
    
    def getPath(self):
        return self.path

pathHolder = PathHolder()

class ImportCompleted:
    def __init__(self) -> None:
        self.isImportCompleted = False
    
    def completeImport(self):
        self.import_completed = True
    
    def uncompleteImport(self):
        self.import_completed = False
    
    def isCompleted(self):
        return self.import_completed
    
importCompleted = ImportCompleted()

def import_task():
    clear_images()
    images, hor, wer = convert2Png(pathHolder.getPath(), storage)
    with open("meta.txt", "w") as meta : 
        meta.writelines([str(hor), "\n" + str(wer)])
    add_images(images)

import_worker = Worker(import_task)

def importCompleteHandler():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowIcon(QIcon("loop.png"))
    msg.setWindowTitle("Завершено")
    msg.setText("Импорт изображения завершен")
    msg.exec_()
    importCompleted.completeImport()

import_worker.task_done.connect(importCompleteHandler)

export_worker = Worker(export_task)

def exportCompleteHandler():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowIcon(QIcon("loop.png"))
    msg.setWindowTitle("Завершено")
    msg.setText("Экспорт XML и обработанного изображения завершен")
    msg.exec_()

export_worker.task_done.connect(exportCompleteHandler)

class CurrentBluePrintTypeHolder():
    class ImportExportHolder():
        def __init__(self, importWorker, exportWorker) -> None:
            self.importWorker = importWorker
            self.exportWorker = exportWorker
        
        def getExport(self):
            return self.exportWorker
        
        def getImport(self):
            return self.importWorker

    def __init__(self, optionWorkersHolders) -> None:
        self.optionWorkersHolders = optionWorkersHolders
        self.optionWorkersHolders = optionWorkersHolders
        self.option = 0

    def setCurrentOption(self, option):
        self.option = option

    def startImport(self):
        self.optionWorkersHolders[self.option].getImport().start()
    
    def startExport(self):
        self.optionWorkersHolders[self.option].getExport().start()

def not_selected_task():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowIcon(QIcon("loop.png"))
    msg.setWindowTitle("Тип чертежа не выбран")
    msg.setText("Вы еще не выбрали тип импортируемого чертежа")
    msg.exec_()

def blank_task():
    pass

notSelectedWorker = Worker(blank_task)
notSelectedWorker.task_done.connect(not_selected_task)

blueprintTypeHolderDict = [
    CurrentBluePrintTypeHolder.ImportExportHolder(notSelectedWorker, notSelectedWorker),
    CurrentBluePrintTypeHolder.ImportExportHolder(import_worker, export_worker)
]

bluePrintTypeHolder = CurrentBluePrintTypeHolder(blueprintTypeHolderDict)

@pyqtSlot()
def exportHandler():
    if (importCompleted.isCompleted()):
        bluePrintTypeHolder.startExport()
        return
    show_not_imported()

def show_not_imported():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowIcon(QIcon("loop.png"))
    msg.setWindowTitle("Чертеж еще не был импортирован")
    msg.setText("Вы еще не импортировали изображение или импорт еще не был завершен")
    msg.exec_()

@pyqtSlot()
def importHandler():
    importCompleted.uncompleteImport()
    path = openFileExplorerAndReturnFileName()
    if path == "" or path == None:
        return
    pathHolder.setPath(path)
    bluePrintTypeHolder.startImport()

def selectHandler(index): 
    bluePrintTypeHolder.setCurrentOption(index)
