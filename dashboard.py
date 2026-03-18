import streamlit as st

def render_header():
    st.set_page_config(page_title="AI BI Dashboard V2", layout="wide", page_icon="💥")
    st.markdown("""
        <style>
            /* Comic Text Font Imports */
            @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@400;700&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Comic Neue', cursive, sans-serif !important;
                color: #000000 !important; /* Force black text for contrast */
            }
            
            h1, h2, h3, h4, .stCodeBlock {
                font-family: 'Bangers', 'Comic Neue', cursive !important;
                letter-spacing: 2px !important;
                color: #d11141 !important; /* Comic Red for Headers */
                text-shadow: 2px 2px 0px #000 !important; /* Heavy drop shadow on titles */
            }
            
            /* Comic Book Panel Container Styling (Halftone effect) */
            .stApp {
                background-color: #fdf5e6;
                background-image: radial-gradient(#000000 1px, transparent 1px);
                background-size: 20px 20px;
                background-attachment: fixed;
            }
            
            /* Inputs and Buttons styling */
            .stButton>button {
                border: 4px solid #000000 !important;
                border-radius: 12px !important;
                box-shadow: 6px 6px 0px #000000 !important;
                transition: all 0.15s ease-in-out !important;
                background-color: #ffde59 !important; /* Comic Yellow */
                color: #000 !important;
                font-family: 'Bangers', cursive !important;
                font-size: 24px !important;
                letter-spacing: 1px !important;
                text-transform: uppercase !important;
            }
            .stButton>button:hover {
                background-color: #ffb100 !important; /* Darker Yellow on hover */
            }
            .stButton>button:active {
                box-shadow: 0px 0px 0px #000000 !important;
                transform: translateY(6px) translateX(6px) !important;
            }
            
            /* Metric and Upload Container Panels */
            [data-testid="stMetric"], .stExpander, div[data-testid="stFileUploader"] {
                border: 4px solid #000 !important;
                border-radius: 4px !important; /* Square-ish comic panels */
                box-shadow: 8px 8px 0px #000 !important;
                background-color: #ffffff !important;
                padding: 15px !important;
                margin-bottom: 15px !important;
                position: relative;
            }
            
            /* Dataframe styling - needs less padding to prevent internal overlap */
            [data-testid="stDataFrame"] {
                border: 4px solid #000 !important;
                border-radius: 4px !important; 
                box-shadow: 8px 8px 0px #000 !important;
                background-color: #ffffff !important;
                margin-bottom: 15px !important;
                position: relative;
                padding: 4px !important; /* minimal padding so the canvas fits */
            }
            
            /* Adding a comic 'tape' corner to the expander */
            .stExpander::before {
                content: '';
                position: absolute;
                top: -10px;
                left: -10px;
                width: 40px;
                height: 20px;
                background: rgba(255,255,255,0.8);
                border: 2px solid #000;
                transform: rotate(-15deg);
                z-index: 99;
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                border-right: 6px solid #000 !important;
                background-color: #00b159 !important; /* Comic Green backdrop */
            }
            
            /* Make sidebar text visible against green */
            [data-testid="stSidebar"] .css-17lntkn, [data-testid="stSidebar"] p {
                color: #ffffff !important;
                font-weight: bold !important;
                text-shadow: 1px 1px 0px #000 !important;
            }
            
            /* Form inputs */
            .stTextInput>div>div>input {
                border: 4px solid #000 !important;
                border-radius: 0px !important;
                box-shadow: 5px 5px 0px #ffde59 !important; /* Yellow shadow */
                font-size: 20px !important;
                padding: 10px !important;
                color: #000 !important;
                background-color: #fff !important;
            }
            
            /* Metric text visibility */
            [data-testid="stMetricValue"] {
                color: #00aedb !important; /* Comic Blue for metrics */
                font-family: 'Bangers', cursive !important;
                text-shadow: 2px 2px 0px #000 !important;
                font-size: 2.2rem !important;
                word-wrap: break-word !important;
                overflow-wrap: break-word !important;
                white-space: normal !important;
                line-height: 1.1 !important;
            }
            [data-testid="stMetricLabel"] *, [data-testid="stMetricLabel"] p {
                color: #000000 !important;
                font-weight: 900 !important;
                font-size: 1.3rem !important;
                word-wrap: break-word !important;
                white-space: normal !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.title("💥 POW! AI BI Dashboard 🚀")
    st.markdown("### 🦸‍♂️ **Validation! Self-Healing! Dynamic Schemas!**")

def render_error(msg):
    st.error(f"☠️ **KABOOM!** System Error: {msg}")

def render_metrics_row(df):
    """If the resulting dataframe is just a single cell metric, render it nicely."""
    val = df.iloc[0, 0]
    col_name = df.columns[0] if len(df.columns) > 0 else "Metric"
    st.metric(label=f"🎯 {col_name.capitalize()}", value=str(val))

def render_charts_and_data(df, fig, code, insights, question):
    st.markdown("---")
    st.subheader(f"✨ Results for: *{question}*")
    
    # NEW KPI CARDS LOGIC
    if not df.empty and len(df.columns) > 0:
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            target_col = numeric_cols[0] # Pick the first numeric col for KPIs
            
            st.subheader(f"⚡ Key Performance Indicators (based on `{target_col}`)")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            
            with kpi1:
                st.metric(label="Average", value=f"{df[target_col].mean():.2f}")
            with kpi2:
                st.metric(label="Maximum", value=f"{df[target_col].max():.2f}")
            with kpi3:
                st.metric(label="Minimum", value=f"{df[target_col].min():.2f}")
            with kpi4:
                st.metric(label="Total Count", value=f"{df[target_col].count():,}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
    # ROW 1: Chart and Data Table Grid
    col_chart, col_data = st.columns([1.5, 1])
    
    with col_chart:
        st.markdown("### 🎨 Visuals (BAM!)")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            # Add HTML export for interactive chart
            chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
            st.download_button(
                label="📊 Download Chart (HTML)",
                data=chart_html,
                file_name="interactive_chart.html",
                mime="text/html",
                key=f"dl_html_{question}"
            )
        else:
            if df.shape == (1, 1):
                # We rendered a standalone metric earlier, but keep it minimal here
                st.info("Standalone metric result displayed. No multidimensional chart available.")
            else:
                st.info("No chart generated for this data shape.")
                
    with col_data:
        st.markdown("### 📑 Data Panel")
        if not (fig is None and df.shape == (1, 1)):
             st.dataframe(df, use_container_width=True, height=400)
             csv = df.to_csv(index=False).encode('utf-8')
             st.download_button(
                 label="💾 Grab the Data (CSV)",
                 data=csv,
                 file_name="query_results.csv",
                 mime="text/csv",
                 key=f"dl_csv_{question}",
                 use_container_width=True
             )
    
    # ROW 2: Insights and Code
    st.markdown("---")
    col_insight, col_code = st.columns([2, 1])
    
    with col_insight:
        st.write("### 💭 AI Thought Bubble (Insights)")
        if insights:
            st.success(insights)
        else:
            st.write("No insights generated for this view.")
            
    with col_code:
        st.write("### 💻 Debug Log")
        with st.expander("Show Generated Python Logic", expanded=False):
            st.code(code, language="python")

def render_demo_buttons():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ✨ Demo Queries")
    demos = [
        "Show average price by model",
        "Show price trend by year",
        "Show count by fuelType",
        "Show mileage vs price",
        "Show cars after 2015 by transmission",
        "Show top 5 expensive models"
    ]
    for q in demos:
        if st.sidebar.button(q):
            st.session_state.demo_query = q
            st.session_state.run_query = True
