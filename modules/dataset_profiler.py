def profile_dataset(df):
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

    suggested_targets = [
        col for col in num_cols
        if df[col].nunique() > 20 and col.lower().endswith(("price", "score", "value"))
    ]

    return {
        "num_cols": num_cols,
        "cat_cols": cat_cols,
        "datetime_cols": datetime_cols,
        "suggested_targets": suggested_targets
    }

def detect_task_type(df, target):
    if df[target].dtype == 'object' or df[target].nunique() <= 10:
        return "Classification"
    return "Regression"
