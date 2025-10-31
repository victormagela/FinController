from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory


class TransactionManager:
    """
    Gerencia uma lista de transações, incluindo operações que ocorrem sobre essa, 
    como adicionar, excluir, filtrar.

    Atributos privados:
    _transaction_list (list[Transaction]) = lista que contém todas as transações adicionadas. 
    É iniciada como uma lista vazia.
    """
    def __init__(self) -> None:
        self._transaction_list: list[Transaction] = []

    # Métodos básicos de lista ---------------------------------------------------------------------------------------- 
    def add_transaction(self, transaction: Transaction) -> None:
        """Adiciona uma (ou mais) transação nova à lista."""
        self._transaction_list.append(transaction)

    def get_all_transactions(self) -> list[Transaction]:
        """Retorna uma cópia da lista de todas as transações."""
        return self._transaction_list.copy()
    
    def del_transaction(self, transaction_id: int) -> None:
        """Exclui uma transação (ou mais) da lista com base no ID dela. Levanta exceção caso não encontrar algum ID."""
        for transaction in self._transaction_list:
            if not any(transaction.id == transaction_id for transaction in self._transaction_list):
                raise ValueError(f'ID {transaction_id} não encontrado!')

        for transaction in self._transaction_list:
            if transaction.id == transaction_id:
                self._transaction_list.remove(transaction)
                break
    
    def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        for transaction in self._transaction_list:
            if transaction_id == transaction.id:
                return transaction

        raise ValueError(f'ID {transaction_id} não encontrado!')

    # Métodos de atualização ------------------------------------------------------------------------------------------    
    def update_transaction_category(
            self, 
            transaction_id: int, 
            new_value: IncomeCategory | ExpenseCategory | None=None
            ) -> None:
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