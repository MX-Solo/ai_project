import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_correlation_heatmap(df):
    """
    Plots a heatmap showing correlations between numerical features in the DataFrame.
    """
    numeric_data = df.select_dtypes(include=[float, int])
    if not numeric_data.empty:
        plt.figure(figsize=(12, 8))
        sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Feature Correlation Heatmap")
        plt.show()

def plot_pairplot(df):
    """
    Plots a pairplot for numerical features to visualize relationships.
    """
    numeric_data = df.select_dtypes(include=[float, int])
    if not numeric_data.empty:
        sns.pairplot(numeric_data)
        plt.show()
