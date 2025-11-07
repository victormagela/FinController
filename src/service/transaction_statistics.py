from dataclasses import dataclass, field
from collections import Counter
import statistics

from src.models.transaction import Transaction
from src.models.enums import TransactionType, IncomeCategory, ExpenseCategory

@dataclass
class TransactionStatistics:
       transaction_count: int = 0
       income_transaction_count: int = 0
       expense_transaction_count: int = 0
       total_income: int | float = 0
       total_expense: int | float = 0
       balance: int | float = 0
       highest_income_amount: int | float = 0
       highest_expense_amount: int | float = 0
       income_category_with_highest_amount: IncomeCategory | None = None
       expense_category_with_highest_amount: ExpenseCategory | None = None
       income_category_with_most_transactions: IncomeCategory | None = None
       expense_category_with_most_transactions: ExpenseCategory | None = None
       total_per_income_category: dict[IncomeCategory, int | float] = field(default_factory=dict)
       total_per_expense_category: dict[ExpenseCategory, int | float] = field(default_factory=dict)
       percentage_per_income_category: dict[IncomeCategory, float] = field(default_factory=dict)
       percentage_per_expense_category: dict[ExpenseCategory, float] = field(default_factory=dict)
       count_per_income_category: dict[IncomeCategory, int] = field(default_factory=dict)
       count_per_expense_category: dict[ExpenseCategory, int] = field(default_factory=dict)
       count_percentage_per_income_category: dict[IncomeCategory, float] = field(default_factory=dict)
       count_percentage_per_expense_category: dict[ExpenseCategory, float] = field(default_factory=dict)
       average_income: float = 0.0
       average_expense: float = 0.0
       median_income: int | float = 0
       median_expense: int | float = 0

