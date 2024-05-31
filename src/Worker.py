from PyQt5.QtCore import QThread, pyqtSignal


class Worker(QThread):
    task_done = pyqtSignal(str)

    def __init__ (self, task, *args, **kwargs):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        print("started")
        result = self.task(*self.args, **self.kwargs)
        self.task_done.emit(result)

