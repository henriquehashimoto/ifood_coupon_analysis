# Análise de Estratégia de Cupons

Please, read until the end to better understand the decision making and thought process.
This code was tested in Windows 10 and Windows 11, one of the decision of using "pure Python" is to be a cross platform code. But, I couldn't test in Mac and Linux, so the behavior may vary.



### Project Structure

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


### Instalation 

```bash
# Clone the repo
git clone https://github.com/henriquehashimoto/ifood_coupon_analysis.git
cd ifood_coupon_analysis
```

# Create virtual environment and install dependencies
```bash
# First, let's install the packages necessary
python -m virtualenv .venv

# To enter the poetry env with the packages installed
source .venv/bin/activate 
# Or if you are on windows
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create kernel for notebooks; may need to restart kernel or the whole vscode/cursor/IDE of choice
python -m ipykernel install --user --name=ifood_coupons_env --display-name "Python (iFood Env)" 
```


# To execute this project

### Main 

- Execute main file with:
- `python main.py`
  - This will execute the "ETL" files on *src/data/*:
  - `data_extraction.py`
  - `data_transformation.py`
  - `data_load.py`
  - This should execute ~10min to 15min
  - With that, you shoud have all necessary files for the rest of the analysis
- Now you can see the notebooks - To use them, enable the recently created Kernel `Python (iFood Env)`, once you open the notebook, (may be necessary the restart of the IDE or kernel)
    - For data exploration `notebooks/01_data_exploratory.ipynb`
    - For A/B test analysis `notebooks/02_ab_test_analysis.ipynb`
    - For customer segmentation tests and analysis `notebooks/03_segmentations.ipynb`


# How this case was built

1. Download the datasets trough the script `src/data/data_extraction.py`
2. Verified data and understood it, also noted what changes was necessary for transformation script, on `notebooks/01_data_exploratory.ipynb`
3. Created data `src/data/transformation` to clean and improve the datasets
4. Created `src/data/data_load` to save transformed data
5. Combine in one ETL on `main.py`
6. Done the analysis of the A/B Test on `notebooks/02_ab_test_analysis.ipynb`
7. Created segmentation on `notebooks/03_segmentations.ipynb`


## Possible future iterations 

This solution was developed as part of a technical case study, and due to time constraints, certain enhancements and optimizations were not implemented. In a production environment or real-world scenario, the following improvements would be prioritized to ensure robustness, scalability, and maintainability:

#### ENGINEERING FUTURE CHANGELOG

- **Configuration Management** - Move hardcoded values to configuration files. Ex.: URLS dictionary created in `data_extraction.py`. This would provide a single source of truth for configuration values
- **Error Handling and Validation** -  Implement more robust error handling with specific exception types. Ex.: if "conversions" variable at `main.py` is listing a column name wrong, this must be treated somehow. Usage of Pydantic or Pandera
- **Logging Enhancements** - Implement structured logging with phisical files as well
- **Performance Optimization** - Use of pyspark (if moved to a cluster) or duckDB (if stays in single node) on the ETL and `main.py` 

Besides that, transform into tables for better and easier consumption. 

##### DATA ANALYSIS FUTURE CHANGELOG

IFood business open the door for multiple opportunity for data analysis, being a company with such a vast combination of possibilites, is hard to list only a couple of analysis that we could do. 

But narrowing down, here a list of the "next steps" that I'd recommend to do with this analysis (besides the proposed A/B test and segmentation): 

- **Use K-means** to create segmentation based on similar behavior in a determined metric
- Experiment **Churn Propensity Model** - Groups customers by their likelihood to churn, enabling proactive retention; or a **Churn recovery focused** experiment
- **Decision Trees** - Creates segments through a series of binary splits based on the most predictive variables

##### Why RFM instead of these others?

On the document describing this challenge, it says: 

> mas a área em que você atua ainda não tem segmentos bem definidos e cada área de Negócio utiliza conceitos diferentes

Jumping straight into advanced methods like decision trees can create a big knowledge gap with the business team, requiring a lot of explanation around statistical and mathematical concepts. In practice, business stakeholders are more likely to support data-driven decisions when they understand the approach.

**Starting with a simpler but effective method like RFM helps build that understanding and trust**. It also lays the foundation for a more data-driven culture, making it easier to introduce more complex segmentation techniques later on.


