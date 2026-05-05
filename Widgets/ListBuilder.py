from PySide6.QtWidgets import (QLineEdit, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, 
                               QTreeWidget, QTreeWidgetItem, QPushButton, QLabel, QInputDialog)
from PySide6.QtCore import Qt

class ListBuilderWidget(QWidget):
    def __init__(self, available_items=None):
        super().__init__()
        
        if available_items is None:
            available_items = ["Parameter 1", "Parameter 2", "Parameter 3", "Parameter 4"]

        main_layout = QHBoxLayout(self)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Available:"))

        self.search_bar = QLineEdit(placeholderText="Search...")
        left_layout.addWidget(self.search_bar)
        
        self.source_list = QListWidget()
        self.source_list.addItems(available_items)
        self.source_list.setSelectionMode(QListWidget.ExtendedSelection) # Allow picking multiple
        left_layout.addWidget(self.source_list)

        middle_layout = QVBoxLayout()
        middle_layout.setAlignment(Qt.AlignCenter)
        
        self.btn_add = QPushButton("Add ➔")
        self.btn_remove = QPushButton("⬅ Remove")
        
        middle_layout.addWidget(self.btn_add)
        middle_layout.addWidget(self.btn_remove)

        right_layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        # header_layout.addWidget(QLabel("Selected:"))
        self.btn_new_group = QPushButton("+ Group")
        header_layout.addWidget(self.btn_new_group)
        right_layout.addLayout(header_layout)
        
        self.group_tree = QTreeWidget()
        self.group_tree.setHeaderHidden(True)
        self.group_tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        right_layout.addWidget(self.group_tree)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(right_layout)

        self.btn_new_group.clicked.connect(lambda: self.add_new_group(f"List {self.group_tree.topLevelItemCount() + 1}")) # If you want to name them yourself then replace it with self.add_new_group()
        self.search_bar.textChanged.connect(self.filter_elements)
        self.btn_add.clicked.connect(self.add_to_group)
        self.btn_remove.clicked.connect(self.remove_from_group)

        self.add_new_group("List 1")

    def add_new_group(self, name=None):
        if not name or not isinstance(name, str):
            name, ok = QInputDialog.getText(self, "New Group", "Enter group name:")
            if not ok or not name:
                return

        group_item = QTreeWidgetItem(self.group_tree, [name])
        group_item.setData(0, Qt.UserRole, "is_group")
        
        group_item.setExpanded(True)
        self.group_tree.setCurrentItem(group_item)

    def add_to_group(self):
        source_items = self.source_list.selectedItems()
        target_item = self.group_tree.currentItem()

        if not source_items or not target_item:
            return

        if target_item.data(0, Qt.UserRole) != "is_group":
            target_item = target_item.parent()

        for item in source_items:
            new_child = QTreeWidgetItem(target_item, [item.text()])
            new_child.setData(0, Qt.UserRole, "is_parameter")
            
        target_item.setExpanded(True)

    def remove_from_group(self):
        for item in self.group_tree.selectedItems():
            if item.data(0, Qt.UserRole) == "is_group":
                index = self.group_tree.indexOfTopLevelItem(item)
                self.group_tree.takeTopLevelItem(index)
            else:
                parent = item.parent()
                parent.removeChild(item)

    def filter_elements(self, text):
        text = text.lower()

        for i in range(self.source_list.count()):
            item = self.source_list.item(i)
            item.setHidden(not (text in item.text().lower()))

    def get_lists_of_lists(self):
        """Returns the data structure for your Writer: [['Param1'], [], ['Param2', 'Param3']]"""
        result = []
        for i in range(self.group_tree.topLevelItemCount()):
            group_item = self.group_tree.topLevelItem(i)
            
            group_params = []
            for j in range(group_item.childCount()):
                child_item = group_item.child(j)
                group_params.append(child_item.text(0))
                
            result.append(group_params)
            
        return result
    
    def load_from_conf(self, iterlist):
        self.group_tree.clear()
        for group in iterlist:
            group_item = QTreeWidgetItem(self.group_tree, [f"List {self.group_tree.topLevelItemCount() + 1}"])
            group_item.setData(0, Qt.UserRole, "is_group")
            for param in group:
                child_item = QTreeWidgetItem(group_item, [param])
                child_item.setData(0, Qt.UserRole, "is_parameter")
            group_item.setExpanded(True)