from pathlib import Path

from PySide6.QtGui import QIcon

# Tabelas que contém todas as categorias válidas
INCOME_CATEGORY_TABLE: dict[str, str] = {
    "1": "salário",
    "2": "investimento",
    "3": "freelance",
    "4": "venda",
    "5": "presente",
    "6": "reembolso",
    "7": "outros",
}
EXPENSE_CATEGORY_TABLE: dict[str, str] = {
    "1": "alimentação",
    "2": "transporte",
    "3": "moradia",
    "4": "saúde",
    "5": "educação",
    "6": "lazer",
    "7": "contas",
    "8": "vestuário",
    "9": "outros",
}

ALL_CATEGORIES_TABLE: dict[str, str] = {
    "1": "salário",
    "2": "investimento",
    "3": "freelance",
    "4": "venda",
    "5": "presente",
    "6": "reembolso",
    "7": "alimentação",
    "8": "transporte",
    "9": "moradia",
    "10": "saúde",
    "11": "educação",
    "12": "lazer",
    "13": "contas",
    "14": "vestuário",
    "15": "outros",
}

# Tabela que contém os tipos de transação válidos
TRANSACTION_TYPE_TABLE: dict[str, str] = {"1": "receita", "2": "despesa"}

# Outras constantes
DATE_FORMAT = "%d/%m/%Y"

APP_TITLE = """
 ####### ### #     #  #####  ####### #     # #######
 #        #  ##    # #     # #     # ##    #    #
 #        #  # #   # #       #     # # #   #    #
 #####    #  #  #  # #       #     # #  #  #    #
 #        #  #   # # #       #     # #   # #    #
 #        #  #    ## #     # #     # #    ##    #
 #       ### #     #  #####  ####### #     #    #
"""

# Padrões regex para validação de formato de dados
AMOUNT_PATTERN: str = r"^\d+([.,]\d{1,2})?$"
DATE_PATTERN: str = r"^\d{2}/\d{2}/\d{4}$"
DESCRIPTION_PATTERN: str = r"^.{0,90}$"

ICONS_DIR = Path(__file__).parent.parent.parent / "assets" / "icons"
ADD_ICON = QIcon(str(ICONS_DIR / "add_fincontroller.svg"))
EDIT_ICON = QIcon(str(ICONS_DIR / "edit_fincontroller.svg"))
DELETE_ICON = QIcon(str(ICONS_DIR / "delete_fincontroller.svg"))
FILTER_ICON = QIcon(str(ICONS_DIR / "filter_fincontroller.svg"))
REPORT_ICON = QIcon(str(ICONS_DIR / "docs_fincontroller.svg"))
WINDOW_ICON = QIcon(str(ICONS_DIR / "app_icon_fincontroller.svg"))