class TransactionStatisticsCalculator:
       def __init__(self, transaction_list: list[Transaction]):
              self._income_transactions = [
                     transaction for transaction in transaction_list 
                     if transaction.transaction_type == TransactionType.INCOME
                     ]
              self._expense_transactions = [
                     transaction for transaction in transaction_list 
                     if transaction.transaction_type == TransactionType.EXPENSE
              ]
              self.statistics = TransactionStatistics()
              if transaction_list:
                     self._calculate_statistics()

       def update_statistics(self, new_transaction_list: list[Transaction]) -> None:
              self._income_transactions = [
                     transaction for transaction in new_transaction_list 
                     if transaction.transaction_type == TransactionType.INCOME
                     ]
              self._expense_transactions = [
                     transaction for transaction in new_transaction_list 
                     if transaction.transaction_type == TransactionType.EXPENSE
              ]
              if not new_transaction_list:
                     self.statistics = TransactionStatistics()
                     return
              
              self._calculate_statistics()

       # Métodos privados ---------------------------------------------------------------------------------------------
       def _calculate_statistics(self) -> None:
              stats = self.statistics

              stats.transaction_count = self._get_transaction_count()
              stats.income_transaction_count = self._get_income_transaction_count()
              stats.expense_transaction_count = self._get_expense_transaction_count()
              stats.total_income = self._calculate_total_income()
              stats.total_expense = self._calculate_total_expense()
              stats.balance = self._calculate_balance()
              stats.highest_income_amount = self._get_highest_income_amount()
              stats.highest_expense_amount = self._get_highest_expense_amount()
              stats.income_category_with_highest_amount = self._get_income_category_with_highest_amount()
              stats.expense_category_with_highest_amount = self._get_expense_category_with_highest_amount()
              stats.income_category_with_most_transactions = (
                     self._get_income_category_with_most_transaction()
              )
              stats.expense_category_with_most_transactions = (
                     self._get_expense_category_with_most_transactions()
              )
              stats.total_per_income_category = self._calculate_total_per_income_category()
              stats.total_per_expense_category = self._calculate_total_per_expense_category()
              stats.percentage_per_income_category = self._calculate_percentage_per_income_category()
              stats.percentage_per_expense_category = self._calculate_percentage_per_expense_category()
              stats.count_per_income_category = self._get_count_per_income_category()
              stats.count_per_expense_category = self._get_count_per_expense_category()
              stats.count_percentage_per_income_category = self._calculate_count_percentage_per_income_category()
              stats.count_percentage_per_expense_category = self._calculate_count_percentage_per_expense_category()
              stats.average_income = self._calculate_average_income()
              stats.average_expense = self._calculate_average_expense()
              stats.median_income = self._get_median_income()
              stats.median_expense = self._get_median_expense()

       def _get_transaction_count(self) -> int:
              return len(self._income_transactions) + len(self._expense_transactions)
       
       def _get_income_transaction_count(self) -> int:
              return len(self._income_transactions)
       
       def _get_expense_transaction_count(self) -> int:
              return len(self._expense_transactions)

       def _calculate_total_income(self) -> float | int:
              result = 0
              for transaction in self._income_transactions:
                     result += transaction.amount
              
              return result

       def _calculate_total_expense(self) -> float | int:
              result = 0
              for transaction in self._expense_transactions:
                     result += transaction.amount
              
              return result

       def _calculate_balance(self) -> float | int:
              return self.statistics.total_income - self.statistics.total_expense
       
       def _get_highest_income_amount(self) -> float | int:
              if not self._income_transactions:
                     return 0
              
              transaction_with_highest_amount = self._get_income_transaction_with_highest_amount()
              return transaction_with_highest_amount.amount
       
       def _get_highest_expense_amount(self) -> float | int:
              if not self._expense_transactions:
                     return 0
              
              transaction_with_highest_amount = self._get_expense_transaction_with_highest_amount()
              return transaction_with_highest_amount.amount
       
       def _get_income_category_with_highest_amount(self) -> IncomeCategory | None:
              if not self._income_transactions:
                     return None
              
              transaction_with_highest_amount = self._get_income_transaction_with_highest_amount()
              return transaction_with_highest_amount.category
       
       def _get_expense_category_with_highest_amount(self) -> ExpenseCategory | None:
              if not self._expense_transactions:
                     return None
              
              transaction_with_highest_amount = self._get_expense_transaction_with_highest_amount()
              return transaction_with_highest_amount.category
       
       def _get_income_category_with_most_transaction(self) -> IncomeCategory | None:
              if not self._income_transactions:
                     return None
              
              category_list = [transaction.category for transaction in self._income_transactions]
              most_common_category, _ = Counter(category_list).most_common(1)[0]

              return most_common_category

       def _get_expense_category_with_most_transactions(self) -> ExpenseCategory | None:
              if not self._expense_transactions:
                     return None
              
              category_list = [transaction.category for transaction in self._expense_transactions]
              most_common_category, _ = Counter(category_list).most_common(1)[0]

              return most_common_category            
       
       def _calculate_total_per_income_category(self) -> dict[IncomeCategory, int | float]:
              if not self._income_transactions:
                     return {}
              
              totals = {}
              for transaction in self._income_transactions:
                     category = transaction.category
                     amount = transaction.amount
                     totals[category] = totals.get(category, 0) + amount

              return totals

       def _calculate_total_per_expense_category(self) -> dict[ExpenseCategory, int | float]:
              if not self._expense_transactions:
                     return {}
              
              totals = {}
              for transaction in self._expense_transactions:
                     category = transaction.category
                     amount = transaction.amount
                     totals[category] = totals.get(category, 0) + amount

              return totals

       def _calculate_percentage_per_income_category(self) -> dict[IncomeCategory, float]:
              if not self._income_transactions:
                     return {}
              
              income_total = self._calculate_total_income()
              income_totals_per_category = self._calculate_total_per_income_category()
              percentages = {}
              for category, total_per_category in income_totals_per_category.items():
                     percentages[category] = (total_per_category / income_total) * 100

              return percentages

       def _calculate_percentage_per_expense_category(self) -> dict[ExpenseCategory, float]:
              if not self._expense_transactions:
                     return {}
              
              expense_total = self._calculate_total_expense()
              expense_totals_per_category = self._calculate_total_per_expense_category()
              percentages = {}
              for category, total_per_category in expense_totals_per_category.items():
                     percentages[category] = (total_per_category / expense_total) * 100

              return percentages
       
       def _get_count_per_income_category(self) -> Counter[IncomeCategory]:
              if not self._income_transactions:
                     return {}
              
              category_list = [transaction.category for transaction in self._income_transactions]
              return Counter(category_list)
              
       def _get_count_per_expense_category(self) -> Counter[ExpenseCategory]:
              if not self._expense_transactions:
                     return {}
              
              category_list = [transaction.category for transaction in self._expense_transactions]
              return Counter(category_list)
       
       def _calculate_count_percentage_per_income_category(self) -> dict[IncomeCategory, float]:
              if not self._income_transactions:
                     return {}
              
              income_transaction_count = self._get_income_transaction_count()
              count_per_category = self._get_count_per_income_category()
              count_percentage = {}
              for category, count in count_per_category.items():
                     count_percentage[category] = (count / income_transaction_count) * 100

              return count_percentage
              
       def _calculate_count_percentage_per_expense_category(self) -> dict[ExpenseCategory, float]:
              if not self._expense_transactions:
                     return {}
              
              expense_transaction_count = self._get_expense_transaction_count()
              count_per_category = self._get_count_per_expense_category()
              count_percentage = {}
              for category, count in count_per_category.items():
                     count_percentage[category] = (count / expense_transaction_count) * 100

              return count_percentage
       
       def _calculate_average_income(self) -> float:
              if not self._income_transactions:
                     return 0.0
              
              income_transaction_total = self._calculate_total_income()
              income_transaction_count = self._get_income_transaction_count()
              return income_transaction_total / income_transaction_count
       
       def _calculate_average_expense(self) -> float:
              if not self._expense_transactions:
                     return 0.0
              
              expense_transaction_total = self._calculate_total_expense()
              expense_transaction_count = self._get_expense_transaction_count()
              return expense_transaction_total / expense_transaction_count
       
       def _get_median_income(self) -> int | float:
              if not self._income_transactions:
                     return 0
              
              amount_list = [transaction.amount for transaction in self._income_transactions]
              return statistics.median(amount_list)
       
       def _get_median_expense(self) -> int | float:
              if not self._expense_transactions:
                     return 0
              
              amount_list = [transaction.amount for transaction in self._expense_transactions]
              return statistics.median(amount_list)
       
       # Métodos menores auxiliares para calcular a transação com maior valor -----------------------------------------
       def _get_income_transaction_with_highest_amount(self) -> Transaction:
              return max(self._income_transactions, key=lambda t: t.amount)
       
       def _get_expense_transaction_with_highest_amount(self) -> Transaction:
              return max(self._expense_transactions, key=lambda t: t.amount)