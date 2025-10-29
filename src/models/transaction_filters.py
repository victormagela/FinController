from datetime import date

from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory


def filter_by_amount_range(
        transaction_list: list[Transaction], 
        start: int | float | None=None, 
        end: int | float | None=None
        ) -> list[Transaction]:
    """Filtra a lista por um alcance de valor, e retorna uma nova lista com somente as transações neste alcance."""
    if start is None:
        start = 0
        
    if end is None:
        end = 1e20

    return [transaction for transaction in transaction_list if start <= transaction.amount <= end]
    
def filter_by_type(transaction_list: list[Transaction], transaction_type: TransactionType) -> list[Transaction]:
    """Filtra a lista por tipo de transação, e retorna uma nova lista com somente as transações deste tipo"""
    return [
        transaction for transaction in transaction_list if transaction.transaction_type == transaction_type
        ]
    
def filter_by_date_range(
        transaction_list: list[Transaction], 
        start: date | None=None, end: date | None=None
        ) -> list[Transaction]:
    """Filtra a lista por período, e retorna uma nova lista com somente as transações feitas neste período"""
    if start is None:
        start = date.min
        
    if end is None:
        end = date.max

    return [transaction for transaction in transaction_list if start <= transaction.transaction_date <= end]

def filter_by_category(
        transaction_list: list[Transaction], 
        category: IncomeCategory | ExpenseCategory
        ) -> list[Transaction]:
    """Filtra a lista por categoria, e retorna uma nova lista com somente as transações desta categoria"""
    return [transaction for transaction in transaction_list if transaction.category == category]