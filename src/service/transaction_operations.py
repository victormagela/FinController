from datetime import date

from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory


# Métodos de filtragem --------------------------------------------------------------------------------------------
def filter_by_amount_range(
        transaction_list: list[Transaction],
        start_amount: int | float, 
        end_amount: int | float,
    ) -> list[Transaction]:
    return [
        transaction for transaction in transaction_list \
            if start_amount <= transaction.amount <= end_amount
    ]
    
def filter_by_type(transaction_type: TransactionType, transaction_list: list[Transaction]) -> list[Transaction]:
    return [
        transaction for transaction in transaction_list if transaction.transaction_type == transaction_type
    ]
    
def filter_by_date_range( 
        transaction_list: list[Transaction],
        start_date: date, 
        end_date: date, 
    ) -> list[Transaction]:
    return [
        transaction for transaction in transaction_list \
            if start_date <= transaction.transaction_date <= end_date]
    
def filter_by_category(category: IncomeCategory | ExpenseCategory, transaction_list: list[Transaction]) -> list[Transaction]:
    return [transaction for transaction in transaction_list if transaction.category == category]
    
# Métodos de ordenação --------------------------------------------------------------------------------------------
def sort_by_amount(
        reverse: bool, 
        transaction_list: list[Transaction]
    ) -> list[Transaction]:
        
    return sorted(transaction_list, key=lambda transaction: transaction.amount, reverse=reverse)
    
def sort_by_date( 
        reverse: bool,
        transaction_list: list[Transaction]
    ) -> list[Transaction]:
        
    return sorted(transaction_list, key=lambda transaction: transaction.transaction_date, reverse=reverse)
    
def sort_by_id( 
                reverse: bool,
                transaction_list: list[Transaction]
    ) -> list[Transaction]:
        
     return sorted(transaction_list, key=lambda transaction: transaction.id, reverse=reverse)

def get_min_date(transaction_list: list[Transaction]) -> date:
    date_list = [transaction.transaction_date for transaction in transaction_list]
    return min(date_list)

def get_max_date(transaction_list: list[Transaction]) -> date:
    date_list = [transaction.transaction_date for transaction in transaction_list]
    return max(date_list)