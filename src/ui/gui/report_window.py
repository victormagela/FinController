from datetime import date

from PySide6.QtWidgets import (
    QWidget, QLabel, QGroupBox, QVBoxLayout, QHBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PySide6.QtCore import Qt

import src.ui.formatter as formatter
from src.service.transaction_statistics import TransactionStatistics


class ReportWindow(QDialog):
    def __init__(self, statistics: TransactionStatistics, start_date: date, end_date: date, parent: QWidget = None):
        super().__init__(parent)
        self._statistics: TransactionStatistics = statistics
        self._start_date: date = start_date
        self._end_date: date = end_date

        # Layouts -----------------------------------------------------------------------------------------------------
        self._main_layout = QVBoxLayout()
        self._general_overview_layout = QVBoxLayout()
        self._type_overview_layout = QHBoxLayout()
        self._income_overview_layout = QVBoxLayout()
        self._expense_overview_layout = QVBoxLayout()
        self._breakdown_table_layout = QHBoxLayout()
        self._income_breakdown_layout = QVBoxLayout()
        self._expense_breakdown_layout = QVBoxLayout()

        # QGroupboxes -------------------------------------------------------------------------------------------------
        self._general_overview_box = QGroupBox('Visão Geral')
        self._income_overview_box = QGroupBox('Receitas')
        self._expense_overview_box = QGroupBox('Despesas')
        self._income_breakdown_box = QGroupBox('Breakdown por Categorias de Receita')
        self._expense_breakdown_box = QGroupBox('Breakdown por Categorias de Despesa')

        # QLabels -----------------------------------------------------------------------------------------------------
        self._general_overview_label = QLabel()
        self._income_overview_label = QLabel()
        self._expense_overview_label = QLabel()

        # QTableWidgets -----------------------------------------------------------------------------------------------
        self._income_breakdown_table = QTableWidget()
        self._expense_breakdown_table = QTableWidget()
        
        self._setup_UI()

    def _setup_UI(self) -> None:
        self.setWindowTitle('Relatório')

        self._configure_layouts()
        self._configure_labels()
        self._configure_tables()

        self.setLayout(self._main_layout)

    def _configure_layouts(self) -> None:
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

        self._breakdown_table_layout.addWidget(self._income_breakdown_box)
        self._breakdown_table_layout.addWidget(self._expense_breakdown_box)

        self._main_layout.addWidget(self._general_overview_box)
        self._main_layout.addLayout(self._type_overview_layout)
        self._main_layout.addLayout(self._breakdown_table_layout)
        if not self._statistics.income_transaction_count:
            self._income_breakdown_box.hide()

        if not self._statistics.expense_transaction_count:
            self._expense_breakdown_box.hide()

    def _configure_labels(self) -> None:
        formatted_balance = formatter.format_currency_for_ptbr(self._statistics.balance)

        general_overview_text = (
            f'Período: {formatter.format_date(self._start_date)} até {formatter.format_date(self._end_date)}\n'
            f'Transações: {self._statistics.transaction_count} | Saldo: {formatted_balance}'
        )

        income_overview_text = self._get_income_overview_text()

        expense_overview_text = self._get_expense_overview_text()

        self._general_overview_label.setText(general_overview_text)
        self._income_overview_label.setText(income_overview_text)
        self._expense_overview_label.setText(expense_overview_text)

        self._general_overview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _configure_tables(self) -> None:
        self._configure_income_table()
        self._configure_expense_table()

        if not self._statistics.income_transaction_count:
            self._income_breakdown_table.hide()

        if not self._statistics.expense_transaction_count:
            self._expense_breakdown_table.hide()

    # Métodos utilitários ---------------------------------------------------------------------------------------------
    def _get_income_overview_text(self) -> str:
        if not self._statistics.income_transaction_count:
            return 'Nenhuma receita registrada.'
        
        income_category_with_highest_amount = (
            formatter.format_category(self._statistics.income_category_with_highest_amount)
        )
        income_category_with_most_transactions = (
            formatter.format_category(self._statistics.income_category_with_most_transactions)
        )
        
        return (
            f'Transações: {self._statistics.income_transaction_count}\n'
            f'Total: {formatter.format_currency_for_ptbr(self._statistics.total_income)}\n'
            f'Média: {formatter.format_currency_for_ptbr(self._statistics.average_income)}\n'
            f'Mediana: {formatter.format_currency_for_ptbr(self._statistics.median_income)}\n'
            f'Maior valor: {formatter.format_currency_for_ptbr(self._statistics.highest_income_amount)}\n'
            f'Categoria com maior valor: {income_category_with_highest_amount}\n'
            f'Categoria com maior número de transações: {income_category_with_most_transactions}'
        )

    def _get_expense_overview_text(self) -> str:
        if not self._statistics.expense_transaction_count:
            return 'Nenhuma despesa registrada.'
        
        expense_category_with_highest_amount = (
            formatter.format_category(self._statistics.expense_category_with_highest_amount)
        )
        expense_category_with_most_transactions = (
            formatter.format_category(self._statistics.expense_category_with_most_transactions)
        )
        
        return (
            f'Transações: {self._statistics.expense_transaction_count}\n'
            f'Total: {formatter.format_currency_for_ptbr(self._statistics.total_expense)}\n'
            f'Média: {formatter.format_currency_for_ptbr(self._statistics.average_expense)}\n'
            f'Mediana: {formatter.format_currency_for_ptbr(self._statistics.median_expense)}\n'
            f'Maior valor: {formatter.format_currency_for_ptbr(self._statistics.highest_expense_amount)}\n'
            f'Categoria com maior valor: {expense_category_with_highest_amount}\n'
            f'Categoria com maior número de transações: {expense_category_with_most_transactions}'
        )

    def _configure_income_table(self) -> None:
        if not self._statistics.income_transaction_count:
            return

        table = self._income_breakdown_table
        
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([            
            "Categoria",
            "Qtd.",
            "% Qtd",
            "% Valor",
            "Total"
        ])

        categories = list(self._statistics.total_per_income_category.keys())
        table.setRowCount(len(categories))

        for row, category in enumerate(categories):
            category_name = formatter.format_category(category)

            total = self._statistics.total_per_income_category[category]
            count = self._statistics.count_per_income_category[category]
            amount_percentage = self._statistics.percentage_per_income_category[category]
            count_percentage = self._statistics.count_percentage_per_income_category[category]

            total_str = formatter.format_currency_for_ptbr(total)
            count_str = str(count)
            amount_percentage_str = f"{amount_percentage:.1f}%"
            count_percentage_str = f"{count_percentage:.1f}%"

            table.setItem(row, 0, QTableWidgetItem(category_name))
            table.setItem(row, 1, QTableWidgetItem(count_str))
            table.setItem(row, 2, QTableWidgetItem(count_percentage_str))
            table.setItem(row, 3, QTableWidgetItem(amount_percentage_str))
            table.setItem(row, 4, QTableWidgetItem(total_str))

        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
    
    def _configure_expense_table(self) -> None:
        if not self._statistics.expense_transaction_count:
            return
        
        table = self._expense_breakdown_table
        
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([           
            "Categoria",
            "Qtd.",
            "% Qtd",
            "% Valor",
            "Total"
        ])

        categories = list(self._statistics.total_per_expense_category.keys())
        table.setRowCount(len(categories))

        for row, category in enumerate(categories):
            category_name = formatter.format_category(category)

            total = self._statistics.total_per_expense_category[category]
            count = self._statistics.count_per_expense_category[category]
            amount_percentage = self._statistics.percentage_per_expense_category[category]
            count_percentage = self._statistics.count_percentage_per_expense_category[category]

            total_str = formatter.format_currency_for_ptbr(total)
            count_str = str(count)
            amount_percentage_str = f"{amount_percentage:.1f}%"
            count_percentage_str = f"{count_percentage:.1f}%"

            table.setItem(row, 0, QTableWidgetItem(category_name))
            table.setItem(row, 1, QTableWidgetItem(count_str))
            table.setItem(row, 2, QTableWidgetItem(count_percentage_str))
            table.setItem(row, 3, QTableWidgetItem(amount_percentage_str))
            table.setItem(row, 4, QTableWidgetItem(total_str))

        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)