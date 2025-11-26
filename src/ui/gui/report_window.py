from datetime import date

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QFrame,
    QHeaderView,
    QTabWidget,
)
from PySide6.QtCore import Qt

import src.ui.formatter as formatter
from src.service.transaction_statistics import TransactionStatistics
from src.utils.constants import WINDOW_ICON


class ReportWindow(QDialog):
    def __init__(
        self,
        statistics: TransactionStatistics,
        start_date: date,
        end_date: date,
        parent: QWidget = None,
    ):
        super().__init__(parent)
        self._statistics: TransactionStatistics = statistics
        self._start_date: date = start_date
        self._end_date: date = end_date

        # Layouts ----------------------------------------------------------------------
        self._main_layout = QVBoxLayout()
        self._card_layout = QVBoxLayout()
        self._general_overview_layout = QVBoxLayout()
        self._type_overview_layout = QHBoxLayout()
        self._income_overview_layout = QVBoxLayout()
        self._expense_overview_layout = QVBoxLayout()
        self._income_breakdown_layout = QVBoxLayout()
        self._expense_breakdown_layout = QVBoxLayout()

        # Frame ------------------------------------------------------------------------
        self._main_card = QFrame()

        # Tabs -------------------------------------------------------------------------
        self._breakdown_tabs = QTabWidget()

        # QGroupboxes ------------------------------------------------------------------
        self._general_overview_box = QGroupBox("Visão Geral")
        self._income_overview_box = QGroupBox("Receitas")
        self._expense_overview_box = QGroupBox("Despesas")
        self._income_breakdown_box = QGroupBox("Breakdown por Categorias de Receita")
        self._expense_breakdown_box = QGroupBox("Breakdown por Categorias de Despesa")

        # QLabels ----------------------------------------------------------------------
        self._title_label = QLabel("Relatório de Transações")
        self._general_overview_label = QLabel()
        self._income_overview_title = QLabel("Receitas")
        self._expense_overview_title = QLabel("Despesas")
        self._income_overview_label = QLabel()
        self._expense_overview_label = QLabel()

        # QTableWidgets ----------------------------------------------------------------
        self._income_breakdown_table = QTableWidget()
        self._expense_breakdown_table = QTableWidget()

        self._setup_UI()

    def _setup_UI(self) -> None:
        self.setWindowTitle("Relatório")
        self.setWindowIcon(WINDOW_ICON)

        self._config_labels()
        self._config_frame()
        self._config_layouts()
        self._config_tables()

        self.setLayout(self._main_layout)

    def _config_layouts(self) -> None:
        self._general_overview_layout.addWidget(self._general_overview_label)
        self._general_overview_box.setLayout(self._general_overview_layout)

        self._income_overview_layout.addWidget(self._income_overview_label)
        self._income_overview_box.setLayout(self._income_overview_layout)

        self._expense_overview_layout.addWidget(self._expense_overview_label)
        self._expense_overview_box.setLayout(self._expense_overview_layout)

        self._type_overview_layout.addWidget(self._income_overview_box)
        self._type_overview_layout.addWidget(self._expense_overview_box)

        self._income_breakdown_layout.addWidget(self._income_breakdown_table)
        self._income_breakdown_box.setLayout(self._income_breakdown_layout)

        self._expense_breakdown_layout.addWidget(self._expense_breakdown_table)
        self._expense_breakdown_box.setLayout(self._expense_breakdown_layout)

        if self._statistics.income_transaction_count:
            self._breakdown_tabs.addTab(self._income_breakdown_box, "Receitas")

        if self._statistics.expense_transaction_count:
            self._breakdown_tabs.addTab(self._expense_breakdown_box, "Despesas")

        self._card_layout.addWidget(
            self._title_label, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self._card_layout.addSpacing(8)
        self._card_layout.addWidget(self._general_overview_box)
        self._card_layout.addSpacing(8)
        self._card_layout.addLayout(self._type_overview_layout)
        self._card_layout.addSpacing(12)
        if self._breakdown_tabs.count() > 0:
            self._card_layout.addWidget(self._breakdown_tabs)

        self._card_layout.setContentsMargins(16, 16, 16, 16)
        self._card_layout.setSpacing(12)

        self._main_layout.addWidget(self._main_card)
        self._main_layout.setContentsMargins(16, 16, 16, 16)
        self._main_layout.setSpacing(12)

        if not self._statistics.income_transaction_count:
            self._income_breakdown_box.hide()

        if not self._statistics.expense_transaction_count:
            self._expense_breakdown_box.hide()

    def _config_labels(self) -> None:
        self._title_label.setObjectName("TitleLabel")

        self._income_overview_title.setProperty("class", "overviewTitle")
        self._expense_overview_title.setProperty("class", "overviewTitle")

        self._income_overview_label.setProperty("class", "overviewBody")
        self._expense_overview_label.setProperty("class", "overviewBody")
        self._general_overview_label.setProperty("class", "overviewBody")

        formatted_balance = formatter.format_currency_for_ptbr(self._statistics.balance)

        start_date_str = formatter.format_date(self._start_date)
        end_date_str = formatter.format_date(self._end_date)

        general_overview_text = (
            f"Período: {start_date_str} até {end_date_str}\n"
            f"Transações: {self._statistics.transaction_count} | "
            f"Saldo: {formatted_balance}"
        )

        income_overview_text = self._get_income_overview_text()

        expense_overview_text = self._get_expense_overview_text()

        self._general_overview_label.setText(general_overview_text)
        self._income_overview_label.setText(income_overview_text)
        self._expense_overview_label.setText(expense_overview_text)

        self._general_overview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _config_tables(self) -> None:
        self._config_income_table()
        self._config_expense_table()

        for table in (self._income_breakdown_table, self._expense_breakdown_table):
            header = table.horizontalHeader()
            header.setHighlightSections(False)
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            table.setWordWrap(False)
            table.setAlternatingRowColors(True)
            table.setShowGrid(False)
            table.verticalHeader().setVisible(False)
            table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            table.setStyleSheet(
                """
            QTableWidget {
                font-size: 11pt;
                font-weight: 400;
            }
            QHeaderView::section {
                font-size: 10pt;
                font-weight: 500;
            }
            """
            )

        if not self._statistics.income_transaction_count:
            self._income_breakdown_table.hide()

        if not self._statistics.expense_transaction_count:
            self._expense_breakdown_table.hide()

    def _config_frame(self) -> None:
        self._main_card.setLayout(self._card_layout)
        self._main_card.setObjectName("Card")

    # Métodos utilitários --------------------------------------------------------------
    def _get_income_overview_text(self) -> str:
        if not self._statistics.income_transaction_count:
            return "Nenhuma receita registrada."

        income_category_with_highest_amount = formatter.format_category(
            self._statistics.income_category_with_highest_amount
        )
        income_category_with_most_transactions = formatter.format_category(
            self._statistics.income_category_with_most_transactions
        )

        return (
            f"Transações: {self._statistics.income_transaction_count}\n"
            f"Total: {
                formatter.format_currency_for_ptbr(
                    self._statistics.total_income
                )
            }\n"
            f"Média: {
                formatter.format_currency_for_ptbr(
                    self._statistics.average_income
                    )
            }\n"
            f"Mediana: {
                formatter.format_currency_for_ptbr(
                    self._statistics.median_income
                )
            }\n"
            f"Maior valor: {
                formatter.format_currency_for_ptbr(
                    self._statistics.highest_income_amount
                )
            }\n"
            f"Categoria com maior valor: {income_category_with_highest_amount}\n"
            f"Categoria com maior número de transações: {
                income_category_with_most_transactions
            }"
        )

    def _get_expense_overview_text(self) -> str:
        if not self._statistics.expense_transaction_count:
            return "Nenhuma despesa registrada."

        expense_category_with_highest_amount = formatter.format_category(
            self._statistics.expense_category_with_highest_amount
        )
        expense_category_with_most_transactions = formatter.format_category(
            self._statistics.expense_category_with_most_transactions
        )

        return (
            f"Transações: {self._statistics.expense_transaction_count}\n"
            f"Total: {
                formatter.format_currency_for_ptbr(self._statistics.total_expense)
            }\n"
            f"Média: {
                formatter.format_currency_for_ptbr(self._statistics.average_expense)
            }\n"
            f"Mediana: {
                formatter.format_currency_for_ptbr(self._statistics.median_expense)
            }\n"
            f"Maior valor: {
                formatter.format_currency_for_ptbr(
                    self._statistics.highest_expense_amount
                )
            }\n"
            f"Categoria com maior valor: {
                expense_category_with_highest_amount
            }\n"
            f"Categoria com maior número de transações: {
                expense_category_with_most_transactions
            }"
        )

    def _config_income_table(self) -> None:
        if not self._statistics.income_transaction_count:
            return

        table = self._income_breakdown_table

        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(
            ["Categoria", "Qtd.", "% Qtd", "% Valor", "Total"]
        )

        categories = list(self._statistics.total_per_income_category.keys())
        table.setRowCount(len(categories))

        for row, category in enumerate(categories):
            category_name = formatter.format_category(category)

            total = self._statistics.total_per_income_category[category]
            count = self._statistics.count_per_income_category[category]
            amount_percentage = self._statistics.percentage_per_income_category[
                category
            ]
            count_percentage = self._statistics.count_percentage_per_income_category[
                category
            ]

            total_str = formatter.format_currency_for_ptbr(total)
            count_str = str(count)
            amount_percentage_str = f"{amount_percentage:.1f}%"
            count_percentage_str = f"{count_percentage:.1f}%"

            table.setItem(row, 0, QTableWidgetItem(category_name))
            table.setItem(row, 1, QTableWidgetItem(count_str))
            table.setItem(row, 2, QTableWidgetItem(count_percentage_str))
            table.setItem(row, 3, QTableWidgetItem(amount_percentage_str))
            table.setItem(row, 4, QTableWidgetItem(total_str))

    def _config_expense_table(self) -> None:
        if not self._statistics.expense_transaction_count:
            return

        table = self._expense_breakdown_table

        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(
            ["Categoria", "Qtd.", "% Qtd", "% Valor", "Total"]
        )

        categories = list(self._statistics.total_per_expense_category.keys())
        table.setRowCount(len(categories))

        for row, category in enumerate(categories):
            category_name = formatter.format_category(category)

            total = self._statistics.total_per_expense_category[category]
            count = self._statistics.count_per_expense_category[category]
            amount_percentage = self._statistics.percentage_per_expense_category[
                category
            ]
            count_percentage = self._statistics.count_percentage_per_expense_category[
                category
            ]

            total_str = formatter.format_currency_for_ptbr(total)
            count_str = str(count)
            amount_percentage_str = f"{amount_percentage:.1f}%"
            count_percentage_str = f"{count_percentage:.1f}%"

            table.setItem(row, 0, QTableWidgetItem(category_name))
            table.setItem(row, 1, QTableWidgetItem(count_str))
            table.setItem(row, 2, QTableWidgetItem(count_percentage_str))
            table.setItem(row, 3, QTableWidgetItem(amount_percentage_str))
            table.setItem(row, 4, QTableWidgetItem(total_str))
