from transaction import Transaction, TransactionType
import datetime


class TransactionManager:
    def __init__(self) -> None:
        self._list_of_transactions: list[Transaction] = []
        self._next_id: int = 1

    def add_transaction(self, transaction: Transaction) -> int:
        """Adiciona uma transação nova à lista, atribui a ela um id, e prepara o número id para um próximo item que possa ser adicionado."""
        transaction._id = self._next_id
        self._next_id += 1
        self._list_of_transactions.append(transaction)
        return transaction._id
    
    def del_transaction(self, transaction_id: int) -> None:
        """Deleta uma transação da lista de transações."""
        del self._list_of_transactions[transaction_id - 1]

    def get_all_transactions(self) -> list[Transaction]:
        """Retorna uma cópia da lista de todas as transações."""
        return self._list_of_transactions.copy()