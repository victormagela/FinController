from typing import TypedDict, NotRequired
from datetime import datetime, date

from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory


class ParsedTransaction(TypedDict):
    amount : float
    transaction_type : str
    transaction_date : date
    category : NotRequired[str|None]
    description : NotRequired[str|None]




class DataParser:
    def parse(self, str_dict: dict[str, str]) -> ParsedTransaction:
        DATE_FORMAT = "%d/%m/%Y"
        
        amount_str = str_dict['amount']
        transaction_type_str = str_dict['transaction_type']
        transacation_date_str = str_dict['transaction_date']
        category_str = str_dict.get('category', None)
        description = str_dict.get('description', None)

        try:
            amount_str_normalized = amount_str.strip().replace(',', '.')
            amount = float(amount_str_normalized)
        except ValueError:
            raise ValueError(f'{amount_str} não é um valor válido.')
        
        transaction_type_str_normalized = transaction_type_str.strip().lower()
        
        try:
            transacation_date_str_normalized = transacation_date_str.strip()
            transaction_date = datetime.strptime(transacation_date_str_normalized, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(f'{transacation_date_str_normalized} não é uma data válida. Siga o formato DD/MM/AAAA')
        
        if category_str is not None:
            category_str_normalized = category_str.strip().lower()
        
        return {
            'amount' : amount,
            'transaction_type' : transaction_type_str_normalized,
            'transaction_date' : transaction_date,
            'category' : category_str_normalized if category_str is not None else category_str,
            'description' : description
        }
    

class TransactionFactory:
    """Construtor alternativo"""

    @staticmethod
    def from_parser(parsed_dict: ParsedTransaction) -> Transaction:
        """
        Converte strings obtidas do DataParser, e retorna uma instância de Transaction.

        Argumentos:
        amount (float): valor da transação.
        transaction_type_normalized (str): string que pode ser 'receita' ou 'despesa', case insensitive.
        transaction_date_str (date): string que contém uma data, deve estar no formato DD/MM/AAAA.
        category_str (str): categoria opcional, com padrão 'outros'.
        description (str): descrição opcional, com padrão 'descrição não adicionada'.

        Returns:
        Transaction construída a partir dos valores convertidos e obtidos.

        Raises:
        Levanta erros ValueErro para qualquer entrada inválida.
        """        

        amount = parsed_dict['amount']
        transaction_type_normalized = parsed_dict['transaction_type']
        transaction_date = parsed_dict['transaction_date']
        category_str = parsed_dict.get('category', None)
        description = parsed_dict.get('description', None)

        try:
            transaction_type = TransactionType(transaction_type_normalized)
        except ValueError:
            raise ValueError(f'{transaction_type_normalized} não é um tipo válido. Use apenas "receita" ou "despesa".')

        if category_str is not None:
            category_str_normalized = category_str.strip().lower()
        
            if transaction_type == TransactionType.INCOME:
                try:
                    category = IncomeCategory(category_str_normalized)
                
                except ValueError:
                    raise ValueError(f'{category_str} não é uma categoria de receita válida!')   

            elif transaction_type == TransactionType.EXPENSE:
                try:
                    category = ExpenseCategory(category_str_normalized)
                
                except ValueError:
                    raise ValueError(f'{category_str} não é uma categoria de despesa válida!')
        
        else:
            category = None
                
        return Transaction(amount, transaction_type, transaction_date, category, description)