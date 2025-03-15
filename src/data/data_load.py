
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger('data_extraction')



#==============================
# Data Loading
#==============================
def load_data(df: pd.DataFrame, file_name:str):
    """
    Load the transformed DataFrame into a Parquet file.

    Parameters:
        df (pd.DataFrame): Transformed DataFrame

    Returns:
        None, it loads the data into a new parquet file
    """
    # Verify if is a dataframe
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    # Verify if is empty
    if df.empty:
        logger.warning("DataFrame is empty, no data to load")
        return

    try:
        logger.info("Loading data into Parquet file")

        # Create the processed data folder if it doesn't exist
        processed_data_folder = Path("data/processed")
        processed_data_folder.mkdir(parents=True, exist_ok=True)

        filename_format = f"{file_name}.parquet"

        # Save the DataFrame to a Parquet file
        parquet_file_path = processed_data_folder.joinpath(filename_format)
        df.to_parquet(parquet_file_path.as_posix(), index=False)

        logger.info(f"Data loaded into {parquet_file_path}")

    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")




# # Example usage:
# # transformed_df = pd.read_csv("transformed_data.csv")
# data = {
#     'A': [1, 2, None, 4],
#     'B': [None, 2, 3, 4],
#     'C': [1, 2, 3, 4]
# }
# df = pd.DataFrame(data)
# load_data(df, 'somehtindash')