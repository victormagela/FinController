"""Este módulo cria TypedDicts para a definição correta de Type Hints em outros módulos."""
from typing import TypedDict, NotRequired
from datetime import date

from src.models.enums import TransactionType, IncomeCategory, ExpenseCategory


class ParsedTransaction(TypedDict):
    amount : float | int
    transaction_type : TransactionType
    transaction_date : date
    category : NotRequired[IncomeCategory | ExpenseCategory | None]
    description : NotRequired[str | None]
    """
    Este campo só é passado quando obtido transações de fora do programa,
    caso contrário o ID é gerado dinâmicamente
    """
    transaction_id : NotRequired[int]


class SerializedTransaction(TypedDict):
    amount : float | int
    transaction_type : str
    transaction_date : str
    category : str
    description : str
    transaction_id : int