import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QAction
from PyQt5.QtGui import QIcon, QFont, QPixmap


class CalorieCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calorie Counter")
        self.setGeometry(100, 100, 800, 600)
        f = open("Calories_Calculator/styles/style.qss")
        stylesheet = f.read()
        self.setStyleSheet(stylesheet)

        f.close()

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

        # Создаем статусную строку
        self.statusBar().showMessage('Готово')

    def create_menu(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('Файл')

        exit_action = QAction(QIcon('exit.png'), 'Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Выход из приложения')
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

    def create_add_food_group(self):
        add_food_group = QVBoxLayout()

        label = QLabel("Добавить продукт")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        add_food_group.addWidget(label)

        name_layout = QHBoxLayout()
        name_label = QLabel("Название:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        add_food_group.addLayout(name_layout)

        calories_layout = QHBoxLayout()
        calories_label = QLabel("Калории:")
        self.calories_input = QLineEdit()
        calories_layout.addWidget(calories_label)
        calories_layout.addWidget(self.calories_input)
        add_food_group.addLayout(calories_layout)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_food)
        add_food_group.addWidget(add_button)

        return add_food_group

    def create_view_foods_group(self):
        view_foods_group = QVBoxLayout()

        label = QLabel("Добавленные продукты")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        view_foods_group.addWidget(label)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Название", "Калории"])
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

            self.name_input.clear()
            self.calories_input.clear()

            total_calories = sum(int(self.table_widget.item(row, 1).text()) for row in range(self.table_widget.rowCount()))
            self.statusBar().showMessage(f'Общее количество калорий: {total_calories}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalorieCounterApp()
    window.show()
    sys.exit(app.exec_())