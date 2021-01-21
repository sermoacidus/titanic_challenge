import shutil
from pathlib import Path

import pandas as pd
import pytest

from utilities import separate_by_prediction


@pytest.fixture
def create_test_file():
    test_df = pd.DataFrame({"name": ["John", "Judy"], "predictions": [1, 0]})
    separate_by_prediction(test_df)
    surv_df = pd.read_csv(Path("./survived/survived.csv"))
    notsurv_df = pd.read_csv(Path("./notsurvived/notsurvived.csv"))
    yield surv_df, notsurv_df
    shutil.rmtree(Path("./survived"))
    shutil.rmtree(Path("./notsurvived"))


def test_separation_logic(create_test_file):
    surv, notsurv = create_test_file
    assert surv.at[0, "predictions"] == 1
    assert notsurv.at[0, "predictions"] == 0
