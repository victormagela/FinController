from src.models.transaction import Transaction


class UIStateManager:
    """Guarda o estado atual da lista mostrada pela UI"""
    def __init__(self) -> None:
        self._filtered_list: list[Transaction] | None = None

    @property
    def filtered_list(self) -> list[Transaction] | None:
        if self._filtered_list is None:
            return None
        
        return self._filtered_list.copy()
    
    def has_active_filter(self) -> bool:
        return self._filtered_list is not None

    def set_filtered_list(self, filtered_list: list[Transaction]) -> None:
        self._filtered_list = filtered_list

    def del_from_filtered_list(self, transaction_id: int) -> None:
        if self._filtered_list is not None:
            self._filtered_list = [
                transaction for transaction in self._filtered_list if transaction.id != transaction_id
            ]

    def clear_filtered_list(self) -> None:
        if self._filtered_list is not None:
            self._filtered_list = None