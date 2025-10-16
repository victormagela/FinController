from __future__ import annotations

from enum import Enum
import datetime
import locale

# Tentativa de configurar locale para formatação em pt_br.
# Nem todos os sistemas têm o mesmo nome de locale, por isso protegemos com um bloco try/except.
try:
    locale.setlocale(locale.LC_ALL, 'pt_br.UTF-8')
except Exception:
    # Caso o sistema não reconheça, mantém a formatação padrão.
    pass


class TransactionType(Enum):
    """
    Enumeração simples que representa os possíveis tipos de transação.

    Valores:
    INCOME: representa uma receita ('receita')
    EXPENSE: representa uma despesa ('despesa')
    """
    INCOME = 'receita'
    EXPENSE = 'despesa'


class IncomeCategory(Enum):
    """
    Enumeração que representa as possíveis categorias de receita.

    Valores:
    WAGE : representa o salário ('salário')
    FREELANCE : representa receitas de trabalho freelancer ('freelance')
    INVESTIMENT : representa o retorno financeiro de investimentos ('investimento')
    SALE : representa receitas advindas de vendas ('venda')
    GIFT : representa presentes em dinheiro ou doações que venha a receber ('presente')
    REIMBURSEMENT : representa devoluções e reembolsos de despesas ('reembolso')
    OTHER : representa uma receita que não se encaixa em nenhuma das categorias acimas, também é a categoria padrão para receitas não definidas pelo usuário ('outros') 
    """
    WAGE = 'salário'
    FREELANCE = 'freelance'
    INVESTIMENT = 'investimento'
    SALE = 'venda'
    GIFT = 'presente'
    REIMBURSEMENT = 'reembolso'
    OTHER = 'outros'


class ExpenseCategory(Enum):
    """
    Enumeração que representa as possíveis categorias de despesa.

    Valores:
    FOOD : representa gastos com alimentação como mercados, restaurantes, delivery ('alimentação')
    TRANSPORTATION : representa gastos com trasportes, como gasolina, transporte público, manutenção de veículo ('transporte')
    HOUSING : representa gastos com moradia, como aluguel, manutenção, IPTU ('moradia')
    HEALTH : representa gastos com saúde como hospital, remédios, academia ('saúde')
    EDUCATION : representa gastos com educação como escola, faculdade, cursos ('educação')
    LEISURE : representa gastos com lazer como cinema, jogos, parques, viagens ('lazer')
    BILLS : representa gastos com contas como água, luz, internet ('contas')
    CLOTHING : representa gastos com vestuário como roupas, calçados, acessórios ('vestuário')
    OTHER : representa uma despesa que não se encaixa em nenhuma das categorias acimas, também é a categoria padrão para receitas não definidas pelo usuário ('outros')
    """
    FOOD = 'alimentação'
    TRANSPORTATION = 'transporte'
    HOUSING = 'moradia'
    HEALTH = 'saúde'
    EDUCATION  = 'educação'
    LEISURE = 'lazer'
    BILLS = 'contas'
    CLOTHING = 'vestuário'
    OTHER = 'outros'


