from typing import Any, Callable

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QObject

from src.models.transaction import Transaction
import src.ui.formatter as formatter


class TableModel(QAbstractTableModel):
    def __init__(
        self,
        transaction_list: list[Transaction] | None = None,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._transaction_list: list[Transaction] = transaction_list or []
        self._column_names: list[str] = [
            "Id",
            "Data",
            "Tipo",
            "Categoria",
            "Descrição",
            "Valor",
        ]
        self._column_descriptions: dict[str, Callable[[Transaction], Any]] = {
            "Id": lambda t: t.id,
            "Data": lambda t: formatter.format_date(t.transaction_date),
            "Tipo": lambda t: formatter.format_transaction_type(t.transaction_type),
            "Categoria": lambda t: formatter.format_category(t.category),
            "Descrição": lambda t: t.description,
            "Valor": lambda t: formatter.format_currency_for_ptbr(t.amount),
        }

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._transaction_list)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._column_names)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None

        if role != Qt.ItemDataRole.DisplayRole:
            return None

        transaction = self._transaction_list[index.row()]
        column_name = self._column_names[index.column()]
        return self._column_descriptions[column_name](transaction)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            if section in range(len(self._column_names)):
                return self._column_names[section]

        return None

    def set_transaction_list(self, new_transaction_list: list[Transaction]) -> None:
        self.beginResetModel()
        self._transaction_list = new_transaction_list
        self.endResetModel()

    def get_transaction_list(self) -> list[Transaction]:
        return self._transaction_list.copy()
