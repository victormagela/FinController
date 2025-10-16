from src.models.transaction_manager import TransactionManager
from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory

class UserInterface:
    """"""
    def __init__(self):
        self.transaction_manager = TransactionManager()

    def show_main_menu(self):
        print('\n' + '=' * 50)
        print('MENU PRINCIPAL')
        print('=' * 50)
        print('1. Adicionar transação\n' \
        '2. Excluir transação\n' \
        '3. Alterar transação\n' \
        '4. Listar transações\n'
        '5. Filtrar transações\n' \
        '6. Sair')