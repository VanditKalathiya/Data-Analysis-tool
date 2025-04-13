from lida import Manager
from lida.datamodel import Goal
import altair as alt

# Initialize LIDA with LLM disabled
lida_manager = Manager()
lida_manager.llm_engine = None 

def generate_lida_charts(df, user_prompt: str):
    dataset_id = "user_data"
    lida_manager.add_data(name=dataset_id, data=df)

    try:
        goals = lida_manager.goals(name=dataset_id, user_input=user_prompt)

        if not goals:
            return None, "⚠️ LIDA couldn't generate a visualization goal."

        chart_code = lida_manager.visualize(name=dataset_id, goal=goals[0])

        if chart_code and "chart_spec" in chart_code:
            chart = alt.Chart.from_dict(chart_code["chart_spec"])
            summary = goals[0].description or "Auto-generated chart."
            return chart, summary
        else:
            return None, "⚠️ LIDA couldn't generate a chart spec."

    except Exception as e:
        return None, f"❌ LIDA error: {e}"
