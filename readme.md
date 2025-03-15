# Case Técnico iFood - Análise de Estratégia de Cupons

Este repositório contém minha solução para o case técnico de Data Analytics do iFood, focado na análise de um teste A/B de estratégia de cupons para retenção de usuários.

### Estrutura do Projeto

- `data/`: Dados brutos e processados
- `notebooks/`: Jupyter notebooks com análises detalhadas
- `src/`: Código fonte Python reutilizável
- `reports/`: Relatório final e visualizações
- `tests/`: Some tests to understand the usage, functions and data overall


### Pré-requisitos
- Python 3.12 ou superior
- Poetry (gerenciador de pacotes e ambientes)


### Instalação 

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

### To execute a .py file
`poetry run python script.py`


### To execute a .ipynb file

- You can direcly open the .ipynb file in your IDE of choice (e.g. vscode). Or use `poetry run jupyter notebook`
- In either case, make sure that you selected the right kernel (`Python (iFood Env)`), created on the "Install Dependencies" above

# To execute this project

### Main 

- Execute main file with:
- `poetry run python main.py`
  - This will execute the "ETL" files on *src/data/*:
  - `data_extraction.py`
  - `data_transformation.py`
  - `data_load.py`
  - This should execute under 10min 
  - Now, you shoud have all necessary files



# How this case was built

1. Donwload the datasets trough the script `src/data/01_data_inestion.py`
   1. Execute: `poetry run python src/data/01_data_ingestion.py`


## Possible future iterations 

This solution was developed as part of a technical case study, and due to time constraints, certain enhancements and optimizations were not implemented. In a production environment or real-world scenario, the following improvements would be prioritized to ensure robustness, scalability, and maintainability:

**ENGINEERING IMPROVEMENTS**

- First of all, I'd productize into tables. the "*raw*" data would be my "bronze" level of tables; with *processed* being my "silver" and what I used in the notebooks would become my "gold" tables in a **medallion modeling**

- **Configuration Management** - Move hardcoded values to configuration files. Ex.: URLS dictionary created in `data_extraction.py`. This would provide a single source of truth for configuration values
- **Error Handling and Validation** -  Implement more robust error handling with specific exception types. Ex.: if "conversions" variable at `main.py` is listing a column name wrong, this must be treated somehow. Usage of Pydantic or Pandera
- **Logging Enhancements** - Implement structured logging with phisical files as well
- **Documentation** - Add more detailed docstrings with examples, data lineage and data catalog 
- **Performance Optimization** - Use of pyspark or duckDB on the ETL and `main.py` 