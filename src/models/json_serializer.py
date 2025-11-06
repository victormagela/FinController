from src.models.transaction import Transaction
from src.models.typed_dicts import SerializedTransaction


"""Serializa um objeto Transaction em dados JSON"""

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