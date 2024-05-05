from src.view_base import BaseView
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QMainWindow, QAction, QFileDialog, QHBoxLayout,QVBoxLayout, QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QLabel, QComboBox, QPushButton, QMenuBar, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QEvent, QSize, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeySequence, QColor
from PyQt5.QtSvg import QSvgWidget
from PyQt5.Qt import QSizePolicy
from src.strategem import Strategem
from src.executer_arduino import ArduinoPassthroughExecuter
from copy import deepcopy
from src import constants

class PyQT5View(BaseView):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.gui = QApplication([])
        self.window = MainWindow(controller)
    
    def add_executor_settings(self, executor):
        self.window.add_executor_settings(executor)

    def show_interface(self):
        self.window.show()
        self.gui.exec()
    
    def update_macros(self):
        self.window.update_macros()
    
    def update_current_loadout(self):
        self.window.update_current_loadout()
        self.window.update_macros()

    def update_armed(self):
        self.window.update_armed()
    
    def on_loadout_changed(self):
        self.window.update_loadout_menu_items()


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Hell snake")
        self.setWindowIcon(QIcon(constants.ICON_BASE_PATH+"hell_snake.png"))
        self.setMinimumSize(350, 225)
        self.resize(350,225)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white")
        self.vBox = QVBoxLayout()
        self.vBox.setSpacing(0)
        self.vBox.setContentsMargins(0,0,0,0)
        central_widget.setLayout(self.vBox)
        self.setCentralWidget(central_widget)

        self.hBox = QHBoxLayout()
        self.hBox.setContentsMargins(0,5,0,0)
        self.armedIcon = QLabel()
        self.armedIcon.setFixedSize(70, 70)
        self.armedIcon.setMargin(5)
        self.armedIcon.setAlignment(Qt.AlignCenter)
        self.armedIcon.setScaledContents(True)
        self.hBox.addWidget(self.armedIcon)

        self.loadout = QLabel()
        self.loadout.setFixedHeight(70)
        self.loadout.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        font = QFont("Arial", 24)
        font.setBold(True)
        self.loadout.setFont(font)
        self.hBox.addWidget(self.loadout)
        self.vBox.addLayout(self.hBox)

        self.armedBar = QLabel()
        self.armedBar.setFixedHeight(10)
        self.vBox.addWidget(self.armedBar)

        self.listwidget = QListWidget()
        self.listwidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.listwidget.setFocusPolicy(Qt.NoFocus)
        self.listwidget.itemClicked.connect(self.on_macro_clicked)
        self.vBox.addWidget(self.listwidget)

        self.setup_toolbar_menu()
        self.update_armed()
    
    def on_strategem_selected(self, key, id):
        self.controller.update_macro_binding(key, id)

    def on_macro_clicked(self, item):
        dialog = FilteredListDialog(self.controller, item.data(Qt.UserRole), self.on_strategem_selected)
        dialog.exec_()

    def update_macros(self):
        self.listwidget.clear()

        for index, (key, value) in enumerate(self.controller.model.macros.items()):
            listAdapter = QLoadoutListAdapter()
            listAdapter.setKey(key)
            listAdapter.setStyleSheet("background-color: transparent")
            listAdapter.setStrategem(value)

            listAdapterItem = QListWidgetItem(self.listwidget)
            listAdapterItem.setData(Qt.UserRole,key)
            listAdapterItem.setSizeHint(listAdapter.sizeHint())
            self.listwidget.addItem(listAdapterItem)
            self.listwidget.setItemWidget(listAdapterItem, listAdapter)

        height = 115 + (len(self.controller.model.macros)*55)
        self.resize(self.geometry().width(), height)

    def update_armed(self):
        if self.controller.model.isArmed:
            self.armedIcon.setPixmap(QPixmap(constants.ICON_BASE_PATH+"armed.png"))
            self.armedBar.setStyleSheet("background-color: red")
        else: 
            self.armedIcon.setPixmap(QPixmap(constants.ICON_BASE_PATH+"disarmed.png"))     
            self.armedBar.setStyleSheet("background-color: gray")
    
    def update_current_loadout(self):
        currentLoadout = self.controller.model.currentLoadout
        if currentLoadout is not None:
            self.loadout.setText(currentLoadout.name) 
        else:
            self.loadout.setText("")

    def setup_toolbar_menu(self):
        # Create a Files menu
        files_menu = self.menuBar().addMenu("Files")

        settingsOptions = files_menu.addMenu(QIcon(constants.ICON_BASE_PATH+"settings.svg"), "Settings")

        print_action = QAction(QIcon(constants.ICON_BASE_PATH+"settings_print.svg"), "Print settings", self)
        print_action.triggered.connect(self.controller.print_settings)
        settingsOptions.addAction(print_action)

        save_action = QAction(QIcon(constants.ICON_BASE_PATH+"settings_save.svg"), "Save settings", self)
        save_action.triggered.connect(self.controller.save_settings)
        settingsOptions.addAction(save_action)

        files_menu.addSeparator()

        exit_action = QAction(QIcon(constants.ICON_BASE_PATH+"exit.svg"),"Exit", self)
        exit_action.triggered.connect(self.controller.exit)
        files_menu.addAction(exit_action)

        arm_action = QAction("Arm", self)
        arm_action.triggered.connect(self.controller.toggle_armed)
        self.menuBar().addAction(arm_action)

        self.loadout_menu = self.menuBar().addMenu("Loadouts")
        self.update_loadout_menu_items()
    
    def update_loadout_menu_items(self):
        self.loadout_menu.clear()
        for loadoutId, loadout in self.controller.model.settings.loadouts.items():
            loadout_action = QAction(loadout.name, self)
            loadout_action.triggered.connect(lambda checked, loadoutId=loadoutId: self.controller.set_active_loadout(loadoutId))
            self.loadout_menu.addAction(loadout_action)
        
        self.loadout_menu.addSeparator()

        loadout_edit_action = QAction(QIcon(constants.ICON_BASE_PATH+"edit_loadout.svg"), "Edit loadouts", self)
        loadout_edit_action.triggered.connect(self.open_edit_loadout_dialog)
        self.loadout_menu.addAction(loadout_edit_action)

    def add_executor_settings(self, executor):
        if isinstance(executor,ArduinoPassthroughExecuter):
            select_serial = self.menuBar().addMenu("Select serial")

            physical_addresses = executor.get_physical_addresses()
            for port, desc, hwid in sorted(physical_addresses):
                serial = QAction(desc, self)
                serial.triggered.connect(lambda checked, port=port: executor.connect_to_arduino(port))
                select_serial.addAction(serial)
    
    def open_edit_loadout_dialog(self):
        dialog = EditLoadoutDialog(self.controller)
        dialog.exec_()

