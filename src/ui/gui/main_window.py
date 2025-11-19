from datetime import date

from PySide6.QtWidgets import QWidget, QMainWindow, QGridLayout, QPushButton, QTableView, QLabel

from src.ui.gui.table_model import TableModel
from src.ui.gui.new_transaction_window import NewTransactionWindow
from src.service.transaction_service import TransactionService
from src.models.transaction import Transaction
from src.models.enums import TransactionType, IncomeCategory, ExpenseCategory


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._service = TransactionService()

        self.central_window = QWidget()

        self.grid_layout = QGridLayout()

        self.add_button = QPushButton('Adicionar Transação')
        self.edit_button = QPushButton('Editar Transação')
        self.filter_button = QPushButton('Filtrar/Ordernar Transações')
        self.report_button = QPushButton('Gerar Relatório')

        self.table = QTableView()
        self.table_model = TableModel()
        self.no_table_label = QLabel('Nenhuma transação encontrada. Por favor adicione uma para começar.')

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('FinController')

        self.setCentralWidget(self.central_window)
        self.central_window.setLayout(self.grid_layout)

        self._configure_layout()

        self._configure_table()

        self._configure_buttons()

    def _configure_layout(self) -> None:
        self.grid_layout.addWidget(self.add_button, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.edit_button, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.filter_button, 0, 2, 1, 1)
        self.grid_layout.addWidget(self.report_button, 0, 3, 1, 1)
        if self._service.get_all_transactions():
            self.grid_layout.addWidget(self.table, 1, 0, 1, 4)
            self.table_model.set_transaction_list(self._service.get_all_transactions())
        
        else:
            self.grid_layout.addWidget(self.no_table_label, 1, 0, 1, 4)

        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 1)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)

    def _configure_table(self) -> None:
        self.table.setModel(self.table_model)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(self._on_table_selection_changed)

    def _configure_buttons(self) -> None:
        self.edit_button.setEnabled(False)

        self.add_button.clicked.connect(self._add_transaction)
        self.edit_button.clicked.connect(self._edit_transaction)
        self.filter_button.clicked.connect(self._filter_transactions)
        self.report_button.clicked.connect(self._generate_report)

    def _add_transaction(self) -> None:
        new_transaction_window = NewTransactionWindow()
        new_transaction_window.exec()
        input_list = new_transaction_window.user_input_list
        for user_input in input_list:
            self._service.add_transaction(user_input)
        
        if input_list:
            self.grid_layout.removeWidget(self.no_table_label)
            self.no_table_label.hide()
            self.table_model.set_transaction_list(self._service.get_all_transactions())
            self.grid_layout.addWidget(self.table, 1, 0, 1, 4)

    def _edit_transaction(self) -> None:
        print('Editar transação')

    def _filter_transactions(self) -> None:
        print('Filtrar Transações')

    def _generate_report(self) -> None:
        print('Gerar relatório')

    def _on_table_selection_changed(self, *_args) -> None:
        self.edit_button.setEnabled(self.table.selectionModel().hasSelection())
