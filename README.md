# FinController

Software de controle de finanças pessoais desenvolvido em Python.

## Sobre

O **FinController** é um projeto pessoal com dupla finalidade:

- Resolver um problema real: organizar minhas finanças pessoais  
- Aprendizado: cimentar e expandir conhecimentos em programação orientada a objetos e desenvolvimento de interfaces (CLI e GUI)

Atualmente o projeto oferece:

- Uma **interface de linha de comando (CLI)** completa  
- Uma **interface gráfica (GUI)** desenvolvida com **PySide6**

## Funcionalidades

- [x] Adicionar transações (receitas e despesas)  
- [x] Salvar transações em arquivo  
- [x] Listar todas as transações  
- [x] Gerar relatório com saldo total  
- [x] Interface de linha de comando (CLI) completa  
- [x] Interface gráfica (GUI) com PySide6  

## Tecnologias Utilizadas

- Python 3.13  
- PySide6 (para a interface gráfica)  
- Rich (para melhorias na interface de linha de comando)  
- Outras dependências descritas em `requirements.txt`

## Status do Projeto

- MVP concluído  
- Interface gráfica (GUI) completa com PySide6  
- Em evolução contínua (novas melhorias e funcionalidades serão adicionadas ao longo do tempo)

---

## Como instalar e executar

### 1. Pré-requisitos

- Python 3.13  
- Git (opcional, para clonar o repositório)  
- `pip` funcionando no terminal

### 2. Clonar o repositório

```bash
git clone https://github.com/victormagela/FinController.git
cd FinController
```

### 3. Criar ambiente virtual e instalar dependências

```bash
python -m venv .venv

# Ativar o ambiente virtual:
#   Windows: .venv\Scripts\activate
#   Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Executar a versão CLI (linha de comando)

```bash
python main.py
```

### 5. Executar a versão GUI (PySide6)

```bash
python app.py
```

---

## Licença

Este é um projeto pessoal de estudo. Caso deseje utilizar o código como base para aprendizado ou projetos próprios, sinta-se à vontade, respeitando boas práticas de referência ao autor.
