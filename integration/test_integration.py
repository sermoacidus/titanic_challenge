import os.path
import sys
import unittest
from turtle import pd


import pytest
import glob
import argparse
from unittest import mock

from main import check_rows, fill_coords, mean_coords, fill_empty_rows, _file_processing, separate_by_prediction, main
from utilities import arg_parsing, collecting_csv_from_paths, get_coords_from_address


@pytest.fixture()
def checked_first_df():
    pattern = os.path.join("../data", '*.csv')
    csv_files = glob.glob(pattern)[0]  # delete [0] to test all csv files
    return csv_files


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = arg_parsing()

    def test_something(self):
        parsed = self.parser.parse_args(['--something', 'test'])
        self.assertEqual(parsed.something, 'test')



def test_check_rows_output(checked_first_df):
    output = check_rows(checked_first_df)


if __name__ == "__main__":
    checked_first_df()
