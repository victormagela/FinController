from PySide6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QLabel, QHeaderView, QMessageBox
)

from src.ui.gui.table_model import TableModel
from src.ui.gui.transaction_form_window import TransactionFormWindow, DialogMode
from src.service.transaction_service import TransactionService
from src.models.transaction import Transaction


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._service = TransactionService()

        self.central_window = QWidget()

        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton('Adicionar Transação')
        self.edit_button = QPushButton('Editar Transação')
        self.delete_button = QPushButton('Excluir Transação')
        self.filter_button = QPushButton('Filtrar/Ordernar Transações')
        self.report_button = QPushButton('Gerar Relatório')

        self.table = QTableView()
        self.table_model = TableModel()
        self.no_table_label = QLabel('Nenhuma transação encontrada. Por favor adicione uma para começar.')

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('FinController')
        self.setFixedSize(610, 400)

        self.status_bar = self.statusBar()

        self.setCentralWidget(self.central_window)
        self.central_window.setLayout(self.main_layout)

        self._configure_layout()

        self._configure_table()

        self._configure_buttons()

    def _configure_layout(self) -> None:
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.filter_button)
        self.button_layout.addWidget(self.report_button)
        self.main_layout.addLayout(self.button_layout)

        if self._service.get_all_transactions():
            self.main_layout.addWidget(self.table)
            self.table_model.set_transaction_list(self._service.get_all_transactions())
        
        else:
            self.main_layout.addWidget(self.no_table_label)

    def _configure_table(self) -> None:
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        self.table.setModel(self.table_model)
        self.table.setColumnWidth(0, 40)   # Id
        self.table.setColumnWidth(1, 80)   # Data
        self.table.setColumnWidth(2, 80)   # Tipo
        self.table.setColumnWidth(3, 100)  # Categoria
        self.table.setColumnWidth(4, 200)  # Descrição
        self.table.setColumnWidth(5, 80)   # Valor
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(self._on_table_selection_changed)

    def _configure_buttons(self) -> None:
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        self.add_button.clicked.connect(self._add_transaction)
        self.edit_button.clicked.connect(self._edit_transaction)
        self.delete_button.clicked.connect(self._delete_transaction)
        self.filter_button.clicked.connect(self._filter_transactions)
        self.report_button.clicked.connect(self._generate_report)

    # Slots principais ------------------------------------------------------------------------------------------------
    def _add_transaction(self) -> None:
        new_transaction_window = TransactionFormWindow(mode=DialogMode.CREATEMODE)
        new_transaction_window.exec()
        input_list = new_transaction_window.user_input_list
        try:
            for user_input in input_list:
                self._service.add_transaction(user_input)
        except ValueError as e:
            error_window = self._configure_error_window(e)
            error_window.exec()
        
        if input_list:
            self.main_layout.removeWidget(self.no_table_label)
            self.no_table_label.hide()
            self.table_model.set_transaction_list(self._service.get_all_transactions())
            self.main_layout.addWidget(self.table)
            self.status_bar.showMessage('Transação adicionada com sucesso!')

    def _edit_transaction(self) -> None:
        transaction_id = self.get_transaction_id()
        transaction = self._service.get_transaction_by_id(transaction_id)

        edit_transaction_window = TransactionFormWindow(mode=DialogMode.EDITMODE, transaction=transaction)
        edit_transaction_window.exec()
        input_dict = edit_transaction_window.user_input_dict

        if input_dict:
            try:
                self._service.update_transaction_category(transaction_id, input_dict.get('category'))
                self._service.update_transaction_description(transaction_id, input_dict.get('description'))
            except ValueError as e:
                error_window = self._configure_error_window(e)
                error_window.exec()

            self.table_model.set_transaction_list(self._service.get_all_transactions())
            self._disable_buttons()
            self.status_bar.showMessage('Transação modificada com sucesso!')

    def _delete_transaction(self) -> None:
        transaction_id = self.get_transaction_id()

        confirmation_window = QMessageBox()
        confirmation_window.setText('Tem certeza que deseja excluir esta transação?')
        confirmation_window.setIcon(QMessageBox.Icon.Question)
        confirmation_window.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirmation_window.setButtonText(QMessageBox.StandardButton.Yes, 'Sim')
        confirmation_window.setButtonText(QMessageBox.StandardButton.No, 'Não')

        confirmation = confirmation_window.exec()
        
        if confirmation == QMessageBox.StandardButton.Yes:
            try:
                self._service.del_transaction(transaction_id)
                self.table_model.set_transaction_list(self._service.get_all_transactions())
                self._disable_buttons()
                self.status_bar.showMessage('Transação excluída com sucesso!')
            except ValueError as e:
                error_window = self._configure_error_window(e)
                error_window.exec()
        
        else:
            return

    def _filter_transactions(self) -> None:
        print('Filtrar Transações')

    def _generate_report(self) -> None:
        print('Gerar relatório')

    # Métodos utilitários ---------------------------------------------------------------------------------------------
    def get_transaction_id(self) -> Transaction:
        selected_rows = self.table.selectionModel().selectedRows()
        return selected_rows[0].data()
    
    def _disable_buttons(self) -> None:
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def _configure_error_window(self, error) -> QMessageBox:
        error_window = QMessageBox()
        error_window.setText(f'{error}')
        error_window.setIcon(QMessageBox.Icon.Critical)
        error_window.setWindowTitle('Erro!')

        return error_window

    # Slots utilitários -----------------------------------------------------------------------------------------------
    def _on_table_selection_changed(self, *_args) -> None:
        self._enable_edit_button()
        self._enable_delete_button()

        self._update_statusbar_msg()

    def _enable_edit_button(self) -> None:
        self.edit_button.setEnabled(self.table.selectionModel().hasSelection())

    def _enable_delete_button(self) -> None:
        self.delete_button.setEnabled(self.table.selectionModel().hasSelection())

    def _update_statusbar_msg(self) -> None:
        selected_rows = self.table.selectionModel().selectedRows()
        row = selected_rows[0].row()
        model = self.table.model()

        values = []
        for col in range(model.columnCount()):
            index = model.index(row, col)
            data = model.data(index)
            if isinstance(data, str):
                values.append(data)

        text = ' '.join(values)
        self.status_bar.showMessage(text)