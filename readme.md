# Case Técnico iFood - Análise de Estratégia de Cupons

Este repositório contém minha solução para o case técnico de Data Analytics do iFood, focado na análise de um teste A/B de estratégia de cupons para retenção de usuários.

## Estrutura do Projeto

- `data/`: Dados brutos e processados
- `notebooks/`: Jupyter notebooks com análises detalhadas
- `src/`: Código fonte Python reutilizável
- `reports/`: Relatório final e visualizações


## Pré-requisitos
- Python 3.12 ou superior
- Poetry (gerenciador de pacotes e ambientes)


## Instalação 

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ifood-case-tecnico.git
cd ifood-case-tecnico
```

# Instale as dependências
```bash
# First, let's install the packages necessary
poetry install 

# To enter the poetry env with the packages installe
poetry shell 

# Create kernel for notebooks; may need to restart kernel or the whole vscode/cursor/IDE of choice
poetry run python -m ipykernel install --user --name=ifood_case_env --display-name "Python (iFood Env)" 
```

## To execute a .py file
`poetry run python script.py`


## To execute a .ipynb file

- You can direcly open the .ipynb file in your IDE of choice (e.g. vscode). Or use `poetry run jupyter notebook`
- In either case, make sure that you selected the right kernel (`Python (iFood Env)`), created on the "Install Dependencies" above



# How this case was built

1. Donwload the datasets trough the script `src/data/01_data_inestion.py`