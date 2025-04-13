import streamlit as st
import pandas as pd
import time
import re
import base64
from modules.file_loader import load_file
from modules.dataset_profiler import profile_dataset
from modules.analyzer import get_summary_stats, get_missing_values, get_top_categoricals
from modules.visualizer import plot_distribution, plot_correlation_heatmap, plot_scatter
from modules.groq_chat import chat_with_groq
from modules.chart_parser import detect_chart_command, detect_bar_chart_intent
from modules.chart_generator import render_chart, render_bar_chart

st.set_page_config(page_title="AI Data Assistant", layout="centered")
st.title("💬 AI Data Assistant")

# 🧼 Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.df = None
    st.session_state.profile = None
    st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None
if "profile" not in st.session_state:
    st.session_state.profile = None

# 📁 File uploader
uploaded_file = st.file_uploader("📁 Upload CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    try:
        df = load_file(uploaded_file)
        st.session_state.df = df
        st.session_state.profile = profile_dataset(df)
        st.success(f"✅ Uploaded: {df.shape[0]} rows × {df.shape[1]} columns.")
    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")

# 💬 Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 💬 Chat input
if prompt := st.chat_input("Ask your data assistant..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build chat context
    chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    if st.session_state.df is not None:
        df = st.session_state.df
        profile = st.session_state.profile
        data_info = f"""
You are helping the user analyze a dataset with {df.shape[0]} rows and {df.shape[1]} columns.
Numeric columns: {profile['num_cols']}
Categorical columns: {profile['cat_cols']}
Datetime columns: {profile['datetime_cols']}
Suggested target columns: {profile['suggested_targets']}
"""
        chat_history.insert(0, {"role": "system", "content": "You are a helpful AI data analyst."})
        chat_history.insert(1, {"role": "system", "content": data_info})
    else:
        chat_history.insert(0, {"role": "system", "content": "You are a helpful AI data analyst. Ask the user to upload a dataset."})

    # 🧠 Get Groq response
    reply = ""
    try:
        reply = chat_with_groq(chat_history)

        # Typing effect: line by line
        with st.chat_message("assistant"):
            response_box = st.empty()
            full_response = ""
            for sentence in re.split(r'(?<=[.!?]) +', reply):
                full_response += sentence + " "
                response_box.markdown(full_response.strip())
                time.sleep(0.25)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"❌ Failed to get response from Groq: {e}")

    # 📊 Visualizations via keywords
    if st.session_state.df is not None:
        lower_prompt = prompt.lower()
        df = st.session_state.df
        num_cols = df.select_dtypes(include='number').columns
        just_charts = "no code" in lower_prompt or "only charts" in lower_prompt or "just plot" in lower_prompt

        # Histogram
        for col in num_cols:
            if col.lower() in lower_prompt and "distribution" in lower_prompt:
                with st.chat_message("assistant"):
                    if df[col].dropna().nunique() > 1:
                        if not just_charts:
                            st.markdown(f"📊 Distribution of `{col}`:")
                        st.pyplot(plot_distribution(df, col))
                    else:
                        st.warning(f"Column `{col}` has insufficient variation to plot.")

        # Correlation heatmap
        if "correlation" in lower_prompt or "heatmap" in lower_prompt:
            with st.chat_message("assistant"):
                if not just_charts:
                    st.markdown("🔗 **Correlation Heatmap**")
                st.pyplot(plot_correlation_heatmap(df))

        # Scatterplot
        found_cols = [col for col in num_cols if col.lower() in lower_prompt]
        if len(found_cols) >= 2 and "vs" in lower_prompt:
            x_col, y_col = found_cols[:2]
            with st.chat_message("assistant"):
                if not just_charts:
                    st.markdown(f"📈 Scatterplot: `{y_col}` vs `{x_col}`")
                st.pyplot(plot_scatter(df, x_col, y_col))

        # 🧠 Bar chart via NLP detection
        chart_type, cols = detect_bar_chart_intent(prompt)
        if chart_type == "bar" and len(cols) == 2:
            x_col, y_col = cols
            with st.chat_message("assistant"):
                st.markdown(f"📊 Bar chart of `{y_col}` by `{x_col}`...")
                encoded_img, summary = render_bar_chart(df, x_col, y_col)
                if encoded_img:
                    st.markdown(f"![Bar Chart](data:image/png;base64,{encoded_img})")
                    st.markdown(summary)
                else:
                    st.warning(summary)

    # 🧠 EDA triggers
    if any(word in prompt.lower() for word in ["summary", "eda", "describe", "null", "missing"]):
        if st.session_state.df is not None:
            with st.chat_message("assistant"):
                st.markdown("📊 **Summary Statistics**")
                st.dataframe(get_summary_stats(st.session_state.df))

                st.markdown("🧼 **Missing Values**")
                st.dataframe(get_missing_values(st.session_state.df))

                st.markdown("🔤 **Top Categorical Values**")
                st.dataframe(get_top_categoricals(st.session_state.df))
