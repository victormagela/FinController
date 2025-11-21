from __future__ import annotations

from datetime import date

from src.models.typed_dicts import ParsedTransaction
from src.models.enums import TransactionType, IncomeCategory, ExpenseCategory


class Transaction():
    """
    Representa uma transação financeira simples.

    Atributos privados:
    _value (float): valor positivo da transação.
    _transaction_type (TransactionType): tipo da transação (receita ou despesa).
    _transaction_date (datetime.date): data que foi feita a transação (não aceita datas futuras).
    _category (str): atributo opcional, define a categoria da transação (máximo de 50 caracteres e mínimo de 3).
    _description (str): atributo opcional, adiciona uma descrição mais longa da transação (máximo de 200 caracteres 
    e mínimo de 3).

    Exemplos:
    Transaction(10.50, TransactionType.INCOME, date(2025, 10, 14))
    Transaction(45, TransactionType.EXPENSE, date(2025, 09, 20), 'alimentação', 
    'Saí para almoçar fora de casa')
    """
    _transaction_counter: int = 0 # Contador de instâncias

    def __init__(
                 self,
                 amount: float, 
                 transaction_type: TransactionType, 
                 transaction_date: date, 
                 category: IncomeCategory | ExpenseCategory = None, 
                 description: str = None,
                 transaction_id: int = None) -> None:
        self._validate_amount(amount)
        self._amount: float = amount
        self._validate_type(transaction_type)
        self._transaction_type: TransactionType = transaction_type
        self._validate_date(transaction_date)
        self._transaction_date: date = transaction_date
        if category is None:
            match transaction_type:
                case TransactionType.INCOME:
                    self._category: IncomeCategory = IncomeCategory.OTHERS
                case TransactionType.EXPENSE:
                    self._category: ExpenseCategory = ExpenseCategory.OTHERS
        else:
            category = self._normalize_others_category_ambiguity(category)
            self._validate_category(category)
            self._category: IncomeCategory | ExpenseCategory = category
        if description is None:
            self._description: str = 'Descrição não adicionada'
        else:
            self._description: str = description
        if transaction_id is None:
            # Incrementa o contador da classe em 1, e define o ID da transação com este novo valor. 
            # Garante que cada nova instância terá um ID único.
            Transaction._transaction_counter += 1
            self._id: int = Transaction._transaction_counter
        else:
            # Se um ID for passado, como no caso da leitura de um arquivo de transações
            # Define o ID da transação com esse ID passado
            self._id = transaction_id
            if transaction_id > Transaction._transaction_counter:
                # Se o ID passado for maior que o contador atual de transações, chama o método que define o contador
                # de transações com o valor do novo ID. Garantindo que qualquer nova transação sempre será gerada
                # a partir do maior ID.
                Transaction.set_transaction_counter(transaction_id)
            


    def __repr__(self):
        return (f"Transaction(value={self._amount!r}, \n"
                f"transaction_type={self._transaction_type.__class__.__name__}.{self._transaction_type.name}, \n"
                f"transaction_date={self._transaction_date!r}, \n"
                f"category={self._category!r}, \n"
                f"description={self._description!r})")

    def __str__(self):
        return (f'ID {self._id} | Tipo {self._transaction_type} | Valor {self._amount} | '
        f'Data {self._transaction_date} | Categoria {self._category} | Descrição {self._description}')
    
    # Métodos de classe -----------------------------------------------------------------------------------------------
    @classmethod
    def get_transaction_counter(cls):
        """Método getter que retorna a contagem de transações para leitura"""
        return cls._transaction_counter
    
    @classmethod
    def set_transaction_counter(cls, value: int):
        """Método setter para atualizar a contagem de transações. Utilizado quando obter transações de um arquivo"""
        cls._transaction_counter = value
    
    @classmethod
    def reset_transaction_counter(cls):
        """Método privado para reiniciar a contagem de transações"""
        cls._transaction_counter = 0

    # Construtores alternativos ---------------------------------------------------------------------------------------
    @classmethod
    def from_user_input(cls, parsed_dict: ParsedTransaction) -> Transaction:
        """Retorna uma instância de Transaction a partir do dicionário obtido de data_parser com os tipos corretos."""        

        amount: float = parsed_dict['amount']
        transaction_type: TransactionType = parsed_dict['transaction_type']
        transaction_date: date = parsed_dict['transaction_date']
        category: ExpenseCategory | IncomeCategory | None = parsed_dict.get('category', None)
        description: str | None = parsed_dict.get('description', None)
                
        return cls(amount, transaction_type, transaction_date, category, description)

    @classmethod
    def from_json(cls, parsed_dict_list: list[ParsedTransaction]) -> list[Transaction]:
        """Retorna lista de instâncias de Transaction a partir da lista de dicionários obtidos de data_parser."""
        transaction_list = []
        for parsed_dict in parsed_dict_list:
            amount = parsed_dict['amount']
            transaction_type = parsed_dict['transaction_type']
            transaction_date = parsed_dict['transaction_date']
            category = parsed_dict['category']
            description = parsed_dict['description']
            transaction_id = parsed_dict['transaction_id']

            transaction_list.append(
                cls(amount, transaction_type, transaction_date, category, description, transaction_id)
            )
        
        return transaction_list

    #Propriedades públicas --------------------------------------------------------------------------------------------
    @property
    def transaction_type(self) -> TransactionType:
        return self._transaction_type

    @property
    def amount(self) -> float:
        return self._amount

    @property   
    def transaction_date(self) -> date:
        return self._transaction_date

    @property
    def category(self) -> IncomeCategory | ExpenseCategory:
        return self._category
    
    @category.setter
    def category(self, new_category: IncomeCategory | ExpenseCategory | None=None) -> None:
        if new_category is None:
            new_category = IncomeCategory.OTHERS if self._transaction_type == TransactionType.INCOME \
            else ExpenseCategory.OTHERS
        
        else:
            new_category = self._normalize_others_category_ambiguity(new_category)
            self._validate_category(new_category)
        
        self._category = new_category

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, new_description: str | None) -> None:
        if new_description is None:
            new_description = "Descrição não adicionada"

        else:
            if len(new_description) > 90:
                raise ValueError('Descrição inválida! A descrição deve conter no máximo 90 caracteres')
    
        self._description = new_description

    @property
    def id(self):
        return self._id

    # Métodos para validação interna ----------------------------------------------------------------------------------
    def _validate_type(self, transaction_type: TransactionType) -> None:
        if not isinstance(transaction_type, TransactionType):
            raise ValueError(f'{transaction_type} não é um tipo válido!')

    def _validate_amount(self, amount: float | int) -> None:
        """Verifica se um valor é válido e maior que zero"""
        if not isinstance(amount, (float, int)) or not amount > 0:
            raise ValueError(f'{amount} não é um valor válido!')
        
    def _validate_date(self, transaction_date: date) -> None:
        """Verifica se uma data não é futura e se é válida"""
        if not isinstance(transaction_date, date) or transaction_date > date.today() :
            raise ValueError(f'{transaction_date} não é uma data válida!')
        
    def _validate_category(self, category: IncomeCategory | ExpenseCategory) -> None:
        """Verifica se é uma categoria de receita ou se ela é de despesa."""
        match self._transaction_type:
            case TransactionType.INCOME if not isinstance(category, IncomeCategory):
                raise ValueError(f'{category} não é uma categoria de receita válida!')
            
            case TransactionType.EXPENSE if not isinstance(category, ExpenseCategory):
                raise ValueError(f'{category} não é uma categoria de despesa válida!')
            
    # Método para detectar e corrigir ambiguidade das categorias 'outros' ---------------------------------------------
    def _normalize_others_category_ambiguity(
            self, 
            category: IncomeCategory | ExpenseCategory
            ) -> IncomeCategory | ExpenseCategory:
        """
        Normaliza categoria OTHERS para o tipo correto se necessário.
    
        Se a categoria for OTHERS mas do tipo incompatível com transaction_type,
        retorna a versão correta de OTHERS. Caso contrário, retorna a 
        categoria original inalterada.
    
        Args:
        category: A categoria a ser normalizada
        
        Returns:
        A categoria normalizada (corrigida se necessário)
        """
        if self._transaction_type == TransactionType.INCOME and category == ExpenseCategory.OTHERS:
            return IncomeCategory.OTHERS

        if self._transaction_type == TransactionType.EXPENSE and category == IncomeCategory.OTHERS:
            return ExpenseCategory.OTHERS
        
        return category