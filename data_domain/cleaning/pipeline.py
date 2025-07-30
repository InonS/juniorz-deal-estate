"""
Data cleaning and transformation pipeline.
"""
import pandas as pd
from typing import Callable, List

def clean_dataframe(df: pd.DataFrame, cleaning_steps: List[Callable[[pd.DataFrame], pd.DataFrame]]) -> pd.DataFrame:
    """
    Apply a list of cleaning functions to a DataFrame.

    Args:
        df: Input DataFrame.
        cleaning_steps: List of functions that accept and return a DataFrame.

    Returns:
        Cleaned DataFrame.

    >>> import pandas as pd
    >>> def drop_na(df): return df.dropna()
    >>> df = pd.DataFrame({'a': [1, None, 3]})
    >>> clean_dataframe(df, [drop_na]).reset_index(drop=True)
       a
    0  1.0
    1  3.0
    """
    for step in cleaning_steps:
        df = step(df)
    return df