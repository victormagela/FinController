from rich.prompt import Prompt

class PromptPTBR(Prompt):
    # Traduz a mensagem de erro da biblioteca Rich para o português
    illegal_choice_message = (
        "[prompt.invalid.choice]Por favor selecione uma das opções disponíveis"
    )