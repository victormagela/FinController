from datetime import date
import locale

# Tentativa de configurar locale para formatação em pt_br.
# Nem todos os sistemas têm o mesmo nome de locale, por isso protegemos com um bloco try/except.
try:
    locale.setlocale(locale.LC_ALL, 'pt_br.UTF-8')
except Exception:
    # Caso o sistema não reconheça, mantém a formatação padrão.
    pass


from src.models.transaction import TransactionType, IncomeCategory, ExpenseCategory
from src.utils.constants import DATE_FORMAT


def format_currency_for_ptbr(amount: float | int) -> str:
    return locale.currency(amount, grouping=True)

def format_transaction_type(transaction_type: TransactionType) -> str:
    return transaction_type.value.capitalize()

def format_date(transaction_date: date) -> str:
    return transaction_date.strftime(DATE_FORMAT)

def format_category(category: IncomeCategory | ExpenseCategory) -> str:
    return category.value.capitalize()

def capitalize_dict_values(dict: dict[str, str]) -> dict[str, str]:
    return {key:value.capitalize() for key, value in dict.items()}