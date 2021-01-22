"""This module contents miscellaneous functions needed for main.py
"""
import argparse
import json
import logging
import sys
import threading
from pathlib import Path
from typing import List, Set, Tuple

import pandas as pd
import requests


def check_rows(csv_path: Path):
    """
    This function filtrate data with zero or NaN meaning in columns Cabin and Age,
    after that delete such passengers.
    """
    df = pd.read_csv(csv_path, index_col=None, header=0)
    df_without_empty_val = df.loc[(df["Cabin"].notnull()) & (df["Age"] > 0)]
    df_without_empty_val = df_without_empty_val.reset_index(drop=True)
    return df_without_empty_val


def fill_coords(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function makes 2 columns in final dataframe with longitude and latitude.
    """
    df["lng"], df["lat"] = "", ""
    for _, row in df.iterrows():
        df.at[_, "lat"], df.at[_, "lng"] = get_coords(str(row["Address"]))
    final_df = df.drop("Address", axis=1)
    return final_df


def mean_coords(df: pd.DataFrame):
    """
    Make average from each column Lat and Lng in dataframe.
    """
    mean_lat = round(df["lat"].mean(), 2)
    mean_lng = round(df["lng"].mean(), 2)
    return mean_lat, mean_lng


def fill_empty_rows(df: pd.DataFrame, mean_lat: float, mean_lng: float) -> pd.DataFrame:
    """
    This func checks addresses from geo util and find ones with zero meaning than it
    changes them to average coordinates of dataframe.
    """
    for _, row in df.iterrows():
        if df.at[_, "lat"] is None:
            df.at[_, "lat"] = mean_lat
        if df.at[_, "lng"] is None:
            df.at[_, "lng"] = mean_lng
    return df


def args_parse(args):
    """Used to set the arguments for the app. Run it from console:
    python main.py -p <path to csv.files> [additional path ...] -t [amount of threads to run with]
    """
    logging.debug(
        f"Checking arguments. All arguments - {sys.argv}, in function - {args}"
    )
    if "-t" in args:
        threads_amount = args[args.index("-t") + 1]
        try:
            if int(threads_amount) < 1:
                raise ValueError
        except (ValueError, TypeError):
            logging.critical("Wrong thread argument, invoking exception")
            raise ValueError(
                "Wrong 'threads' argument, it must be integer and it's value must be more then zero"
            )
    parser = argparse.ArgumentParser(
        description="Parser for files' path and threads amount"
    )
    parser.add_argument(
        "-p", "--path", nargs="+", help='set the path to the folder with "*.csv" files'
    )
    parser.add_argument(
        "-t",
        "--threads",
        nargs="?",
        const="threads",
        default=None,
        help="set the number of threads for the script",
        type=int,
    )
    logging.info("Successful parsing of arguments")
    return parser.parse_args(args)


def collect_and_check_files(list_of_paths: List[Path]) -> Set[Path]:
    """Checking if the files are present on the path from your input and giving collection of files"""
    logging.info("Looking for suitable files")
    files_to_read = set()
    for path in list_of_paths:
        files_to_read.update(set(Path(path).glob("**/*.csv")))
    if not files_to_read:
        logging.critical("Wrong input path")
        raise FileNotFoundError(
            "Your path has no csv files. Either wrong path or no files on path."
            "Please set another path"
        )
    logging.info("Files collected.")
    return files_to_read


def get_coords(address: str) -> Tuple:
    """Takes address and transforms it to coordinates using 'positionstack.com' service.
    Detailed info about terms of usage you can find in readme file.
    """
    logging.debug(
        f"Starting fetching coordinates in thread - {threading.current_thread().name},"
        f" sending address {address}"
    )
    with open("config.json") as json_file:
        key = json.load(json_file)["API_KEY"]
    url = "http://api.positionstack.com/v1/forward"
    payload = {
        "access_key": key,
        "query": address.replace(" ", ","),
        "limit": "1",
    }
    r = requests.get(url, params=payload)
    if r.status_code == 429:
        logging.warning(
            f"API exception. Status code - {r.status_code}, API response - {r.json()}"
        )
        raise ConnectionRefusedError(
            "The given user account has reached its monthly allowed request volume."
        )
    elif r.status_code == 401:
        logging.warning(
            f"API exception. Status code - {r.status_code}, API response - {r.json()}"
        )
        raise ConnectionRefusedError("An invalid API access key was supplied.")
    try:
        latitude = float(r.json()["data"][0]["latitude"])
        longitude = float(r.json()["data"][0]["longitude"])
    except (TypeError, IndexError, KeyError) as e:
        logging.warning(
            f"Address {address} is not found by API, returning None,"
            f" the answer of API is {r.json()}, the exception is {type(e), e}"
        )
        return None, None
    logging.debug(f"Address {address} is successfully found, returning coordinates")
    return latitude, longitude


def separate_by_prediction(df_with_predictions: pd.DataFrame):
    """Use to create two folders with csv files in it based on model predictions.
    Folder #1 - Survived, has csv with passengers who has '1' in dataframe's 'predictions' column
    Folder #2 - NotSurvived, has csv with passengers who has '0' in dataframe's 'predictions' column
    """
    logging.info("Separating by result in prediction started")
    survived_df = df_with_predictions[df_with_predictions["predictions"] == 1]
    not_survived_df = df_with_predictions[df_with_predictions["predictions"] == 0]
    output_dir = Path("./survived")
    output_dir.mkdir(exist_ok=True)
    output_dir = Path("./notsurvived")
    output_dir.mkdir(exist_ok=True)
    survived_df.to_csv(Path("survived/survived.csv"))
    not_survived_df.to_csv(Path("notsurvived/notsurvived.csv"))
