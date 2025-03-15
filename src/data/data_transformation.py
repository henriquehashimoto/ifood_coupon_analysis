# Data Transformation for iFood Technical Case
# This notebook handles the transformation of raw data into processed datasets

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from pathlib import Path


#==============================
# Define constants
#==============================
raw_dir = Path("data/raw")
extract_dir = Path("data/extracted")
logger = logging.getLogger('data_transformation')



#==============================
# Handle NA's
#==============================
def handle_na_data(df:pd.DataFrame, columns, action, add_params=None):
    """
    Handle missing data in a DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame to handle missing data
        columns (list): List of columns to handle missing data
        action (str): Action to take on missing data 
        add_params (any, optional): Value to fill missing data with (required for 'fill' action)

    Returns:
        pd.DataFrame: DataFrame with handled missing data
    """
    logger.info("Handling missing data in DataFrame")
    
    if action == 'fill':
        if add_params is None:
            raise ValueError("Please, provide what will be used to fill na on 'add_param', it must be provided for the 'fill' action.")        
        
        for col in columns:
            df[col].fillna(add_params, inplace=True)

    
    elif action == 'drop':
        df.dropna(subset=columns, inplace=True) # Columns to be verified if theres na to be droped

    else:
        raise ValueError("Invalid action. Use 'fill' or 'drop'.")

    logger.info("Missing data handling completed")
    return df


#==============================
# Convert Column Data Type
#==============================
def convert_column(df:pd.DataFrame, conversions:tuple):
    """
    Convert multiple columns in a DataFrame to specified data types with error handling.

    Parameters:
        df (pd.DataFrame): The DataFrame to modify.
        conversions (list of tuples): List of (column, dtype) pairs.

    Returns:
        pd.DataFrame: The modified DataFrame.

    Raises:
        ValueError: If conversion fails for any column.
    """
    
    # Validate conversions input
    if not isinstance(conversions, list):
        raise ValueError("`conversions` must be a list of tuples.")
    
    for item in conversions:
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError("Each item in `conversions` must be a tuple of (column, dtype).")
            
    logger.info(f"Start of the conversion of columns data type")

    # For each column + data type
    for column, dtype in conversions:
        if column not in df.columns:
            logging.warning(f"Column '{column}' not found in DataFrame. Skipping.")
            continue

        try:
            if dtype == 'datetime':
                df[column] = pd.to_datetime(df[column])
                logging.info(f"Converted the column '{column}' to datetime")
            
            elif dtype == 'date':
                df[column] = pd.to_datetime(df[column]).dt.date
                logging.info(f"Converted the column '{column}' to date")
            
            elif dtype == 'int':
                df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
                logging.info(f"Converted the column '{column}' to int")
            
            elif dtype == 'float':
                df[column] = pd.to_numeric(df[column], errors='coerce').astype(float)
                logging.info(f"Converted the column '{column}' to float")
            
            elif dtype == 'str':
                df[column] = df[column].astype(str)
                logging.info(f"Converted the column '{column}' to str")
            
            else:
                logging.error(f"Unsupported dtype: {dtype} for column '{column}'")
                raise ValueError(f"Unsupported dtype: {dtype}")
        
        except Exception as e:
            logging.error(f"Failed to convert column '{column}' to {dtype}. Error: {e}")
            raise ValueError(f"Failed to convert column '{column}' to {dtype}. Error: {e}")
    
        logger.info(f"Column {column} converted to {dtype} data type")

    return df
    
    



#==============================
# Remove Duplicates
#==============================
def remove_duplicates(df: pd.DataFrame, column: str, column_deduplicate: str):
    """
    Remove duplicates from a DataFrame based on another column

    Parameters:
        df (pd.DataFrame): DataFrame to remove duplicates frsom
        column (str): Column to remove duplicates from
        column_deduplicate (str): Column to use for deduplication

    Returns:
        pd.DataFrame: DataFrame with duplicates removed
    """
    logger.info(f"Removing duplicates from column {column} based on {column_deduplicate}")

    # Sort the DataFrame by the column_deduplicate in descending order
    df = df.sort_values(by=column_deduplicate, ascending=False)

    # Remove duplicates from the column, keeping the first occurrence (which is the most recent)
    df = df.drop_duplicates(subset=column, keep='first')

    logger.info(f"Duplicates removed from column {column}")
    return df




# # Example DataFrame
# data = {
#     'A': [1, 2, None, 4],
#     'B': [None, 2, 3, 4],
#     'C': [1, 2, 3, 4]
# }
# df = pd.DataFrame(data)


# if __name__ == "__main__":
#     # handle_na_data(df, ['A','B'], 'fill', 0)
#     df = pd.DataFrame({'date': ['2022-01-01 15:30:22', '2022-01-02 15:30:22'], 'value': [1.2, 3.4]})
#     df2 = convert_column(df, 'date', 'date')
#     df3 = convert_column(df, 'value', 'int')
#     print(df2)
#     print(df3)
    