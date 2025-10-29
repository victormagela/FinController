import os
import re
from collections.abc import Callable

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich import box
from rich.table import Table

from src.service.transaction_service import TransactionService
from src.utils.utils import PromptPTBR, IntPromptPTBR
from src.utils.constants import INCOME_CATEGORY_TABLE, EXPENSE_CATEGORY_TABLE,\
    ALL_CATEGORIES_TABLE, TRANSACTION_TYPE_TABLE
from src.models.transaction import Transaction
from src.ui.ui_state_manager import UIStateManager


class PanelBuilder:
    """Constrói Menus e Painéis para a interface CLI"""
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
        return ['1', '2', '3', '0']
    
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
        self._state_manager: UIStateManager = UIStateManager()
        # Dicionários para execução dos comandos com o padrão Dispatch Table
        self._main_menu_dispatch_table: dict[str, Callable[[], None]] = {
            '1': self._add_transaction,
            '2': self._manage_transactions
        }
        self._transaction_management_submenu_dispatch_table: dict[str, Callable[[], None]] = {
            '1': self._modify_transaction,
            '2': self._filter_transactions,
            '3': self._sort_transactions
        }
        self._transaction_modification_submenu_dispatch_table: dict[str, Callable[[int], None]] = {
            '1': self._del_transaction,
            '2': self._update_category,
            '3': self._update_description
        }
        self.transaction_filter_submenu_dispatch_table: dict[str, Callable[[], list[Transaction]]] = {
            '1': self._filter_by_amount,
            '2': self._filter_by_type,
            '3': self._filter_by_date,
            '4': self._filter_by_category
        }
        
    def run(self) -> None:
        while True:
            option: str = self._collect_main_menu_choice()
            if option == '0':
                self._console.print('\n')
                self._console.print('Obrigado por usar o FinController!', style='green')
                break

            command: Callable[[], None] = self._main_menu_dispatch_table.get(option)
            command()

    def _collect_main_menu_choice(self) -> str:
        main_menu = PanelBuilder.build_main_menu()
        main_menu_choices = PanelBuilder.get_main_menu_choices()
        
        self._console.print('\n')
        self._clear_screen()
        self._console.print(main_menu, justify='center')
        option: str = PromptPTBR.ask(
            'Digite o número da opção desejada', 
            choices=main_menu_choices)
        return option
    
    def _add_transaction(self) -> None:
        try:
            raw_data_dict = self._collect_transaction_info()
            self._service.add_transaction(raw_data_dict)

            confirmation_msg = 'Transação adicionada com sucesso!'
            confirmation_panel = PanelBuilder.build_confirmation_panel(confirmation_msg)
            self._console.print(confirmation_panel, justify='center')
            self._pause_and_clear()
        except ValueError as e:
            self._console.print('\n')
            self._console.print(f'[red]{e}[/]')
            self._pause_and_clear()
    
    def _collect_transaction_info(self) -> dict[str, str]:
        """
        Método que chama os métodos de coleta individuais
        e os adiciona a um dicionário para ser usado pela camada de serviço
        """
        raw_transaction_data_dict: dict[str, str] = {}

        self._clear_screen()
        self._console.print('\n')
        self._console.print(Rule('[bold blue]Nova Transação[/]', style='cyan'))
        self._console.print('\n')

        self._console.print(Rule('[bold blue]Valor da Transação[/]', style='cyan', characters='.'))
        amount: str = self._collect_amount()
        raw_transaction_data_dict['amount'] = amount
        
        self._console.print(Rule('\n[bold blue]Tipo da Transação[/]', style='cyan', characters='.'))
        transaction_type: str = self._collect_transaction_type()
        raw_transaction_data_dict['transaction_type'] = transaction_type

        self._console.print(Rule('\n[bold blue]Data da Transação[/]', style='cyan', characters='.'))
        transaction_date: str = self._collect_transaction_date()
        raw_transaction_data_dict['transaction_date'] = transaction_date

        self._console.print(Rule('\n[bold blue]Categoria da Transação[/]', style='cyan', characters='.'))
        category: str | None = self._collect_category(transaction_type)
        if category:
            raw_transaction_data_dict['category'] = category

        self._console.print(Rule('\n[bold blue]Descrição da Transação[/]', style='cyan', characters='.'))
        description: str | None = self._collect_description()
        if description:
            raw_transaction_data_dict['description'] = description

        return raw_transaction_data_dict
    
    def _manage_transactions(self) ->None:
        """
        Método que pega a lista de transações do _service e as mostra, 
        juntamente de um submenu com opções de gerenciamento.
        """
        while True:
            self._clear_screen()
            if self._state_manager.has_active_filter():
                transaction_list = self._state_manager.filtered_list
            
            else:
                transaction_list = self._service.get_all_transactions()
                
            if not transaction_list:
                self._console.print('\n')
                self._console.print('[red]Não há nenhum item na sua lista de transações. Adicione um primeiro.[/]')
                self._pause_and_clear()
                return
            
            self._show_all_transactions(transaction_list)
            transaction_management_submenu = PanelBuilder.build_transaction_management_submenu()
            transaction_management_choices = PanelBuilder.get_transaction_management_submenu_choices()

            self._console.print('\n')
            self._console.print(transaction_management_submenu, justify='center')
            option = PromptPTBR.ask(
                'Digite o número da opção desejada',
                choices= transaction_management_choices
                )
            if option == '0':
                break

            command: Callable = self._transaction_management_submenu_dispatch_table.get(option)
            command()
        
        if self._state_manager.has_active_filter():
            self._state_manager.clear_filtered_list()
    
    def _show_all_transactions(self, transaction_list) -> list[Transaction]:
        """Mostra a lista de todas as transações no terminal"""
        transaction_table: Table = GraphTableBuilder.build_transaction_table(transaction_list)

        self._console.print(Rule('[bold blue]Lista de Transações[/]', style='cyan'))
        self._console.print('\n')        
        self._console.print(transaction_table)

        return transaction_list
    
    def _modify_transaction(self) -> None:
        """Apresenta um menu de possíveis modificações, captura a escolha do usuário e a executa"""
        transaction_modification_submenu = PanelBuilder.build_transaction_modification_submenu()
        transaction_modification_choices = PanelBuilder.get_transaction_modification_submenu_choices()

        while True:
            self._clear_screen()
            if self._state_manager.has_active_filter():
                transaction_list = self._state_manager.filtered_list
            
            else:
                transaction_list = self._service.get_all_transactions()
            
            if not transaction_list:
                return

            self._show_all_transactions(transaction_list)
            self._console.print('\n')
            self._console.print(transaction_modification_submenu, justify='center')
            option = PromptPTBR.ask(
                'Digite o número da opção desejada',
                choices= transaction_modification_choices
                )
            if option == '0':
                return

            self._console.print('\n')
            transaction_id: int = IntPromptPTBR.ask('Digite o índice da transação')
            try:
                self._service.get_transaction_by_id(transaction_id)
            except ValueError as e:
                self._console.print(f'[red]{e}[/]')
                self._pause_and_clear()
                return
            
            command: Callable[[int], None] = self._transaction_modification_submenu_dispatch_table.get(option)
            try:
                command(transaction_id)
                confirmation_msg = 'Operação executada com sucesso!'
                confirmation_panel = PanelBuilder.build_confirmation_panel(confirmation_msg)
                self._console.print(confirmation_panel, justify='center')
                self._pause_and_clear()
            except ValueError as e:
                self._console.print(f'{e}')
                self._pause_and_clear()

    def _filter_transactions(self) -> None:
        """Exibe um menu com todas as opções de filtragem, captura a escolha do usuário e a executa"""
        transaction_filter_submenu = PanelBuilder.build_transaction_filter_submenu()
        transaction_filter_choices = PanelBuilder.get_transaction_filter_submenu_choices()

        while True:
            self._clear_screen()
            if self._state_manager.has_active_filter():
                transaction_list = self._state_manager.filtered_list
            
            else:
                transaction_list = self._service.get_all_transactions()
                
            if not transaction_list:
                return
            
            self._show_all_transactions(transaction_list)
            self._console.print('\n')
            self._console.print(transaction_filter_submenu, justify='center')
            option = PromptPTBR.ask(
                'Digite o número da opção desejada',
                choices=transaction_filter_choices
                )
            if option == '0':
                return
            
            if option == '5':
                self._state_manager.clear_filtered_list()
                continue
            
            try:
                command = self.transaction_filter_submenu_dispatch_table.get(option)
                if not self._state_manager.has_active_filter():
                    filtered_list = command()
                    self._state_manager.set_filtered_list(filtered_list)
                
                filtered_list = command(self._state_manager.filtered_list)
                self._state_manager.set_filtered_list(filtered_list)

            except ValueError as e:
                self._console.print(f'[red]{e}[/]')
                self._pause_and_clear()    

    def _sort_transactions(self) -> None:
        ...

    # Métodos para atualizar dados individuais (categoria ou descrição) ou excluir uma transação da lista -------------
    def _del_transaction(self, transaction_id: int) -> None:
        self._service.del_transaction(transaction_id)

        if self._state_manager.has_active_filter():
            self._state_manager.del_from_filtered_list(transaction_id)

    def _update_category(self, transaction_id: int) -> None:
        orientation_msg = 'Nota: Alterar a categoria de uma transação' \
        ' irá resetar o filtro de transações se houver um ativo.'
        orientation_panel = PanelBuilder.build_orientation_panel(orientation_msg)

        self._console.print(orientation_panel)
        transaction_type = self._service.get_transaction_type(transaction_id)

        new_category = self._collect_category(transaction_type)
        self._service.update_transaction_category(transaction_id, new_category)
        
        if self._state_manager.has_active_filter():
            self._state_manager.clear_filtered_list()

    def _update_description(self, transaction_id: int) -> None:
        new_description = self._collect_description()
        self._service.update_transaction_description(transaction_id, new_description)

    # Métodos individuais para as opções de filtragem -----------------------------------------------------------------
    def _filter_by_amount(self, filtered_list: list[Transaction]=None) -> list[Transaction]:
        orientation_msg = 'Você pode omitir um dos valores abaixos para a filtragem.'
        orientation_panel = PanelBuilder.build_orientation_panel(orientation_msg)

        self._console.print(orientation_panel)
        start_amount: str = self._console.input('Digite o valor inicial de filtragem: ').strip() or None
        end_amount: str = self._console.input('Digite o valor final de filtragem: ').strip() or None

        if filtered_list is None:
            return self._service.filter_by_amount_range(start_amount, end_amount)
        
        return self._service.filter_by_amount_range(start_amount, end_amount, filtered_list)
    
    def _filter_by_type(self, filtered_list: list[Transaction]=None) -> list[Transaction]:
        transaction_type: str = self._collect_transaction_type()
        if filtered_list is None:
            return self._service.filter_by_type(transaction_type)

        return self._service.filter_by_type(transaction_type, filtered_list)
    
    def _filter_by_date(self, filtered_list: list[Transaction]=None) -> list[Transaction]:
        orientation_msg = 'Você pode omitir uma das datas abaixos para a filtragem.'
        orientation_panel = PanelBuilder.build_orientation_panel(orientation_msg)
        DATE_FORMAT = """[yellow]DD/MM/AAAA
Exemplo: 01/01/2025[/]"""
        date_format_panel = PanelBuilder.build_orientation_panel(DATE_FORMAT)

        self._console.print('\n')
        self._console.print(date_format_panel)
        self._console.print(orientation_panel)
        start_date: str = self._console.input('Digite a data inicial de filtragem: ').strip() or None
        end_date: str = self._console.input('Digite a data final de filtragem: ').strip() or None

        if filtered_list is None:
            return self._service.filter_by_date_range(start_date, end_date)
        
        return self._service.filter_by_date_range(start_date, end_date, filtered_list)

    def _filter_by_category(self, filtered_list: list[Transaction]=None) -> list[Transaction]:
        all_categories_menu = PanelBuilder.build_all_categories_filter_menu()
        all_categories_choices = PanelBuilder.get_all_categories_choices()

        self._console.print('\n')
        self._console.print(all_categories_menu, justify='center')
        category_option: str = PromptPTBR.ask(
            'Digite o número da categoria',
            choices=all_categories_choices
        )
        category: str = ALL_CATEGORIES_TABLE.get(category_option)

        if filtered_list is None:
            return self._service.filter_by_category(category)
        
        return self._service.filter_by_category(category, filtered_list)

    # Métodos de coleta de dados individuais --------------------------------------------------------------------------
    def _collect_amount(self) -> str:
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

        date_format_panel = PanelBuilder.build_orientation_panel(DATE_FORMAT)

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

        description_panel = PanelBuilder.build_orientation_panel(description_note)

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

    # Métodos internos útilitários ------------------------------------------------------------------------------------
    def _clear_screen(self):
        os.system('cls')

    def _pause_and_clear(self, msg: str='\nPressione enter para voltar...'):
        self._console.input(msg)
        self._clear_screen()
