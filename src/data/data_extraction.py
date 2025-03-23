from datetime import datetime
from operator import contains
import os
import gzip
import tarfile
import json
import pandas as pd
import requests
import logging
from pathlib import Path
import io

#==============================
# Define constants
#==============================
raw_dir = Path("data/raw")
extract_dir = Path("data/extracted")
URLS = {
    'orders.json.gz': "https://data-architect-test-source.s3-sa-east-1.amazonaws.com/order.json.gz",
    'consumers.csv.gz': "https://data-architect-test-source.s3-sa-east-1.amazonaws.com/consumer.csv.gz",
    'restaurants.csv.gz': "https://data-architect-test-source.s3-sa-east-1.amazonaws.com/restaurant.csv.gz",
    'ab_test.tar.gz': "https://data-architect-test-source.s3-sa-east-1.amazonaws.com/ab_test_ref.tar.gz"
}

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data_extraction')



#==============================
# Download files
#==============================
def download_file(url: str, filename:str, dir:Path=raw_dir):
    """
    Download files from web

    Parameters:
        url: the link for the file
        filename: name of the file
        dir: directory to save
    
    returns:
        It downloads the file and return the path that was saved
    """
    filepath = dir / filename

    try:
        if os.path.exists(filepath):
            logger.info(f"File already exists: {filepath}")
            return True
    
        else:
            # GET request to get data from S3
            response = requests.get(url, stream=True)
            # Raise an exception if the HTTP request returned an unsuccessful status code
            response.raise_for_status()    

            with open(filepath, 'wb') as f:
                # Open the file with "write - binary" mode and write each 8192 bytes
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return filepath

    except Exception as e:
        logger.error(f"Error downloading file {url}: {e}")
        return False



#==============================
# Extract compressed files
#==============================
def extract_files(file_name:str, file_type:str, read_path:Path=raw_dir, extract_path:Path=extract_dir):
    """
    Process gzipped files

    Parameters:
        filename: name of the file to be extracted
        file_type: file format 
        read_path: path - path of the file to be read
        extract_path: path - path of the extraction folder -> send to "extracted folder" 

    Returns:
        Extract file in the "data/extracted/" folder as parquet to standardize, optimize space and performance
        Also, return a pd.DataFrame

    """
    # "Universal" variables
    path_read = read_path / file_name
    path_extract = str(extract_path / file_name[:-7])

    try:
        if os.path.exists(path_extract):
            logger.info(f"Extracted file already exists: {path_extract}")
            return True
    
        #=================================
        # Extract if the compacted file is a gzip csv
        #=================================
        elif file_type == 'gzip_csv':
            logger.info(f"Extracting {file_name} to {path_extract}")
            df = pd.read_csv(path_read, compression='gzip')
            
            df.to_parquet(path_extract + ".parquet", index=False, compression="gzip")
            logger.info(f"Extraction completed: {path_extract} + '.parquet'")           
            
            return df


        #=================================
        # Extract if the compacted file is a gzip json
        #=================================
        elif file_type == 'gzip_json':
            logger.info(f"Extracting {file_name} to {path_extract}")
            # Read file .gz and process json line by lineLer o arquivo .gz e processar JSON linha por linha            
            records = []
            with gzip.open(path_read, 'rt', encoding='utf-8') as f:
                for line in f:
                    try:
                        # Parsear cada linha como um objeto JSON
                        record = json.loads(line.strip())
                        records.append(record)
                    except json.JSONDecodeError as e:
                        print(f"Erro ao processar linha: {e}")

            # Convert to DF
            df = pd.DataFrame(records)

            logger.info(f"Extraction completed: {path_extract}" + 'parquet')
            df.to_parquet(path_extract + 'parquet', index=False, compression="gzip")
            return df


        #=================================
        # Extract if the compacted file is a tar csv
        #=================================
        elif file_type == 'tar_csv':
            logger.info(f"Extracting {file_name} to {path_extract}")
            with tarfile.open(path_read, "r") as tar:
                #tar.extractall(path_extract,filter=None)
                for member in tar.getmembers():  
                    if member.isfile() and member.name.endswith(".csv") and member.name.startswith("ab"):  # Filtra arquivos CSV
                        file = tar.extractfile(member)  # Lê o conteúdo do arquivo dentro do .tar
                        if file:
                            df = pd.read_csv(io.BytesIO(file.read()))  # Converte para DataFrame
            
            df.to_parquet(path_extract + '.parquet', index=False, compression="gzip")
            logger.info(f"Extraction completed: {path_extract}" + '.parquet')
            
            return df

    
    except Exception as e:
        logger.error(f"Error extracting file {path_extract}: {e}")
        return False



    
#==============================
# Main
#==============================
# if __name__ == "__main__":
#     # start_time = datetime.now()
#     # logger.info("Starting data extraction process")
    
#     # for i in range(len(list(URLS.keys()))):    
#     #     download_file(list(URLS.values())[i], list(URLS.keys())[i]) # Reading values of dict (URL to download) and its keys (file name)
        
#     #     # If is a csv tar gziped files:
#     #     if ".tar.gz" in list(URLS.keys())[i]:
#     #         extract_files(list(URLS.keys())[i], 'tar_csv')
       
#     #     # If is the csv gziped files:
#     #     if ".csv.gz" in list(URLS.keys())[i]:
#     #         extract_files(list(URLS.keys())[i], 'gzip_csv')

#     #     # If is the json gziped files:
#     #     if ".json.gz" in list(URLS.keys())[i]:
#     #         extract_files(list(URLS.keys())[i], 'gzip_json')       

#     # end_time = datetime.now()
#     # logger.info(f"Data extraction process completed in {end_time - start_time}")