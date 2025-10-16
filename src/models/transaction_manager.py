from transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory
from datetime import datetime, date


class TransactionManager:
    """
    Gerencia uma lista de transações, incluindo operações que ocorrem sobre essa, como adicionar, excluir, filtrar.

    Atributos privados:
    _transaction_list (list[Transaction]) = lista que contém todas as transações adicionadas. É iniciada como uma lista vazia.
    """
    def __init__(self) -> None:
        self._transaction_list: list[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """Adiciona uma (ou mais) transação nova à lista."""
        self._transaction_list.append(transaction)

    def del_transaction(self, *transaction_ids: int) -> None:
        """Exclui uma transação (ou mais) da lista com base no ID dela. Levanta exceção caso não encontrar algum ID."""
        for transaction_id in transaction_ids:
            if not any(transaction.id == transaction_id for transaction in self._transaction_list):
                raise ValueError(f'ID {transaction_id} não encontrado!')

        for transaction_id in transaction_ids:
            for transaction in self._transaction_list:
                if transaction.id == transaction_id:
                    self._transaction_list.remove(transaction)
                    break
    
    def update_transaction_category(self, transaction_id: int, new_value: IncomeCategory|ExpenseCategory):
        """Altera a categoria da transação. Levanta exceção caso não encontrar o ID."""
        for transaction in self._transaction_list:
            if transaction.id == transaction_id:
                transaction.category = new_value
                return
                    
        raise ValueError(f'ID {transaction_id} não encontrado!')
    
    def update_transaction_description(self, transaction_id: int, new_value: str):
        """Altera os descrição da transação. Levanta exceção caso não encontrar o ID."""
        for transaction in self._transaction_list:
            if transaction.id == transaction_id:
                transaction.description = new_value
                return
                    
        raise ValueError(f'ID {transaction_id} não encontrado!')
    
    def get_all_transactions(self) -> list[Transaction]:
        """Retorna uma cópia da lista de todas as transações."""
        return self._transaction_list.copy()
    
    def filter_by_value_range(self, start: int|float = 0, end: int|float = 1e20):
        """Filtra a lista por um alcance de valor, e retorna uma nova lista com somente as transações neste alcance."""
        return [transaction for transaction in self._transaction_list if start <= transaction.value <= end]
    
    def filter_by_type(self, transaction_type: TransactionType) -> list[Transaction]:
        """Filtra a lista por tipo de transação, e retorna uma nova lista com somente as transações deste tipo"""
        return [transaction for transaction in self._transaction_list if transaction.transaction_type == transaction_type]
    
    def filter_by_date_range(self, start: date = None, end: date = None) -> list[Transaction]:
        """Filtra a lista por período, e retorna uma nova lista com somente as transações feitas neste período"""
        if start is None:
            start = date.min
        
        if end is None:
            end = date.max

        return [transaction for transaction in self._transaction_list if start <= transaction.transaction_date <= end]

    def filter_by_category(self, category: IncomeCategory|ExpenseCategory) -> list[Transaction]:
        """Filtra a lista por categoria, e retorna uma nova lista com somente as transações desta categoria"""
        return [transaction for transaction in self._transaction_list if transaction.category == category]
    

# Testes -------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Teste 1: Criar transação SEM categoria (deve usar OUTROS automaticamente)
    t1 = Transaction(550, TransactionType.INCOME, date(2025, 10, 14))
    print(f"T1 - Categoria automática: {t1.category.value}")  # Deve printar 'outros'
    
    # Teste 2: Criar transação COM categoria válida
    t2 = Transaction(550.50, TransactionType.EXPENSE, date(2025, 10, 15), 
                     category=ExpenseCategory.FOOD)
    print(f"T2 - Categoria definida: {t2.category.value}")  # Deve printar 'alimentação'
    
    # Teste 3: Usar from_user_input com categoria
    t3 = Transaction.from_user_input('1800.55', 'receita', '15/10/2025', 
                                     'salário', 'Pagamento mensal')
    print(f"T3 - Categoria via input: {t3.category.value}")  # Deve printar 'salário'
    
    # Teste 4: Tentar categoria inválida (deve dar erro)
    try:
        t4 = Transaction.from_user_input('100', 'receita', '16/10/2025', 'alimentação')
        print("ERRO: Deveria ter dado exceção!")
    except ValueError as e:
        print(f"✓ Erro esperado capturado: {e}")
    
    # Teste 5: TransactionManager - adicionar e filtrar
    tm = TransactionManager()
    tm.add_transaction(t1)
    tm.add_transaction(t2)
    tm.add_transaction(t3)
    
    receitas = tm.filter_by_type(TransactionType.INCOME)
    print(f"\nTotal de receitas: {len(receitas)}")
    
    alimentacao = tm.filter_by_category(ExpenseCategory.FOOD)
    print(f"Transações de alimentação: {len(alimentacao)}")
    
    # Teste 6: Atualizar categoria
    tm.update_transaction_category(2, ExpenseCategory.TRANSPORTATION)
    print(f"T2 após update: {t2.category.value}")  # Deve printar 'transporte'