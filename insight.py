import streamlit as st
from llm import query_gemini

@st.cache_data(show_spinner=False)
def generate_insights(df_snippet: str, question: str) -> str:
    """
    Takes a string representation of the generated dataframe and the user's question,
    and asks the LLM to write a concise, human-readable summary or insight.
    """
    prompt = f"""
    You are a professional Data Analyst AI. 
    The user asked: "{question}"
    
    The database correctly executed the query and returned this EXACT data snapshot:
    {df_snippet}
    
    Provide 3-4 professional insights directly interpreting this specific dataset snippet. 
    You MUST adhere to these strict accuracy rules:
    1. NEVER hallucinate numbers or categories not present in the {df_snippet}.
    2. If the snippet is small (e.g. 1 row), just summarize that exact metric.
    3. Mentally verify your calculations before outputting them.
    4. Highlight the highest value, lowest value, average, or most common category ONLY if that data is explicitly visible in the snippet.

    Strictly follow these formatting rules:
    - Use Markdown bullet points (`* `).
    - Bold key metrics or column names for readability (e.g., **$50,000**, **Model X**).
    - Maintain a highly concise, professional tone.
    """
    
    return query_gemini(prompt)
