from enum import Enum


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
    TRANSPORTATION : representa gastos com trasportes, como gasolina, transporte público, 
    manutenção de veículo ('transporte')
    HOUSING : representa gastos com moradia, como aluguel, manutenção, IPTU ('moradia')
    HEALTH : representa gastos com saúde como hospital, remédios, academia ('saúde')
    EDUCATION : representa gastos com educação como escola, faculdade, cursos ('educação')
    LEISURE : representa gastos com lazer como cinema, jogos, parques, viagens ('lazer')
    BILLS : representa gastos com contas como água, luz, internet ('contas')
    CLOTHING : representa gastos com vestuário como roupas, calçados, acessórios ('vestuário')
    OTHER : representa uma despesa que não se encaixa em nenhuma das categorias acimas, 
    também é a categoria padrão para receitas não definidas pelo usuário ('outros')
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