import argparse
import csv
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
import requests

import config
from src.model.model import TitanicClassificationModel


def args_parse(args):
    """
    Used to set the arguments for the app. Run it from console:
    python main.py <path to the folder> [amount of threads to run with]
    author: Vadim
    """
    parser = argparse.ArgumentParser(
        description="Parser for files' path and threads amount"
    )
    parser.add_argument("path", help='set the path to the folder with "*.csv" files')
    parser.add_argument(
        "threads",
        help="set the number of threads for the script",
        type=int,
    )
    return parser.parse_args(args)


def check_columns_and_rows(files):
    """
    author: Dmitry
    """
    li = []
    # for filename in files:   uncomment for several files
    df = pd.read_csv(
        files[0], index_col=None, header=0
    )  # change files[0] to filename for several files
    li.append(df)  # indent if work with several files
    df = pd.concat(li, axis=0, ignore_index=True)
    newdf = df.loc[(df["Cabin"].notnull()) & (df["Age"] > 0)]
    return newdf


def collect_and_check_files(path) -> List[Path]:
    """
    Checking if the files are present on the path from your input
    """
    files_to_read = list(Path(path).glob("**/*.csv"))
    print(files_to_read)
    if not files_to_read:
        raise FileNotFoundError("Your path has no csv files. Please set another path")
    return files_to_read


def get_coords(address: str) -> Tuple[float, float]:
    """
    Taking address and transform it to coordinates using 'positionstack.com' service.
    Detailed info about terms of usage you can find in readme file.
    author: Vadim
    """
    url = "http://api.positionstack.com/v1/forward"
    payload = {"access_key": config.GEO_API_CONFIG, "query": address}
    r = requests.get(url, params=payload)
    try:
        latitude = float(r.json()["data"][0]["latitude"])
        longitude = float(r.json()["data"][0]["longitude"])
    except TypeError:
        return 0.0000, 0.0000
    return latitude, longitude


def check_address(df):
    """
    author: Dmitry
    """
    lng = []
    lat = []
    # ad_df = df.head(2)
    address_list = list(df["Address"])
    for address in address_list:
        latt, long = get_coords(address)
        lng.append(long)
        lat.append(latt)
    avg_long = np.mean(np.round(np.array(lng, dtype=np.float64), 2))
    avg_lat = np.mean(np.round(np.array(lat, dtype=np.float64), 2))
    for ind, coord in enumerate(lat):
        if coord == 0:
            lat[ind] = avg_lat
    for ind, coord in enumerate(lng):
        if coord == 0:
            lng[ind] = avg_long
    return [lng, lat]


def csv_writer(new_df, arg):
    """
    author: Dmitry
    """
    export_data = zip(*arg)
    with open("cords.csv", "w", encoding="ISO-8859-1", newline="") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("lng", "lat"))
        wr.writerows(export_data)
    myfile.close()

    df_2 = pd.read_csv("cords.csv", header=0, low_memory=True)
    final_df = pd.concat([new_df, df_2], axis=1).drop("Address", axis=1)

    final_df.to_csv("final.csv", index=False)


def file_processing(files):
    new_df = check_columns_and_rows(files)
    csv_writer(new_df, check_address(new_df))


def main():
    parser = args_parse(sys.argv[1:])
    files = collect_and_check_files(parser.path)
    with ThreadPoolExecutor(max_workers=parser.threads) as executor:
        future = executor.submit(file_processing, files)
        print(future.result())
    df = pd.read_csv("final.csv", header=0)
    clf = TitanicClassificationModel(df)
    result_df = clf.predict()
    print(result_df)


if __name__ == "__main__":
    main()
