import os
import re

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from src.service.transaction_service import TransactionService
from src.utils.utils import PromptPTBR


class UserInterface:
    """Interface CLI do Programa"""
    # Padrões regex para validação de dados
    AMOUNT_PATTERN: str = r'^\d+([.,]\d{1,2})?$'
    DATE_PATTERN: str = r'^\d{2}/\d{2}/\d{4}$'
    # Tabelas que contém todas as categorias válidas
    INCOME_CATEGORY_TABLE: dict[int, str] = {
        1: 'salário',
        2: 'investimento',
        3: 'freelance',
        4: 'venda',
        5: 'presente',
        6: 'reembolso',
        7: 'outros'
        }
    EXPENSE_CATEGORY_TABLE: dict[int, str] = {
        1: 'alimentação',
        2: 'transporte',
        3: 'moradia',
        4: 'saúde',
        5: 'educação',
        6: 'lazer',
        7: 'contas',
        8: 'vestuário',
        9: 'outros'
        }
    

    def __init__(self):
        self._service: TransactionService = TransactionService()
        self.console = Console()

    def show_main_menu(self):
        menu_text: str = """[cyan][1][/cyan] Adicionar Transação
[cyan][2][/cyan] Listar Transações
[cyan][3][/cyan] Excluir Transação
[cyan][4][/cyan] Alterar Transação
[cyan][5][/cyan] Filtrar Transações
[cyan][6][/cyan] Ordenar Transações
[cyan][0][/cyan] Sair"""

        panel = Panel(
            menu_text,
            title='[bold blue]Menu Principal[/bold blue]',
            border_style='cyan',
            padding=(1,4),
            expand=False,
            )
        
        self.console.print('\n')
        self.console.print(panel, justify='center')
        option: str = PromptPTBR.ask(
            'Digite o número da opção desejada', 
            choices=['1', '2', '3', '4', '5', '6', '0'], )
        return option
    
    def add_transaction(self) -> None:
        raw_data_dict = self.collect_transaction_info()
        self._service.add_transaction(raw_data_dict)
    
    def collect_transaction_info(self) -> dict[str, str]:
        raw_transaction_data_dict: dict[str, str] = {}

        self.console.clear()
        self.console.print(Rule('[bold blue]Nova Transação[/]', style='cyan'))

        amount: str = self.collect_amount()
        raw_transaction_data_dict['amount'] = amount
        
        transaction_type: str = self.collect_transaction_type()
        raw_transaction_data_dict['transaction_type'] = transaction_type

        transaction_date: str = self.collect_transaction_date()
        raw_transaction_data_dict['transaction_date'] = transaction_date

        category: str | None = self.collect_category(transaction_type)
        if category:
            raw_transaction_data_dict['category'] = category

        description: str | None = self.collect_description()
        if description:
            raw_transaction_data_dict['description'] = description

        return raw_transaction_data_dict

    def collect_amount(self) -> str:
        while True:
            amount_str : str = self.console.input('Digite o valor da transação: ').strip()
            if not amount_str:
                self.console.print('[red]Valor inválido.[/]')
                continue

            if not self._validate_amount(amount_str):
                self.console.print('[red]Formato inválido! Digite apenas números, e utilize "." e ","' \
                ' apenas para casas decimais')
                continue

            return amount_str

    def collect_transaction_type(self) -> str:
        transaction_type_text: str = """[cyan][1][/] Receita
[cyan][2][/] Despesa"""

        transaction_type_panel = Panel(
            transaction_type_text,
            title='[bold blue]Tipos de Transação[/]',
            border_style='cyan',
            padding=(1,4),
            expand=False
        )

        self.console.print(transaction_type_panel, justify='center')
        transaction_type_option: str = PromptPTBR.ask(
            'Digite o número do tipo da transação',
            choices=['1', '2']
            )
        
        return 'receita' if transaction_type_option == '1' else 'despesa'

    def collect_transaction_date(self) -> str:
        DATE_FORMAT = """[yellow]DD/MM/AAAA
Exemplo: 01/01/2025[/]"""

        date_format_panel = Panel(
            DATE_FORMAT, 
            title='Formato de Data',
            border_style='yellow',
            expand=False,
            padding=(1,4))
        
        self.console.print(date_format_panel)
        while True:
            date_str = self.console.input('Digite a data da transação: ').strip()
            if not date_str:
                self.console.print('[red]Valor inválido.[/]')
                continue

            if not self._validate_date(date_str):
                self.console.print('[red]Formato de data inválido.[/]')
                continue
            
            return date_str
        
    def collect_category(self, transaction_type_str: str) -> str | None:
        match transaction_type_str:
            case 'receita':    
                income_categories_text: str = """[cyan][1][/] Salário
[cyan][2][/] Freelance
[cyan][3][/] Investimento
[cyan][4][/] Venda
[cyan][5][/] Presente
[cyan][6][/] Reembolso
[cyan][7][/] Outros
[cyan][8][/] Definir mais tarde""" 
                income_categories_panel = Panel(
                    income_categories_text, 
                    title='[bold blue]Categorias de Receita[/]',
                    border_style='cyan',
                    padding=(1,4)
                    )
                
                self.console.print(income_categories_panel, justify='center')
                income_category_option: str = PromptPTBR.ask(
                    'Digite o número da categoria',
                    choices=['1', '2', '3', '4', '5', '6', '7', '8']
                )
                income_category_option= int(income_category_option)

                category: str | None = self.income_category_table.get(income_category_option, None)
                return category
            
            case 'despesa':
                expense_categories_text: str = """[cyan][1][/] Alimentação
[cyan][2][/] Transporte
[cyan][3][/] Moradia
[cyan][4][/] Saúde
[cyan][5][/] Educação
[cyan][6][/] Lazer
[cyan][7][/] Contas
[cyan][8][/] Vestuário
[cyan][9][/] Outros
[cyan][0][/] Definir mais tarde"""

                expense_categories_panel = Panel(
                    expense_categories_text,
                    title='[bold blue]Categorias de Despesa[/]',
                    border_style='cyan',
                    expand=False,
                    padding=(1,4)
                )

                self.console.print(expense_categories_panel, justify='center')
                expense_category_option = PromptPTBR.ask(
                    'Digite o número da categoria',
                    choices=['1','2','3','4','5','6','7','8','9','0']
                )
                expense_category_option = int(expense_category_option)

                category: str | None = self.expense_category_table.get(expense_category_option, None)
                return category
            
    def collect_description(self) -> str | None:
        description = self.console.input('\nDigite uma descrição para a transação. [yellow]Nota: Este campo é opcional, ' \
        'apenas digite enter se quiser pula-lo.[/]' \
        '\n>>>>>')

        return description if description else None

    # Métodos internos de validação por regex -------------------------------------------------------------------------
    def _validate_amount(self, amount_str: str) -> bool:
        if not bool(re.fullmatch(self.AMOUNT_PATTERN, amount_str)):
            return False
        
        return True
    
    def _validate_date(self, date_str: str) -> bool:
        if not bool(re.fullmatch(self.DATE_PATTERN, date_str)):
            return False
        
        return True