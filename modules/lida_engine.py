from lida import Manager
import altair as alt
import pandas as pd

lida_manager = Manager()

def generate_lida_charts(df: pd.DataFrame, user_prompt: str):
    dataset_id = "user_data"
    lida_manager.add_data(name=dataset_id, data=df)

    try:
        charts = lida_manager.suggest_visualizations(
            name=dataset_id,
            user_input=user_prompt,
            num_results=1
        )

        if charts:
            spec = charts[0].get("chart_spec")
            summary = charts[0].get("summary", "No summary provided.")
            chart = alt.Chart.from_dict(spec)
            return chart, summary
        else:
            return None, "⚠️ LIDA couldn't generate a chart for this prompt."
    except Exception as e:
        return None, f"❌ LIDA error: {e}"
