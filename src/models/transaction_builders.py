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
    # Método de conversão geral ---------------------------------------------------------------------------------------
    @staticmethod
    def parse(str_dict: dict[str, str]) -> ParsedTransaction:
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

        amount: float = DataParser.to_valid_amount(amount_str)

        transaction_type: TransactionType = DataParser.to_valid_transaction_type(transaction_type_str)
        
        transaction_date: date = DataParser.to_valid_transaction_date(transaction_date_str, DATE_FORMAT)
        
        category: IncomeCategory| ExpenseCategory | None = DataParser.to_valid_category(category_str)
                        
        return {
            'amount' : amount,
            'transaction_type' : transaction_type,
            'transaction_date' : transaction_date,
            'category' : category,
            'description' : description
        }
    
    # Métodos individuais de conversão --------------------------------------------------------------------------------
    @staticmethod
    def to_valid_amount(amount_str: str) -> float:
        try:
            amount_str_normalized = amount_str.strip()
            if ',' in amount_str_normalized:
                amount_str_normalized = amount_str.strip().replace('.', '').replace(',', '.')
            
            amount = float(amount_str_normalized)
        except ValueError:
            raise ValueError(f'{amount_str} não é um valor válido!')

        return amount
    
    @staticmethod
    def to_valid_transaction_type(transaction_type_str: str) -> TransactionType:
        try:
            transaction_type_str_normalized = transaction_type_str.strip().lower()
            transaction_type = TransactionType(transaction_type_str_normalized)
        except ValueError:
            raise ValueError(f'{transaction_type_str} não é um tipo válido!'
                              'Só deve ser aceito "receita" ou "despesa".')
        
        return transaction_type
    
    @staticmethod
    def to_valid_transaction_date(transaction_date_str: str, date_format) -> date:
        try:
            transaction_date_str_normalized = transaction_date_str.strip()
            transaction_date = datetime.strptime(transaction_date_str_normalized, date_format).date()
        except ValueError:
            raise ValueError(f'{transaction_date_str} não é uma data válida! Siga o formato DD/MM/AAAA.')
        
        return transaction_date
    
    @staticmethod
    def to_valid_category(category_str: str | None=None) -> IncomeCategory | ExpenseCategory | None:
        category: IncomeCategory | ExpenseCategory | None = None
        if category_str is not None:
            category_str_normalized: str = category_str.strip().lower()
            if category_str_normalized in IncomeCategory.get_all_values():
                category = IncomeCategory(category_str_normalized)
                
            elif category_str_normalized in ExpenseCategory.get_all_values():
                category = ExpenseCategory(category_str_normalized)

            else:
                raise ValueError(f'{category_str} não é uma categoria válida!')
                
        return category
    
    @staticmethod
    def to_boolean_sort_order(order: str='crescente') -> bool:
        """
        Normaliza a string e converte a ordem de ordenação em booleano para uso com sorted(reverse=...).

        - 'crescente'  => True  (reverse=False)
        - 'decrescente' => False (reverse=True)

        Inverte o valor para se alinhar ao parâmetro reverse.
        """
        order_normalized = order.strip().lower()
        match order_normalized:
            case 'decrescente':
                return True
            case 'crescente':
                return False
            case _:
                raise ValueError(f'Não reconheço {order}!')

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