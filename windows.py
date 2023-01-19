from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QTableWidgetItem

import MainWindow
import AddPasswordWindow
import generator
import encryption


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
        super().__init__()
        self.setupUi(self)  # Инициализация дизайна
        self.search = ''
        self.add_new_pass_window = None
        self.pushButton.clicked.connect(self.create_new_password_btn_clicked)
        self.tableWidget.itemClicked.connect(self.password_clicked)

    def create_new_password_btn_clicked(self):
        """Обработчик нажатия на кнопку 'создать новый пароль'."""
        self.add_new_pass_window = AddPasswordWindow()
        self.add_new_pass_window.show()

    def update_table(self):
        with open('passwords.txt') as file:
            # Словарь с ключами в виде меток и значениями в виде зашифрованных паролей
            passwords = {line.split()[0]: line.split()[1] for line in file}
        self.tableWidget.setHorizontalHeaderLabels(['Метка', 'Пароль (в зашифрованном виде)'])
        self.tableWidget.setVerticalHeaderLabels(list(map(str, range(1, len(passwords) + 1))))
        for i in range(1, 2+1):
            for j in range(1, len(passwords)+1):
                print(i, j, list(passwords.items())[j][i])
                self.tableWidget.setItem(i, j, QTableWidgetItem(list(passwords.items())[j][i]))


    def password_clicked(self, item):
        print(item.text())


class AddPasswordWindow(QtWidgets.QMainWindow, AddPasswordWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Инициализация дизайна
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
