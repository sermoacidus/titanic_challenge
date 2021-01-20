import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from src.model.model import TitanicClassificationModel
from utilities import arg_parsing, collecting_csv_from_paths, get_coords_from_address


def check_rows(csv_path):
    """
    This function filtrate data with zero or NaN meaning in columns Cabin and Age,
    after that delete such passengers.
    """
    df = pd.read_csv(csv_path, index_col=None, header=0)
    df_without_empty_val = df.loc[(df["Cabin"].notnull()) & (df["Age"] > 0)]
    df_without_empty_val = df_without_empty_val.reset_index(drop=True)
    return df_without_empty_val


def fill_coords(df):
    """
    This function makes 2 columns in final dataframe with longitude and latitude.
    """
    df["lng"], df["lat"] = "", ""
    for _, row in df.iterrows():
        df.at[_, "lat"], df.at[_, "lng"] = get_coords_from_address.get_coords(
            str(row["Address"])
        )
    final_df = df.drop("Address", axis=1)
    return final_df


def average_coords(df):
    """
    This func checks addresses from geo util and find ones with zero meaning than it
    changes them to average coordinates of dataframe.
    """
    mean_lat = round(df['lat'].mean(), 2)
    mean_lng = round(df['lng'].mean(), 2)
    for _, row in df.iterrows():
        if df.at[_, 'lat'] is None:
            df.at[_, 'lat'] = mean_lat
        if df.at[_, 'lng'] is None:
            df.at[_, 'lng'] = mean_lng
    print(df)
    return df


def _file_processing(file):
    df = check_rows(file)
    new_df = fill_coords(df)
    average_df = average_coords(new_df)
    print(average_df)


if __name__ == "__main__":

    _file_processing(r"C:\Users\admin\Desktop\Titanic\titanic_challenge\data\part-00000-aa9f9ca2-85c7-4b59-ae17-553ce05f6af5-c000.csv")

