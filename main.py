import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Set

import numpy as np
import pandas as pd

from src.model.model import TitanicClassificationModel
from utilities.get_coords_from_address import get_coords


def args_parse(args):
    """
    Used to set the arguments for the app. Run it from console:
    python main.py -p path to csv.files [addition path ...] -t [amount of threads to run with]
    """
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
        default=1,
        help="set the number of threads for the script",
        type=int,
    )
    return parser.parse_args(args)


def check_columns_and_rows(files):

    li = []
    for filename in files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    df = pd.concat(li, axis=0, ignore_index=True)
    newdf = df.loc[(df["Cabin"].notnull()) & (df["Age"] > 0)]
    newdf = newdf.reset_index(drop=True)
    return newdf


def collect_and_check_files(list_of_paths) -> Set[Path]:
    """
    Checking if the files are present on the path from your input and giving collection of files
    """
    files_to_read = set()
    for path in list_of_paths:
        files_to_read.update(set(Path(path).glob("**/*.csv")))
    if not files_to_read:
        raise FileNotFoundError("Your path has no csv files. Please set another path")
    return files_to_read


def check_address(df):
    current_row_for_counter = 1
    lng = []
    lat = []
    index = df.index
    number_of_rows = len(index)
    for _, row in df.head(
        3
    ).iterrows():  # change "head" value to work with larger set or delete "head" to work with all data
        latt, long = get_coords(row["Address"])
        lng.append(long)
        lat.append(latt)
        print(f"parsing data ({current_row_for_counter}/{number_of_rows})")
        current_row_for_counter += 1
    avg_long = np.mean(np.round(np.array(lng, dtype=np.float64), 2))
    avg_lat = np.mean(np.round(np.array(lat, dtype=np.float64), 2))
    for ind, coord in enumerate(lat):
        if coord == 0:
            lat[ind] = avg_lat
    for ind, coord in enumerate(lng):
        if coord == 0:
            lng[ind] = avg_long
    return [lng, lat]


def file_processing(file):
    df = check_columns_and_rows(file)
    new_df = check_address(df)
    clf = TitanicClassificationModel(new_df)
    result_df = clf.predict()
    return result_df


def separate_by_prediction(df_with_predictions: pd.DataFrame):
    """
    Use to create two folders with csv files in it based on model predictions.
    Folder #1 - Survived, has csv with passengers who has '1' in dataframe's 'predictions' column
    Folder #2 - NotSurvived, has csv with passengers who has '0' in dataframe's 'predictions' column
    """
    survived_df = df_with_predictions[df_with_predictions["predictions"] == 1]
    not_survived_df = df_with_predictions[df_with_predictions["predictions"] == 0]
    output_dir = Path("./survived")
    output_dir.mkdir(exist_ok=True)
    output_dir = Path("./notsurvived")
    output_dir.mkdir(exist_ok=True)
    survived_df.to_csv("survived/survived.csv")
    not_survived_df.to_csv("notsurvived/notsurvived.csv")


def main():
    parser = args_parse(sys.argv[1:])
    files = collect_and_check_files(parser.path)
    result_dfs = []
    with ThreadPoolExecutor(max_workers=parser.threads) as executor:
        futures = [executor.submit(file_processing, file) for file in files]
        for future in as_completed(futures):
            result_dfs.append(future.result())
    df_with_predictions = pd.concat(result_dfs, axis=0, ignore_index=True)
    separate_by_prediction(df_with_predictions)


if __name__ == "__main__":
    main()
