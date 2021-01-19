import os.path
from glob import glob

import pytest

from main import check_rows


def test_existing_file_csv():
    if os.path.exists(r"\titanic_challenge\data\*.csv"):
        print("File exist")
    else:
        print("File not exist")

def test_