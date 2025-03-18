# Case Técnico iFood - Análise de Estratégia de Cupons

Este repositório contém minha solução para o case técnico de Data Analytics do iFood, focado na análise de um teste A/B de estratégia de cupons para retenção de usuários.

### Estrutura do Projeto

- `data/`: Dados brutos e processados
- `notebooks/`: Jupyter notebooks com análises detalhadas
- `src/`: Código fonte Python reutilizável
- `reports/`: Relatório final e visualizações
- `tests/`: Some tests to understand the usage, functions and data overall


```bash
ifood_data_analyst_case/
│
├── data/                           # Data storage directory
│   ├── extracted/                  # Extracted data from raw sources
│   ├── processed/                  # Processed/transformed data ready for analysis
│   └── raw/                        # Raw data downloads
│
├── notebooks/                      # Jupyter notebooks for analysis
│   ├── imgs/                       # Images used in notebooks
│   │   └── abtest_comparing_groups.png
│   ├── 01_data_exploratory.ipynb   # Initial data exploration
│   ├── 02_ab_test_analysis.ipynb   # A/B test analysis
│   └── 03_segmentations.ipynb      # Customer segmentation analysis
│
├── src/                            # Source code
│   ├── analysis/                   # Analysis modules
│   └── data/                       # Data processing modules
│       ├── __pycache__/
│       ├── data_extraction.py      # Data extraction functionality
│       ├── data_load.py            # Data loading functionality
│       └── data_transformation.py  # Data transformation functionality
│
├── tests/                          # Test files
│   ├── data/                       # Test data
│   │   └── processed/              # Processed test data
│   ├── data_snipped.py             # Script to view data snippets
│   └── tests.ipynb                 # Test notebook
│
├── main.py                         # Main ETL orchestration script
├── poetry.lock                     # Poetry dependency lock file
├── pyproject.toml                  # Project configuration and dependencies
└── readme.md                       # Project documentation
```

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

# To enter the poetry env with the packages installed
poetry shell 

# Create kernel for notebooks; may need to restart kernel or the whole vscode/cursor/IDE of choice
poetry run python -m ipykernel install --user --name=ifood_case_env --display-name "Python (iFood Env)" 
```

### To execute a .py file
`poetry run python script_name.py`

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
  - This should execute ~10min 
  - Now, you shoud have all necessary files for the rest of the analysis



# How this case was built

1. Donwload the datasets trough the script `src/data/data_extraction.py`
2. Verified data and understood it, also noted what changes was necesary for transformation script, on `notebooks/01_data_exploratory.ipynb`
3. Created data `src/data/transformation` to clean and improve the datasets
4. Created `src/data/data_load` to save transformed data
5. 


## Possible future iterations 

This solution was developed as part of a technical case study, and due to time constraints, certain enhancements and optimizations were not implemented. In a production environment or real-world scenario, the following improvements would be prioritized to ensure robustness, scalability, and maintainability:

**ENGINEERING FUTURE CHANGELOG**

- **Configuration Management** - Move hardcoded values to configuration files. Ex.: URLS dictionary created in `data_extraction.py`. This would provide a single source of truth for configuration values
- **Error Handling and Validation** -  Implement more robust error handling with specific exception types. Ex.: if "conversions" variable at `main.py` is listing a column name wrong, this must be treated somehow. Usage of Pydantic or Pandera
- **Logging Enhancements** - Implement structured logging with phisical files as well
- **Performance Optimization** - Use of pyspark or duckDB on the ETL and `main.py` 

Besides that, transform into tables for better and easier consumption. 

**DATA ANALYSIS FUTURE CHANGELOG**

IFood business open the door for multiple opportunity for data analysis, being a company with such a vast combination of possibilites, is hard to list only a couple of analysis that we could do. 

But narrowing down, here a list of the "next steps" that I'd recommend to do with this analysis (besides the proposed A/B test): 

- Do the same segmentation and deep analysis that I did for the group "Hybrid Segments" for the other groups
- Churn analysis - understand if the campaign helped in prevent churn 
- Multi "category" user - analysis to see if there's any difference in behavior of users that consume different types of restaurants or even different types of iFood services (like supermarket delivery). And if this campaign helped to increase the number of "multi category" users
- Cohort Analysis: Track long-term effects by analyzing customer behavior 30/60/90 days post-campaign
- Customer Journey Mapping: Analyze how the campaign affected different stages of the customer lifecycle

