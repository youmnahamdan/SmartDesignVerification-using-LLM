# ORIGINAL FILE
'''from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot

# Global pool
global_thread_pool = QThreadPool.globalInstance()

# Worker Signals
class WorkerSignals(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

# Generic Worker
class Worker(QRunnable):
    def __init__(self, fn, *args):
        super().__init__()
        self.fn = fn
        self.args = args
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))



def run_task_in_pool(func, callback, *args, error_callback=None):
    worker = Worker(func, *args)
    worker.signals.finished.connect(callback)
    if error_callback:
        worker.signals.error.connect(error_callback)
    global_thread_pool.start(worker)'''
    

# STOP SIGNAL
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from threading import Event

# Worker Signals
class WorkerSignals(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    cancelled = pyqtSignal()

# Generic Worker with Stop Support
class Worker(QRunnable):
    def __init__(self, fn, *args):
        super().__init__()
        self.fn = fn
        self.args = args
        self.signals = WorkerSignals()
        self._is_interrupted = False

    def stop(self):
        self._is_interrupted = True

    def is_stopped(self):
        return self._is_interrupted

    @pyqtSlot()
    def run(self):
        try:
            # pass a reference to the worker itself so the function can check if it should stop
            result = self.fn(*self.args)
            if not self._is_interrupted:
                self.signals.finished.emit(result)
            else:
                self.signals.cancelled.emit()
        except Exception as e:
            self.signals.error.emit(str(e))