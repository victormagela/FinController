from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum, StrEnum

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QRadioButton,
    QLabel,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QButtonGroup,
)
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from src.utils.constants import (
    DATE_PATTERN,
    AMOUNT_PATTERN,
    INCOME_CATEGORY_TABLE,
    EXPENSE_CATEGORY_TABLE,
    ALL_CATEGORIES_TABLE,
    TRANSACTION_TYPE_TABLE,
)
import src.ui.formatter as formatter


class SortingFieldCode(Enum):
    ID = 0
    AMOUNT = 1
    DATE = 2


class SortingOrderCode(StrEnum):
    ASCENDING = "crescente"
    DESCENDING = "decrescente"


@dataclass
class SortingCriteria:
    field: SortingFieldCode = SortingFieldCode.ID
    order: SortingOrderCode = SortingOrderCode.ASCENDING


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

        self._filter_criteria = FilterCriteria()
        self._sorting_criteria = SortingCriteria()
        self._clear_filters = False

        self.field_map: dict[int, SortingFieldCode] = {
            1: SortingFieldCode.ID,
            2: SortingFieldCode.AMOUNT,
            3: SortingFieldCode.DATE,
        }
        self.order_map: dict[int, SortingOrderCode] = {
            1: SortingOrderCode.ASCENDING,
            2: SortingOrderCode.DESCENDING,
        }

        # Layouts ----------------------------------------------------------------------
        self._main_layout = QVBoxLayout()
        self._form_layout = QFormLayout()
        self._buttons_layout = QHBoxLayout()
        self._sorting_layout = QHBoxLayout()
        self._sort_criteria_layout = QVBoxLayout()
        self._sort_order_layout = QVBoxLayout()

        # Group boxes ------------------------------------------------------------------
        self._sort_criteria_box = QGroupBox("Ordenar por: ")
        self._sort_order_box = QGroupBox("Direção: ")

        # Group buttons ----------------------------------------------------------------
        self._sort_field_group = QButtonGroup()
        self._sort_order_group = QButtonGroup()

        # Line Edits -------------------------------------------------------------------
        self._min_amount = QLineEdit()
        self._max_amount = QLineEdit()

        self._start_date = QLineEdit()
        self._end_date = QLineEdit()

        # Combo Boxes ------------------------------------------------------------------
        self._type_combobox = QComboBox()
        self._category_combobox = QComboBox()

        # Buttons ----------------------------------------------------------------------
        self._amount_sorting_button = QRadioButton("Valor")
        self._date_sorting_button = QRadioButton("Data")
        self._id_sorting_button = QRadioButton("ID")

        self._ascending_button = QRadioButton("Crescente")
        self._descending_button = QRadioButton("Decrescente")

        self._confirm_button = QPushButton("Confirmar")
        self._reset_button = QPushButton("Limpar Filtros")

        # Labels -----------------------------------------------------------------------
        self._min_amount_label = QLabel("Valor Inicial: ")
        self._max_amount_label = QLabel("Valor Final: ")

        self._start_date_label = QLabel("De: ")
        self._end_date_label = QLabel("Até:  ")

        self._type_label = QLabel("Tipo: ")

        self._category_label = QLabel("Categoria: ")

        self.initUI()

    @property
    def filter_criteria(self) -> FilterCriteria:
        return self._filter_criteria

    @property
    def sorting_criteria(self) -> SortingCriteria:
        return self._sorting_criteria

    @property
    def clear_filters(self) -> bool:
        return self._clear_filters

    def initUI(self) -> None:
        self.setWindowTitle("Filtrar/Ordenar Transações")

        self._config_layout()
        self._config_lines()
        self._config_comboboxes()
        self._config_buttons()

        self.setLayout(self._main_layout)

    def _config_lines(self) -> None:
        self._min_amount.setValidator(
            QRegularExpressionValidator(QRegularExpression(AMOUNT_PATTERN))
        )
        self._max_amount.setValidator(
            QRegularExpressionValidator(QRegularExpression(AMOUNT_PATTERN))
        )
        self._start_date.setValidator(
            QRegularExpressionValidator(QRegularExpression(DATE_PATTERN))
        )
        self._end_date.setValidator(
            QRegularExpressionValidator(QRegularExpression(DATE_PATTERN))
        )

        self._min_amount.setTextMargins(5, 2, 5, 2)
        self._max_amount.setTextMargins(5, 2, 5, 2)
        self._start_date.setTextMargins(5, 2, 5, 2)
        self._end_date.setTextMargins(5, 2, 5, 2)

        self._min_amount.setPlaceholderText("ex: 1.234,50 ou 1234.50")
        self._max_amount.setPlaceholderText("ex: 1.234,50 ou 1234.50")
        self._start_date.setPlaceholderText("dd/mm/aaaa")
        self._end_date.setPlaceholderText("dd/mm/aaaa")

        self._min_amount.textChanged.connect(self._on_any_field_filled)
        self._max_amount.textChanged.connect(self._on_any_field_filled)
        self._start_date.textChanged.connect(self._on_any_field_filled)
        self._end_date.textChanged.connect(self._on_any_field_filled)

    def _config_comboboxes(self) -> None:
        self._type_combobox.addItem("")
        self._category_combobox.addItem("")

        self._type_combobox.addItems(
            formatter.capitalize_dict_values(TRANSACTION_TYPE_TABLE).values()
        )
        self._category_combobox.addItems(self._get_category_combobox_items())

        self._type_combobox.currentTextChanged.connect(self._on_type_selection_changed)
        self._type_combobox.currentTextChanged.connect(
            self._on_combobox_selection_changed
        )
        self._category_combobox.currentTextChanged.connect(
            self._on_combobox_selection_changed
        )

    def _config_buttons(self) -> None:
        self._confirm_button.setEnabled(False)

        self._confirm_button.clicked.connect(self._on_confirm_button_clicked)
        self._reset_button.clicked.connect(self._on_reset_button_clicked)

        self._id_sorting_button.setChecked(True)
        self._ascending_button.setChecked(True)

        self._sort_field_group.addButton(self._id_sorting_button, 1)
        self._sort_field_group.addButton(self._amount_sorting_button, 2)
        self._sort_field_group.addButton(self._date_sorting_button, 3)

        self._sort_order_group.addButton(self._ascending_button, 1)
        self._sort_order_group.addButton(self._descending_button, 2)

    def _config_labels(self) -> None: ...

    def _config_layout(self):
        self._form_layout.addRow(self._min_amount_label, self._min_amount)
        self._form_layout.addRow(self._max_amount_label, self._max_amount)

        self._form_layout.addRow(self._start_date_label, self._start_date)
        self._form_layout.addRow(self._end_date_label, self._end_date)

        self._form_layout.addRow(self._type_label, self._type_combobox)

        self._form_layout.addRow(self._category_label, self._category_combobox)

        self._buttons_layout.addWidget(self._confirm_button)
        self._buttons_layout.addWidget(self._reset_button)

        self._sort_criteria_layout.addWidget(self._id_sorting_button)
        self._sort_criteria_layout.addWidget(self._amount_sorting_button)
        self._sort_criteria_layout.addWidget(self._date_sorting_button)

        self._sort_order_layout.addWidget(self._ascending_button)
        self._sort_order_layout.addWidget(self._descending_button)

        self._sort_criteria_box.setLayout(self._sort_criteria_layout)

        self._sort_order_box.setLayout(self._sort_order_layout)

        self._sorting_layout.addWidget(self._sort_criteria_box)
        self._sorting_layout.addWidget(self._sort_order_box)

        self._main_layout.addLayout(self._buttons_layout)
        self._main_layout.addLayout(self._form_layout)
        self._main_layout.addLayout(self._sorting_layout)

    # Métodos utilitários e slots ------------------------------------------------------
    def _on_any_field_filled(self, *_args) -> None:
        if (
            self._min_amount.text()
            or self._max_amount.text()
            or self._start_date.text()
            or self._end_date.text()
        ):
            self._confirm_button.setEnabled(True)

        else:
            self._confirm_button.setEnabled(False)

    def _on_combobox_selection_changed(self, *_args) -> None:
        if self._type_combobox.currentText() or self._category_combobox.currentText():
            self._confirm_button.setEnabled(True)

        else:
            self._confirm_button.setEnabled(False)

    def _on_type_selection_changed(self, *_args) -> None:
        self._category_combobox.clear()
        self._category_combobox.addItem("")
        self._category_combobox.addItems(self._get_category_combobox_items())

    def _on_confirm_button_clicked(self) -> None:
        self._build_filter_criteria()
        self._build_sorting_criteria()

        self.accept()

    def _on_reset_button_clicked(self) -> None:
        self._clear_filters = True

        self.accept()

    def _get_category_combobox_items(self) -> Iterable[str]:
        match self._type_combobox.currentText():
            case "Receita":
                return formatter.capitalize_dict_values(INCOME_CATEGORY_TABLE).values()

            case "Despesa":
                return formatter.capitalize_dict_values(EXPENSE_CATEGORY_TABLE).values()

            case _:
                return formatter.capitalize_dict_values(ALL_CATEGORIES_TABLE).values()

    def _build_filter_criteria(self) -> None:
        self._filter_criteria.min_amount = self._min_amount.text() or None
        self._filter_criteria.max_amount = self._max_amount.text() or None

        self._filter_criteria.start_date = self._start_date.text() or None
        self._filter_criteria.end_date = self._end_date.text() or None

        self._filter_criteria.type = self._type_combobox.currentText() or None

        self._filter_criteria.category = self._category_combobox.currentText() or None

    def _build_sorting_criteria(self) -> None:
        self.sorting_criteria.field = self.field_map.get(
            self._sort_field_group.checkedId(), self.sorting_criteria.field
        )
        self.sorting_criteria.order = self.order_map.get(
            self._sort_order_group.checkedId(), self.sorting_criteria.order
        )
