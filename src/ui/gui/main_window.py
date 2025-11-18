from datetime import date

from PySide6.QtWidgets import QWidget, QMainWindow, QGridLayout, QPushButton, QTableView

from src.ui.gui.table_model import TableModel
from src.models.transaction import Transaction
from src.models.enums import TransactionType, IncomeCategory, ExpenseCategory


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.fake_transactions: list[Transaction] = [
    # Receitas
    Transaction(
        amount=3500.00,
        transaction_type=TransactionType.INCOME,
        transaction_date=date(2025, 10, 5),
        category=IncomeCategory.WAGE,
        description="Salário empresa X",
    ),
    Transaction(
        amount=500.00,
        transaction_type=TransactionType.INCOME,
        transaction_date=date(2025, 10, 15),
        category=IncomeCategory.FREELANCE,
        description="Freelancer de desenvolvimento",
    ),

    # Despesas
    Transaction(
        amount=120.75,
        transaction_type=TransactionType.EXPENSE,
        transaction_date=date(2025, 10, 8),
        category=ExpenseCategory.FOOD,
        description="Alimentação – almoço fora",
    ),
    Transaction(
        amount=250.00,
        transaction_type=TransactionType.EXPENSE,
        transaction_date=date(2025, 10, 12),
        category=ExpenseCategory.BILLS,
        description="Conta de energia",
    ),
    Transaction(
        amount=89.90,
        transaction_type=TransactionType.EXPENSE,
        transaction_date=date(2025, 11, 1),
        category=ExpenseCategory.LEISURE,
        description="Assinatura de serviços de streaming",
    ),
    Transaction(
        amount=1500.00,
        transaction_type=TransactionType.EXPENSE,
        transaction_date=date(2025, 11, 5),
        category=ExpenseCategory.HOUSING,
        description="Aluguel",
    ),
]
        self.central_window = QWidget()

        self.grid_layout = QGridLayout()

        self.add_button = QPushButton('Adicionar Transação')
        self.edit_button = QPushButton('Editar Transação')
        self.filter_button = QPushButton('Filtrar/Ordernar Transações')
        self.report_button = QPushButton('Gerar Relatório')

        self.table = QTableView()
        self.table_model = TableModel()

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('FinController')

        self.setCentralWidget(self.central_window)
        self.central_window.setLayout(self.grid_layout)

        self.grid_layout.addWidget(self.add_button, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.edit_button, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.filter_button, 0, 2, 1, 1)
        self.grid_layout.addWidget(self.report_button, 0, 3, 1, 1)
        if self.fake_transactions:
            self.grid_layout.addWidget(self.table, 1, 0, 1, 4)
        
        else:
            ...

        self.table_model.set_transaction_list(self.fake_transactions)
        self._configure_table()
        self._configure_buttons()

        #self.table.selectionModel.selectionChanged.connect(self._on_table_selection_changed)

    def _configure_table(self) -> None:
        self.table.setModel(self.table_model)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

    def _configure_buttons(self) -> None:
        self.edit_button.setEnabled(False)

        self.add_button.clicked.connect(self._add_transaction)
        self.edit_button.clicked.connect(self._edit_transaction)
        self.filter_button.clicked.connect(self._filter_transactions)
        self.report_button.clicked.connect(self._generate_report)

    def _add_transaction(self) -> None:
        print('Adicionar transação')

    def _edit_transaction(self) -> None:
        print('Editar transação')

    def _filter_transactions(self) -> None:
        print('Filtrar Transações')

    def _generate_report(self) -> None:
        print('Gerar relatório')

    def _on_table_selection_changed(self) -> None:
        if self.table.selectionModel().hasSelection():
            self.edit_button.setEnabled(self.table.selectionModel().hasSelection())
