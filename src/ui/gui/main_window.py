from PySide6.QtWidgets import QWidget, QMainWindow, QGridLayout, QPushButton


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.central_window = QWidget()

        self.grid_layout = QGridLayout()

        self.add_button = QPushButton('Adicionar Transação')
        self.edit_button = QPushButton('Editar Transação')
        self.filter_button = QPushButton('Filtrar/Ordernar Transações')
        self.report_button = QPushButton('Gerar Relatório')

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('FinController')

        self.setCentralWidget(self.central_window)
        self.central_window.setLayout(self.grid_layout)

        self.grid_layout.addWidget(self.add_button, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.edit_button, 1, 2, 1, 1)
        self.grid_layout.addWidget(self.filter_button, 1, 3, 1, 1)
        self.grid_layout.addWidget(self.report_button, 1, 4, 1, 1)