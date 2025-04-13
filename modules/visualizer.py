import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(df, column):
    fig, ax = plt.subplots()
    sns.histplot(df[column].dropna(), kde=True, ax=ax)
    ax.set_title(f"Distribution of {column}")
    return fig

def plot_correlation_heatmap(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    corr = df.select_dtypes(include='number').corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")
    return fig

def plot_scatter(df, x_col, y_col):
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
    ax.set_title(f"{y_col} vs {x_col}")
    return fig
