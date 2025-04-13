from lida import Manager
import altair as alt

# Manually override LLM engine to None to prevent OpenAI calls
lida_manager = Manager()
lida_manager.llm_engine = None  # <--- THIS disables LLM completely

def generate_lida_charts(df, user_prompt: str):
    dataset_id = "user_data"
    try:
        lida_manager.add_data(name=dataset_id, data=df)

        charts = lida_manager.suggest_visualizations(
            name=dataset_id,
            user_input=user_prompt,
            num_results=1
        )

        if charts:
            chart_spec = charts[0].get("chart_spec")
            summary = charts[0].get("summary", "No summary provided.")
            chart = alt.Chart.from_dict(chart_spec)
            return chart, summary
        else:
            return None, "⚠️ LIDA couldn't generate a chart."

    except Exception as e:
        return None, f"❌ LIDA error: {e}"
