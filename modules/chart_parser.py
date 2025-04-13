import re

def detect_chart_command(prompt: str):
    prompt = prompt.lower()
    
    # Chart types supported
    if "distribution" in prompt or "hist" in prompt:
        return "hist", extract_column(prompt)
    elif "scatter" in prompt or "vs" in prompt:
        return "scatter", extract_columns(prompt)
    elif "correlation" in prompt or "heatmap" in prompt:
        return "heatmap", []
    
    return None, []

def extract_column(text: str):
    match = re.search(r"plot\s+(\w+)", text)
    return [match.group(1)] if match else []

def extract_columns(text: str):
    match = re.search(r"(\w+)\s+vs\s+(\w+)", text)
    return [match.group(1), match.group(2)] if match else []
