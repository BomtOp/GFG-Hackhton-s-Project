import streamlit as st
import pandas as pd
from query_engine import run_query_pipeline
from chart_selector import generate_figure
from dashboard import render_header, render_error, render_charts_and_data, render_demo_buttons
from insight import generate_insights

# 1. Page Header & Session State Init
render_header()

if 'history' not in st.session_state:
    st.session_state.history = []
if 'demo_query' not in st.session_state:
    st.session_state.demo_query = ""
if 'run_query' not in st.session_state:
    st.session_state.run_query = False
if 'last_code' not in st.session_state:
    st.session_state.last_code = "None"

# 2. Sidebar Data Upload and Setup
st.sidebar.markdown("## 📚 Data Comic Book")
uploaded_file = st.sidebar.file_uploader("Upload CSV Data 🦇", type=["csv"])

@st.cache_data
def load_data(file):
    if file is not None:
        try:
            return pd.read_csv(file)
        except Exception as e:
            st.sidebar.error(f"Upload error: {e}")
            return None
    else:
        try:
            return pd.read_csv("data/BMW Vehicle Inventory.csv")
        except Exception:
            return None

df = load_data(uploaded_file)
render_demo_buttons()

if df is not None and not df.empty:
    with st.expander("🔍 Peeking into the Dataset...", expanded=False):
        st.markdown(f"**Dataset Shape:** `{df.shape[0]:,} Rows` × `{df.shape[1]} Columns`")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Column Types:**")
            dtypes = df.dtypes.value_counts().reset_index()
            dtypes.columns = ['Type', 'Count']
            st.dataframe(dtypes, use_container_width=True, hide_index=True)
        with c2:
            st.markdown("**Missing Values:**")
            missing = df.isnull().sum().reset_index()
            missing.columns = ['Column', 'Missing']
            missing = missing[missing['Missing'] > 0]
            if missing.empty:
                st.success("No missing values detected.")
            else:
                st.dataframe(missing, use_container_width=True, hide_index=True)
        
        st.markdown("**Data Preview:**")
        st.dataframe(df.head(3), use_container_width=True)
            
        st.caption(f"Detected Super-Powers (Columns): {', '.join(df.columns)}")

    # 3. Query Input System
    st.markdown("### 🗯️ What's the mission? (Enter Prompt)")
    
    # Pre-fill with demo query if clicked
    default_q = st.session_state.demo_query if st.session_state.demo_query else ""
    
    colA, colB = st.columns([4, 1])
    with colA:
        question = st.text_input("e.g. 'Show average price by model'", value=default_q, key="query_input")
    with colB:
        st.write("")
        st.write("")
        generate_btn = st.button("Generate! 💥", use_container_width=True)
        
    # Clear session state so input doesn't get stuck on demo
    if st.session_state.demo_query and st.session_state.run_query:
        # Instead of clearing instantly which breaks render, use it as query.
        question = st.session_state.demo_query

    # 4. Engine Execution Pipeline
    if question and (generate_btn or st.session_state.run_query):
        # We hold the run_query active during processing to ensure UI components 
        # that depend on 'rendering state' function properly.
        current_query = question
        st.session_state.run_query = False # Reset flag 
        st.session_state.demo_query = ""   # Reset demo text
        with st.spinner("AI is analyzing prompt, mapping schema, and executing code..."):
            
            # Formulate full context including last query
            context = "None"
            if len(st.session_state.history) > 0:
                 last_q = st.session_state.history[-1]
                 context = f"Last User Query: {last_q}\nLast Code: {st.session_state.last_code}"
            
            result_df, code_or_err = run_query_pipeline(df, question, previous_context=context, max_retries=2)
            
            if result_df is None:
                render_error(code_or_err)
            else:
                # 5. Chart Selection & Render
                st.session_state.last_code = code_or_err # Save valid code for follow-ups
                st.session_state.history.append(question)
                
                chart_fig, chart_type = generate_figure(result_df, question)
                
                # 6. Insight Generation
                snippet = result_df.head(10).to_string()
                insights = generate_insights(snippet, question)
                
                render_charts_and_data(result_df, chart_fig, code_or_err, insights, question)
                
    # 7. Rendering Follow-Up Memory Log
    if st.session_state.history:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🕒 Query History")
        for i, q in enumerate(reversed(st.session_state.history[-5:])):
            if st.sidebar.button(f"💭 {q}", key=f"hist_{i}"):
                st.session_state.demo_query = q
                st.session_state.run_query = True
                st.rerun()
else:
    render_error("Fatal: No Data available. Core systems offline. Please upload a CSV.")
