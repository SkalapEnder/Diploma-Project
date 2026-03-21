from PySide6 import QtWidgets  # Импорт модуля QtWidgets из библиотеки PySide6
import sys  # Импорт модуля sys для работы с системными параметрами и выходом из программы

# Создание экземпляра QApplication, который управляет основным циклом событий и инициализацией приложения
app = QtWidgets.QApplication(sys.argv)

# Создание главного окна приложения
window = QtWidgets.QWidget()

# Установка заголовка главного окна
window.setWindowTitle("PySide6 Application")

# Установка размеров главного окна
window.resize(300, 250)

# Создание метки (надписи) с текстом "Hello World!"
lbl = QtWidgets.QLabel("Hello World!")

# Создание кнопки с надписью "Close"
btn = QtWidgets.QPushButton("Close")

# Создание вертикального блока для размещения метки и кнопки
# Вертикальный блок из себя представляет контейнер в который мы помещаем элементы
box = QtWidgets.QVBoxLayout()

# Добавление метки и кнопки в вертикальный блок
box.addWidget(lbl)
box.addWidget(btn)

# Установка вертикального блока в качестве компоновщика главного окна
window.setLayout(box)

# Подключение обработчика события "clicked" кнопки к методу app.quit, вызывающему завершение приложения
btn.clicked.connect(app.quit)

# Отображение главного окна
window.show()

# Запуск основного цикла обработки событий приложения
sys.exit(app.exec())  # После завершения цикла приложение выходит из программы