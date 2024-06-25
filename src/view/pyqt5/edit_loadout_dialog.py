import constants
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QAbstractItemView, QMenuBar, QAction, QWidget, QLabel, QListWidgetItem, QInputDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtSvg import QSvgWidget
from copy import deepcopy
from src.view.pyqt5.filter_dialog import FilteredListDialog
from src.view.pyqt5.util import show_capture_key_dialog

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
        confirm_buttons_layout.setContentsMargins(0,30,0,0)
        layout.addLayout(confirm_buttons_layout)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_save = QPushButton("Apply")
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
    
    def add_macro(self):
        show_capture_key_dialog(self, self.controller, self.on_next_key, "Press key for new macro")
    
    def delete_current_macro(self):
        macro = self.list_widget.currentItem()
        if macro is not None:
            key = macro.data(Qt.UserRole)
            self.editLoadout.macroKeys.pop(key)
            self.update_macros()
    
    def change_current_macro(self):
        currentMacro = self.list_widget.currentItem()
        if currentMacro is not None:
            key = currentMacro.data(Qt.UserRole)
            dialog = FilteredListDialog(self.controller, key, self.on_stratagem_selected)
            dialog.exec_()
    
    def on_stratagem_selected(self, key, id):
        self.editLoadout.macroKeys[key] = id
        self.update_macros()

    def on_next_key(self, key):
        if key not in self.editLoadout.macroKeys:
            self.editLoadout.macroKeys.update({key:"0"})
            self.update_macros()

    def update_loadout(self):
        if self.loadoutId is not None:
            before = deepcopy(self.editLoadout.macroKeys)
            self.editLoadout.macroKeys.clear()
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                key = item.data(Qt.UserRole)
                stratagemId = before[key]
                self.editLoadout.macroKeys.update({key:stratagemId})

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
        for id, loadout in self.controller.model.loadoutManager.loadouts.items():
            self.dropdown.addItem(loadout.name, id)
        if self.dropdown.count() > 0:
            self.dropdown.setCurrentIndex(0)
        else:
            self.set_loadout()

    def set_loadout(self):
        self.loadoutId = self.dropdown.currentData()
        if self.loadoutId is None:
            self.edit_field.setText("")
            self.editLoadout = None
            self.update_macros()
            return
        
        self.editLoadout = deepcopy(self.controller.model.loadoutManager.loadouts[self.loadoutId])
        self.edit_field.setText(self.editLoadout.name)
        self.update_macros()

    def update_macros(self):
        # Update list widget based on selected item
        self.list_widget.clear()
        # Add all items to the QListWidget
        self.editMacros = {}
        if self.editLoadout is not None:
            for key, stratagemId in self.editLoadout.macroKeys.items():
                self.editMacros.update({key:self.controller.model.stratagems[stratagemId]})

        for index, (key, value) in enumerate(self.editMacros.items()):
            listAdapter = QEditLoadoutListAdapter()
            listAdapter.setStyleSheet("background-color: transparent")
            listAdapter.setStratagem(value)
            listAdapter.setKey(key)

            listAdapterItem = QListWidgetItem(self.list_widget)
            listAdapterItem.setData(Qt.UserRole,key)
            listAdapterItem.setSizeHint(listAdapter.sizeHint())
            self.list_widget.addItem(listAdapterItem)
            self.list_widget.setItemWidget(listAdapterItem, listAdapter)

    def on_loadout_name_changed(self, name):
        self.editLoadout.name = name

class QEditLoadoutListAdapter(QWidget):
    def __init__ (self, parent = None):
        super(QEditLoadoutListAdapter, self).__init__(parent)

        self.hBox  = QHBoxLayout()
        self.hBox.setContentsMargins(5,5,5,0)
        
        self.icon = QLabel()
        self.icon.setFixedSize(25, 25)
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setStyleSheet("background-color: "+constants.COLOR_STRATAGEM_BACKGROUND)
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

    def setStratagem(self, stratagem):
        self.name.setText(stratagem.name)
        svg_widget = QSvgWidget(constants.STRATAGEM_ICON_PATH+stratagem.icon_name)
        svg_widget.setFixedSize(20,20)
        svg_widget.setStyleSheet("background-color: transparent")
        self.icon.setPixmap(svg_widget.grab())  
    
    def setKey(self, key):
        self.id = key
        self.key.setText(key)