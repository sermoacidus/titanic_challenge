"""This script is a control file for running the 'Titanic_challenge' predictive model.
Information on 'How to?' you can find in README.md
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from src.model.model import TitanicClassificationModel
from utilities import (
    args_parse,
    collect_and_check_files,
    get_coords,
    separate_by_prediction,
)


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


def mean_coords(df):
    """
    Make average from each column Lat and Lng in dataframe.
    """
    mean_lat = round(df["lat"].mean(), 2)
    mean_lng = round(df["lng"].mean(), 2)
    return mean_lat, mean_lng


def fill_empty_rows(df: pd.DataFrame, mean_lat, mean_lng) -> pd.DataFrame:
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


def file_processing(path: Path) -> pd.DataFrame:
    """Function processing your csv data, transferring to classification model and
    then to prediction module.
    """
    clean_df = check_rows(path)
    df_w_coords = fill_coords(clean_df)
    mean_lat, mean_lng = mean_coords(df_w_coords)
    average_df = fill_empty_rows(df_w_coords, mean_lat, mean_lng)
    clf = TitanicClassificationModel(average_df)
    result_df = clf.predict()
    return result_df


def main():
    """Distributing files (from user paths) processing between threads (from user input),
    concatenating results and dividing according to predictions
    """
    parser = args_parse(sys.argv[1:])
    paths_of_files = collect_and_check_files(parser.path)
    result_dfs = []
    with ThreadPoolExecutor(max_workers=parser.threads) as executor:
        futures = [executor.submit(file_processing, path) for path in paths_of_files]
        for future in as_completed(futures):
            result_dfs.append(future.result())
    df_with_predictions = pd.concat(result_dfs, axis=0, ignore_index=True)
    separate_by_prediction(df_with_predictions)


if __name__ == "__main__":
    main()
