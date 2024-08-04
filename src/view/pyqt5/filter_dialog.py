import constants
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QLineEdit, QListWidget, QAbstractItemView, QHBoxLayout, QLabel, QListWidgetItem
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtSvg import QSvgWidget
from src.view.view_utilities import filter_stratagems, sort_stratagems

class FilteredListDialog(QDialog):
    def __init__(self, controller, key, callback = None):
        super().__init__()
        self.callback = callback
 
        self.controller = controller
        self.key = key
        self.setMinimumSize(325, 300)
        self.resize(325,800)

        self.setWindowTitle("Select new stratagem for: "+self.key)
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

    def update_macros(self, text):
        # Clear the current items in the QListWidget
        self.list_widget.clear()

        # Filter and sort items
        stratagem_list = filter_stratagems(self.controller.get_stratagems(), text)
        stratagem_list = sort_stratagems(stratagem_list)

        # Add all items to the QListWidget
        for id, stratagem in stratagem_list.items():
            listAdapter = QFilterListAdapter()
            listAdapter.setStyleSheet("background-color: transparent")
            listAdapter.setStratagem(stratagem)

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
        self.icon.setStyleSheet("background-color: "+constants.COLOR_STRATAGEM_BACKGROUND)
        self.icon.setAlignment(Qt.AlignCenter)
        self.hBox.addWidget(self.icon)
        
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
