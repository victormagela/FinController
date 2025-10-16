from transaction import Transaction, TransactionType
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
    
    def update_transaction_category(self, transaction_id: int, new_value: str):
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
    
    def filter_by_type(self, transaction_type: str) -> list[Transaction]:
        """Filtra a lista por tipo de transação, e retorna uma nova lista com somente as transações deste tipo"""
        normalized = transaction_type.lower().strip()
        return [transaction for transaction in self._transaction_list if transaction.transaction_type.value == normalized]
    
    def filter_by_date_range(self, start: date = None, end: date = None) -> list[Transaction]:
        """Filtra a lista por período, e retorna uma nova lista com somente as transações feitas neste período"""
        if start is None:
            start = date.min
        
        if end is None:
            end = date.max

        return [transaction for transaction in self._transaction_list if start <= transaction.transaction_date <= end]

    def filter_by_category(self, category: str) -> list[Transaction]:
        """Filtra a lista por categoria, e retorna uma nova lista com somente as transações desta categoria"""
        normalized = category.lower().strip()
        return [transaction for transaction in self._transaction_list if transaction.category.lower().strip() == normalized]
    

# Testes -------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    t1 = Transaction(550, TransactionType.INCOME, date(2025, 10, 14))
    t2 = Transaction(550.50, TransactionType.EXPENSE, date(2025, 10, 15))
    t3 = Transaction(value = 1800.55, 
                    transaction_type = TransactionType.INCOME, 
                    transaction_date = date(2025, 10, 15), 
                    category = 'Salário', 
                    description = 'Pagamento mensal')

    tm1 = TransactionManager()
    tm1.add_transaction(t1)
    tm1.add_transaction(t2)
    tm1.add_transaction(t3)
    # tm1.update_transaction_category(1, 'Consumo')
    # tm1.update_transaction_description(1, 'Comprei um game novo.')
    # # print(tm1.get_all_transactions())
    # tm1.del_transaction(1)
    # tm1.del_transaction(3, 4)
    # print(tm1.get_all_transactions())
    print(tm1.filter_by_date_range())