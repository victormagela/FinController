from collections.abc import Iterable
from datetime import date
from copy import deepcopy

from PySide6.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QGridLayout, QComboBox
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from src.utils.constants import TRANSACTION_TYPE_TABLE, INCOME_CATEGORY_TABLE, EXPENSE_CATEGORY_TABLE, DATE_FORMAT

 
class NewTransactionWindow(QDialog):
    # Padrões regex para validação de formato de dados
    AMOUNT_PATTERN: str = r'^\d+([.,]\d{1,2})?$'
    DATE_PATTERN: str = r'^\d{2}/\d{2}/\d{4}$'

    def __init__(self, parent = None):
        super().__init__(parent)
        self._user_input_list: list[dict[str, str]] = []

        self._grid_layout = QGridLayout()
        
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

        self.setLayout(self._grid_layout)

    def _config_lines(self) -> None:
        self._amount_line.setTextMargins(5, 2, 5, 2)
        self._date_line.setTextMargins(5, 2, 5, 2)
        self._description_line.setTextMargins(5, 2, 5, 2)

        self._amount_line.setPlaceholderText('ex: 1.234,50 ou 1234.50')
        self._date_line.setPlaceholderText('dd/mm/aaaa')
        self._description_line.setPlaceholderText('ex: Almoço de domingo')

        self._date_line.setText(date.today().strftime(DATE_FORMAT))

        self._amount_line.setValidator(QRegularExpressionValidator(QRegularExpression(self.AMOUNT_PATTERN)))
        self._date_line.setValidator(QRegularExpressionValidator(QRegularExpression(self.DATE_PATTERN)))

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
        self._grid_layout.addWidget(self._amount_label, 0, 0)
        self._grid_layout.addWidget(self._amount_line, 0, 1)
        self._grid_layout.addWidget(self._date_label, 1, 0)
        self._grid_layout.addWidget(self._date_line, 1, 1)
        self._grid_layout.addWidget(self._type_label, 2, 0)
        self._grid_layout.addWidget(self._type_combobox, 2, 1)
        self._grid_layout.addWidget(self._category_label, 3, 0)
        self._grid_layout.addWidget(self._category_combobox, 3, 1)
        self._grid_layout.addWidget(self._description_label, 4, 0)
        self._grid_layout.addWidget(self._description_line, 4, 1)

        self._grid_layout.addWidget(self._confirm_button, 6, 1)

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