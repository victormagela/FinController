import json
from pathlib import Path

from src.models.transaction import Transaction, IncomeCategory, ExpenseCategory
import src.models.data_parser as parser
from src.models.typed_dicts import SerializedTransaction
import src.models.json_serializer as serializer


class TransactionManager:
    """
    Gerencia uma lista de transações, incluindo operações que ocorrem sobre essa, 
    como adicionar, excluir, modificar.

    Atributos privados:
    _repository = referência ao Repositório de dados
    _transaction_list (list[Transaction]) = lista que contém todas as transações adicionadas. 
    É iniciada como uma lista vazia.
    """
    def __init__(self) -> None:
        self._repository = TransactionRepository()
        self._transaction_list: list[Transaction] = self._repository.get_all_transactions()

    # Métodos básicos de lista ---------------------------------------------------------------------------------------- 
    def add_transaction(self, transaction: Transaction) -> None:
        """Adiciona uma (ou mais) transação nova à lista."""
        self._transaction_list.append(transaction)
        self._repository.save(self._transaction_list)

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
        
        self._repository.save(self._transaction_list)
    
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
                self._repository.save(self._transaction_list)
                return
                    
        raise ValueError(f'ID {transaction_id} não encontrado!')
    
    def update_transaction_description(self, transaction_id: int, new_value: str):
        """Altera os descrição da transação. Levanta exceção caso não encontrar o ID."""
        for transaction in self._transaction_list:
            if transaction.id == transaction_id:
                transaction.description = new_value
                self._repository.save(self._transaction_list)
                return
                    
        raise ValueError(f'ID {transaction_id} não encontrado!')
    

class TransactionRepository:
    def __init__(self):
        self._file_name: str = "transactions.json"
        self._file_path: Path = self._get_data_path() / self._file_name

    def _get_data_path(self) -> Path:
        current_file_path = Path(__file__)
        src_file_path = current_file_path.parent.parent
        data_file_path = src_file_path / "data"
        data_file_path.mkdir(parents=True, exist_ok=True)
        return data_file_path
    
    def save(self, transaction_list: list[Transaction]) -> None:
        transaction_json = serializer.to_JSON(transaction_list)

        with open(self._file_path, 'w', encoding='utf-8') as file:
            json.dump(transaction_json, file, indent=4, ensure_ascii=False)

    def get_all_transactions(self) -> list[Transaction]:
        file_content = self._load()
        if file_content is None:
            return []

        parsed_transaction_dict_list = parser.parse_from_json(file_content)
        return Transaction.from_json(parsed_transaction_dict_list)

    def _load(self) -> list[SerializedTransaction] | None:
        if self._file_path.exists():
            try:
                with open(self._file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                return None
        
        return None