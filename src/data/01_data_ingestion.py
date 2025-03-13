from operator import contains
import os
import gzip
import tarfile
import json
import pandas as pd
import requests
from pathlib import Path

from urllib3 import response

# Define constants
raw_dir = Path("data/raw")
extract_dir = Path("data/extracted")
URLS = {
    # 'orders.json.gz': "https://data-architect-test-source.s3-sa-east-1.amazonaws.com/order.json.gz",
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
def process_gzip_csv(file_name:str, read_path:Path=raw_dir, extract_path:Path=extract_dir):
    """
    Process gzipped CSV file

    Parameters:
        filename - str - name of the file to be extracted
        read_path - path - path of the file to be read
        extract_path - path - path of the extraction folder

    Returns:
        Extract file in the "data/extracted/" folder

    """
    path_read = read_path / file_name
    path_extract = extract_path / file_name[:-3]

    df = pd.read_csv(path_read, compression='gzip')
    
    return df.to_csv(path_extract, index=False)


def process_gzip_json(file_name:Path, read_path:Path=raw_dir, extract_path:Path=extract_dir) -> pd.DataFrame:
    """
    Process gzipped JSON file
    
    Parameters:
        filename - str - name of the file to be extracted
        read_path - path - path of the file to be read
        extract_path - path - path of the extraction folder

    Returns:
        Extract file in the "data/extracted/" folder
    """
    path_read = read_path / file_name
    path_extract = extract_path / file_name[:-3]
    
    with gzip.open(path_read, 'rt', encoding='utf-8') as f:
        df = pd.DataFrame(json.load(f))
    
    return df.to_json(path_extract, index=False)


def process_tar_csv(file_name:Path, read_path:Path=raw_dir, extract_path:Path=extract_dir):
    """
    Process CSV file from tar.gz
    
    Parameters:
        filename - str - name of the file to be extracted
        read_path - path - path of the file to be read
        extract_path - path - path of the extraction folder

    Returns:
        Extract file in the "data/extracted/" folder
    """
    path_read = read_path / file_name
    path_extract = extract_path / Path(str(file_name[:-6]) + 'csv')

    with tarfile.open(path_read, 'r:gz') as tar:
        csv_file = tar.getnames()[0]
        df = pd.read_csv(tar.extractfile(csv_file), encoding='latin1')
    
    return print(df.head())



if __name__ == "__main__":
    for i in range(len(list(URLS.keys()))):    
        download_file(list(URLS.values())[i], list(URLS.keys())[i]) # Reading values of dict (URL to download) and its keys (file name)
        
        # If is a csv tar gziped files:
        if ".tar.gz" in list(URLS.keys())[i]:
            process_tar_csv(list(URLS.keys())[i])
       
        # # If is the csv gziped files:
        # if ".csv.gz" in list(URLS.keys())[i]:
        #     process_gzip_csv(list(URLS.keys())[i])

       




# def ensure_raw_dir(raw_dir: Path = raw_dir) -> None:
#     """Create data directory if it doesn't exist"""
#     raw_dir.mkdir(parents=True, exist_ok=True)


# def download_file(url: str, filename: str, raw_dir: Path = raw_dir) -> Path:
#     """Download file from URL and save to data directory"""
#     filepath = raw_dir / filename
#     response = requests.get(url, stream=True)
#     response.raise_for_status()
    
#     with open(filepath, 'wb') as f:
#         for chunk in response.iter_content(chunk_size=8192):
#             f.write(chunk)
#     return filepath

# def process_gzip_json(filepath: Path) -> pd.DataFrame:
#     """Process gzipped JSON file"""
#     with gzip.open(filepath, 'rt', encoding='utf-8') as f:
#         data = json.load(f)
#     return pd.DataFrame(data)

# def process_gzip_csv(filepath: Path) -> pd.DataFrame:
#     """Process gzipped CSV file"""
#     return pd.read_csv(filepath, compression='gzip')

# def process_tar_csv(filepath: Path) -> pd.DataFrame:
#     """Process CSV file from tar.gz"""
#     with tarfile.open(filepath, 'r:gz') as tar:
#         csv_file = tar.extractfile(tar.getmembers()[0])
#         return pd.read_csv(csv_file)

# def load_dataset(dataset_name: str, url: str, raw_dir: Path = raw_dir) -> pd.DataFrame:
#     """Load a specific dataset based on its type"""
#     if dataset_name == 'orders':
#         filepath = download_file(url, 'order.json.gz', raw_dir)
#         return process_gzip_json(filepath)
#     elif dataset_name in ['consumers', 'restaurants']:
#         filepath = download_file(url, f'{dataset_name}.csv.gz', raw_dir)
#         return process_gzip_csv(filepath)
#     elif dataset_name == 'ab_test':
#         filepath = download_file(url, 'ab_test_ref.tar.gz', raw_dir)
#         return process_tar_csv(filepath)
#     else:
#         raise ValueError(f"Unknown dataset: {dataset_name}")

# def load_all_datasets(urls: dict = URLS) -> dict:
#     """Load all datasets and return them in a dictionary"""
#     ensure_raw_dir()
    
#     datasets = {}
#     for name, url in urls.items():
#         print(f"Loading {name} dataset...")
#         datasets[name] = load_dataset(name, url)
#         print(f"Loaded {name} dataset: {datasets[name].shape} rows")
    
#     return datasets

# def print_dataset_info(datasets: dict) -> None:
#     """Print basic information about loaded datasets"""
#     for name, df in datasets.items():
#         print(f"\nDataset: {name}")
#         print(f"Shape: {df.shape}")
#         print("Columns:", df.columns.tolist())
#         print("Sample of data types:")
#         print(df.dtypes)

# if __name__ == "__main__":
#     # Load all datasets
#     datasets = load_all_datasets()
    
#     # Print information about loaded datasets
#     print("\nDataset Information:")
#     print_dataset_info(datasets)