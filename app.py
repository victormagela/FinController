from PySide6.QtWidgets import QApplication

from src.ui.gui.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication()

    main_window = MainWindow()
    
    main_window.show()
    app.exec()