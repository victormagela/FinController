from __future__ import annotations

from enum import Enum
from datetime import date, datetime
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
    OTHERS = 'outros'

    @classmethod
    def get_all_values(cls):
        """Retorna uma lista com todos os valores possíveis de categoria."""
        return [income.value for income in cls]


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
    OTHERS = 'outros'

    @classmethod
    def get_all_values(cls):
        """Retorna uma lista com todos os valores possíveis de categoria."""
        return [expense.value for expense in cls]


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

    def __init__(self, amount: float, 
                 transaction_type: TransactionType, 
                 transaction_date: date, 
                 category: IncomeCategory | ExpenseCategory = None, 
                 description: str = None) -> None:
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
        # Incrementa o contador da classe em 1, e define o ID da transação com este novo valor. Garante que cada instância terá um ID único.
        Transaction._transaction_counter += 1
        self._id: int = Transaction._transaction_counter 

    def __repr__(self):
        return (f"Transaction(value={self._amount!r}, \n"
                f"transaction_type={self._transaction_type.__class__.__name__}.{self._transaction_type.name}, \n"
                f"transaction_date={self._transaction_date!r}, \n"
                f"category={self._category!r}, \n"
                f"description={self._description!r})")

    def __str__(self):
        return (f'ID {self._id}| {self.transaction_type_str} de {self.amount_formatted_brazil} em '
        f'{self.transaction_date_str}.| {self._category}| {self._description}')
    
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

    #Propriedades públicas --------------------------------------------------------------------------------------------
    @property
    def transaction_type(self) -> TransactionType:
        return self._transaction_type

    @property
    def transaction_type_str(self) -> str:
        """Retorna o tipo da transação em formato mais legível."""
        return str(self._transaction_type.value).capitalize()

    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def amount_formatted_brazil(self) -> str:
        """Retorna o valor formatado em moeda brasileira (ex. R$ 1.234,50) para melhor legibilidade."""
        return locale.currency(self._amount, grouping=True)

    @property   
    def transaction_date(self) -> date:
        return self._transaction_date
    
    @property
    def transaction_date_str(self) -> str:
        """Retorna a data da transação em formato DD/MM/AAAA para melhor legibilidade."""
        return datetime.strftime(self._transaction_date, '%d/%m/%Y')

    @property
    def category(self) -> str:
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
    def description(self, description: str) -> None:
        if not isinstance(description, str) or 3 > len(description) or len(description) > 200:
            raise ValueError('Descrição inválida! A descrição deve conter no mínimo 3 caracteres' \
            ' e no máximo 200 caracteres')
        
        self._description = description

    @property
    def id(self):
        return self._id

    # Métodos para validação interna ----------------------------------------------------------------------------------
    def _validate_type(self, transaction_type) -> None:
        if not isinstance(transaction_type, TransactionType):
            raise ValueError(f'{transaction_type} não é um tipo válido!')

    def _validate_amount(self, amount) -> None:
        """Verifica se um valor é válido e maior que zero"""
        if not isinstance(amount, (float, int)) or not amount > 0:
            raise ValueError(f'{amount} não é um valor válido!')
        
    def _validate_date(self, transaction_date) -> None:
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
    