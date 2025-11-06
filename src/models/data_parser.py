from datetime import datetime, date

from src.models.enums import TransactionType, IncomeCategory, ExpenseCategory
from src.models.typed_dicts import ParsedTransaction, SerializedTransaction



# Métodos de conversão geral ---------------------------------------------------------------------------------------
def parse_from_user(str_dict: dict[str, str]) -> ParsedTransaction:
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

    amount: float | int = to_valid_amount(amount_str)

    transaction_type: TransactionType = to_valid_transaction_type(transaction_type_str)
    
    transaction_date: date = to_valid_transaction_date(transaction_date_str, DATE_FORMAT)
    
    category: IncomeCategory| ExpenseCategory | None = to_valid_category(category_str)
                    
    return {
        'amount' : amount,
        'transaction_type' : transaction_type,
        'transaction_date' : transaction_date,
        'category' : category,
        'description' : description
    }

def parse_from_json(transaction_json: list[SerializedTransaction]) -> list[ParsedTransaction]:
    DATE_FORMAT = "%d/%m/%Y"
    parsed_transaction_dict_list = []
    for transaction_dict in transaction_json:
        amount = transaction_dict['amount']
        transaction_type_str = transaction_dict['transaction_type']
        transaction_date_str = transaction_dict['transaction_date']
        category_str = transaction_dict['category']
        description = transaction_dict['description']
        transaction_id = transaction_dict['transaction_id']

        transaction_type = to_valid_transaction_type(transaction_type_str)
        transaction_date = to_valid_transaction_date(transaction_date_str, DATE_FORMAT)
        category = to_valid_category(category_str)

        transaction_dict = {
        'amount' : amount,
        'transaction_type' : transaction_type,
        'transaction_date' : transaction_date,
        'category' : category,
        'description' : description,
        'transaction_id' : transaction_id
    }
        parsed_transaction_dict_list.append(transaction_dict)

    return parsed_transaction_dict_list

# Métodos individuais de conversão --------------------------------------------------------------------------------
def to_valid_amount(amount_str: str) -> float:
    try:
        amount_str_normalized = amount_str.strip()
        if ',' in amount_str_normalized:
            amount_str_normalized = amount_str.strip().replace('.', '').replace(',', '.')
        
        amount = float(amount_str_normalized)
    except ValueError:
        raise ValueError(f'{amount_str} não é um valor válido!')

    return amount

def to_valid_transaction_type(transaction_type_str: str) -> TransactionType:
    try:
        transaction_type_str_normalized = transaction_type_str.strip().lower()
        transaction_type = TransactionType(transaction_type_str_normalized)
    except ValueError:
        raise ValueError(f'{transaction_type_str} não é um tipo válido!'
                            'Só deve ser aceito "receita" ou "despesa".')
    
    return transaction_type

def to_valid_transaction_date(transaction_date_str: str, date_format) -> date:
    try:
        transaction_date_str_normalized = transaction_date_str.strip()
        transaction_date = datetime.strptime(transaction_date_str_normalized, date_format).date()
    except ValueError:
        raise ValueError(f'{transaction_date_str} não é uma data válida! Siga o formato DD/MM/AAAA.')
    
    return transaction_date

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