from datetime import date

from src.models.transaction_manager import TransactionManager
from src.models.transaction_builders import ParsedTransaction, DataParser, TransactionFactory
from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory
from src.service.filter_engine import FilterEngine


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
        parsed_transaction_dict: ParsedTransaction = DataParser.parse_from_user(str_dict)

        transaction: Transaction = TransactionFactory.from_user(parsed_transaction_dict)
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
            transaction_list: list[Transaction], 
            start_amount: str | None=None, 
            end_amount: str | None=None,
            ) -> list[Transaction]:
        """"
        Inicializa os valores convertidos com valores padrão. Se o usuário não fornecer um valor,
        esses valores serão utilizados e interpretados como "sem limite"
        (usando 0 ou 1e20 conforme apropriado).
        """
        parsed_start_amount: int | float = 0
        parsed_end_amount: int | float = 1e20
        
        if start_amount and isinstance(start_amount, str):
            parsed_start_amount = DataParser.to_valid_amount(start_amount)   

        if end_amount and isinstance(end_amount, str):    
            parsed_end_amount = DataParser.to_valid_amount(end_amount)

        return FilterEngine.filter_by_amount_range(transaction_list, parsed_start_amount, parsed_end_amount)
    
    def filter_by_type(self, transaction_type_str: str, transaction_list: list[Transaction]) -> list[Transaction]:
        parsed_type: TransactionType = DataParser.to_valid_transaction_type(transaction_type_str)

        return FilterEngine.filter_by_type(parsed_type, transaction_list)
    
    def filter_by_date_range(
            self, 
            transaction_list: list[Transaction],
            start_date: str=None, 
            end_date: str=None, 
            ) -> list[Transaction]:
        DATE_FORMAT = "%d/%m/%Y"
        
        """"Inicializa as datas convertidas com valores padrão. Se o usuário não fornecer uma data,
        esses valores serão utilizados e interpretados como "sem limite"
        (usando date.min ou date.max conforme apropriado)"""
        parsed_start_date: date = date.min
        parsed_end_date: date = date.max
        if start_date:
            parsed_start_date = DataParser.to_valid_transaction_date(start_date, DATE_FORMAT)

        if end_date:
            parsed_end_date = DataParser.to_valid_transaction_date(end_date, DATE_FORMAT)

        return FilterEngine.filter_by_date_range(transaction_list, parsed_start_date, parsed_end_date) 
    
    def filter_by_category(self, category: str, transaction_list: list[Transaction]) -> list[Transaction]:
        
        parsed_category: IncomeCategory | ExpenseCategory = DataParser.to_valid_category(category)

        """
        Se a categoria for 'outros', como ela existe tanto em despesas quanto receitas, retornamos as transações
        dessa categoria de ambos os tipos.
        Se houver uma listada filtrada, aplicamos o novo filtro sobre ela ao invés da lista original.
        """
        if parsed_category == IncomeCategory.OTHERS or parsed_category == ExpenseCategory.OTHERS:
            income_others = FilterEngine.filter_by_category(IncomeCategory.OTHERS, transaction_list)
            expense_others = FilterEngine.filter_by_category(ExpenseCategory.OTHERS, transaction_list)
            return income_others + expense_others
    
        # Caso normal: filtrar pela categoria específica
        return FilterEngine.filter_by_category(parsed_category, transaction_list)
    
    # Métodos de ordenação --------------------------------------------------------------------------------------------
    def sort_by_amount(
            self, 
            order: str, 
            transaction_list: list[Transaction]
            ) -> list[Transaction]:
        reverse: bool = DataParser.to_boolean_sort_order(order)

        return FilterEngine.sort_by_amount(reverse, transaction_list)
    
    def sort_by_date(
            self, 
            order: str,
            transaction_list: list[Transaction]
            ) -> list[Transaction]:
        reverse: bool = DataParser.to_boolean_sort_order(order)
        return FilterEngine.sort_by_date(reverse, transaction_list)
    
    def sort_by_id(
            self, 
            order: str,
            transaction_list: list[Transaction]
            ) -> list[Transaction]:
        reverse: bool = DataParser.to_boolean_sort_order(order)

        return FilterEngine.sort_by_id(reverse, transaction_list)