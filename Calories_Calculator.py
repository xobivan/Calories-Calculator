import sys
import pickle
from PyQt5.QtWidgets import (QApplication, QMainWindow, 
                             QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, 
                             QTableWidgetItem, QAction, 
                             QHeaderView, QMenu)
from PyQt5.QtGui import QContextMenuEvent, QIcon
from PyQt5.QtCore import QEvent, Qt


class CalorieCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calories Counter")
        self.setGeometry(100, 100, 800, 600)

        f = open("./styles/style.qss")
        stylesheet = f.read()
        self.setStyleSheet(stylesheet)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Создаем вертикальный layout для размещения виджетов
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Создаем меню
        self.create_menu()

        # Создаем группу виджетов для добавления нового продукта
        add_food_group = self.create_add_food_group()
        layout.addLayout(add_food_group)

        # Создаем группу виджетов для просмотра добавленных продуктов
        view_foods_group = self.create_view_foods_group()
        layout.addLayout(view_foods_group)

        self.load_foods()

        self.statusBar().showMessage('Ready')

        # Присоединяем обработчик контекстного меню к таблице
        
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.showContextMenu)

    def create_menu(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')

        exit_action = QAction(QIcon('./assets/pics/exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Quit the app')
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

    def create_add_food_group(self):
        add_food_group = QVBoxLayout()

        label = QLabel("Add Product")
        add_food_group.addWidget(label)

        name_layout = QHBoxLayout()
        name_label = QLabel("Product:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        add_food_group.addLayout(name_layout)

        calories_layout = QHBoxLayout()
        calories_label = QLabel("Calories:")
        self.calories_input = QLineEdit()
        calories_layout.addWidget(calories_label)
        calories_layout.addWidget(self.calories_input)
        add_food_group.addLayout(calories_layout)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_food)
        add_food_group.addWidget(add_button)

        return add_food_group
    

    def create_view_foods_group(self):
        view_foods_group = QVBoxLayout()

        label = QLabel("Added Products")
        view_foods_group.addWidget(label)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Calories"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        view_foods_group.addWidget(self.table_widget)

        return view_foods_group

    def add_food(self):

        name = self.name_input.text()
        calories = self.calories_input.text()

        if name and calories:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(name))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(calories))
            total_calories = sum(int(self.table_widget.item(row, 1).text()) for row in range(self.table_widget.rowCount()))
            self.statusBar().showMessage(f'Total amount of calories: {total_calories} kcal')
        
        self.name_input.clear()
        self.calories_input.clear()

    def save_foods(self):
        foods = []
        for row in range(self.table_widget.rowCount()):
            name = self.table_widget.item(row, 0).text()
            calories = int(self.table_widget.item(row, 1).text())
            foods.append((name, calories))

        with open('foods.pkl', 'wb') as f:
            pickle.dump(foods, f)


        # Создаем статусную строку
        self.statusBar().showMessage('Ready')

    def load_foods(self):
        try:
            with open('foods.pkl', 'rb') as f:
                foods = pickle.load(f)

            for name, calories in foods:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(name))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(str(calories)))

                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_food(row))
                self.table_widget.setCellWidget(row_position, 2, delete_button)

        except FileNotFoundError:
            pass

    def showContextMenu(self, pos):
        menu = QMenu(self)
        delete_action = QAction(QIcon('./assets/pics/delete.png'),"Delete row", self)
        delete_action.triggered.connect(self.deleteSelectedRow)
        delete_action.setEnabled(self.table_widget.rowCount() > 0)
        menu.addAction(delete_action)
        menu.exec_(self.table_widget.mapToGlobal(pos))

    def deleteSelectedRow(self):
        selected_row = self.table_widget.currentRow()
        self.table_widget.removeRow(selected_row)

    def closeEvent(self, event):
        self.save_foods()  # Сохраняем данные перед закрытием окна
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalorieCounterApp()
    window.show()
    sys.exit(app.exec_())