class QLoadoutListAdapter(QWidget):
    def __init__ (self, parent = None):
        super(QLoadoutListAdapter, self).__init__(parent)

        self.hBox  = QHBoxLayout()
        self.hBox.setContentsMargins(5,5,5,0)
        
        self.icon = QLabel()
        self.icon.setFixedSize(50, 50)
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setStyleSheet("background-color: #ff1f2832")
        self.hBox.addWidget(self.icon)
        
        self.key = QLabel()
        self.key.setFixedSize(50, 50)
        self.key.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 24)
        font.setBold(True)
        self.key.setFont(font)
        self.hBox.addWidget(self.key)
        
        self.name = QLabel()
        self.name.setFixedHeight(50)
        self.hBox.addWidget(self.name)
           
        self.setLayout(self.hBox)

    def setStrategem(self, strategem):
        self.name.setText(strategem.name)
        svg_widget = QSvgWidget(constants.STRATEGEM_ICON_PATH+strategem.icon_name)
        svg_widget.setFixedSize(40,40)
        svg_widget.setStyleSheet("background-color: transparent")
        self.icon.setPixmap(svg_widget.grab())  
    
    def setKey(self, key):
        self.id = key
        self.key.setText(key)

class FilteredListDialog(QDialog):
    def __init__(self, controller, key, callback = None):
        super().__init__()
        self.callback = callback
 
        self.controller = controller
        self.key = key
        self.setMinimumSize(300, 300)
        self.resize(300,800)

        self.setWindowTitle("Select new strategem for: "+self.key)
        self.setWindowIcon(QIcon(constants.ICON_BASE_PATH+"hell_snake.png"))

        # Create a layout for the dialog
        layout = QVBoxLayout(self)

        # Create an edit field
        self.edit_field = QLineEdit()
        self.edit_field.setPlaceholderText("Search...")
        self.edit_field.textChanged.connect(self.update_macros)
        layout.addWidget(self.edit_field)

        # Create a QListWidget for the list of items
        # TODO On tab, the first item isn't selected
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.installEventFilter(self)
        layout.addWidget(self.list_widget)

        # Populate the QListWidget with items
        self.update_macros("")
    
    def eventFilter(self, watched, event):
        if event.type() == QEvent.KeyPress and event.matches(QKeySequence.InsertParagraphSeparator):
            i = self.list_widget.selectedItems()
            if(len(i) > 0):
                self.on_item_clicked(i[0])
                return True
        
        return False

    def on_item_clicked(self, item):
        id = item.data(Qt.UserRole)
        self.callback(self.key, id)
        self.close()

    def filter_strategems(self, filter_text):
        filtered_list = {}
        for id, strategem in self.controller.model.strategems.items():
            if filter_text in strategem.name.lower():
                filtered_list.update({id:strategem})

        return filtered_list
    
    def sort_strategems(self, strategemDict):
        return dict(sorted(strategemDict.items(), key=lambda value:(value[1].category, value[1].name)))

    def update_macros(self, text):
        # Clear the current items in the QListWidget
        self.list_widget.clear()

        # Filter and sort items
        strategem_list = self.filter_strategems(text)
        strategem_list = self.sort_strategems(strategem_list)

        # Add all items to the QListWidget
        for id, strategem in strategem_list.items():
            listAdapter = QFilterListAdapter()
            listAdapter.setStyleSheet("background-color: transparent")
            listAdapter.setStrategem(strategem)

            listAdapterItem = QListWidgetItem(self.list_widget)
            listAdapterItem.setData(Qt.UserRole, id)
            listAdapterItem.setSizeHint(listAdapter.sizeHint())
            self.list_widget.addItem(listAdapterItem)
            self.list_widget.setItemWidget(listAdapterItem, listAdapter)
        self.list_widget.setCurrentRow(0)

