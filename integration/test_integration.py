from pathlib import Path
from unittest.mock import MagicMock, PropertyMock

import pandas as pd
import requests

from src.model.model import TitanicClassificationModel
from utilities import (
    check_rows,
    fill_empty_rows,
    get_coords,
    mean_coords,
    separate_by_prediction,
)


def test_output(monkeypatch):
    mock = MagicMock(return_value=requests.models.Response)
    pock = PropertyMock(return_value=200)
    data = {"data": [{"latitude": 40.68295, "longitude": -73.9708}]}
    monkeypatch.setattr(requests, "get", mock)
    requests.get("Moscow Russia").status_code = pock
    monkeypatch.setattr(requests.models.Response, "json", MagicMock(return_value=data))
    assert get_coords("Moscow Russia") == (40.68295, -73.9708)


def test_filtrating_data():
    first_action = check_rows("test_1.csv")
    assert type(first_action) == pd.DataFrame


def test_file_process():
    second_df = pd.read_csv("test_2_with_coords.csv", index_col=0, header=0)
    mean_lat, mean_lng = mean_coords(second_df)
    average_df = fill_empty_rows(second_df, mean_lat, mean_lng)
    clf = TitanicClassificationModel(average_df)
    result_df = clf.predict()
    sep_res = separate_by_prediction(result_df)
    return sep_res


def test_output_exist():
    if (
        Path("integration/survived/survived.csv").is_dir()
        and Path("integration/notsurvived/notsurvived.csv").is_dir()
    ):
        assert Path is True


def test_comparison_final_res():
    with open("test_survived.csv", "r") as t1, open(
        "../integration/survived/survived.csv", "r"
    ) as t2:
        file_1 = t1.readlines()
        file_2 = t2.readlines()

        for line in file_2:
            if line not in file_1:
                assert False
            else:
                assert True


if __name__ == "__main__":
    # test_file_process()
    test_comparison_final_res()
