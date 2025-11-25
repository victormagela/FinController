"""Define a janela principal da aplicação FinController."""

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QLabel,
    QHeaderView,
    QMessageBox,
    QFrame,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QSize

from src.ui.gui.table_model import TableModel
from src.ui.gui.transaction_form_window import (
    TransactionFormWindow,
    DialogMode,
)
from src.ui.gui.transaction_filter_window import (
    TransactionFilterWindow,
    SortingFieldCode,
)
from src.ui.gui.report_window import ReportWindow
from src.service.transaction_service import TransactionService
from src.models.transaction import Transaction

from src.utils.constants import (
    ADD_ICON,
    EDIT_ICON,
    DELETE_ICON,
    FILTER_ICON,
    REPORT_ICON,
    WINDOW_ICON,
)


class MainWindow(QMainWindow):
    """Janela principal da aplicação FinController."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._service = TransactionService()

        # Central Widget e Layouts -----------------------------------------------------
        self.central_window = QWidget()

        self.main_layout = QVBoxLayout()

        self.main_card = QFrame()

        self.card_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        # Botões -----------------------------------------------------------------------
        self.add_button = QPushButton("Adicionar\nTransação")
        self.edit_button = QPushButton("Editar\nTransação")
        self.delete_button = QPushButton("Excluir\nTransação")
        self.filter_button = QPushButton("Filtrar/Ordernar")
        self.report_button = QPushButton("Gerar\nRelatório")

        # Tabela e Modelo --------------------------------------------------------------
        self.table = QTableView()
        self.table_model = TableModel()

        # Labels -----------------------------------------------------------------------
        self.title_label = QLabel("FinController")
        self.no_table_label = QLabel(
            "Nenhuma transação encontrada. Por favor adicione uma para começar."
        )

        self.configure_user_interface()

    def configure_user_interface(self) -> None:
        """Configura a interface gráfica do usuário."""
        self.setWindowTitle("FinController")
        self.setFixedSize(1200, 800)
        self.setWindowIcon(WINDOW_ICON)

        self.status_bar = self.statusBar()

        self.setCentralWidget(self.central_window)
        self.central_window.setLayout(self.main_layout)

        self._configure_labels()
        self._configure_layout()
        self._configure_frame()
        self._configure_table()
        self._configure_buttons()

    def _configure_layout(self) -> None:
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.filter_button)
        self.button_layout.addWidget(self.report_button)

        self.main_layout.addWidget(self.main_card)

        self.card_layout.addWidget(
            self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter
        )

        self.card_layout.addLayout(self.button_layout)
        self.card_layout.addSpacing(12)

        transactions = self._service.get_all_transactions()
        if transactions:
            self.card_layout.addWidget(self.table)
            self.table_model.set_transaction_list(transactions)

        else:
            self.card_layout.addWidget(self.no_table_label)

        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(0)

        self.card_layout.setContentsMargins(16, 16, 16, 16)
        self.card_layout.setSpacing(12)

        self.button_layout.setSpacing(12)

    def _configure_frame(self) -> None:
        self.main_card.setObjectName("mainCard")

        self.main_card.setLayout(self.card_layout)

    def _configure_table(self) -> None:
        table = self.table
        horizontal_header = table.horizontalHeader()
        vertical_header = table.verticalHeader()

        horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        horizontal_header.setHighlightSections(False)

        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical_header.setVisible(False)

        table.setModel(self.table_model)
        table.setSelectionBehavior(table.SelectionBehavior.SelectRows)
        table.setSelectionMode(table.SelectionMode.SingleSelection)
        table.setEditTriggers(table.EditTrigger.NoEditTriggers)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.selectionModel().selectionChanged.connect(
            self._on_table_selection_changed
        )
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)

    def _configure_buttons(self) -> None:
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        if not self.table_model.rowCount() > 0:
            self.filter_button.setEnabled(False)
            self.report_button.setEnabled(False)

        self.add_button.setIcon(ADD_ICON)
        self.edit_button.setIcon(EDIT_ICON)
        self.delete_button.setIcon(DELETE_ICON)
        self.filter_button.setIcon(FILTER_ICON)
        self.report_button.setIcon(REPORT_ICON)

        self.add_button.clicked.connect(self._on_add_transaction_clicked)
        self.edit_button.clicked.connect(self._on_edit_transaction_clicked)
        self.delete_button.clicked.connect(self._on_delete_transaction_clicked)
        self.filter_button.clicked.connect(self._on_filter_transactions_clicked)
        self.report_button.clicked.connect(self._on_generate_report_clicked)

        buttons = (
            self.add_button,
            self.edit_button,
            self.delete_button,
            self.filter_button,
            self.report_button,
        )

        for button in buttons:
            button.setProperty("class", "mainActionButton")
            button.setMinimumHeight(80)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            button.setIconSize(QSize(32, 32))

    def _configure_labels(self) -> None:
        self.title_label.setObjectName("titleLabel")
        self.no_table_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    # Slots principais -----------------------------------------------------------------
    def _on_add_transaction_clicked(self) -> None:
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
            self.card_layout.removeWidget(self.no_table_label)
            self.no_table_label.hide()
            self.table_model.set_transaction_list(self._service.get_all_transactions())
            self.card_layout.addWidget(self.table)
            self.status_bar.showMessage("Transação adicionada com sucesso!")

            if not self.filter_button.isEnabled():
                self.filter_button.setEnabled(True)

            if not self.report_button.isEnabled():
                self.report_button.setEnabled(True)

    def _on_edit_transaction_clicked(self) -> None:
        transaction_id = self._get_transaction_id()
        transaction = self._service.get_transaction_by_id(transaction_id)

        edit_transaction_window = TransactionFormWindow(
            mode=DialogMode.EDITMODE, transaction=transaction
        )
        edit_transaction_window.exec()
        input_dict = edit_transaction_window.user_input_dict

        if input_dict:
            try:
                self._service.update_transaction_category(
                    transaction_id, input_dict.get("category")
                )
                self._service.update_transaction_description(
                    transaction_id, input_dict.get("description")
                )
            except ValueError as e:
                error_window = self._configure_error_window(e)
                error_window.exec()

            self.table_model.set_transaction_list(self._service.get_all_transactions())
            self._disable_buttons()
            self.status_bar.showMessage("Transação modificada com sucesso!")

    def _on_delete_transaction_clicked(self) -> None:
        transaction_id = self._get_transaction_id()

        confirmation_window = QMessageBox()
        confirmation_window.setText("Tem certeza que deseja excluir esta transação?")
        confirmation_window.setIcon(QMessageBox.Icon.Question)
        confirmation_window.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        confirmation_window.setButtonText(QMessageBox.StandardButton.Yes, "Sim")
        confirmation_window.setButtonText(QMessageBox.StandardButton.No, "Não")

        confirmation = confirmation_window.exec()

        if confirmation == QMessageBox.StandardButton.Yes:
            try:
                self._service.del_transaction(transaction_id)
                self.table_model.set_transaction_list(
                    self._service.get_all_transactions()
                )
                self._disable_buttons()
                self.status_bar.showMessage("Transação excluída com sucesso!")
                if self.table_model.rowCount() < 1:
                    self.filter_button.setEnabled(False)
                    self.report_button.setEnabled(False)

            except ValueError as e:
                error_window = self._configure_error_window(e)
                error_window.exec()

        else:
            return

    def _on_filter_transactions_clicked(self) -> None:
        filter_window = TransactionFilterWindow()
        result = filter_window.exec()

        if result == TransactionFilterWindow.DialogCode.Accepted:
            transaction_list = self._service.get_all_transactions()

            if filter_window.clear_filters:
                self.table_model.set_transaction_list(transaction_list)
                if self.table_model.rowCount() > 0:
                    self.report_button.setEnabled(True)
                self.status_bar.showMessage("Filtros limpos!")

            else:
                filter_criteria = filter_window.filter_criteria
                sorting_criteria = filter_window.sorting_criteria

                if (
                    filter_criteria.min_amount is not None
                    or filter_criteria.max_amount is not None
                ):
                    transaction_list = self._service.filter_by_amount_range(
                        transaction_list,
                        filter_criteria.min_amount,
                        filter_criteria.max_amount,
                    )

                if (
                    filter_criteria.start_date is not None
                    or filter_criteria.end_date is not None
                ):
                    transaction_list = self._service.filter_by_date_range(
                        transaction_list,
                        filter_criteria.start_date,
                        filter_criteria.end_date,
                    )

                if filter_criteria.type is not None:
                    transaction_list = self._service.filter_by_type(
                        filter_criteria.type, transaction_list
                    )

                if filter_criteria.category is not None:
                    transaction_list = self._service.filter_by_category(
                        filter_criteria.category, transaction_list
                    )

                if sorting_criteria.field == SortingFieldCode.ID:
                    transaction_list = self._service.sort_by_id(
                        sorting_criteria.order, transaction_list
                    )

                elif sorting_criteria.field == SortingFieldCode.AMOUNT:
                    transaction_list = self._service.sort_by_amount(
                        sorting_criteria.order, transaction_list
                    )

                elif sorting_criteria.field == SortingFieldCode.DATE:
                    transaction_list = self._service.sort_by_date(
                        sorting_criteria.order, transaction_list
                    )

                self.table_model.set_transaction_list(transaction_list)
                if self.table_model.rowCount() < 1:
                    self.report_button.setEnabled(False)
                self.status_bar.showMessage("Filtros aplicados com sucesso!")

    def _on_generate_report_clicked(self) -> None:
        transaction_list = self.table_model.get_transaction_list()
        self._service.update_statistics(transaction_list)
        statistics = self._service.get_statistics()
        start_date = self._service.get_min_date(transaction_list)
        end_date = self._service.get_max_date(transaction_list)

        report_window = ReportWindow(statistics, start_date, end_date)
        report_window.exec()

    # Métodos utilitários --------------------------------------------------------------
    def _get_transaction_id(self) -> Transaction:
        selected_rows = self.table.selectionModel().selectedRows()
        return selected_rows[0].data()

    def _disable_buttons(self) -> None:
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def _configure_error_window(self, error) -> QMessageBox:
        error_window = QMessageBox()
        error_window.setText(f"{error}")
        error_window.setIcon(QMessageBox.Icon.Critical)
        error_window.setWindowTitle("Erro!")

        return error_window

    # Slots utilitários ----------------------------------------------------------------
    def _on_table_selection_changed(self, *_args) -> None:
        self._enable_edit_button()
        self._enable_delete_button()

        self._update_statusbar_with_row_values()

    def _enable_edit_button(self) -> None:
        self.edit_button.setEnabled(self.table.selectionModel().hasSelection())

    def _enable_delete_button(self) -> None:
        self.delete_button.setEnabled(self.table.selectionModel().hasSelection())

    def _update_statusbar_with_row_values(self) -> None:
        selected_rows = self.table.selectionModel().selectedRows()
        row = selected_rows[0].row()
        model = self.table.model()

        values = []
        for col in range(model.columnCount()):
            index = model.index(row, col)
            data = model.data(index)
            if isinstance(data, str):
                values.append(data)

        text = " ".join(values)
        self.status_bar.showMessage(text)
