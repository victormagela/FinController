from datetime import date

from src.models.transaction_manager import TransactionManager
from src.models.transaction_builders import ParsedTransaction, DataParser, TransactionFactory
from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory


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
    def filter_by_amount_range(self, start_amount: str | float=0, end_amount: str | float=1e20) -> list[Transaction]:
        if isinstance(start_amount, str):
            parsed_start_amount: float = DataParser.to_valid_amount(start_amount)

        else:
            parsed_start_amount: float = start_amount    
        
        if isinstance(end_amount, str):    
            parsed_end_amount: float = DataParser.to_valid_amount(end_amount)
        
        else:
            parsed_end_amount: float = end_amount
            
        return self._manager.filter_by_amount_range(parsed_start_amount, parsed_end_amount)
    
    def filter_by_type(self, type_) -> list[Transaction]:
        parsed_type: TransactionType = DataParser.to_valid_transaction_type(type_)
        return self._manager.filter_by_type(parsed_type)
    
    def filter_by_date_range(self, start_date: str=None, end_date: str=None) -> list[Transaction]:
        DATE_FORMAT = "%d/%m/%Y"
        
        """"Inicializa as datas convertidas como None. Se o usuário não fornecer uma data,
        None será passado para o manager, que interpretará como "sem limite"
        (usando date.min ou date.max conforme apropriado)"""
        parsed_start_date: date | None = None
        parsed_end_date: date | None = None
        if start_date:
            parsed_start_date: date = DataParser.to_valid_transaction_date(start_date, DATE_FORMAT)

        if end_date:
            parsed_end_date: date = DataParser.to_valid_transaction_date(end_date, DATE_FORMAT)

        return self._manager.filter_by_date_range(parsed_start_date, parsed_end_date)
    
    def filter_by_category(self, category: str) -> list[Transaction]:
        
        parsed_category: IncomeCategory | ExpenseCategory = DataParser.to_valid_category(category)
        """Se a categoria for 'outros', como ela existe tanto em despesas quanto receitas, retornamos as transações
        da dessa categoria de ambos os tipos."""
        if parsed_category == IncomeCategory.OTHERS or parsed_category == ExpenseCategory.OTHERS:
            income_others: list[Transaction] = self._manager.filter_by_category(IncomeCategory.OTHERS)
            expense_others: list[Transaction] = self._manager.filter_by_category(ExpenseCategory.OTHERS)
            return income_others + expense_others
        
        return self._manager.filter_by_category(parsed_category)
    
    # Métodos de ordenação --------------------------------------------------------------------------------------------
    def sort_by_amount(self, order: str='crescente') -> list[Transaction]:
        reverse: bool = DataParser.to_boolean_sort_order(order)
        return self._manager.sort_by_amount(reverse)
    
    def sort_by_date(self, order: str='crescente') -> list[Transaction]:
        reverse: bool = DataParser.to_boolean_sort_order(order)
        return self._manager.sort_by_date(reverse)
    
    def sort_by_id(self, order: str='crescente') -> list[Transaction]:
        reverse: bool = DataParser.to_boolean_sort_order(order)
        return self._manager.sort_by_id(reverse)