from operator import contains
import os
import gzip
import tarfile
import json
import pandas as pd
import requests
from pathlib import Path
import io

# Define constants
raw_dir = Path("data/raw")
extract_dir = Path("data/extracted")
URLS = {
    'orders.json.gz': "https://data-architect-test-source.s3-sa-east-1.amazonaws.com/order.json.gz",
    'consumers.csv.gz': "https://data-architect-test-source.s3-sa-east-1.amazonaws.com/consumer.csv.gz",
    'restaurants.csv.gz': "https://data-architect-test-source.s3-sa-east-1.amazonaws.com/restaurant.csv.gz",
    'ab_test.tar.gz': "https://data-architect-test-source.s3-sa-east-1.amazonaws.com/ab_test_ref.tar.gz"
}


#==============================
# Download files
#==============================
def download_file(url: str, filename:str, dir:Path=raw_dir):
    filepath = dir / filename

    response = requests.get(url, stream=True)
    response.raise_for_status()    

    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return filepath



#==============================
# Extract compressed files
#==============================
def extract_files(file_name:str, file_type:str, read_path:Path=raw_dir, extract_path:Path=extract_dir):
    """
    Process gzipped CSV file

    Parameters:
        filename - str - name of the file to be extracted
        read_path - path - path of the file to be read
        extract_path - path - path of the extraction folder

    Returns:
        Extract file in the "data/extracted/" folder as parquet to optimize space and performance

    """
    # "Universal" variables
    path_read = read_path / file_name
    path_extract = str(extract_path / file_name[:-7])

    # Extract if the compacted file is a gzip csv
    if file_type == 'gzip_csv':
        df = pd.read_csv(path_read, compression='gzip')
    
        return df.to_parquet(path_extract + ".parquet", index=False, compression="gzip")
    

    # Extract if the compacted file is a gzip json
    if file_type == 'gzip_json':
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
        
                
        return df.to_parquet(path_extract + 'parquet', index=False, compression="gzip")


    # Extract if the compacted file is a tar csv
    if file_type == 'tar_csv':
        with tarfile.open(path_read, "r") as tar:
            #tar.extractall(path_extract,filter=None)
            for member in tar.getmembers():  
                if member.isfile() and member.name.endswith(".csv") and member.name.startswith("ab"):  # Filtra arquivos CSV
                    file = tar.extractfile(member)  # Lê o conteúdo do arquivo dentro do .tar
                    if file:
                        df = pd.read_csv(io.BytesIO(file.read()))  # Converte para DataFrame

        return df.to_parquet(path_extract + '.parquet', index=False, compression="gzip")        




    
#==============================
# Main
#==============================
if __name__ == "__main__":
    for i in range(len(list(URLS.keys()))):    
        download_file(list(URLS.values())[i], list(URLS.keys())[i]) # Reading values of dict (URL to download) and its keys (file name)
        
        # If is a csv tar gziped files:
        if ".tar.gz" in list(URLS.keys())[i]:
            extract_files(list(URLS.keys())[i], 'tar_csv')
       
        # If is the csv gziped files:
        if ".csv.gz" in list(URLS.keys())[i]:
            extract_files(list(URLS.keys())[i], 'gzip_csv')

        # If is the json gziped files:
        if ".json.gz" in list(URLS.keys())[i]:
            extract_files(list(URLS.keys())[i], 'gzip_json')       



