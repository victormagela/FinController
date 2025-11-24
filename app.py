"""Utiliza o módulo sys para para poder passar argumentos de linha de comando
ao QApplication e inicializar a aplicação FinController."""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

from src.ui.gui.main_window import MainWindow


def get_qss_file_path() -> Path:
    """Retorna o caminho absoluto do arquivo QSS."""
    current_file_path = Path(__file__).parent
    qss_file_path = current_file_path / "src" / "ui" / "gui" / "styles"
    return qss_file_path


QSS_FILE_NAME = "fincontroller_dark.qss"
QSS_FILE_PATH = get_qss_file_path() / QSS_FILE_NAME


def main():
    """Inicia o Qt Application e a Main Window."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#101214"))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor("#181b1f"))
    palette.setColor(QPalette.AlternateBase, QColor("#14171a"))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor("#181b1f"))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Highlight, QColor("#2ecc71"))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    with open(QSS_FILE_PATH, encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read())

    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    main()
