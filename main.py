# Main ETL Pipeline 
# This script orchestrates the entire ETL process: extraction, transformation, and loading data

from datetime import datetime
import logging
import pandas as pd
from pathlib import Path
import gc  # For garbage collection

# Import our modules 
from src.data.data_extraction import download_file, extract_files, URLS
from src.data.data_transformation import handle_na_data, convert_column, remove_duplicates
from src.data.data_load import load_data


#==============================
# Define constants
#==============================
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('main')


#==============================
# Process Tar Files
#==============================
def process_tar_file(filename, file_name_only, path_extract):
    """
    Process tar.gz files through the ETL pipeline
    
    Args:
        filename (str): Name of the file to process
        file_name_only (str): Name of the file without extension
        path_extract (str): Path to extract the data to
        
    Returns:
        None
    """
    #--------------
    # Step 1: Extract Data
    #--------------
    logger.info(f"Step 1: Extracting data for: {filename}")
    df_tar = extract_files(filename, 'tar_csv')
    df_tar.to_parquet(path_extract + '.parquet', index=False, compression="gzip")
    
    #--------------
    # Step 2: Transform Data                
    #--------------
    logger.info(f"Step 2: Transforming data for: {filename}")
    # No transformations needed for this file
    
    #--------------
    # Step 3: Load data
    #--------------
    logger.info(f"Step 3: Loading transformed {file_name_only} data")
    load_data(df_tar, file_name_only)
    
    # Free memory
    del df_tar
    gc.collect()


#==============================
# Process CSV Files
#==============================
def process_csv_file(filename, file_name_only, path_extract):
    """
    Process csv.gz files through the ETL pipeline.
    
    Args:
        filename (str): Name of the file to process
        file_name_only (str): Name of the file without extension
        path_extract (str): Path to extract the data to
        
    Returns:
        None
    """
    #--------------
    # Step 1: Extracting Data
    #--------------
    logger.info(f"Step 1: Extracting data for: {filename}")
    df_csv = extract_files(filename, 'gzip_csv')
    df_csv.to_parquet(path_extract + ".parquet", index=False, compression="gzip")

    
    #--------------
    # Step 2: Transform Data
    #--------------
    name = file_name_only #filename.replace('.csv.gz', '')
    
    # Restaurants transformation
    if name == 'restaurants':
        logger.info(f"Step 2: Transforming data of: {name}")

        # Converting columns
        conversions = [
            ('created_at', 'datetime'),
            ('price_range', 'int'),
            ('takeout_time', 'int'),
            ('average_ticket', 'float'),
            ('delivery_time', 'float'),
            ('minimum_order_value', 'float')
        ]
        # Instead of doing: "df_rest = convert_column(df_csv, conversions)", using pipe to not generate multiple DFs
        df_transformed  = (
            df_csv.pipe(handle_na_data, ['minimum_order_value'], 'fill', 0)
                  .pipe(convert_column, conversions)
                  .pipe(remove_duplicates, 'id', 'created_at')
        )

  
    # Consumers transformation
    elif name == 'consumers':
        logger.info(f"Step 2: Transforming data of: {name}")

        # Converting columns
        conversions = [
            ('created_at', 'datetime'),
            ('customer_phone_number', 'int')
        ]
        df_transformed = (
            df_csv.pipe(handle_na_data, ['customer_name'], 'fill', 'n/d')
                  .pipe(convert_column, conversions)
                  .pipe(remove_duplicates, 'customer_id', 'created_at')
        )
        
    else:
        logger.warning(f"No specific transformation for {name}, using original data")
        df_transformed = df_csv

    
    #--------------
    # Step 3: Load Data
    #--------------
    logger.info(f"Step 3: Loading transformed {name} data")
    load_data(df_transformed , f"{name}_processed")

    # Free memory
    del df_csv, df_transformed
    gc.collect()



#==============================
# Process Tar Files
#==============================
def process_json_file(filename, file_name_only, path_extract):
    """
    Process json.gz files through the ETL pipeline
    
    Args:
        filename (str): Name of the file to process
        file_name_only (str): Name of the file without extension
        path_extract (str): Path to extract the data to
        
    Returns:
        None
    """
    name = file_name_only

    #--------------
    # Step 1: Extract Data
    #--------------
    logger.info(f"Step 1: Extracting data for: {filename}")
    df_json = extract_files(filename, 'gzip_json')
    df_json.to_parquet(path_extract + '.parquet', index=False, compression="gzip")
    
    #--------------
    # Step 2: Transform Data
    #--------------
    logger.info(f"Step 2: Transforming data for: {filename}")
    if name == 'orders':
        logger.info(f"Step 2: Transforming data of: {name}")

        # Converting columns
        conversions = [
            ('order_created_at', 'datetime'),
            ('order_total_amount', 'float'),
            ('order_scheduled_date', 'datetime')
        ]        
        df_transformed  = (
            df_json.pipe(handle_na_data, ['customer_id'], 'drop') # Deleting rows without a customer_id as we wont be able to joinn with the other datasets to understand the a/b tests
                  .pipe(convert_column, conversions)
                  .pipe(remove_duplicates, 'order_id', 'order_created_at')
        )

    
    
    #--------------
    # Step 3: Load data
    #--------------
    logger.info(f"Step 3: Loading transformed {file_name_only} data")
    load_data(df_transformed, file_name_only)
    
    # Free memory
    del df_transformed
    gc.collect()



#==============================
# Main ETL Pipeline
#==============================
def main():
    """
    Execute the complete ETL pipeline
    
    The pipeline consists of three main steps:
    1. Extract - Downloads and extracts data from S3
    2. Transform - Cleans and processes the extracted data
       - Transformations are applied to specific columns based on data type and requirements
       - For one-time analysis, manual transformations are applied (ex.: explicit select which columns I want to convert)
       - For production/scheduled ETL, a more automated approach would be implemented; being a selected trade-off due to time management
    3. Load - Saves the transformed data in parquet format for better performance and storage
    
    Data Sources:
        - Orders (JSON)
        - Consumers (CSV)
        - Restaurants (CSV)
        - AB Test Data (TAR)
    
    Returns:
        None, but creates processed parquet files in the data/processed directory
    """
    start_time = datetime.now()
    logger.info("Starting ETL pipeline")
    
    # Create necessary directories if they dont exist
    Path("data/extracted").mkdir(parents=True, exist_ok=True)
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    # Process each file from the URLs dictionary
    for filename, url in URLS.items(): # URLS is a dictionary that contains the file name and URL to download the datasets
        try:
            if download_file(url, filename):
                # Set up file paths
                file_name_only = filename.split('.')[0]  # Getting filename without extension
                path_extract = f'data/extracted/{file_name_only}'
                
                # Process each file types
                if ".tar.gz" in filename:
                    process_tar_file(filename, file_name_only, path_extract)
                
                elif ".csv.gz" in filename:
                    process_csv_file(filename, file_name_only, path_extract)
                
                elif ".json.gz" in filename:
                    process_json_file(filename, file_name_only, path_extract)
                
                else:
                    logger.warning(f"Unsupported file format: {filename}")

            else:
                logger.error(f"Failed to download {filename} from {url}")
        
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}", exc_info=True)
    
    end_time = datetime.now()
    logger.info(f"ETL pipeline completed in {end_time - start_time}")



#==============================
# Main
#==============================
if __name__ == "__main__":
    main()