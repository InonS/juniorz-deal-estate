"""
Time series forecasting data prep for Prophet.
"""
import pandas as pd

def prepare_prophet_dataframe(df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
    """
    Prepare a DataFrame for Prophet forecasting.

    Args:
        df: Input DataFrame.
        date_col: Name of the date column.
        value_col: Name of the value column.

    Returns:
        DataFrame with columns ['ds', 'y'].

    >>> import pandas as pd
    >>> df = pd.DataFrame({'date': ['2020-01-01'], 'price': [100]})
    >>> out = prepare_prophet_dataframe(df, 'date', 'price')
    >>> set(out.columns) == {'ds', 'y'}
    True
    """
    return df.rename(columns={date_col: "ds", value_col: "y"})[['ds', 'y']]