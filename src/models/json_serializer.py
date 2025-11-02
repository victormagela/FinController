from typing import TypedDict

from src.models.transaction import Transaction


class SerializedTransaction(TypedDict):
    amount : float | int
    transaction_type : str
    transaction_date : str
    category : str
    description : str
    transaction_id : int


class JSONSerializer:
    """Serializa um objeto Transaction em dados JSON"""

    @staticmethod
    def to_JSON(transaction_list: list[Transaction]) -> list[SerializedTransaction]:
        DATE_FORMAT = "%d/%m/%Y"
        transaction_json = []
        for transaction in transaction_list:
            amount = transaction.amount
            transaction_type = transaction.transaction_type.value
            transaction_date = transaction.transaction_date.strftime(DATE_FORMAT)
            category = transaction.category.value
            description = transaction.description
            transaction_id = transaction.id

            transaction_dict = {
                "amount" : amount,
                "transaction_type" : transaction_type,
                "transaction_date" : transaction_date,
                "category" : category,
                "description" : description,
                "transaction_id" : transaction_id
            }

            transaction_json.append(transaction_dict)

        return transaction_json