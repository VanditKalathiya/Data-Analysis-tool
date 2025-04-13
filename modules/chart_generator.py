import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64

def render_chart(df: pd.DataFrame, chart_type: str, cols: list):
    fig, ax = plt.subplots()

    if chart_type == "hist" and cols:
        sns.histplot(df[cols[0]].dropna(), ax=ax, kde=True)
        ax.set_title(f"Distribution of {cols[0]}")
    
    elif chart_type == "scatter" and len(cols) == 2:
        sns.scatterplot(x=df[cols[0]], y=df[cols[1]], ax=ax)
        ax.set_title(f"{cols[1]} vs {cols[0]}")
    
    elif chart_type == "heatmap":
        corr = df.select_dtypes(include='number').corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap")
    
    else:
        return None

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    return encoded
