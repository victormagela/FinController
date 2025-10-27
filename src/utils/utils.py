from rich.prompt import Prompt, IntPrompt

class PromptPTBR(Prompt):
    # Traduz a mensagem de erro da biblioteca Rich para o português
    illegal_choice_message = (
        "[prompt.invalid.choice]Por favor selecione uma das opções disponíveis"
    )

class IntPromptPTBR(IntPrompt):
    # Traduz a mensagem de erro da biblioteca Rich para o português
    validate_error_message = (
        "[prompt.invalid.choice]Por favor digite um número."
    )