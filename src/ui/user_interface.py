import re

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich import box
from rich.table import Table

from src.service.transaction_service import TransactionService
from src.utils.utils import PromptPTBR
from src.utils.constants import INCOME_CATEGORY_TABLE, EXPENSE_CATEGORY_TABLE, TRANSACTION_TYPE_TABLE
from src.models.transaction import Transaction


class PanelBuilder:
    """Constrói Menus e Painéis para a interface CLI"""
    @staticmethod
    def build_main_menu() -> Panel:
        menu_text: str = """[cyan][1][/cyan] Adicionar Transação
[cyan][2][/cyan] Listar Transações
[cyan][3][/cyan] Excluir Transação
[cyan][4][/cyan] Alterar Transação
[cyan][5][/cyan] Filtrar Transações
[cyan][6][/cyan] Ordenar Transações
[cyan][0][/cyan] Sair"""

        main_menu = Panel(
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

        transaction_type_menu = Panel(
            transaction_type_menu_text,
            title='[bold blue]Tipos de Transação[/]',
            expand=False,
            border_style='cyan',
            padding=(1,4)
            )
            
        return transaction_type_menu
        
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

        category_menu = Panel(
            category_menu_text,
            title=panel_title,
            expand=False,
            border_style='cyan',
            padding=(1,4)
            )
            
        return category_menu
        
    # Métodos que retornam uma lista de opções para o Prompt de Rich --------------------------------------------------
    @staticmethod
    def get_main_menu_choices() -> list[str]:
        return ['1', '2', '3', '4', '5', '6', '0']

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
    

class GraphTableBuilder:
    @staticmethod
    def build_transaction_table(transactions_list: list[Transaction]) -> Table:
        transaction_table = Table(
            '[cyan]ID[/]', 
            '[cyan]Tipo[/]', 
            '[cyan]Valor[/]',
            '[cyan]Data[/]',  
            '[cyan]Categoria[/]', 
            '[cyan]Descrição[/]', 
            title='Transações', 
            style='bold blue'
            )
        
        for transaction in transactions_list:
            transaction_table.add_row(
                str(transaction.id), 
                transaction.transaction_type_str, 
                transaction.amount_formatted_brazil, 
                transaction.transaction_date_str, 
                transaction.category_str, 
                transaction.description, 
                style='green' if transaction.transaction_type_str == 'Receita' else 'red')

        return transaction_table
    

class UserInterface:
    """Interface CLI do Programa"""
    # Padrões regex para validação de formato de dados
    AMOUNT_PATTERN: str = r'^\d+([.,]\d{1,2})?$'
    DATE_PATTERN: str = r'^\d{2}/\d{2}/\d{4}$'

    def __init__(self):
        self._service: TransactionService = TransactionService()
        self._console: Console = Console()

    def show_main_menu(self):
        main_menu = PanelBuilder.build_main_menu()
        main_menu_choices = PanelBuilder.get_main_menu_choices()
        
        self._console.print('\n')
        self._console.print(main_menu, justify='center')
        option: str = PromptPTBR.ask(
            'Digite o número da opção desejada', 
            choices=main_menu_choices)
        return option
    
    def add_transaction(self) -> None:
        try:
            raw_data_dict = self.collect_transaction_info()
            self._service.add_transaction(raw_data_dict)
        except ValueError as e:
            self._console.print('\n')
            self._console.print(f'[red]{e}[/]')
    
    def collect_transaction_info(self) -> dict[str, str]:
        """
        Método que chama os métodos de coleta individuais
        e os adiciona a um dicionário para ser usado pela camada de serviço
        """
        raw_transaction_data_dict: dict[str, str] = {}

        self._console.clear()
        self._console.print('\n')
        self._console.print(Rule('[bold blue]Nova Transação[/]', style='cyan'))
        self._console.print('\n')

        amount: str = self._collect_amount()
        raw_transaction_data_dict['amount'] = amount
        
        transaction_type: str = self._collect_transaction_type()
        raw_transaction_data_dict['transaction_type'] = transaction_type

        transaction_date: str = self._collect_transaction_date()
        raw_transaction_data_dict['transaction_date'] = transaction_date

        category: str | None = self._collect_category(transaction_type)
        if category:
            raw_transaction_data_dict['category'] = category

        description: str | None = self._collect_description()
        if description:
            raw_transaction_data_dict['description'] = description

        return raw_transaction_data_dict
    
    def show_all_transactions(self) -> None:
        """Coleta a lista de todas as transações por meio de TransactionService e as mostra no terminal"""
        transaction_list: list[Transaction] = self._service.get_all_transactions()

        if not transaction_list:
            self._console.print('\n')
            self._console.print('[red]Não há nenhum item na sua lista de transações. Adicione um primeiro.[/]')
            return

        transaction_table: Table = GraphTableBuilder.build_transaction_table(transaction_list)

        self._console.print('\n')
        self._console.print(Rule('[bold blue]Lista de Transações[/]', style='cyan'))
        self._console.print('\n')        
        self._console.print(transaction_table)

    # Métodos de coleta de dados individuais --------------------------------------------------------------------------
    def _collect_amount(self) -> str:
        self._console.print(Rule('[bold blue]Valor da Transação[/]', style='cyan', characters='.'))
        self._console.print('\n')

        while True:
            amount_str : str = self._console.input('Digite o valor da transação: ').strip()
            if not amount_str:
                self._console.print('[red]Valor inválido.[/]')
                continue

            if not self._validate_amount_format(amount_str):
                self._console.print('[red]Formato inválido! Digite apenas números, e utilize "." e ","' \
                ' apenas para casas decimais')
                continue

            return amount_str

    def _collect_transaction_type(self) -> str:
        transaction_type_panel: Panel = PanelBuilder.build_transaction_type_menu()
        transaction_type_choices: list[str] = PanelBuilder.get_transaction_type_choices()

        self._console.print(Rule('\n[bold blue]Tipo da Transação[/]', style='cyan', characters='.'))
        self._console.print('\n')
        self._console.print(transaction_type_panel, justify='center')
        transaction_type_option: str = PromptPTBR.ask(
            'Digite o número do tipo da transação',
            choices=transaction_type_choices
            )
        
        return 'receita' if transaction_type_option == '1' else 'despesa'

    def _collect_transaction_date(self) -> str:
        DATE_FORMAT = """[yellow]DD/MM/AAAA
Exemplo: 01/01/2025[/]"""

        date_format_panel = Panel(
            DATE_FORMAT, 
            title='Formato de Data',
            box=box.SQUARE,
            border_style='yellow',
            expand=False,
            padding=(1,4))
        
        self._console.print(Rule('\n[bold blue]Data da Transação[/]', style='cyan', characters='.'))
        self._console.print('\n')
        self._console.print(date_format_panel)
        while True:
            date_str = self._console.input('Digite a data da transação: ').strip()
            if not date_str:
                self._console.print('[red]Valor inválido.[/]')
                continue

            if not self._validate_date_format(date_str):
                self._console.print('[red]Formato de data inválido.[/]')
                continue
            
            return date_str
        
    def _collect_category(self, transaction_type_str: str) -> str | None:
        self._console.print(Rule('\n[bold blue]Categoria da Transação[/]', style='cyan', characters='.'))

        category_panel : Panel = PanelBuilder.build_category_menu(transaction_type_str)
        category_choices: str = PanelBuilder.get_category_choices(transaction_type_str)
                
        self._console.print('\n')
        self._console.print(category_panel, justify='center')
        income_category_option: str = PromptPTBR.ask(
            'Digite o número da categoria',
            choices=category_choices
        )
        match transaction_type_str:
            case 'receita':
                categories: dict[str, str] = INCOME_CATEGORY_TABLE

            case 'despesa':
                categories: dict[str, str] = EXPENSE_CATEGORY_TABLE

        category: str | None = categories.get(income_category_option, None)
        return category
            
    def _collect_description(self) -> str | None:
        description_note = '[yellow]Nota: Este campo é opcional, pressione enter para pula-lo.[/]'

        description_panel = Panel(
            description_note, 
            box=box.SQUARE,
            border_style='yellow',
            expand=False,
            padding=(0,0)
            )

        self._console.print(Rule('\n[bold blue]Descrição da Transação[/]', style='cyan', characters='.'))
        self._console.print('\n')
        self._console.print(description_panel)
        description = self._console.input('Digite uma descrição para a transação: ')
        self._console.print('\n')

        return description if description else None

    # Métodos internos de validação por regex -------------------------------------------------------------------------
    def _validate_amount_format(self, amount_str: str) -> bool:
        if not bool(re.fullmatch(self.AMOUNT_PATTERN, amount_str)):
            return False
        
        return True
    
    def _validate_date_format(self, date_str: str) -> bool:
        if not bool(re.fullmatch(self.DATE_PATTERN, date_str)):
            return False
        
        return True