class Transaction():
    """
    Representa uma transação financeira simples.

    Atributos privados:
    _value (float): valor positivo da transação.
    _transaction_type (TransactionType): tipo da transação (receita ou despesa).
    _transaction_date (datetime.date): data que foi feita a transação (não aceita datas futuras).
    _category (str): atributo opcional, define a categoria da transação (máximo de 50 caracteres e mínimo de 3).
    _description (str): atributo opcional, adiciona uma descrição mais longa da transação (máximo de 200 caracteres e mínimo de 3).

    Exemplos:
    Transaction(10.50, TransactionType.INCOME, datetime.date(2025, 10, 14))
    Transaction(45, TransactionType.EXPENSE, datetime.date(2025, 09, 20), 'Alimentação', 'Saí para almoçar fora de casa')
    """
    _transaction_counter: int = 0 # Contador de instâncias

    def __init__(self, value: float, 
                 transaction_type: TransactionType, 
                 transaction_date: datetime.date, 
                 category: IncomeCategory|ExpenseCategory = None, 
                 description: str = 'Descrição não adicionada') -> None:
        self._validate_value(value)
        self._value = value
        self._validate_type(transaction_type)
        self._transaction_type = transaction_type
        self._validate_date(transaction_date)
        self._transaction_date = transaction_date
        if category is None:
            if transaction_type == TransactionType.INCOME:
                self._category = IncomeCategory.OTHER
            else:
                self._category = ExpenseCategory.OTHER
        else:
            self._validate_category(category, transaction_type)
            self._category = category
        self._description = description
        # Incrementa o contador da classe em 1, e define o ID da transação com este novo valor. Garante que cada instância terá um ID único.
        Transaction._transaction_counter += 1
        self._id: int = Transaction._transaction_counter 

    def __repr__(self):
        return (f"Transaction(value={self._value!r}, \n"
                f"transaction_type={self._transaction_type.__class__.__name__}.{self._transaction_type.name}, \n"
                f"transaction_date={self._transaction_date!r}, \n"
                f"category={self._category!r}, \n"
                f"description={self._description!r})")

    def __str__(self):
        return f'ID {self._id}| {self.transaction_type_str} de {self.value_formated_ptbr} em {self.transaction_date_str}.| {self._category}| {self._description}'
    
    # Métodos de classe --------------------------------------------------------------------------------------------------------------------------
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

    # Construtor alternativo ---------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def from_user_input(value_str: str, 
                        transaction_type_str: str, 
                        transaction_date_str: str, 
                        category_str: str = None, 
                        description: str = 'Descrição não adicionada') -> Transaction:
        """
        Converte strings obtidas do usuário, e retorna uma instância de Transaction.

        Argumentos:
        value_str (str): string que contém um número.
        transaction_type_str (str): string que pode ser 'receita' ou 'despesa', case insensitive.
        transaction_date_str (str): string que contém uma data, deve estar no formato DD/MM/AAAA.
        category (str): categoria opcional, com padrão 'outros'.
        description (str): descrição opcional, com padrão 'descrição não adicionada'.

        Returns:
        Transaction construída a partir dos valores convertidos.

        Raises:
        Levanta erros ValueErro para qualquer entrada inválida.
        """
        try:
            value = float(value_str.strip().replace(',', '.'))
        except ValueError:
            raise ValueError(f'{value_str} não é um valor válido.')
        
        try:
            transaction_type = TransactionType(transaction_type_str.lower().strip())
        except ValueError:
            raise ValueError(f'{transaction_type_str} não é um tipo válido. Use apenas "receita" ou "despesa".')
        
        try:
            transaction_date = datetime.datetime.strptime(transaction_date_str.strip(), "%d/%m/%Y").date()
        except ValueError:
            raise ValueError(f'{transaction_date_str} não é uma data válida. Siga o formato DD/MM/AAAA')
        
        category = None
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
            
        return Transaction(value, transaction_type, transaction_date, category, description)

    #Propriedades públicas ---------------------------------------------------------------------------------------------------------
    @property
    def transaction_type(self) -> TransactionType:
        return self._transaction_type

    @property
    def transaction_type_str(self) -> str:
        """Retorna o tipo da transação em formato mais legível."""
        return str(self._transaction_type.value).capitalize()

    @property
    def value(self) -> float:
        return self._value
    
    @property
    def value_formated_ptbr(self) -> str:
        """Retorna o valor formatado em moeda brasileira (ex. R$ 1.234,50) para melhor legibilidade."""
        return locale.currency(self._value, grouping=True)

    @property   
    def transaction_date(self) -> datetime.date:
        return self._transaction_date
    
    @property
    def transaction_date_str(self) -> str:
        """Retorna a data da transação em formato DD/MM/AAAA para melhor legibilidade."""
        return datetime.datetime.strftime(self._transaction_date, '%d/%m/%Y')

    @property
    def category(self) -> str:
        return self._category
    
    @category.setter
    def category(self, category: IncomeCategory|ExpenseCategory) -> None:
        if self._transaction_type == TransactionType.INCOME:
            if not isinstance(category, IncomeCategory):
                raise ValueError(f'{category} não é uma categoria de receita válida!')
        
        elif self._transaction_type == TransactionType.EXPENSE:
            if not isinstance(category, ExpenseCategory):
                raise ValueError(f'{category} não é uma categoria de despesa válida!')
        
        self._category = category

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, description: str) -> None:
        if not isinstance(description, str) or 3 > len(description) or len(description) > 200:
            raise ValueError('Descrição inválida! A descrição deve conter no mínimo 3 caracteres e no máximo 200 caracteres')
        
        self._description = description

    @property
    def id(self):
        return self._id

    # Métodos para validação interna -----------------------------------------------------------------------------------------------------
    def _validate_type(self, transaction_type) -> None:
        if not isinstance(transaction_type, TransactionType):
            raise ValueError(f'{transaction_type} não é um tipo válido!')

    def _validate_value(self, value) -> None:
        """Verifica se um valor é válido e maior que zero"""
        if not isinstance(value, (float, int)) or not value > 0:
            raise ValueError(f'{value} não é um valor válido!')
        
    def _validate_date(self, transaction_date) -> None:
        """Verifica se uma data não é futura e se é válida"""
        if not isinstance(transaction_date, datetime.date) or transaction_date > datetime.date.today() :
            raise ValueError(f'{transaction_date} não é uma data válida!')
        
    def _validate_category(self, category, transaction_type) -> None:
        """Verifica se é uma categoria de receita se a transação for desse tipo, ou se ela é de despesa caso a transação for desse tipo"""
        if transaction_type == TransactionType.INCOME:
            if not isinstance(category, IncomeCategory):
                raise ValueError(f'{category} não é uma categoria de receita válida!')
        
        elif transaction_type == TransactionType.EXPENSE:
            if not isinstance(category, ExpenseCategory):
                raise ValueError(f'{category} não é uma categoria de despesa válida!')


