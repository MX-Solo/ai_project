import pandas as pd
from scipy.stats import zscore

def detect_outliers_zscore(df, threshold=3):
    """
    Detects outliers in numerical columns using the Z-score method.
    """
    outliers = pd.DataFrame()
    for col in df.select_dtypes(include=[float, int]):
        z_scores = zscore(df[col])
        outliers[col] = abs(z_scores) > threshold
    return outliers

def remove_outliers(df, outliers):
    """
    Removes rows identified as outliers.
    """
    outlier_indices = outliers.any(axis=1)
    return df[~outlier_indices]
