from collections.abc import Iterable
from datetime import date
from copy import deepcopy

from PySide6.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QVBoxLayout, QFormLayout, QComboBox
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from src.utils.constants import (
    TRANSACTION_TYPE_TABLE, INCOME_CATEGORY_TABLE, EXPENSE_CATEGORY_TABLE, DATE_FORMAT, AMOUNT_PATTERN, DATE_PATTERN,
    DESCRIPTION_PATTERN
)

 
class NewTransactionWindow(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._user_input_list: list[dict[str, str]] = []

        self._main_layout = QVBoxLayout()
        self._form_layout = QFormLayout()
        
        # Line Edits --------------------------------------------------------------------------------------------------
        self._amount_line = QLineEdit()
        self._date_line = QLineEdit()
        self._description_line = QLineEdit()

        # Dropdown de categorias e tipos ------------------------------------------------------------------------------
        self._type_combobox = QComboBox()
        self._category_combobox = QComboBox()

        # Botão de confirmação ----------------------------------------------------------------------------------------
        self._confirm_button = QPushButton('Adicionar Transação')

        # Labels ------------------------------------------------------------------------------------------------------
        self._amount_label = QLabel('Valor:')
        self._date_label = QLabel('Data:')
        self._type_label = QLabel('Tipo:')
        self._category_label = QLabel('Categoria:')
        self._description_label = QLabel('Descrição:')

        self.initUI()

    @property
    def user_input_list(self):
        return deepcopy(self._user_input_list)


    def initUI(self) -> None:
        self.setWindowTitle('Nova Transação')

        self._config_lines()
        self._config_button()
        self._config_combobox()
        self._config_layout()

        self.setLayout(self._main_layout)

    def _config_lines(self) -> None:
        self._amount_line.setTextMargins(5, 2, 5, 2)
        self._date_line.setTextMargins(5, 2, 5, 2)
        self._description_line.setTextMargins(5, 2, 5, 2)

        self._amount_line.setPlaceholderText('ex: 1.234,50 ou 1234.50')
        self._date_line.setPlaceholderText('dd/mm/aaaa')
        self._description_line.setPlaceholderText('Campo opcional')

        self._date_line.setText(date.today().strftime(DATE_FORMAT))

        self._amount_line.setValidator(QRegularExpressionValidator(QRegularExpression(AMOUNT_PATTERN)))
        self._date_line.setValidator(QRegularExpressionValidator(QRegularExpression(DATE_PATTERN)))
        self._description_line.setValidator(QRegularExpressionValidator(QRegularExpression(DESCRIPTION_PATTERN)))

        self._amount_line.textChanged.connect(self._on_necessary_fields_filled)
        self._date_line.textChanged.connect(self._on_necessary_fields_filled)

    def _config_combobox(self) -> None:
        self._type_combobox.addItems(TRANSACTION_TYPE_TABLE.values())
        self._category_combobox.addItems(self._get_category_combobox_items())

        self._type_combobox.currentTextChanged.connect(self._on_type_selection_changed)

    def _config_labels(self) -> None:
        ...

    def _config_button(self) -> None:
        self._confirm_button.setEnabled(False)

        self._confirm_button.clicked.connect(self._add_transaction)

    def _config_layout(self) -> None:
        self._form_layout.addRow(self._amount_label, self._amount_line)
        self._form_layout.addRow(self._date_label, self._date_line)
        self._form_layout.addRow(self._type_label, self._type_combobox)
        self._form_layout.addRow(self._category_label, self._category_combobox)
        self._form_layout.addRow(self._description_label, self._description_line)

        self._main_layout.addWidget(self._confirm_button)

        self._main_layout.addLayout(self._form_layout)

    def _add_transaction(self) -> None:
        str_dict = {}
        str_dict['amount'] = self._amount_line.text()
        str_dict['transaction_type'] = self._type_combobox.currentText()
        str_dict['transaction_date'] = self._date_line.text()
        str_dict['category'] = self._category_combobox.currentText()
        str_dict['description'] = self._description_line.text()

        print(f'Adicionando transação: \n'
            f'valor: {self._amount_line.text()}\n'
            f'data: {self._date_line.text()}\n'
            f'tipo: {self._type_combobox.currentText()}\n'
            f'categoria: {self._category_combobox.currentText()}\n'
            f'descrição: {self._description_line.text()}\n'
        )

        self._amount_line.clear()
        self._date_line.clear()
        self._description_line.clear()

        self._user_input_list.append(str_dict)

    def _on_type_selection_changed(self) -> None:
        self._category_combobox.clear()
        self._category_combobox.addItems(self._get_category_combobox_items())

    def _on_necessary_fields_filled(self) -> None:
        if self._amount_line.hasAcceptableInput() and self._date_line.hasAcceptableInput():
            self._confirm_button.setEnabled(True)

        else:
            self._confirm_button.setEnabled(False)

    def _get_category_combobox_items(self) -> Iterable[str]:
        if self._type_combobox.currentText() == 'receita':
            return INCOME_CATEGORY_TABLE.values()

        return EXPENSE_CATEGORY_TABLE.values()