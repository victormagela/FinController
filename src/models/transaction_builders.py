from typing import TypedDict, NotRequired
from datetime import datetime, date

from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory


class ParsedTransaction(TypedDict):
    amount : float
    transaction_type : TransactionType
    transaction_date : date
    category : NotRequired[IncomeCategory | ExpenseCategory | None]
    description : NotRequired[str | None]


class DataParser:
    def parse(self, str_dict: dict[str, str]) -> ParsedTransaction:
        """
        Converte dados recebidos do usuário nos tipos corretos para a construção do objeto Transaction.
        
        Returns:
        Dicionário com chaves str e valores com os dados que foram convertidos.

        Raises:
        Levanta erros ValueErro para qualquer entrada inválida.
        """

        DATE_FORMAT = "%d/%m/%Y"
        
        amount_str: str = str_dict['amount']
        transaction_type_str: str = str_dict['transaction_type']
        transaction_date_str: str = str_dict['transaction_date']
        category_str: str | None = str_dict.get('category', None)
        description: str | None = str_dict.get('description', None)

        try:
            amount_str_normalized = amount_str.strip()
            if ',' in amount_str_normalized:
                amount_str_normalized = amount_str.strip().replace('.', '').replace(',', '.')
            amount = float(amount_str_normalized)
        except ValueError:
            raise ValueError(f'{amount_str} não é um valor válido.')

        try:
            transaction_type_str_normalized = transaction_type_str.strip().lower()
            transaction_type = TransactionType(transaction_type_str_normalized)
        except ValueError:
            raise ValueError(f'{transaction_type_str} não é um tipo válido. Só deve ser aceito "receita" ou "despesa".')
        
        try:
            transaction_date_str_normalized = transaction_date_str.strip()
            transaction_date = datetime.strptime(transaction_date_str_normalized, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(f'{transaction_date_str} não é uma data válida. Siga o formato DD/MM/AAAA')
        
        category = None
        if category_str is not None:
            category_str_normalized = category_str.strip().lower()
            try:
                if transaction_type == TransactionType.INCOME:
                    category = IncomeCategory(category_str_normalized)
                
                elif transaction_type == TransactionType.EXPENSE:
                    category = ExpenseCategory(category_str_normalized)
            except ValueError:
                if transaction_type == TransactionType.INCOME:
                    raise ValueError(f'{category_str} não é uma categoria de receita válida.')
                elif transaction_type == TransactionType.EXPENSE:
                    raise ValueError(f'{category_str} não é uma categoria de despesa válida.')
                        
        return {
            'amount' : amount,
            'transaction_type' : transaction_type,
            'transaction_date' : transaction_date,
            'category' : category,
            'description' : description
        }
    

class TransactionFactory:
    """Construtor alternativo"""

    @staticmethod
    def from_parser(parsed_dict: ParsedTransaction) -> Transaction:
        """Retorna uma instância de Transaction a partir do dicionário obtido de DataParser com os tipos corretos."""        

        amount: float = parsed_dict['amount']
        transaction_type: TransactionType = parsed_dict['transaction_type']
        transaction_date: date = parsed_dict['transaction_date']
        category: ExpenseCategory | IncomeCategory | None = parsed_dict.get('category', None)
        description: str | None = parsed_dict.get('description', None)
                
        return Transaction(amount, transaction_type, transaction_date, category, description)