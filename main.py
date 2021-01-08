import pandas as pd
from src.model.model import TitanicClassificationModel
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests
import config

def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='setup the path to the folder with "*.csv" files')
    parser.add_argument('threads', help='setup the number of threads for the script', type=int)
    args = parser.parse_args()
    path_to_data = args.path
    threads_amount = args.threads
    p = Path(path_to_data)
    files_to_read = list(p.glob('**/*.csv'))
    if not files_to_read:
        raise ValueError('Your path has no csv files. Please choose another path')
    return files_to_read, threads_amount

def get_coords(address: str): #returns tuple with 2 floats
    url = 'http://api.positionstack.com/v1/forward'
    payload = {'access_key': config.GEO_API_CONFIG, "query": address}
    r = requests.get(url, params=payload)
    latitude = float(r.json()['data'][0]["latitude"])
    longitude = float(r.json()['data'][0]["longitude"])
    return latitude, longitude

def main():
    print(get_coords("Oblastnaya 1 Kudrovo Saint-Petersburg Russia"))
    files_to_read, threads_amount = args_parse()
    with ThreadPoolExecutor(max_workers=threads_amount) as pool:
        responses = pool.map(print, files_to_read)
        df = pd.read_csv('path_to_file/path_to_files', header=0)
        clf = TitanicClassificationModel(df)
        result_df = clf.predict()

if __name__ == '__main__':
    main()
