from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QThread

def show_capture_key_dialog(obj, controller, callback, msg):
    # Create a dialog for capturing a key input
    key_dialog = QMessageBox()
    key_dialog.setContentsMargins(10,10,10,10)
    key_dialog.setStandardButtons(QMessageBox.Cancel)
    key_dialog.setDefaultButton(QMessageBox.Cancel)
    key_dialog.setText(msg)

    thread = QThread()
    obj.listener = KeyListener(controller)
    obj.listener.moveToThread(thread)
    thread.started.connect(obj.listener.run_task)
    obj.listener.finished.connect(key_dialog.reject)
    obj.listener.finished.connect(callback)
    thread.start()

    key_dialog.rejected.connect(obj.listener.disconnect)
    key_dialog.finished.connect(thread.quit)
    key_dialog.exec_()

class KeyListener(QObject):
    finished = pyqtSignal(str)

    def __init__ (self, controller):
        super().__init__()
        self.controller = controller

    def run_task(self):
        self.controller.keyListener.get_next_key(self.on_next_key)
        
        # Emit signal with result
    def on_next_key(self, key):
        self.finished.emit(key)