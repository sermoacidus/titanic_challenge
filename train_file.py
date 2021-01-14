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


def check_columns_and_rows():
    """
    author: Dmitry
    """
    li = []
    # for filename in files:   uncomment for several files
    df = pd.read_csv(
        r"C:\Users\admin\Desktop\Titanic\titanic_challenge\data\part-00000-aa9f9ca2-85c7-4b59-ae17-553ce05f6af5-c000.csv", index_col=None, header=0
    )  # change files[0] to filename for several files
    li.append(df)  # indent if work with several files
    df = pd.concat(li, axis=0, ignore_index=True)
    newdf = df.loc[(df["Cabin"].notnull()) & (df["Age"] > 0)]
    newdf = newdf.reset_index(drop=True)
    #newdf = newdf.to_csv('train_file.csv', index=False)
    return newdf


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
    df = pd.read_csv("train_file.csv", header=0, low_memory = True)
    
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
    
    export_data = zip(*arg)
    with open("cords.csv", "w", encoding="ISO-8859-1", newline="") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("lng", "lat"))
        wr.writerows(export_data)
    myfile.close()

    df_2 = pd.read_csv("cords.csv", header=0, low_memory=True)
   
    final_df = pd.merge(new_df, df_2, left_index=True, right_index=True)
  
    final_df = final_df.drop("Address", axis=1)

    final_df.to_csv("final.csv", index=False)


def file_processing():
    new_df = check_columns_and_rows()
    csv_writer(new_df, check_address(new_df))


if __name__ == "__main__":
    
    check_columns_and_rows()
    #check_address()
    file_processing()

   