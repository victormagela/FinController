from collections.abc import Iterable
from datetime import date
from copy import deepcopy
from enum import Enum

from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QWidget,
    QFrame,
)
from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QRegularExpressionValidator

from src.utils.constants import (
    TRANSACTION_TYPE_TABLE,
    INCOME_CATEGORY_TABLE,
    EXPENSE_CATEGORY_TABLE,
    AMOUNT_PATTERN,
    DATE_PATTERN,
    DESCRIPTION_PATTERN,
    WINDOW_ICON,
)
from src.models.transaction import Transaction
import src.ui.formatter as formatter


class DialogMode(Enum):
    CREATEMODE = 0
    EDITMODE = 1


class TransactionFormWindow(QDialog):
    def __init__(
        self,
        parent: QWidget = None,
        mode: DialogMode = DialogMode.CREATEMODE,
        transaction: Transaction = None,
    ):
        super().__init__(parent)
        if transaction is not None:
            self._transaction = transaction

        self._main_layout = QVBoxLayout()

        self._main_card = QFrame()
        self._card_layout = QVBoxLayout()

        self._form_layout = QFormLayout()

        # Line Edits -------------------------------------------------------------------
        self._amount_line = QLineEdit()
        self._date_line = QLineEdit()
        self._description_line = QLineEdit()

        # Dropdown de categorias e tipos -----------------------------------------------
        self._type_combobox = QComboBox()
        self._category_combobox = QComboBox()

        # Botão de confirmação ---------------------------------------------------------
        self._confirm_button = QPushButton()

        # Labels -----------------------------------------------------------------------
        self.title_label = QLabel()

        self._amount_label = QLabel("Valor:")
        self._date_label = QLabel("Data:")
        self._type_label = QLabel("Tipo:")
        self._category_label = QLabel("Categoria:")
        self._description_label = QLabel("Descrição:")

        if mode == DialogMode.CREATEMODE:
            self._user_input_list: list[dict[str, str]] = []

        if mode == DialogMode.EDITMODE:
            self._user_input_dict: dict[str, str] = {}

        self._configure_user_interface(mode)

    @property
    def user_input_list(self) -> list[dict[str, str]]:
        return deepcopy(self._user_input_list)

    @property
    def user_input_dict(self) -> dict[str, str]:
        return deepcopy(self._user_input_dict)

    def _configure_user_interface(self, mode) -> None:
        self.setWindowIcon(WINDOW_ICON)

        if mode == DialogMode.CREATEMODE:
            self.setWindowTitle("Nova Transação")

        if mode == DialogMode.EDITMODE:
            self.setWindowTitle("Editar Transação")

        self._config_labels(mode)
        self._config_lines(mode)
        self._config_combobox(mode)
        self._config_button(mode)
        self._config_frame()
        self._config_layout()

        self.setLayout(self._main_layout)

    def _config_labels(self, mode) -> None:
        if mode == DialogMode.CREATEMODE:
            self.title_label.setText("Nova Transação")

        else:
            self.title_label.setText("Editar Transação")

    def _config_lines(self, mode) -> None:
        self._description_line.setValidator(
            QRegularExpressionValidator(QRegularExpression(DESCRIPTION_PATTERN))
        )
        if mode == DialogMode.CREATEMODE:
            self._date_line.setText(formatter.format_date(date.today()))

            self._amount_line.setValidator(
                QRegularExpressionValidator(QRegularExpression(AMOUNT_PATTERN))
            )
            self._date_line.setValidator(
                QRegularExpressionValidator(QRegularExpression(DATE_PATTERN))
            )

            self._amount_line.textChanged.connect(self._on_necessary_fields_filled)
            self._date_line.textChanged.connect(self._on_necessary_fields_filled)

        else:
            self._amount_line.setText(
                formatter.format_currency_for_ptbr(self._transaction.amount)
            )
            self._date_line.setText(
                formatter.format_date(self._transaction.transaction_date)
            )
            self._description_line.setText(self._transaction.description)

            self._amount_line.setDisabled(True)
            self._date_line.setDisabled(True)

        self._amount_line.setTextMargins(5, 2, 5, 2)
        self._date_line.setTextMargins(5, 2, 5, 2)
        self._description_line.setTextMargins(5, 2, 5, 2)

        self._amount_line.setPlaceholderText("ex: 1.234,50 ou 1234.50")
        self._date_line.setPlaceholderText("dd/mm/aaaa")
        self._description_line.setPlaceholderText("Campo opcional")

    def _config_combobox(self, mode) -> None:
        self._type_combobox.addItems(
            formatter.capitalize_dict_values(TRANSACTION_TYPE_TABLE).values()
        )

        if mode == DialogMode.CREATEMODE:
            self._type_combobox.currentTextChanged.connect(
                self._on_type_selection_changed
            )
            self._category_combobox.addItems(self._get_category_combobox_items())

        else:
            self._type_combobox.setCurrentText(
                formatter.format_transaction_type(self._transaction.transaction_type)
            )
            self._type_combobox.setDisabled(True)

            self._category_combobox.addItems(self._get_category_combobox_items())
            self._category_combobox.setCurrentText(
                formatter.format_category(self._transaction.category)
            )

    def _config_button(self, mode) -> None:
        if mode == DialogMode.CREATEMODE:
            self._confirm_button.setEnabled(False)
            self._confirm_button.setText("Adicionar Transação")
            self._confirm_button.clicked.connect(self._on_add_transaction_clicked)

        else:
            self._confirm_button.setText("Editar Transação")
            self._confirm_button.clicked.connect(self._on_edit_transaction_clicked)

    def _config_layout(self) -> None:
        self._form_layout.addRow(self._amount_label, self._amount_line)
        self._form_layout.addRow(self._date_label, self._date_line)
        self._form_layout.addRow(self._type_label, self._type_combobox)
        self._form_layout.addRow(self._category_label, self._category_combobox)
        self._form_layout.addRow(self._description_label, self._description_line)

        self._main_layout.addWidget(self._main_card)

        self._card_layout.addWidget(
            self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self._card_layout.addLayout(self._form_layout)
        self._card_layout.addWidget(self._confirm_button)

    def _config_frame(self) -> None:
        self.setLayout(self._card_layout)

    # Slots ----------------------------------------------------------------------------
    def _on_add_transaction_clicked(self) -> None:
        str_dict = {}
        str_dict["amount"] = self._amount_line.text()
        str_dict["transaction_type"] = self._type_combobox.currentText()
        str_dict["transaction_date"] = self._date_line.text()
        str_dict["category"] = self._category_combobox.currentText()
        description = self._description_line.text().strip()
        if description:
            str_dict["description"] = description

        self._amount_line.clear()
        self._date_line.clear()
        self._description_line.clear()

        self._user_input_list.append(str_dict)

    def _on_edit_transaction_clicked(self) -> None:
        str_dict = {}
        str_dict["category"] = self._category_combobox.currentText()
        description = self._description_line.text().strip()
        if description:
            str_dict["description"] = description

        self._user_input_dict.update(str_dict)
        self.destroy()

    def _on_type_selection_changed(self, *_args) -> None:
        self._category_combobox.clear()
        self._category_combobox.addItems(self._get_category_combobox_items())

    def _on_necessary_fields_filled(self, *_args) -> None:
        if (
            self._amount_line.hasAcceptableInput()
            and self._date_line.hasAcceptableInput()
        ):
            self._confirm_button.setEnabled(True)
        else:
            self._confirm_button.setEnabled(False)

    def _get_category_combobox_items(self) -> Iterable[str]:
        match self._type_combobox.currentText():
            case "Receita":
                return formatter.capitalize_dict_values(INCOME_CATEGORY_TABLE).values()

            case "Despesa":
                return formatter.capitalize_dict_values(EXPENSE_CATEGORY_TABLE).values()
