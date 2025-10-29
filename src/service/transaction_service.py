from datetime import date

from src.models.transaction_manager import TransactionManager
from src.models.transaction_builders import ParsedTransaction, DataParser, TransactionFactory
from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory
import src.models.transaction_filters as filters


class TransactionService:
    """
    Camada de serviço que serve de ponte entre a interface de usuário e a lógica de negócio.

    Atributos privados:
    _manager: Instancia um novo TransactionManager para as operações sobre a lista de transações.
    """
    def __init__(self):
        self._manager = TransactionManager()

    # Métodos básicos de lista ----------------------------------------------------------------------------------------
    def add_transaction(self, str_dict: dict[str, str]) -> Transaction:
        parsed_transaction_dict: ParsedTransaction = DataParser.parse(str_dict)

        transaction: Transaction = TransactionFactory.from_parser(parsed_transaction_dict)
        self._manager.add_transaction(transaction)

        return transaction
    
    def get_all_transactions(self) -> list[Transaction]:
        return self._manager.get_all_transactions()
    
    def del_transaction(self, transaction_id: str) -> None:
        self._manager.del_transaction(transaction_id)

    def get_transaction_by_id(self, transaction_id: str):
        transaction_id: int = int(transaction_id)

        self._manager.get_transaction_by_id(transaction_id)

    def get_transaction_type(self, transaction_id: str) -> Transaction:
        transaction_id = int(transaction_id)

        transaction = self._manager.get_transaction_by_id(transaction_id)
        return transaction.transaction_type.value

    # Métodos de atualização ------------------------------------------------------------------------------------------
    def update_transaction_category(self, transaction_id: int, new_value: str):
        parsed_new_value: IncomeCategory | ExpenseCategory | None = DataParser.to_valid_category(new_value)
        self._manager.update_transaction_category(transaction_id, parsed_new_value)

    def update_transaction_description(self, transaction_id: int, new_value: str):
        self._manager.update_transaction_description(transaction_id, new_value)

    # Métodos de filtragem --------------------------------------------------------------------------------------------
    def filter_by_amount_range(
            self, 
            start_amount: str | None=None, 
            end_amount: str | None=None,
            filtered_list: list[Transaction]=None
            ) -> list[Transaction]:
        """"
        Inicializa os valores convertidos como None. Se o usuário não fornecer um valor,
        None será passado para o manager, que interpretará como "sem limite"
        (usando 0 ou 1e20 conforme apropriado).
        Se já houver uma lista filtrada, aplica o novo filtro sobre essa ao invés da lista original.
        """
        parsed_start_amount: int | float | None = None
        parsed_end_amount: int | float | None = None
        
        if start_amount and isinstance(start_amount, str):
            parsed_start_amount = DataParser.to_valid_amount(start_amount)   

        if end_amount and isinstance(end_amount, str):    
            parsed_end_amount = DataParser.to_valid_amount(end_amount)

        return self._manager.filter_by_amount_range(parsed_start_amount, parsed_end_amount) if filtered_list is None \
            else filters.filter_by_amount_range(filtered_list, parsed_start_amount, parsed_end_amount)
    
    def filter_by_type(self, transaction_type_str: str, filtered_list: list[Transaction]=None) -> list[Transaction]:
        parsed_type: TransactionType = DataParser.to_valid_transaction_type(transaction_type_str)

        return self._manager.filter_by_type(parsed_type) if filtered_list is None \
            else filters.filter_by_type(filtered_list, parsed_type)
    
    def filter_by_date_range(
            self, 
            start_date: str=None, 
            end_date: str=None, 
            filtered_list: list[Transaction]=None
            ) -> list[Transaction]:
        DATE_FORMAT = "%d/%m/%Y"
        
        """"Inicializa as datas convertidas como None. Se o usuário não fornecer uma data,
        None será passado para o manager, que interpretará como "sem limite"
        (usando date.min ou date.max conforme apropriado)"""
        parsed_start_date: date | None = None
        parsed_end_date: date | None = None
        if start_date:
            parsed_start_date = DataParser.to_valid_transaction_date(start_date, DATE_FORMAT)

        if end_date:
            parsed_end_date = DataParser.to_valid_transaction_date(end_date, DATE_FORMAT)

        return self._manager.filter_by_date_range(parsed_start_date, parsed_end_date) if filtered_list is None \
            else filters.filter_by_date_range(filtered_list, parsed_start_date, parsed_end_date)
    
    def filter_by_category(self, category: str, filtered_list: list[Transaction]=None) -> list[Transaction]:
        
        parsed_category: IncomeCategory | ExpenseCategory = DataParser.to_valid_category(category)

        # Decide qual lista usar como base
        if filtered_list is None:
            base_list: list[Transaction] = self._manager.get_all_transactions()
        else:
            base_list: list[Transaction] = filtered_list
        """
        Se a categoria for 'outros', como ela existe tanto em despesas quanto receitas, retornamos as transações
        dessa categoria de ambos os tipos.
        Se houver uma listada filtrada, aplicamos o novo filtro sobre ela ao invés da lista original.
        """
        if parsed_category == IncomeCategory.OTHERS or parsed_category == ExpenseCategory.OTHERS:
            income_others = filters.filter_by_category(base_list, IncomeCategory.OTHERS)
            expense_others = filters.filter_by_category(base_list, ExpenseCategory.OTHERS)
            return income_others + expense_others
    
        # Caso normal: filtrar pela categoria específica
        return filters.filter_by_category(base_list, parsed_category)
    
    # Métodos de ordenação --------------------------------------------------------------------------------------------
    def sort_by_amount(
            self, 
            order: str, 
            filtered_list: list[Transaction] | None= None
            ) -> list[Transaction]:
        reverse: bool = DataParser.to_boolean_sort_order(order)

        if filtered_list is None:
            return self._manager.sort_by_amount(reverse)
        
        return sorted(filtered_list, key=lambda transaction: transaction.amount, reverse=reverse)
    
    def sort_by_date(
            self, 
            order: str,
            filtered_list: list[Transaction] | None= None
            ) -> list[Transaction]:
        reverse: bool = DataParser.to_boolean_sort_order(order)

        if filtered_list is None:
            return self._manager.sort_by_date(reverse)
        
        return sorted(filtered_list, key=lambda transaction: transaction.transaction_date, reverse=reverse)
    
    def sort_by_id(self, 
                   order: str,
                   filtered_list: list[Transaction] | None= None
                   ) -> list[Transaction]:
        reverse: bool = DataParser.to_boolean_sort_order(order)

        if filtered_list is None:
            return self._manager.sort_by_id(reverse)
        
        return sorted(filtered_list, key=lambda transaction: transaction.id, reverse=reverse)