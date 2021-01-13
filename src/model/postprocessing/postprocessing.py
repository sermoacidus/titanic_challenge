"""module for generation output template"""
import numpy as np
import pandas as pd


def generate_output_df(df: pd.DataFrame, predictions: np.array) -> pd.DataFrame:
    """Joining input dataframe with predicted values"""
    return df.join(
        pd.DataFrame(predictions, columns=["predictions"]),
    )
