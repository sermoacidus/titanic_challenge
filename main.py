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
    for _, row in df.apply():
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
    mean_lat = df['lat'].mean()
    mean_lng = df['lng'].mean()
    for _, row in df.iterrows():
        if df.at[_, 'lat'] == 0:
            df.at[_, 'lat'] = mean_lat
        if df.at[_, 'lng'] == 0:
            df.at[_, 'lng'] = mean_lng
    return df


def _file_processing(file):
    df = check_rows(file)
    new_df = fill_coords(df)
    average_df = average_coords(new_df)
    clf = TitanicClassificationModel(average_df)
    result_df = clf.predict()
    return result_df


def separate_by_prediction(df_with_predictions: pd.DataFrame):
    """Use to create two folders with csv files in it based on model predictions.
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
    """Distributing files (from user paths) processing between threads (from user input),
    concatenating results and dividing according to predictions
    """
    parser = arg_parsing.args_parse(sys.argv[1:])
    files = collecting_csv_from_paths.collect_and_check_files(parser.path)
    result_dfs = []
    with ThreadPoolExecutor(max_workers=parser.threads) as executor:
        futures = [executor.submit(_file_processing, file) for file in files]
        for future in as_completed(futures):
            result_dfs.append(future.result())
    df_with_predictions = pd.concat(result_dfs, axis=0, ignore_index=True)
    separate_by_prediction(df_with_predictions)


if __name__ == "__main__":
    main()