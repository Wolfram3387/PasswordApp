from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QTableWidgetItem

import AddPasswordWindow
import MainWindow
import encryption
import generator


def warning(text, title='Предупреждение', icon=QMessageBox.Warning, button=QMessageBox.Ok):
    """Показывает окно предупреждения для пользователя"""
    warning_msg = QMessageBox()
    warning_msg.setText(text)
    warning_msg.setIcon(icon)
    warning_msg.setWindowTitle(title)
    warning_msg.setStandardButtons(button)
    warning_msg.exec_()


class MainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()  # Инициализация системного окна
        self.setupUi(self)  # Инициализация дизайна

        # Инициализация переменных и подключение функций-обработчиков
        self.search = ''
        self.add_new_pass_window = None
        self.pushButton.clicked.connect(self.create_new_password_btn_clicked)
        self.tableWidget.itemClicked.connect(self.password_clicked)
        self.update_table()
        self.lineEdit_search.textChanged.connect(self.text_search_changed)

    def text_search_changed(self, text):
        """Меняет искомое значение (self.search) в таблице"""
        self.search = text
        self.update_table()

    def create_new_password_btn_clicked(self):
        """Обработчик нажатия на кнопку 'создать новый пароль'."""
        self.add_new_pass_window = AddPasswordWindow()
        self.add_new_pass_window.show()

    def update_table(self):
        """Обновляет таблицу"""
        with open('passwords.txt') as file:
            # Словарь с ключами в виде меток и значениями в виде зашифрованных паролей
            passwords = {' '.join(line.split()[:-1]): line.split()[-1] for line in file}

        # Подготовка таблицы
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['Метка', 'Пароль (в зашифрованном виде)'])
        self.tableWidget.setVerticalHeaderLabels(list(map(str, range(1, len(passwords) + 1))))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(passwords))

        # Помещаем в ячейки все пароли, удовлетворяющие поиску self.search
        row = 0
        for mark, password in passwords.items():
            if self.search in mark or self.search in password:
                self.tableWidget.setItem(row, 0, QTableWidgetItem(mark))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(password))
                row += 1

        # Задаём столбцам нужную ширину
        column_size = (self.size().width() - 24) // self.tableWidget.columnCount() - 10
        self.tableWidget.setColumnWidth(0, column_size)
        self.tableWidget.setColumnWidth(1, column_size)
        self.tableWidget.resizeRowsToContents()

    def password_clicked(self, item):
        """Обработчик нажатия на строку с паролями"""
        with open('passwords.txt') as file:
            # Словарь с ключами в виде меток и значениями в виде зашифрованных паролей
            passwords = {' '.join(line.split()[:-1]): line.split()[-1] for line in file}

        # Копируем пароль из выбранной строки и показываем уведомление
        for mark, password in passwords.items():
            if item.text() in (mark, password):
                QApplication.clipboard().setText(encryption.decrypt_password(password))
        warning(
            text='Расшифрованный пароль скопирован в буфер обмена', title='Уведомление', icon=QMessageBox.Information)

    def resizeEvent(self, event):
        # При изменении главного окна, изменяется и размер таблицы
        self.update_table()


class AddPasswordWindow(QtWidgets.QMainWindow, AddPasswordWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_generate_clicked)

    def btn_generate_clicked(self):
        """Обработчик нажатия на кнопку 'сгенерировать пароль'."""
        # Проверяем, что пользователь ввёл какую-либо метку
        mark = self.lineEdit_mark.text()
        if not mark:
            warning(text='Необходимо задать метку для пароля')
            return

        # Генерируем зашифрованный пароль
        password = generator.generate_password()
        token = encryption.encrypt_password(password)

        # Добавляем метку и зашифрованный пароль в passwords.txt
        with open('passwords.txt', 'a') as file:
            file.write(f'{mark} {token}\n')

        main_window.update_table()  # Обновляем список всех паролей на главной странице

        # Добавляем сгенерированный пароль в буфер обмена и показываем соответствующее уведомление
        QApplication.clipboard().setText(password)
        warning(text='Пароль скопирован в буфер обмена и добавлен в список паролей!',
                title='Уведомление', icon=QMessageBox.Information)
        self.close()


main_window = MainWindow()
