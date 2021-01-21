import glob
import os.path

import pandas as pd
import pytest
import csv

from main import check_rows, fill_coords, mean_coords, fill_empty_rows


def test_existing_file_csv():
    pattern = os.path.join("./data", "*.csv")
    csv_files = glob.glob(pattern)
    if len(csv_files):
        print("File exist")
    else:
        raise FileNotFoundError("No csv files in directory")


@pytest.fixture()
def checked_first_df():
    pattern = os.path.join("./data", "*.csv")
    csv_files = glob.glob(pattern)[0]  # delete [0] to test all csv files
    df_rows = check_rows(csv_files)
    return df_rows


def test_check_rows(checked_first_df):
    df_rows = checked_first_df
    for i in df_rows["Cabin"]:
        if i:
            return True
        else:
            raise ZeroDivisionError(f"No data in {i}")

    for i in df_rows["Age"]:
        if i:
            return True
        else:
            raise ZeroDivisionError(f"No data in {i}")


@pytest.fixture()
def test_csv():
    list1 = [3.67, None, 7.32, 1.45, None]
    list2 = [2.56, None, 7.48, 2.4, None]
    d = [list1, list2]
    export_data = zip(*d)
    file = 'test_data.csv'
    with open(file, 'w', encoding="ISO-8859-1", newline='') as f:
        wr = csv.writer(f)
        wr.writerow(("lat", "lng"))
        wr.writerows(export_data)
    yield file
    os.remove(file)


def test_fill_empty_rows(test_csv):

    df = pd.read_csv(test_csv, index_col=None)

    new_df = fill_empty_rows(df, 1, 1)

    df_lng = new_df["lng"]
    df_lat = new_df["lat"]

    for i in df_lng:
        if i is not None:
            assert True
        else:
            print("No data in row")

    for j in df_lat:
        if j is not None:
            assert True
        else:
            print("No data in row")


def test_average(test_csv):

    df = pd.read_csv(test_csv, index_col=None, header=0)
    mean_lat, mean_lng = mean_coords(df)

    avg_lat = round(df["lat"].mean(), 2)
    avg_lng = round(df["lng"].mean(), 2)

    assert mean_lat == avg_lat
    assert mean_lng == avg_lng
