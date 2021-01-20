import os.path

import pytest
import glob

from main import fill_coords, check_rows, mean_coords


def test_existing_file_csv():
    pattern = os.path.join("../data", '*.csv')
    csv_files = glob.glob(pattern)
    if len(csv_files):
        print("File exist")
    else:
        raise FileNotFoundError("No csv files in directory")


@pytest.fixture()
def checked_first_df():
    pattern = os.path.join("../data", '*.csv')
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


def test_fill_cords(checked_first_df):
    df = fill_coords(checked_first_df)
    print(df)
    df_lng = df['lng']
    df_lat = df['lat']

    num_lng = []
    for i in df_lng:
        if i is not None:
            assert True
        elif i is None:
            num_lng = checked_first_df.index[df_lng == i].tolist()
    print(f"Rows without address {num_lng}")

    for j in df_lat:
        if j > 0:
            assert True

    if "Address" in df:
        assert False


def test_average(checked_first_df):
    df = fill_coords(checked_first_df)
    mean_lat, mean_lng = mean_coords(checked_first_df)
    print(mean_lat, mean_lng)

    avg_lat = round(df['lat'].mean(), 2)
    avg_lng = round(df['lng'].mean(), 2)
    print(avg_lat, avg_lng)

    assert mean_lat == avg_lat
    assert mean_lng == avg_lng





