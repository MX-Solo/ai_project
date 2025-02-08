import pandas as pd
import numpy as np

def read_data(file_path, column_names):
    """
    Reads data from a CSV file and applies column names.
    """
    return pd.read_csv(file_path, header=None, names=column_names)

def handle_missing_values(df, threshold=0.5):
    """
    Replaces '-' with NaN and drops columns with more than `threshold` missing values.
    """
    df.replace('-', np.nan, inplace=True)
    threshold_value = threshold * len(df)
    df.dropna(axis=1, thresh=threshold_value, inplace=True)
    return df

def drop_constant_columns(df, threshold=0.9):
    """
    Drops columns with constant values or a high percentage of identical values.
    """
    for col in df.columns:
        if df[col].nunique() <= 1 or (df[col].value_counts(normalize=True).max() >= threshold):
            df.drop(columns=[col], inplace=True)
    return df

def fill_missing_values_with_mode(df):
    """
    Fills missing values in the DataFrame with the mode of each column.
    """
    return df.apply(lambda col: col.fillna(col.mode()[0]))


def replace_dash_with_mode(df):
    """
    Replaces all occurrences of '-' in the DataFrame with the mode of their respective column.
    """
    for col in df.columns:
        if (df[col] == '-').any():  
            mode_value = df.loc[df[col] != '-', col].mode()[0]  
            df[col] = df[col].replace('-', mode_value)  
    return df