# Testes ----------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    ...
    # t1 = Transaction(550, TransactionType.INCOME, datetime.date(2025, 10, 14))
    # t2 = Transaction(550.50, TransactionType.EXPENSE, datetime.date(2025, 10, 15))
    # print(t1.id)
    # print(t2.id)
    # print(Transaction.get_transaction_counter())
    # t3 = Transaction.from_user_input('1100.55', 'receita', '15/10/2025')
    # print(t3.id)
    # print(Transaction.get_transaction_counter())
    # Transaction.reset_transaction_counter()
    # print(Transaction.get_transaction_counter())
    # Transaction.set_transaction_counter(3)
    # print(Transaction.get_transaction_counter())
    # print(t1)
    # print(t2)
    # print(t3)
    # print(t1.__repr__())
    # print(t2.__repr__())
    # print(t3.__repr__())

    # t1 = Transaction(value = 1100.55, 
    #                 transaction_type = TransactionType.INCOME, 
    #                 transaction_date = datetime.date(2025, 10, 15), 
    #                 category = 'Categoria não adicionada', 
    #                 description = 'Descrição não adicionada')

    # print(repr(t1))

    # t2 = Transaction(value=1100.55, 
    # transaction_type=TransactionType.INCOME, 
    # transaction_date=datetime.date(2025, 10, 15), 
    # category='Categoria não adicionada', 
    # description='Descrição não adicionada')
    # print(t2)

    # t2 = Transaction(value = 1100.55, 
    # transaction_type = TransactionType.INCOME, 
    # transaction_date = datetime.date(2025, 10, 15), 
    # category = 'Categoria não adicionada', 
    # description = 'Descrição não adicionada')