class QFilterListAdapter(QWidget):
    def __init__ (self, parent = None):
        super(QFilterListAdapter, self).__init__(parent)

        self.hBox  = QHBoxLayout()
        self.hBox.setContentsMargins(5,5,5,0)

        self.icon = QLabel()
        self.icon.setFixedSize(25, 25)
        self.icon.setStyleSheet("background-color: #ff1f2832")
        self.icon.setAlignment(Qt.AlignCenter)
        self.hBox.addWidget(self.icon)
        
        self.name = QLabel()
        self.name.setFixedHeight(25)
        self.hBox.addWidget(self.name)
           
        self.setLayout(self.hBox)

    def setStrategem(self, strategem):
        self.name.setText(strategem.name)
        svg_widget = QSvgWidget(constants.STRATEGEM_ICON_PATH+strategem.icon_name)
        svg_widget.setFixedSize(20,20)
        svg_widget.setStyleSheet("background-color: transparent")
        self.icon.setPixmap(svg_widget.grab())

class EditLoadoutDialog(QDialog):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        
        self.setWindowTitle("Edit loadouts")
        self.setWindowIcon(QIcon(constants.ICON_BASE_PATH+"hell_snake.png"))
        self.setMinimumSize(300, 300)
        self.resize(300,600)

        iconSize = QSize(30, 30)
        # Layout
        layout = QVBoxLayout(self)

        # Dropdown selector
        self.dropdown = QComboBox()
        self.set_loadout_dropdown_items()
        layout.addWidget(self.dropdown)

        loadout_buttons_layout = QHBoxLayout()
        loadout_buttons_layout.setContentsMargins(0,10,0,0)

        # Edit field
        self.edit_field = QLineEdit()
        self.edit_field.setFixedHeight(30)
        self.edit_field.textChanged.connect(self.on_loadout_name_changed)
        loadout_buttons_layout.addWidget(self.edit_field)

        delete_loadout_button = QPushButton("")
        delete_loadout_button.setIcon(QIcon(constants.ICON_BASE_PATH+"settings_delete"))
        delete_loadout_button.setFixedSize(30,30)
        delete_loadout_button.clicked.connect(self.delete_current_loadout)
        loadout_buttons_layout.addWidget(delete_loadout_button)
        layout.addLayout(loadout_buttons_layout)

        # List widget
        self.list_widget = QListWidget()
        self.list_widget.model().rowsMoved.connect(self.macro_rearranged)
        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)
        layout.addWidget(self.list_widget)

        # Create macro control buttons
        buttons_layout = QHBoxLayout()
        
        delete_button = QPushButton("")
        delete_button.setIcon(QIcon(constants.ICON_BASE_PATH+"settings_delete"))
        delete_button.setIconSize(iconSize)
        delete_button.clicked.connect(self.delete_current_macro)
        buttons_layout.addWidget(delete_button)
        
        change_button = QPushButton("")
        change_button.setIcon(QIcon(constants.ICON_BASE_PATH+"settings_swap"))
        change_button.setIconSize(iconSize)
        change_button.clicked.connect(self.change_current_macro)
        buttons_layout.addWidget(change_button)

        add_button = QPushButton("")
        add_button.setIcon(QIcon(constants.ICON_BASE_PATH+"settings_add"))
        add_button.setIconSize(iconSize)
        add_button.clicked.connect(self.add_macro)
        buttons_layout.addWidget(add_button)

        layout.addLayout(buttons_layout)

        # Create confirmation buttons
        confirm_buttons_layout = QHBoxLayout()
        margin = confirm_buttons_layout.setContentsMargins(0,30,0,0)
        layout.addLayout(confirm_buttons_layout)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_save = QPushButton("Save")
        confirm_buttons_layout.addStretch(1)
        confirm_buttons_layout.addWidget(self.btn_cancel)
        confirm_buttons_layout.addWidget(self.btn_save)

        self.btn_cancel.clicked.connect(self.close)
        self.btn_save.clicked.connect(self.update_loadout)
        self.dropdown.currentIndexChanged.connect(self.set_loadout)

        # Menu bar
        menu_bar = QMenuBar()
        add_loadout_action = QAction("Add Loadout", self)
        add_loadout_action.triggered.connect(self.add_loadout)
        menu_bar.addAction(add_loadout_action)

        layout.setMenuBar(menu_bar)

        self.set_loadout()
    
    def delete_current_macro(self):
        macro = self.list_widget.currentItem()
        if macro != None:
            key = macro.data(Qt.UserRole)
            self.editLoadout.macroKeys.pop(key)
            self.update_macros()
    
    def change_current_macro(self):
        currentMacro = self.list_widget.currentItem()
        if currentMacro is not None:
            key = currentMacro.data(Qt.UserRole)
            dialog = FilteredListDialog(self.controller, key, self.on_strategem_selected)
            dialog.exec_()
    
    def on_strategem_selected(self, key, id):
        self.editLoadout.macroKeys[key] = id
        self.update_macros()

    def on_next_key(self, key):
        self.add_macro_box.close()
        self.thread.quit()
        if key not in self.editLoadout.macroKeys:
            self.editLoadout.macroKeys.update({key:"0"})
            self.update_macros()

    def start_task(self):
        self.thread = QThread()
        self.worker = Worker(self.controller)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_task)
        self.worker.finished.connect(self.on_next_key)
        self.thread.start()

    def add_macro(self):
        # Create a QMessageBox
        self.start_task()
        self.add_macro_box = QMessageBox()
        self.add_macro_box.setText("Press key for new macro")
        self.add_macro_box.exec_()

    def macro_rearranged(self, parent, start, end, destination, row):
        key = self.list_widget.currentItem().data(Qt.UserRole)
        row = self.list_widget.currentRow()

    def update_loadout(self):
        if self.loadoutId is not None:
            before = deepcopy(self.editLoadout.macroKeys)
            self.editLoadout.macroKeys.clear()
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                key = item.data(Qt.UserRole)
                strategemId = before[key]
                self.editLoadout.macroKeys.update({key:strategemId})

            self.controller.update_loadout(self.loadoutId, self.editLoadout)
            self.dropdown.setItemText(self.dropdown.currentIndex(), self.editLoadout.name)

    def add_loadout(self):
        loadoutName, ok = QInputDialog.getText(self, "Add Loadout", "Enter loadout name:")
        if ok:
            self.controller.add_loadout(loadoutName)
            self.set_loadout_dropdown_items()
            self.dropdown.setCurrentIndex(self.dropdown.count() - 1)
    
    def delete_current_loadout(self):
        if self.loadoutId is not None:
            self.controller.delete_loadout(self.loadoutId)
            self.set_loadout_dropdown_items()

    def set_loadout_dropdown_items(self):
        self.dropdown.clear()
        for id, loadout in self.controller.model.settings.loadouts.items():
            self.dropdown.addItem(loadout.name, id)
        if self.dropdown.count() > 0:
            self.dropdown.setCurrentIndex(0)
        else:
            self.set_loadout()

    def set_loadout(self):
        self.loadoutId = self.dropdown.currentData()
        if self.loadoutId == None:
            self.edit_field.setText("")
            self.editLoadout = None
            self.update_macros()
            return
        
        self.editLoadout = deepcopy(self.controller.model.settings.loadouts[self.loadoutId])
        self.edit_field.setText(self.editLoadout.name)
        self.update_macros()

    def update_macros(self):
        # Update list widget based on selected item
        self.list_widget.clear()
        # Add all items to the QListWidget
        self.editMacros = {}
        if self.editLoadout is not None:
            for key, strategemId in self.editLoadout.macroKeys.items():
                self.editMacros.update({key:self.controller.model.strategems[strategemId]})

        for index, (key, value) in enumerate(self.editMacros.items()):
            listAdapter = QEditLoadoutListAdapter()
            listAdapter.setStyleSheet("background-color: transparent")
            listAdapter.setStrategem(value)
            listAdapter.setKey(key)

            listAdapterItem = QListWidgetItem(self.list_widget)
            listAdapterItem.setData(Qt.UserRole,key)
            listAdapterItem.setSizeHint(listAdapter.sizeHint())
            self.list_widget.addItem(listAdapterItem)
            self.list_widget.setItemWidget(listAdapterItem, listAdapter)

    def on_loadout_name_changed(self, name):
        self.editLoadout.name = name

