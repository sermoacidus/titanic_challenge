import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import csv

from src.model.model import TitanicClassificationModel
from utilities import args_parse, collect_and_check_files, get_coords


def check_rows(csv_path: Path):
    """
    This function filtrate data with zero or NaN meaning in columns Cabin and Age,
    after that delete such passengers.
    """
    df = pd.read_csv(csv_path, index_col=None, header=0)
    df_without_empty_val = df.loc[(df["Cabin"].notnull()) & (df["Age"] > 0)]
    df_without_empty_val = df_without_empty_val.reset_index(drop=True)
    print(df_without_empty_val)
    return df_without_empty_val


def fill_coords(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function makes 2 columns in final dataframe with longitude and latitude.
    """
    df["lat"], df["lng"] = "", ""
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


def _file_processing(file):
    df = check_rows(file)
    new_df = fill_coords(df)
    mean_lat, mean_lng = mean_coords(new_df)
    average_df = fill_empty_rows(new_df, mean_lat, mean_lng)
    average_df.to_csv('test_2_with_coords.csv')
    print(average_df)



if __name__ == "__main__":
    _file_processing(r"C:\Users\admin\Desktop\Titanic\titanic_challenge\integration\test_1.csv")