import sys
from PyQt5 import QtWidgets


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    from windows import main_window
    main_window.show()  # Показываем главное окно
    app.exec_()  # Запускаем приложение
