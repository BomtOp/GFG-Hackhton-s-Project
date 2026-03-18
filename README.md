# Conversational AI for Instant Business Intelligence Dashboards 📊 *(V2 Pro Edition)*

## 💡 Problem
Non-technical users struggle to extract actionable insights from raw data. Traditional BI tools are complex, require SQL/Pandas programming knowledge, and are prone to creating hallucinatory or inaccurate results when paired with basic LLMs.

## 🚀 Solution
This web application bridges the accessibility gap by allowing users to instantly generate fully interactive BI dashboards using colloquial, plain English queries.

What sets **V2** apart is the robust **200% Accuracy Engine**. We utilize a multi-agent pipeline strategy:
- Schema rules are strictly injected.
- Generated code passes an Abstract Syntax Tree (AST) Security Validator.
- Errors trigger an advanced AI Self-Healing Loop.
- Context is held in memory for fluent Follow-Up queries.
- Actionable Textual Insights summarize data seamlessly.

## 🏗️ Architecture Pipeline
1. **Prompt Processor & Schema Injection**: User queries are bound to explicit Dataset schemas before hitting Gemini.
2. **LLM Query Generator**: Translates NLP into execution-ready Python logic.
3. **AST Query Validator**: Syntax scanning logic blocks hallucinated columns and unauthorized system modules (`os`, `exec`).
4. **Pandas Safe Execution**: Computes the dataframe cleanly.
5. **Self-Healing Loop Engine**: Catches `KeyError` or logic faults, passing the stack trace back to Gemini to rewrite the script over a retry threshold.
6. **Chart Selector AI**: Matches datatypes to optimal visual representations (e.g. `%` to Pie, `Time` to Line, `Category` to Bar).
7. **Insight Generator AI**: Parses the resulting slice of data, formulating 3 fast, bulleted human-readable interpretations.
8. **Dashboard Builder**: Streamlit beautifully stitches data, interactive Plotly charts, AI summaries, and the extraction logs neatly.

## ✨ Features
- **Dynamic CSV Upload**: Instantly detects and binds to a newly generated schema.
- **Follow Up Memory**: Filter down existing queries simply by typing context like "Now only show Diesel". 
- **100% Hallucination Free**: Strict data typing ensures you never get fake visualization coordinates.
- **Auto Chart Matching**: Visualizations intelligently represent the dimensional bounds.
- **Textual Insights**: Real-time analyst-level bullet points interpreting the rendered data.
- **Code Transparency Viewer**: UI features an expander component proving exact computations.

## 🚀 Run on GitHub (Streamlit Cloud)

You can run this dashboard live on the web for free!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)

1. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **"New app"**.
3. Select this GitHub repository: `BomtOp/GFG-Hackhton-s-Project`.
4. Set the Main file path to: `app.py`.
5. **IMPORTANT:** Go to **Advanced settings...** -> **Secrets** and paste your `GEMINI_API_KEY`:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
6. Click **Deploy!** 💥

## 🛠️ How to run locally
... (rest of the file)

1. **Clone & Set up Environment**
```bash
cd Conversational-BI-Dashboard-V2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure API Keys**
Create a `.env` file in the directory:
```ini
GEMINI_API_KEY=AIzaSy...
```

3. **Start the Engine**
```bash
streamlit run app.py
```

## 📸 Demo Queries to Copy & Paste
- "Show average price by model"
- "Show price trend by year"
- "Show count by fuelType"
- "Show mileage vs price"
- "Show cars after 2015 by transmission"
- "Show top 5 expensive models"
- *"Now show only automatic transmission"* (Try this as a follow-up!)
