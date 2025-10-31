from datetime import date

from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory


class FilterEngine:
    # Métodos de filtragem --------------------------------------------------------------------------------------------
    @staticmethod
    def filter_by_amount_range(
            transaction_list: list[Transaction],
            start_amount: int | float, 
            end_amount: int | float,
            ) -> list[Transaction]:
        return [
            transaction for transaction in transaction_list \
                if start_amount <= transaction.amount <= end_amount
            ]
    
    @staticmethod
    def filter_by_type(transaction_type: TransactionType, transaction_list: list[Transaction]) -> list[Transaction]:
        return [
            transaction for transaction in transaction_list if transaction.transaction_type == transaction_type
            ]
    
    @staticmethod
    def filter_by_date_range( 
            transaction_list: list[Transaction],
            start_date: date, 
            end_date: date, 
            ) -> list[Transaction]:
        return [
            transaction for transaction in transaction_list \
                if start_date <= transaction.transaction_date <= end_date]
    
    @staticmethod
    def filter_by_category(category: IncomeCategory | ExpenseCategory, transaction_list: list[Transaction]) -> list[Transaction]:
        return [transaction for transaction in transaction_list if transaction.category == category]
    
    # Métodos de ordenação --------------------------------------------------------------------------------------------
    @staticmethod
    def sort_by_amount(
            reverse: bool, 
            transaction_list: list[Transaction]
            ) -> list[Transaction]:
        
        return sorted(transaction_list, key=lambda transaction: transaction.amount, reverse=reverse)
    
    @staticmethod
    def sort_by_date( 
            reverse: bool,
            transaction_list: list[Transaction]
            ) -> list[Transaction]:
        
        return sorted(transaction_list, key=lambda transaction: transaction.transaction_date, reverse=reverse)
    
    @staticmethod
    def sort_by_id( 
                   reverse: bool,
                   transaction_list: list[Transaction]
                   ) -> list[Transaction]:
        
        return sorted(transaction_list, key=lambda transaction: transaction.id, reverse=reverse)