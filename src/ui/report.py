from datetime import date
from rich.panel import Panel
from rich.table import Table

from src.service.transaction_statistics import TransactionStatistics
import src.service.transaction_formatter as formatter
from src.ui.panel_table_builder import PanelBuilder, GraphTableBuilder

class ReportConstructor:
    def __init__(self, statistics: TransactionStatistics, start_date: date, end_date: date):
        self._statistics: TransactionStatistics = statistics
        self._start_date: date = start_date
        self._end_date: date = end_date

    def generate_full_report(self) -> tuple[Panel | Table]:
        overview_text = self._compose_overview_text()
        income_overview_text = self._compose_income_overview_text()
        expense_overview_text = self._compose_expense_overview_text()

        overview_panel = PanelBuilder.build_general_overview_panel(overview_text)
        income_overview_panel = PanelBuilder.build_income_overview_panel(income_overview_text)
        expense_overview_panel = PanelBuilder.build_expense_overview_panel(expense_overview_text)

        income_table_row_content = self._get_income_report_table_content()
        income_report_table = GraphTableBuilder.build_income_report_table(income_table_row_content)

        expense_table_row_content = self._get_expense_report_table_content()
        expense_report_table = GraphTableBuilder.build_expense_report_table(expense_table_row_content)

        return overview_panel, income_overview_panel, expense_overview_panel, income_report_table, expense_report_table



    def _compose_overview_text(self) -> str:
        formatted_start_date = formatter.format_date(self._start_date)
        formatted_end_date = formatter.format_date(self._end_date)
        transaction_count = self._statistics.transaction_count
        formatted_balance = formatter.format_currency_for_ptbr(self._statistics.balance)
        return (
            f'Período: {formatted_start_date} até {formatted_end_date}\n'
            f'Transações: {transaction_count} | Saldo: {formatted_balance}'
        )

    def _compose_income_overview_text(self) -> str:
        if self._statistics.income_category_with_highest_amount is None \
        and self._statistics.income_category_with_most_transactions is None:
            return 'nenhuma receita encontrada'
        
        income_count = self._statistics.income_transaction_count
        total_income = formatter.format_currency_for_ptbr(self._statistics.total_income)
        average_income = formatter.format_currency_for_ptbr(self._statistics.average_income)
        median_income = formatter.format_currency_for_ptbr(self._statistics.median_income)
        highest_income_amount = formatter.format_currency_for_ptbr(self._statistics.highest_income_amount)
        income_category_with_highest_amount = (
            formatter.format_category(self._statistics.income_category_with_highest_amount)
        )
        income_category_with_most_transactions = (
            formatter.format_category(self._statistics.income_category_with_most_transactions)
        )
        return (
            f'Transações: {income_count}\n'
            f'Total: {total_income}\n'
            f'Média: {average_income}\n'
            f'Mediana: {median_income}\n'
            f'Maior valor: {highest_income_amount}\n'
            f'Categoria com maior valor: {income_category_with_highest_amount}\n'
            f'Categoria com maior número de transações: {income_category_with_most_transactions}'
        )
    
    def _compose_expense_overview_text(self) -> str:
        if self._statistics.expense_category_with_highest_amount is None \
        and self._statistics.expense_category_with_most_transactions is None:
            return 'nenhuma receita encontrada'
        
        expense_count = self._statistics.expense_transaction_count
        total_expense = formatter.format_currency_for_ptbr(self._statistics.total_expense)
        average_expense = formatter.format_currency_for_ptbr(self._statistics.average_expense)
        median_expense = formatter.format_currency_for_ptbr(self._statistics.median_expense)
        highest_expense_amount = formatter.format_currency_for_ptbr(self._statistics.highest_expense_amount)
        expense_category_with_highest_amount = (
            formatter.format_category(self._statistics.expense_category_with_highest_amount)
        )
        expense_category_with_most_transactions = (
            formatter.format_category(self._statistics.expense_category_with_most_transactions)
        )
        return (
            f'Transações: {expense_count}\n'
            f'Total: {total_expense}\n'
            f'Média: {average_expense}\n'
            f'Mediana: {median_expense}\n'
            f'Maior valor: {highest_expense_amount}\n'
            f'Categoria com maior valor: {expense_category_with_highest_amount}\n'
            f'Categoria com maior número de transações: {expense_category_with_most_transactions}'
        )
    
    def _get_income_report_table_content(self) -> list[list[str]]:
        if not self._statistics.total_per_income_category:
            return []
        
        rows = []

        for category in self._statistics.total_per_income_category:
            category_name = category.value
            total = self._statistics.total_per_income_category[category]
            count = self._statistics.count_per_income_category[category]
            amount_percentage = self._statistics.percentage_per_income_category[category]
            count_percentage = self._statistics.count_percentage_per_income_category[category]

            total_str = formatter.format_currency_for_ptbr(total)
            count_str = str(count)
            amount_percentage_str = f'{amount_percentage:.1f}%'
            count_percentage_str = f'{count_percentage:.1f}%'

            row = [
                category_name,
                count_str,
                amount_percentage_str,
                count_percentage_str,
                total_str
            ]

            rows.append(row)

        return rows
    
    def _get_expense_report_table_content(self) -> list[list[str]]:
        if not self._statistics.total_per_expense_category:
            return []
        
        rows = []

        for category in self._statistics.total_per_expense_category:
            category_name = category.value
            total = self._statistics.total_per_expense_category[category]
            count = self._statistics.count_per_expense_category[category]
            amount_percentage = self._statistics.percentage_per_expense_category[category]
            count_percentage = self._statistics.count_percentage_per_expense_category[category]

            total_str = formatter.format_currency_for_ptbr(total)
            count_str = str(count)
            amount_percentage_str = f'{amount_percentage:.1f}%'
            count_percentage_str = f'{count_percentage:.1f}%'

            row = [
                category_name,
                count_str,
                amount_percentage_str,
                count_percentage_str,
                total_str
            ]

            rows.append(row)

        return rows

