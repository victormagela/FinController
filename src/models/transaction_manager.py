from transaction import Transaction, TransactionType
import datetime


class TransactionManager:
    def __init__(self) -> None:
        self._list_of_transactions: list[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """Adiciona uma transação nova à lista, atribui a ela um id, e prepara o número id para um próximo item que possa ser adicionado."""
        self._list_of_transactions.append(transaction)

    def get_all_transactions(self) -> list[Transaction]:
        """Retorna uma cópia da lista de todas as transações."""
        return self._list_of_transactions.copy()