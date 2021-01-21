import csv
import os.path
import sys

import pandas as pd
from pathlib import Path

import pytest
import glob
import argparse
from unittest import mock

from main import check_rows, fill_coords, mean_coords, fill_empty_rows, separate_by_prediction
from src.model.model import TitanicClassificationModel
from utilities import args_parse, collect_and_check_files, get_coords


def test_filtrating_data():
    first_action = check_rows('test_1.csv')
    assert type(first_action) == pd.DataFrame


def test_file_process():
    second_df = pd.read_csv('test_2_with_coords.csv', index_col=0, header=0)
    mean_lat, mean_lng = mean_coords(second_df)
    average_df = fill_empty_rows(second_df, mean_lat, mean_lng)
    clf = TitanicClassificationModel(average_df)
    result_df = clf.predict()
    sep_res = separate_by_prediction(result_df)


def test_output_exist():
    if Path('integration/survived/survived.csv').is_dir() and Path('integration/notsurvived/notsurvived.csv').is_dir():
        assert Path is True


def test_comparison_final_res():
    with open('test_survived.csv', 'r') as t1, open('../integration/survived/survived.csv', 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

        for line in filetwo:
            if line not in fileone:
                print("Bad")
            else:
                print("All good")


if __name__ == "__main__":
    # test_file_process()
    test_comparison_final_res()

