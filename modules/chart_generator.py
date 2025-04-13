import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64

def render_bar_chart(df: pd.DataFrame, x_col: str, y_col: str):
    if x_col not in df.columns or y_col not in df.columns:
        return None, f"❌ Columns `{x_col}` or `{y_col}` not found in dataset."

    df_grouped = df.groupby(x_col)[y_col].sum().reset_index()
    df_grouped = df_grouped.sort_values(y_col, ascending=False)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=df_grouped, x=x_col, y=y_col, ax=ax)
    ax.set_title(f"Bar Chart: {y_col} by {x_col}")
    plt.xticks(rotation=45)

    # Save chart to base64
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()

    # Build bullet insights
    bullet_points = [
        f"{i+1}. **{row[x_col]}** – {row[y_col]}" for i, row in df_grouped.head(5).iterrows()
    ]
    summary = f"📌 Top {min(5, len(bullet_points))} {x_col}s by {y_col}:\n\n" + "\n".join(bullet_points)
    return encoded, summary

