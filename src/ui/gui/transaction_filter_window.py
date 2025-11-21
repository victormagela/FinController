from collections.abc import Iterable
from dataclasses import dataclass

from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QRadioButton, QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from src.utils.constants import (
    DATE_PATTERN, AMOUNT_PATTERN, INCOME_CATEGORY_TABLE, EXPENSE_CATEGORY_TABLE, ALL_CATEGORIES_TABLE, 
    TRANSACTION_TYPE_TABLE
)
import src.ui.formatter as formatter


@dataclass
class FilterCriteria:
    min_amount: str | None = None
    max_amount: str | None = None

    start_date: str | None = None
    end_date: str | None = None

    type: str | None = None

    category: str | None = None


class TransactionFilterWindow(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # Layouts -----------------------------------------------------------------------------------------------------
        self._main_layout = QVBoxLayout()
        self._form_layout = QFormLayout()
        self._buttons_layout = QHBoxLayout()

        # Line Edits --------------------------------------------------------------------------------------------------
        self._min_amount = QLineEdit()
        self._max_amount = QLineEdit()

        self._start_date = QLineEdit()
        self._end_date = QLineEdit()

        # Combo Boxes -------------------------------------------------------------------------------------------------
        self._type_combobox = QComboBox()
        self._category_combobox = QComboBox()

        # Buttons -----------------------------------------------------------------------------------------------------
        self._amount_order_button = QRadioButton()
        self._date_order_button = QRadioButton()
        self._id_order_button = QRadioButton()
        
        self._ascending_button = QRadioButton()
        self._descending_button = QRadioButton()
        
        self._confirm_button = QPushButton("Confirmar Filtros")
        self._reset_button = QPushButton("Resetar Filtros")

        # Labels ------------------------------------------------------------------------------------------------------
        self._min_amount_label = QLabel("Valor Inicial: ")
        self._max_amount_label = QLabel("Valor Final: ")

        self._start_date_label = QLabel("De: ")
        self._end_date_label = QLabel("Até:  ")

        self._type_label = QLabel("Tipo: ")

        self._category_label = QLabel("Categoria: ")

        self.initUI()
    
    def initUI(self) -> None:
        self.setWindowTitle('Filtrar/Ordenar Transações')

        self._config_layout()
        self._config_lines()
        self._config_comboboxes()
        self._config_buttons()

        self.setLayout(self._main_layout)

    def _config_lines(self) -> None:
        self._min_amount.setValidator(QRegularExpressionValidator(QRegularExpression(AMOUNT_PATTERN)))
        self._max_amount.setValidator(QRegularExpressionValidator(QRegularExpression(AMOUNT_PATTERN)))
        self._start_date.setValidator(QRegularExpressionValidator(QRegularExpression(DATE_PATTERN)))
        self._end_date.setValidator(QRegularExpressionValidator(QRegularExpression(DATE_PATTERN)))

        self._min_amount.setTextMargins(5, 2, 5, 2)
        self._max_amount.setTextMargins(5, 2, 5, 2)
        self._start_date.setTextMargins(5, 2, 5, 2)
        self._end_date.setTextMargins(5, 2, 5, 2)

        self._min_amount.setPlaceholderText('ex: 1.234,50 ou 1234.50')
        self._max_amount.setPlaceholderText('ex: 1.234,50 ou 1234.50')
        self._start_date.setPlaceholderText('dd/mm/aaaa')
        self._end_date.setPlaceholderText('dd/mm/aaaa')

    def _config_comboboxes(self) -> None:
        self._type_combobox.addItem('')
        self._category_combobox.addItem('')

        self._type_combobox.addItems(formatter.capitalize_dict_values(TRANSACTION_TYPE_TABLE).values())
        self._category_combobox.addItems(self._get_category_combobox_items())

        self._type_combobox.currentTextChanged.connect(self._on_type_selection_changed)

    def _config_buttons(self) -> None:
        self._confirm_button.clicked.connect(self._on_confirm_button_clicked)
        self._reset_button.clicked.connect(self._on_reset_button_clicked)

    def _config_labels(self) -> None:
        ...

    def _config_layout(self):
        self._form_layout.addRow(self._min_amount_label, self._min_amount)
        self._form_layout.addRow(self._max_amount_label, self._max_amount)
        
        self._form_layout.addRow(self._start_date_label, self._start_date)
        self._form_layout.addRow(self._end_date_label, self._end_date)

        self._form_layout.addRow(self._type_label, self._type_combobox)

        self._form_layout.addRow(self._category_label, self._category_combobox)

        self._buttons_layout.addWidget(self._confirm_button)
        self._buttons_layout.addWidget(self._reset_button)

        self._main_layout.addLayout(self._buttons_layout)
        self._main_layout.addLayout(self._form_layout)

    # Métodos utilitários e slots -------------------------------------------------------------------------------------
    def _on_confirm_button_clicked(self) -> None:
        print('Confirmando filtros')

    def _on_reset_button_clicked(self) -> None:
        print('Resetando filtros')

    def _on_type_selection_changed(self, *_args) -> None:
        self._category_combobox.clear()
        self._category_combobox.addItem('')
        self._category_combobox.addItems(self._get_category_combobox_items())

    def _get_category_combobox_items(self) -> Iterable[str]:
        match self._type_combobox.currentText():
            case "Receita":
                return formatter.capitalize_dict_values(INCOME_CATEGORY_TABLE).values()

            case "Despesa":
                return formatter.capitalize_dict_values(EXPENSE_CATEGORY_TABLE).values()
            
            case _:
                return formatter.capitalize_dict_values(ALL_CATEGORIES_TABLE).values()