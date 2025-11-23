from PySide6.QtWidgets import QWidget, QLabel, QGroupBox, QVBoxLayout, QHBoxLayout, QDialog, QTableWidget

import src.ui.formatter as formatter


class ReportWindow(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

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

    def _configure_labels(self) -> None:
        general_overview_text = (
            f'Período: formatted_start_date até formatted_end_date\n'
            f'Transações: transaction_count | Saldo: formatted_balance'
        )

        income_overview_text = (
            f'Transações: income_count\n'
            f'Total: total_income\n'
            f'Média: average_income\n'
            f'Mediana: median_income\n'
            f'Maior valor: highest_income_amount\n'
            f'Categoria com maior valor: income_category_with_highest_amount\n'
            f'Categoria com maior número de transações: income_category_with_most_transactions'
        )

        expense_overview_text = (
            f'Transações: expense_count\n'
            f'Total: total_expense\n'
            f'Média: average_expense\n'
            f'Mediana: median_expense\n'
            f'Maior valor: highest_expense_amount\n'
            f'Categoria com maior valor: expense_category_with_highest_amount\n'
            f'Categoria com maior número de transações: expense_category_with_most_transactions'
        )

        self._general_overview_label.setText(general_overview_text)
        self._income_overview_label.setText(income_overview_text)
        self._expense_overview_label.setText(expense_overview_text)

    def _configure_tables(self) -> None:
        ...