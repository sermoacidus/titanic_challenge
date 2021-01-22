from pathlib import Path

import pandas as pd

from src.model.model import TitanicClassificationModel
from utilities import check_rows, fill_empty_rows, mean_coords, separate_by_prediction


def test_filtrating_data():
    first_action = check_rows("test_1.csv")
    if type(first_action) != pd.DataFrame:
        raise TypeError("Wrong file type")


def test_file_process():
    second_df = pd.read_csv("test_2_with_coords.csv", index_col=0, header=0)
    mean_lat, mean_lng = mean_coords(second_df)
    average_df = fill_empty_rows(second_df, mean_lat, mean_lng)
    clf = TitanicClassificationModel(average_df)
    result_df = clf.predict()
    sep_res = separate_by_prediction(result_df)
    return sep_res


def test_output_exist():
    if Path("survived/").is_dir() and Path("notsurvived/").is_dir():
        print("Files exists")

    else:
        raise FileNotFoundError("No file in this folder")


if __name__ == "__main__":
    test_file_process()
