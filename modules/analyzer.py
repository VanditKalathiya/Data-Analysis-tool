import pandas as pd

def get_summary_stats(df: pd.DataFrame):
    return df.describe(include='all').transpose().round(2)

def get_missing_values(df: pd.DataFrame):
    nulls = df.isnull().sum()
    percent = (nulls / len(df)) * 100
    missing_df = pd.DataFrame({
        "Missing Count": nulls,
        "Missing %": percent
    })
    return missing_df[missing_df["Missing Count"] > 0].sort_values("Missing %", ascending=False)

def get_top_categoricals(df: pd.DataFrame, top_n: int = 1):
    cat_cols = df.select_dtypes(include='object').columns
    data = {
        col: df[col].value_counts().head(top_n).to_dict()
        for col in cat_cols if df[col].nunique() < 50
    }
    return pd.DataFrame.from_dict(data, orient="index")
