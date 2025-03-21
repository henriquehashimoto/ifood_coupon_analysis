# Case Técnico iFood - Análise de Estratégia de Cupons

Please, read until the end to better understand the decision making and thought process.


This repository contains my solution for iFood's Data Analytics technical case, focused on analyzing an A/B test of a coupon strategy for user retention.


### Estrutura do Projeto

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

### Prerequisites
- Python 3.12 ou higher
- Poetry (library that manages packages)


### Instalation 

```bash
# Clone the repo
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


# To execute this project

### Main 

- Execute main file with:
- `poetry run python main.py`
  - This will execute the "ETL" files on *src/data/*:
  - `data_extraction.py`
  - `data_transformation.py`
  - `data_load.py`
  - This should execute ~10min to 15min
  - Now, you shoud have all necessary files for the rest of the analysis
- Now you can see the notebooks 
  - `poetry run jupyter notebook notebooks/01_data_exploratory.ipynb`
  - `poetry run jupyter notebook notebooks/02_ab_test_analysis.ipynb`
  - `poetry run jupyter notebook notebooks/03_segmentations.ipynb`


# How this case was built

1. Download the datasets trough the script `src/data/data_extraction.py`
2. Verified data and understood it, also noted what changes was necesary for transformation script, on `notebooks/01_data_exploratory.ipynb`
3. Created data `src/data/transformation` to clean and improve the datasets
4. Created `src/data/data_load` to save transformed data
5. Done the analysis of the A/B Test on `02_ab_test_analysis.ipynb`
6. Created segmentation on `03_segmentations.ipynb`


## Possible future iterations 

This solution was developed as part of a technical case study, and due to time constraints, certain enhancements and optimizations were not implemented. In a production environment or real-world scenario, the following improvements would be prioritized to ensure robustness, scalability, and maintainability:

#### ENGINEERING FUTURE CHANGELOG

- **Configuration Management** - Move hardcoded values to configuration files. Ex.: URLS dictionary created in `data_extraction.py`. This would provide a single source of truth for configuration values
- **Error Handling and Validation** -  Implement more robust error handling with specific exception types. Ex.: if "conversions" variable at `main.py` is listing a column name wrong, this must be treated somehow. Usage of Pydantic or Pandera
- **Logging Enhancements** - Implement structured logging with phisical files as well
- **Performance Optimization** - Use of pyspark or duckDB on the ETL and `main.py` 

Besides that, transform into tables for better and easier consumption. 

##### DATA ANALYSIS FUTURE CHANGELOG

IFood business open the door for multiple opportunity for data analysis, being a company with such a vast combination of possibilites, is hard to list only a couple of analysis that we could do. 

But narrowing down, here a list of the "next steps" that I'd recommend to do with this analysis (besides the proposed A/B test): 

- Do the same segmentation and **deep analysis** that I did for the group "Hybrid Segments" **for the other groups**
- **Use K-means** to create segmentation based on similar behavior in a determined metric
- Experiment **Churn Propensity Model** - Groups customers by their likelihood to churn, enabling proactive retention
- **Decision Trees** - Creates segments through a series of binary splits based on the most predictive variables

##### Why RFM instead of these others?

On the document describing this challenge, it says: 

> mas a área em que você atua ainda não tem segmentos bem definidos e cada área de Negócio utiliza conceitos diferentes

Jumping straight into advanced methods like decision trees can create a big knowledge gap with the business team, requiring a lot of explanation around statistical and mathematical concepts. In practice, business stakeholders are more likely to support data-driven decisions when they understand the approach.

**Starting with a simpler but effective method like RFM helps build that understanding and trust**. It also lays the foundation for a more data-driven culture, making it easier to introduce more complex segmentation techniques later on.


