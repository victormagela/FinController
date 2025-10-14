from enum import Enum
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'pt_br')


class TransactionType(Enum):
    INCOME = 'receita'
    EXPENSE = 'despesa'


class Transaction():
    def __init__(self, value: float, transaction_type: TransactionType, date: datetime.date, category: str = 'Categoria não adicionada', description: str = 'Descrição não adicionada'):
        self._validate_value(value)
        self._value = value
        self._validate_type(transaction_type)
        self._transaction_type = transaction_type
        self._validate_date(date)
        self._date = date
        self._category = category
        self._description = description

    def __repr__(self):
        return (f"value = {self._value} "
                f"transaction_type = {self._transaction_type} "
                f"date = {self._date} "
                f"category = '{self._category}' "
                f"description = '{self._description}'")

    def __str__(self):
        return f'{self.transaction_type_str} de {self.value_formated_ptbr} em {self.date_str}.| {self._category}| {self._description}'

    @staticmethod
    def from_user_input(value_str: str, transaction_type_str: str, date_str: str, category: str = 'Categoria não adicionada', description: str = 'Descrição não adicionada'):
        try:
            value = float(value_str.strip())
        except ValueError:
            raise ValueError(f'{value_str} não é um valor válido.')
        
        try:
            transaction_type = TransactionType(transaction_type_str.lower().strip())
        except ValueError:
            raise ValueError(f'{transaction_type_str} não é um tipo válido. Use apenas "receita" ou "despesa".')
        
        try:
            date = datetime.datetime.strptime(date_str.strip(), "%d/%m/%Y").date()
        except ValueError:
            raise ValueError(f'{date_str} não é uma data válida. Siga o formato DD/MM/AAAA')

        return Transaction(value, transaction_type, date, category, description)

    @property
    def transaction_type(self):
        return self._transaction_type

    @property
    def transaction_type_str(self):
        return str(self._transaction_type.value).capitalize()

    @property
    def value(self):
        return self._value
    
    @property
    def value_formated_ptbr(self):
        return locale.currency(self._value, grouping=True)

    @property   
    def date(self):
        return self._date
    
    @property
    def date_str(self):
        return datetime.datetime.strftime(self._date, '%d/%m/%Y')

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        if not isinstance(category, str) or 3 > len(category) or len(category) > 50:
            raise ValueError('Categoria inválida!')
        
        self._category = category

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        if not isinstance(description, str) or 3 > len(description) or len(description) > 200:
            raise ValueError('Descrição inválida! A descrição deve conter no mínimo 3 caracteres e no máximo 200 caracteres')
        
        self._description = description

    def _validate_type(self, transaction_type) -> None:
        if not isinstance(transaction_type, TransactionType):
            raise ValueError('Tipo inválido!')

    def _validate_value(self, value) -> None:
        if not isinstance(value, (float, int)) or not value > 0:
            raise ValueError('Valor inválido!')
        
    def _validate_date(self, date) -> None:
        if not isinstance(date, datetime.date) or date > datetime.date.today() :
            raise ValueError('Data inválida!')