class Worker(QObject):
    finished = pyqtSignal(str)

    def __init__ (self, controller):
        super().__init__()
        self.controller = controller

    def run_task(self):
        self.controller.keyListener.get_next_key(self.on_next_key)
        
        # Emit signal with result
    def on_next_key(self, key):
        self.finished.emit(key)

class QEditLoadoutListAdapter(QWidget):
    def __init__ (self, parent = None):
        super(QEditLoadoutListAdapter, self).__init__(parent)

        self.hBox  = QHBoxLayout()
        self.hBox.setContentsMargins(5,5,5,0)
        
        self.icon = QLabel()
        self.icon.setFixedSize(25, 25)
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setStyleSheet("background-color: #ff1f2832")
        self.hBox.addWidget(self.icon)
        
        self.key = QLabel()
        self.key.setFixedSize(25, 25)
        self.key.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 18)
        font.setBold(True)
        self.key.setFont(font)
        self.hBox.addWidget(self.key)
        
        self.name = QLabel()
        self.name.setFixedHeight(25)
        self.hBox.addWidget(self.name)
           
        self.setLayout(self.hBox)

    def setStrategem(self, strategem):
        self.name.setText(strategem.name)
        svg_widget = QSvgWidget(constants.STRATEGEM_ICON_PATH+strategem.icon_name)
        svg_widget.setFixedSize(20,20)
        svg_widget.setStyleSheet("background-color: transparent")
        self.icon.setPixmap(svg_widget.grab())  
    
    def setKey(self, key):
        self.id = key
        self.key.setText(key)