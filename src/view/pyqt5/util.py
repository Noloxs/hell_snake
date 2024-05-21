from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
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

class DropdownDialog(QDialog):
    def __init__(self, items_dict, callback):
        super().__init__()

        self.items_dict = items_dict
        self.callback = callback
        self.setWindowTitle("Select an Item")
        self.resize(300, 100)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Add a label
        label = QLabel("Please select an item:")
        layout.addWidget(label)

        # Create and populate the dropdown menu
        self.combo_box = QComboBox()
        self.combo_box.addItems(self.items_dict.values())
        layout.addWidget(self.combo_box)

        # Create the OK button
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.on_ok_clicked)
        button_layout.addWidget(ok_button)
        
        # Optionally add a Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_ok_clicked(self):
        selected_value = self.combo_box.currentText()
        selected_key = None

        # Find the corresponding key for the selected value
        for key, value in self.items_dict.items():
            if value == selected_value:
                selected_key = key
                break
        
        if selected_key is not None:
            self.callback(selected_key)
        
        self.accept()