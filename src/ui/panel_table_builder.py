from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text

from src.utils.constants import (
    TRANSACTION_TYPE_TABLE, INCOME_CATEGORY_TABLE, EXPENSE_CATEGORY_TABLE, ALL_CATEGORIES_TABLE
)
import src.service.transaction_formatter as formatter
from src.models.transaction import Transaction
from src.service.transaction_statistics import TransactionStatistics

class PanelBuilder:
    """Constrói Menus e Painéis para a interface CLI"""

    @staticmethod
    def build_dashboard() -> Panel:
        dashboard_text = Text('Suas Finanças - Resumo', style='cyan', justify='center')

        return Panel(dashboard_text, box=box.SQUARE_DOUBLE_HEAD, border_style='blue')

    @staticmethod
    def build_main_menu() -> Panel:
        menu_text: str = """[cyan][1][/cyan] Adicionar Transação
[cyan][2][/cyan] Gerenciar Transações
[cyan][0][/cyan] Sair"""

        return Panel(
            menu_text,
            title='[bold blue]Menu Principal[/bold blue]',
            border_style='cyan',
            padding=(1,4),
            expand=False,
            )

    @staticmethod
    def build_transaction_type_menu() -> Panel:
        menu_lines = []

        for index, transaction_type in TRANSACTION_TYPE_TABLE.items():
            menu_lines.append(f'[cyan][{index}][/] {transaction_type.capitalize()}')
            
        transaction_type_menu_text: str = '\n'.join(menu_lines)

        return Panel(
            transaction_type_menu_text,
            title='[bold blue]Tipos de Transação[/]',
            expand=False,
            border_style='cyan',
            padding=(1,4)
            )
        
    @staticmethod
    def build_category_menu(transaction_type: str) -> Panel:

        match transaction_type:
            case 'receita':
                categories = INCOME_CATEGORY_TABLE
                panel_title = '[bold blue]Categorias de Receita[/]'
            
            case 'despesa':
                categories = EXPENSE_CATEGORY_TABLE
                panel_title = '[bold blue]Categorias de Despesa[/]'

        menu_lines: list[str] = []
        for index, category in categories.items():
            menu_lines.append(f'[cyan][{index}][/] {category.capitalize()}')

        menu_lines.append('[cyan][0][/] Definir mais tarde')
        category_menu_text: str = '\n'.join(menu_lines)

        return Panel(
            category_menu_text,
            title=panel_title,
            expand=False,
            border_style='cyan',
            padding=(1,4)
            )
    
    @staticmethod
    def build_all_categories_filter_menu() -> Panel:
        panel_title = '[bold blue]Todas as Categorias[/]'
        menu_lines: list[str] = []
        for index, category in ALL_CATEGORIES_TABLE.items():
            menu_lines.append(f'[cyan][{index}][/] {category.capitalize()}')

        all_categories_menu_text: str = '\n'.join(menu_lines)

        return Panel(
            all_categories_menu_text,
            title=panel_title,
            expand=False,
            border_style='cyan',
            padding=(1,4)
        )

    
    @staticmethod
    def build_transaction_management_submenu() -> Panel:
        submenu_text = """[cyan][1][/]: Modificar Transação
[cyan][2][/]: Filtrar Transações
[cyan][3][/]: Ordenar Transações
[cyan][4][/]: Gerar Relatório
[cyan][0][/]: Voltar"""
        submenu_title = '[bold blue]Opções de Gerenciamento[/]'

        return Panel(
            submenu_text,
            title=submenu_title,
            expand=False,
            border_style='cyan',
            padding=(1,4))
    
    @staticmethod
    def build_transaction_modification_submenu() -> Panel:
        submenu_text = """[cyan][1][/]: Excluir Transação
[cyan][2][/]: Alterar Categoria
[cyan][3][/]: Alterar Descrição
[cyan][0][/]: Voltar"""
        submenu_title = '[bold blue]Opções de Modificação[/]'

        return Panel(
            submenu_text,
            title=submenu_title,
            expand=False,
            border_style='cyan',
            padding=(1,4)
        )
    
    @staticmethod
    def build_transaction_filter_submenu() -> Panel:
        submenu_text = """[cyan][1][/]: Filtrar por Valor
[cyan][2][/]: Filtrar por Tipo
[cyan][3][/]: Filtrar por Data
[cyan][4][/]: Filtrar por Categoria
[cyan][5][/]: Resetar Filtro
[cyan][0][/]: Voltar"""
        submenu_title = '[bold blue]Opções de Filtragem[/]'

        return Panel(
            submenu_text, 
            title=submenu_title, 
            expand=False,
            border_style='cyan',
            padding=(1,4)
        )
    
    @staticmethod
    def build_transaction_sorter_submenu() -> Panel:
        submenu_text = """[cyan][1][/]: Ordenar por Valor
[cyan][2][/]: Ordenar por Data
[cyan][3][/]: Ordenar por ID
[cyan][0][/]: Voltar"""
        submenu_title = '[bold blue]Opções de Ordenação'

        return Panel(
            submenu_text,
            title=submenu_title,
            expand=False,
            border_style='cyan',
            padding=(1,4)
        )
    
    @staticmethod
    def build_transaction_sort_order_submenu() -> Panel:
        submenu_text = """[cyan][1][/]: Ordem Crescente
[cyan][2][/]: Ordem Decrescente
[cyan][0][/]: Voltar"""

        return Panel(
            submenu_text,
            expand=False,
            border_style='cyan',
            padding=(1,4)
        )

    @staticmethod
    def build_confirmation_panel(msg: str) -> Panel:
        return Panel(
            msg, 
            box=box.SQUARE,
            style='bold green',
            expand=False,
            padding=(0,0)
        )
    
    @staticmethod
    def build_orientation_panel(msg: str) -> Panel:
        return Panel(
            msg, 
            box=box.SQUARE,
            style='yellow',
            expand=False,
            padding=(0,0)
        )
    
    @staticmethod
    def build_general_overview_panel(msg: str) -> Panel:
        return Panel(
            msg,
            box=box.DOUBLE_EDGE,
            title='[bold blue]Relatório Financeiro[/]',
            style='cyan',
            expand=False,
            padding=(1,4)
        )
    
    @staticmethod
    def build_income_overview_panel(msg: str) -> Panel:
        return Panel(
            msg,
            box=box.SQUARE,
            title='[bold blue]Receitas[/]',
            style='cyan',
            expand=False,
            padding=(1,4)
        )
    
    @staticmethod
    def build_expense_overview_panel(msg: str) -> Panel:
        return Panel(
            msg,
            box=box.SQUARE,
            title='[bold blue]Despesas[/]',
            style='cyan',
            expand=False,
            padding=(1,4)
        )
        
    # Métodos que retornam uma lista de opções para o Prompt de Rich --------------------------------------------------
    @staticmethod
    def get_main_menu_choices() -> list[str]:
        return ['1', '2', '0']

    @staticmethod
    def get_transaction_type_choices() -> list[str]:
        return [number for number in TRANSACTION_TYPE_TABLE]
        
    @staticmethod
    def get_category_choices(transaction_type: str) -> list[str]:
        match transaction_type:
            case 'receita':
                categories: dict[str, str] = INCOME_CATEGORY_TABLE

            case 'despesa':
                categories: dict[str, str] = EXPENSE_CATEGORY_TABLE

        choices = [number for number in categories]
        choices.append('0') # Opção de pular
        return choices
    
    @staticmethod
    def get_all_categories_choices() -> list[str]:
        return [number for number in ALL_CATEGORIES_TABLE]
    
    @staticmethod
    def get_transaction_management_submenu_choices() -> list[str]:
        return ['1', '2', '3', '4', '0']
    
    @staticmethod
    def get_transaction_modification_submenu_choices() -> list[str]:
        return ['1', '2', '3', '0']
    
    @staticmethod
    def get_transaction_filter_submenu_choices() -> list[str]:
        return ['1', '2', '3', '4', '5', '0']
    
    @staticmethod
    def get_transaction_sorter_submenu_choices() -> list[str]:
        return ['1', '2', '3', '0']
    
    @staticmethod
    def get_transaction_sort_order_choices() -> list[str]:
        return ['1', '2', '0']
    

