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
def convert_column(df:pd.DataFrame, column:str, data_type:str):
    """
    Convert a column's data type in a DataFrame

    Parameters:
        df (pd.DataFrame): DataFrame to convert column data type
        column (str): Column to convert data type
        data_type (str): Data type to convert to ('date', 'datetime', 'int', 'decimal', 'str')

    Returns:
        pd.DataFrame: DataFrame with converted column data type
    """
    logger.info(f"Converting column {column} to {data_type} data type")

    # Converting to date type
    if data_type == 'date':
        try:
            df[column] = pd.to_datetime(df[column]).dt.date
        except ValueError:
            raise ValueError(f"Invalid date format in column {column}. Please use YYYY-MM-DD.")

    # Converting to datetime type        
    elif data_type == 'datetime':
        try:
            df[column] = pd.to_datetime(df[column])
        except ValueError:
            raise ValueError(f"Invalid datetime format in column {column}. Please use YYYY-MM-DD HH:MM:SS.")
    
    # Converting to int type
    elif data_type == 'int':
        try:
            df[column] = df[column].astype(int)
        except ValueError:
            raise ValueError(f"Invalid integer value in column {column}. Please enter a whole number.")
    
    # Converting to float type
    elif data_type == 'float':
        try:
            df[column] = df[column].astype(float)
        except ValueError:
            raise ValueError(f"Invalid float value in column '{column}'. Please enter a number with decimal places.")
    
    # Converting to string type
    elif data_type == 'str':
        df[column] = df[column].astype(str)
    
    else:
        raise ValueError("Invalid data type. Use 'date', 'datetime', 'int', 'decimal', or 'str'.")


    logger.info(f"Column {column} converted to {data_type} data type")
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




# Example DataFrame
data = {
    'A': [1, 2, None, 4],
    'B': [None, 2, 3, 4],
    'C': [1, 2, 3, 4]
}
df = pd.DataFrame(data)


if __name__ == "__main__":
    # handle_na_data(df, ['A','B'], 'fill', 0)
    df = pd.DataFrame({'date': ['2022-01-01 15:30:22', '2022-01-02 15:30:22'], 'value': [1.2, 3.4]})
    df2 = convert_column(df, 'date', 'date')
    df3 = convert_column(df, 'value', 'int')
    print(df2)
    print(df3)
    