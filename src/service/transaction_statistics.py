from src.models.transaction import Transaction, TransactionType


def get_number_of_transactions(transaction_list: list[Transaction]) -> int:
    return len(transaction_list)

def calculate_balance(transaction_list: list[Transaction]) -> float | int:
        total_income = calculate_total_income(transaction_list)

        total_expense = calculate_total_expense(transaction_list)

        return total_income - total_expense

def calculate_total_income(transaction_list: list[Transaction]) -> float | int:
        result = 0
        for transaction in transaction_list:
               if transaction.transaction_type == TransactionType.INCOME:
                      result += transaction.amount
        
        return result

def calculate_total_expense(transaction_list: list[Transaction]) -> float | int:
        result = 0
        for transaction in transaction_list:
               if transaction.transaction_type == TransactionType.EXPENSE:
                      result += transaction.amount
        
        return result