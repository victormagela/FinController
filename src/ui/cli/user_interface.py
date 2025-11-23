import os
import re
from collections.abc import Callable

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from src.service.transaction_service import TransactionService
from src.utils.utils import PromptPTBR, IntPromptPTBR
from src.utils.constants import (
    INCOME_CATEGORY_TABLE, EXPENSE_CATEGORY_TABLE, ALL_CATEGORIES_TABLE, APP_TITLE, DATE_PATTERN, AMOUNT_PATTERN,
    DESCRIPTION_PATTERN
)
from src.models.transaction import Transaction
from src.ui.cli.ui_state_manager import UIStateManager
import src.ui.formatter as formatter
from src.ui.cli.report_constructor import ReportConstructor
import  src.ui.cli.panel_table_builder as ptbuilder
    

class UserInterface:
    """Interface CLI do Programa"""
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
            '3': self._sort_transactions,
            '4': self._show_report
        }
        self._transaction_modification_submenu_dispatch_table: dict[str, Callable[[int], None]] = {
            '1': self._del_transaction,
            '2': self._update_category,
            '3': self._update_description
        }
        self.transaction_filter_submenu_dispatch_table: dict[
            str, Callable[[list[Transaction] | None], list[Transaction]]
            ] = {
            '1': self._filter_by_amount,
            '2': self._filter_by_type,
            '3': self._filter_by_date,
            '4': self._filter_by_category
        }
        self.transaction_sorter_submenu_dispatch_table: dict[
            str, Callable[[str, list[Transaction] | None], list[Transaction]]
            ] = {
            '1': self._sort_by_amount,
            '2': self._sort_by_date,
            '3': self._sort_by_id
            }
        
    def run(self) -> None:
        while True:
            self._clear_screen()
            title = APP_TITLE
            self._console.print(title, style='bold blue')
            self.show_dashboard()
            option: str = self._collect_main_menu_choice()
            if option == '0':
                self._console.print('\n')
                self._console.print('Obrigado por usar o FinController!', style='green')
                break

            command: Callable[[], None] = self._main_menu_dispatch_table.get(option)
            command()

    def show_dashboard(self) -> None:
        dashboard = ptbuilder.build_dashboard()
        self._console.print(dashboard)
        transaction_list = self._service.get_all_transactions()
        self._service.update_statistics(transaction_list)
        statistics = self._service.get_statistics()
        transaction_count = statistics.transaction_count
        total_income = statistics.total_income
        total_expense = statistics.total_expense
        balance = statistics.balance
        formatted_number_of_transaction = Text(
            f'Você possui {transaction_count} transação(ões) contabilizada(s).', style='cyan'
        )
        cyan_line_separator = Text("─"*50, style='cyan', justify='center')
        formatted_income = Text(
            f'Receitas: {formatter.format_currency_for_ptbr(total_income)}', style='green'
        )
        formatted_expense = Text(
            f'Despesas: {formatter.format_currency_for_ptbr(total_expense)}', style='red'
        )
        formatted_balance = Text(
            f'Saldo: {formatter.format_currency_for_ptbr(balance)}',
            style='green' if balance >= 0 else 'red',
        )
        self._console.print(
            formatted_number_of_transaction,
            cyan_line_separator,
            formatted_income,
            formatted_expense,
            cyan_line_separator,
            formatted_balance,
            sep='\n',
            justify='center'
        )

    def _collect_main_menu_choice(self) -> str:
        main_menu = ptbuilder.build_main_menu()
        main_menu_choices = ptbuilder.get_main_menu_choices()
        
        self._console.print('\n')
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
            confirmation_panel = ptbuilder.build_confirmation_panel(confirmation_msg)
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
        self._print_section_title('Nova Transação')

        self._print_section_title('Valor da Transação', characters='.')
        amount: str = self._collect_amount()
        raw_transaction_data_dict['amount'] = amount
        
        self._print_section_title('Tipo da Transação', characters='.')
        transaction_type: str = self._collect_transaction_type()
        raw_transaction_data_dict['transaction_type'] = transaction_type

        self._print_section_title('Data da Transação', characters='.')
        transaction_date: str = self._collect_transaction_date()
        raw_transaction_data_dict['transaction_date'] = transaction_date

        self._print_section_title('Categoria da Transação', characters='.')
        category: str | None = self._collect_category(transaction_type)
        if category:
            raw_transaction_data_dict['category'] = category

        self._print_section_title('Descrição da Transação', characters='.')
        description: str | None = self._collect_description()
        if description:
            raw_transaction_data_dict['description'] = description

        return raw_transaction_data_dict

    # Métodos que representam os diversos submenus do programa e suas funcionalidades ---------------------------------
    def _manage_transactions(self) ->None:
        """
        Método que pega a lista de transações do _service e as mostra, 
        juntamente de um submenu com opções de gerenciamento.
        """
        while True:
            self._clear_screen()
            transaction_list = self._get_transaction_list_for_display()    
            if not transaction_list:
                self._console.print('\n')
                self._console.print('[red]Não há nenhum item na sua lista de transações. Adicione um primeiro.[/]')
                self._pause_and_clear()
                break

            self._service.update_statistics(transaction_list)
            self._show_all_transactions(transaction_list)
            if self._state_manager.has_active_filter():
                filter_warning = ptbuilder.build_orientation_panel('Você possui um filtro ativo.')
                self._console.print(filter_warning)
            transaction_management_submenu = ptbuilder.build_transaction_management_submenu()
            transaction_management_choices = ptbuilder.get_transaction_management_submenu_choices()

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
    
    def _modify_transaction(self) -> None:
        """Apresenta um menu de possíveis modificações, captura a escolha do usuário e a executa"""
        transaction_modification_submenu = ptbuilder.build_transaction_modification_submenu()
        transaction_modification_choices = ptbuilder.get_transaction_modification_submenu_choices()

        while True:
            self._clear_screen()
            transaction_list = self._get_transaction_list_for_display()
            if not transaction_list:
                return

            self._service.update_statistics(transaction_list)
            self._show_all_transactions(transaction_list)
            if self._state_manager.has_active_filter():
                filter_warning = ptbuilder.build_orientation_panel('Você possui um filtro ativo.')
                self._console.print(filter_warning)
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
                confirmation_panel = ptbuilder.build_confirmation_panel(confirmation_msg)
                self._console.print(confirmation_panel, justify='center')
                self._pause_and_clear()
            except ValueError as e:
                self._console.print(f'{e}')
                self._pause_and_clear()

    def _filter_transactions(self) -> None:
        """Exibe um menu com todas as opções de filtragem, captura a escolha do usuário e a executa"""
        transaction_filter_submenu = ptbuilder.build_transaction_filter_submenu()
        transaction_filter_choices = ptbuilder.get_transaction_filter_submenu_choices()

        while True:
            self._clear_screen()
            transaction_list = self._get_transaction_list_for_display()
            if not transaction_list:
                return
            
            self._service.update_statistics(transaction_list)
            self._show_all_transactions(transaction_list)
            if self._state_manager.has_active_filter():
                filter_warning = ptbuilder.build_orientation_panel('Você possui um filtro ativo.')
                self._console.print(filter_warning)
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
                command: Callable[
                    [list[Transaction]], list[Transaction]
                    ] = self.transaction_filter_submenu_dispatch_table.get(option)
                
                transaction_list = command(transaction_list)
                self._state_manager.set_filtered_list(transaction_list)

            except ValueError as e:
                self._console.print(f'[red]{e}[/]')
                self._pause_and_clear()    

    def _sort_transactions(self) -> None:
        transaction_sorter_submenu = ptbuilder.build_transaction_sorter_submenu()
        transaction_sorter_choices = ptbuilder.get_transaction_sorter_submenu_choices()

        while True:
            transaction_list = self._get_transaction_list_for_display()
            if not transaction_list:
                return
            
            self._service.update_statistics(transaction_list)
            self._show_all_transactions(transaction_list)
            if self._state_manager.has_active_filter():
                filter_warning = ptbuilder.build_orientation_panel('Você possui um filtro ativo.')
                self._console.print(filter_warning)
            self._console.print('\n')
            self._console.print(transaction_sorter_submenu, justify='center')
            option = PromptPTBR.ask('Digite o número da opção desejada', choices=transaction_sorter_choices)

            if option == '0':
                return
            
            try:
                command: Callable[
                    [list[Transaction]], list[Transaction]
                    ] = self.transaction_sorter_submenu_dispatch_table.get(option)
                
                transaction_list = command(transaction_list)
                self._state_manager.set_filtered_list(transaction_list)
            
            except ValueError as e:
                self._console.print(f'[red]{e}[/]')
                self._pause_and_clear()

    def _show_report(self) -> None:
        self._clear_screen()
        transaction_list = self._get_transaction_list_for_display()  
        if not transaction_list:
            return
        
        statistics = self._service.get_statistics()
        start_date = self._service.get_min_date(transaction_list)
        end_date = self._service.get_max_date(transaction_list)
        report_constructor = ReportConstructor(statistics, start_date, end_date)
        overview_panel, income_overview_panel, expense_overview_panel, income_report_table, expense_report_table \
        = report_constructor.generate_full_report()

        self._console.print(overview_panel)
        self._console.print(income_overview_panel)
        self._console.print(expense_overview_panel)
        if income_report_table.row_count > 0:
            self._console.print(income_report_table)
        if expense_report_table.row_count > 0:
            self._console.print(expense_report_table)
        self._pause_and_clear()

    # Métodos para atualizar dados individuais (categoria ou descrição) ou excluir uma transação da lista -------------
    def _del_transaction(self, transaction_id: int) -> None:
        self._service.del_transaction(transaction_id)

        if self._state_manager.has_active_filter():
            self._state_manager.del_from_filtered_list(transaction_id)

    def _update_category(self, transaction_id: int) -> None:
        orientation_msg = 'Nota: Alterar a categoria de uma transação' \
        ' irá resetar o filtro de transações se houver um ativo.'
        orientation_panel = ptbuilder.build_orientation_panel(orientation_msg)

        self._console.print(orientation_panel)
        transaction_type = self._service.get_transaction_type(transaction_id)

        new_category = self._collect_category(transaction_type)
        self._service.update_transaction_category(transaction_id, new_category)
        
        if self._state_manager.has_active_filter():
            self._state_manager.clear_filtered_list()

    def _update_description(self, transaction_id: int) -> None:
        new_description = self._collect_description()
        self._service.update_transaction_description(transaction_id, new_description)

    # Métodos individuais para as opções de ordenação -----------------------------------------------------------------
    def _sort_by_amount(self, transaction_list : list[Transaction] | None) -> list[Transaction]:
        sort_order_menu = ptbuilder.build_transaction_sort_order_submenu()
        sort_order_choices = ptbuilder.get_transaction_sort_order_choices()

        self._console.print(sort_order_menu, justify='center')
        option = PromptPTBR.ask('Digite o número da ordenação desejada', choices=sort_order_choices)
        order = 'crescente' if option == '1' else 'decrescente'

        if transaction_list is None:
            return self._service.sort_by_amount(order)
        
        return self._service.sort_by_amount(order, transaction_list)

    def _sort_by_date(self, transaction_list : list[Transaction] | None) -> list[Transaction]:
        sort_order_menu = ptbuilder.build_transaction_sort_order_submenu()
        sort_order_choices = ptbuilder.get_transaction_sort_order_choices()

        self._console.print(sort_order_menu, justify='center')
        option = PromptPTBR.ask('Digite o número da ordenação desejada', choices=sort_order_choices)
        order = 'crescente' if option == '1' else 'decrescente'

        if transaction_list is None:
            return self._service.sort_by_date(order)
        
        return self._service.sort_by_date(order, transaction_list)

    def _sort_by_id(self, transaction_list : list[Transaction] | None) -> list[Transaction]:
        sort_order_menu = ptbuilder.build_transaction_sort_order_submenu()
        sort_order_choices = ptbuilder.get_transaction_sort_order_choices()

        self._console.print(sort_order_menu, justify='center')
        option = PromptPTBR.ask('Digite o número da ordenação desejada', choices=sort_order_choices)
        order = 'crescente' if option == '1' else 'decrescente'

        if transaction_list is None:
            return self._service.sort_by_id(order)
        
        return self._service.sort_by_id(order, transaction_list)

    # Métodos individuais para as opções de filtragem -----------------------------------------------------------------
    def _filter_by_amount(self, transaction_list: list[Transaction]) -> list[Transaction]:
        orientation_msg = 'Você pode omitir um dos valores abaixos para a filtragem.'
        orientation_panel = ptbuilder.build_orientation_panel(orientation_msg)

        self._console.print(orientation_panel)
        start_amount: str = self._console.input('Digite o valor inicial de filtragem: ').strip() or None
        end_amount: str = self._console.input('Digite o valor final de filtragem: ').strip() or None

        return self._service.filter_by_amount_range(transaction_list, start_amount, end_amount)
    
    def _filter_by_type(self, transaction_list: list[Transaction]) -> list[Transaction]:
        transaction_type: str = self._collect_transaction_type()

        return self._service.filter_by_type(transaction_type, transaction_list)
    
    def _filter_by_date(self, transaction_list: list[Transaction]) -> list[Transaction]:
        orientation_msg = 'Você pode omitir uma das datas abaixos para a filtragem.'
        orientation_panel = ptbuilder.build_orientation_panel(orientation_msg)
        DATE_FORMAT = """[yellow]DD/MM/AAAA
Exemplo: 01/01/2025[/]"""
        date_format_panel = ptbuilder.build_orientation_panel(DATE_FORMAT)

        self._console.print('\n')
        self._console.print(date_format_panel)
        self._console.print(orientation_panel)
        start_date: str = self._console.input('Digite a data inicial de filtragem: ').strip() or None
        end_date: str = self._console.input('Digite a data final de filtragem: ').strip() or None
        
        return self._service.filter_by_date_range(transaction_list, start_date, end_date)

    def _filter_by_category(self, transaction_list: list[Transaction]) -> list[Transaction]:
        all_categories_menu = ptbuilder.build_all_categories_filter_menu()
        all_categories_choices = ptbuilder.get_all_categories_choices()

        self._console.print('\n')
        self._console.print(all_categories_menu, justify='center')
        category_option: str = PromptPTBR.ask(
            'Digite o número da categoria',
            choices=all_categories_choices
        )
        category: str = ALL_CATEGORIES_TABLE.get(category_option)

        if transaction_list is None:
            return self._service.filter_by_category(category)
        
        return self._service.filter_by_category(category, transaction_list)

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
        transaction_type_panel: Panel = ptbuilder.build_transaction_type_menu()
        transaction_type_choices: list[str] = ptbuilder.get_transaction_type_choices()

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

        date_format_panel = ptbuilder.build_orientation_panel(DATE_FORMAT)

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
        category_panel : Panel = ptbuilder.build_category_menu(transaction_type_str)
        category_choices: str = ptbuilder.get_category_choices(transaction_type_str)
                
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

        description_panel = ptbuilder.build_orientation_panel(description_note)

        while True:
            self._console.print('\n')
            self._console.print(description_panel)
            description = self._console.input('Digite uma descrição para a transação: ')
            self._console.print('\n')

            if not self._validate_description_format(description):
                self._console.print('[red]A descrição deve conter no máximo 90 caracteres.[/]')
                continue

            return description if description else None

    # Métodos internos de validação por regex -------------------------------------------------------------------------
    def _validate_amount_format(self, amount_str: str) -> bool:
        if not bool(re.fullmatch(AMOUNT_PATTERN, amount_str)):
            return False
        
        return True
    
    def _validate_date_format(self, date_str: str) -> bool:
        if not bool(re.fullmatch(DATE_PATTERN, date_str)):
            return False
        
        return True
    
    def _validate_description_format(self, description: str) -> bool:
        if not bool(re.fullmatch(DESCRIPTION_PATTERN, description)):
            return False
        
        return True

    # Métodos internos útilitários ------------------------------------------------------------------------------------
    def _get_transaction_list_for_display(self) -> list[Transaction]:
            if self._state_manager.has_active_filter():
                transaction_list = self._state_manager.filtered_list
            
            else:
                transaction_list = self._service.get_all_transactions()

            return transaction_list
    
    def _show_all_transactions(self, transaction_list: list[Transaction]) -> list[Transaction]:
        """Mostra a lista de todas as transações no terminal"""
        statistics = self._service.get_statistics()
        transaction_table: Table = ptbuilder.build_transaction_table(transaction_list, statistics)

        self._console.print(Rule('[bold blue]Lista de Transações[/]', style='cyan'))
        self._console.print('\n')        
        self._console.print(transaction_table, justify='center')

        return transaction_list
    
    def _print_section_title(self, rule_title: str, characters: str = '─') -> None:
        self._console.print(Rule(f'\n[bold blue]{rule_title}[/]', style='cyan', characters=characters))
        self._console.print('\n')

    def _clear_screen(self):
        os.system('cls')
        self._console.print('\n')

    def _pause_and_clear(self, msg: str='\nPressione enter para voltar...'):
        self._console.input(msg)
        self._clear_screen()