class GraphTableBuilder:
    @staticmethod
    def build_transaction_table(transactions_list: list[Transaction], statistics: TransactionStatistics) -> Table:
        transaction_table = Table( 
            title='Transações', 
            style='bold blue',
            show_footer=True
            )
        transaction_count = statistics.transaction_count
        formatted_number_of_transactions = f'{transaction_count} transação(ões) contabilizada(s).'
        total_balance = statistics.balance
        formatted_balance = formatter.format_currency_for_ptbr(total_balance)
        transaction_table.add_column(
            '[cyan]ID[/]', style='cyan', footer=formatted_number_of_transactions, footer_style='cyan'
            )
        transaction_table.add_column('[cyan]Tipo[/]', style='cyan')
        transaction_table.add_column(
            '[cyan]Valor[/]',
            style='cyan',
            footer=f'Saldo: {formatted_balance}',
            footer_style='green' if total_balance >= 0 else 'red',
            justify='right'
            )
        transaction_table.add_column('[cyan]Data[/]', style='cyan')
        transaction_table.add_column('[cyan]Categoria[/]', style='cyan')
        transaction_table.add_column('[cyan]Descrição[/]', style='cyan')
        
        for transaction in transactions_list:
            transaction_table.add_row(
                str(transaction.id), 
                formatter.format_transaction_type(transaction.transaction_type), 
                formatter.format_currency_for_ptbr(transaction.amount), 
                formatter.format_date(transaction.transaction_date), 
                formatter.format_category(transaction.category), 
                transaction.description, 
                style='green' if transaction.transaction_type.value == 'receita' else 'red')

        return transaction_table
    
    @staticmethod 
    def build_income_report_table(row_content: list[list[str]]) -> Table:
        report_table = Table(
            title='Breakdown de Receitas por Categoria',
            style='bold blue'
        )

        report_table.add_column('Categoria', style='cyan')
        report_table.add_column('Transações', style='cyan')
        report_table.add_column('Valor %', style='cyan')
        report_table.add_column('Contagem %', style='cyan')
        report_table.add_column('Total', style='cyan')

        for content in row_content:
            report_table.add_row(*content)

        return report_table
    
    @staticmethod 
    def build_expense_report_table(row_content: list[list[str]]) -> Table:
        report_table = Table(
            title='Breakdown de Despesas por Categoria',
            style='bold blue'
        )

        report_table.add_column('Categoria', style='cyan')
        report_table.add_column('Transações', style='cyan')
        report_table.add_column('Valor %', style='cyan')
        report_table.add_column('Contagem %', style='cyan')
        report_table.add_column('Total', style='cyan')

        for content in row_content:
            report_table.add_row(*content)

        return report_table