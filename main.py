"""This script is a control file for running the 'Titanic_challenge' predictive model.
Information on 'How to?' you can find in README.md
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from src.model.model import TitanicClassificationModel
from utilities import (
    args_parse,
    collect_and_check_files,
    separate_by_prediction,
    check_rows,
    fill_coords,
    mean_coords,
    fill_empty_rows
)


def file_processing(path: Path) -> pd.DataFrame:
    """Function processing your csv data, transferring to classification model and
    then to prediction module.
    """
    clean_df = check_rows(path)
    df_w_coords = fill_coords(clean_df)
    mean_lat, mean_lng = mean_coords(df_w_coords)
    average_df = fill_empty_rows(df_w_coords, mean_lat, mean_lng)
    clf = TitanicClassificationModel(average_df)
    result_df = clf.predict()
    return result_df


def main():
    """Distributing files (from user paths) processing between threads (from user input),
    concatenating results and dividing according to predictions
    """
    parser = args_parse(sys.argv[1:])
    paths_of_files = collect_and_check_files(parser.path)
    result_dfs = []
    with ThreadPoolExecutor(max_workers=parser.threads) as executor:
        futures = [executor.submit(file_processing, path) for path in paths_of_files]
        for future in as_completed(futures):
            result_dfs.append(future.result())
    df_with_predictions = pd.concat(result_dfs, axis=0, ignore_index=True)
    separate_by_prediction(df_with_predictions)


def sep_results():
    """Return final predictions of survived and not survived people.
    """
    df_survive = pd.read_csv('survived/survived.csv', index_col=0, header=0)
    df_nsurvive = pd.read_csv('notsurvived/notsurvived.csv', index_col=0, header=0)
    survive = df_survive['predictions'].count()
    nsurvive = df_nsurvive['predictions'].count()
    print(f"Выжившие {survive}, Невыжившие {nsurvive}")


if __name__ == "__main__":
    main()
    sep_results()
