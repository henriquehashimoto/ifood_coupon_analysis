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
logger = logging.getLogger(__name__)



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



# Example DataFrame
data = {
    'A': [1, 2, None, 4],
    'B': [None, 2, 3, 4],
    'C': [1, 2, 3, 4]
}
df = pd.DataFrame(data)


if __name__ == "__main__":
    handle_na_data(df, ['A','B'], 'fill', 0)
    print(df)
    