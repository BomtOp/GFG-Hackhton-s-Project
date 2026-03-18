import plotly.express as px
import pandas as pd

def select_chart_type(df: pd.DataFrame, query: str) -> str:
    """
    Smart rule-based chart detection.
    Rules:
    time -> line chart
    category -> bar chart
    numeric vs numeric -> scatter
    percentage -> pie
    ranking -> bar
    grouped -> bar
    single value -> metric
    """
    
    # 1. Check shape
    if df.shape == (1, 1):
        return 'metric'
        
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(exclude='number').columns.tolist()
    
    q = query.lower()
    
    # 2. Heuristics based on natural language query keywords
    if any(word in q for word in ['percentage', 'share', 'ratio', 'pie', 'proportion']):
        if len(cat_cols) > 0 and len(num_cols) > 0:
            return 'pie'
            
    if any(word in q for word in ['time', 'trend', 'year', 'month', 'history', 'daily']):
        if 'year' in df.columns or 'date' in df.columns or 'month' in df.columns:
            return 'line'
            
    if any(word in q for word in ['vs', 'versus', 'scatter', 'correlation', 'relation']):
        if len(num_cols) >= 2:
            return 'scatter'
            
    if any(word in q for word in ['top', 'bottom', 'ranking', 'highest', 'lowest', 'best', 'worst']):
        if len(cat_cols) > 0 and len(num_cols) > 0:
            return 'bar'
        
    if any(word in q for word in ['distribution', 'frequency', 'histogram', 'spread']):
        if len(num_cols) > 0:
            return 'histogram'
            
    if any(word in q for word in ['box', 'outliers', 'quartiles']):
        if len(cat_cols) > 0 and len(num_cols) > 0:
            return 'box'
        
    # Default fallbacks based on column types if query keywords miss
    if len(cat_cols) == 1 and len(num_cols) == 1:
        # Category vs Numeric -> Bar (most standard)
        return 'bar'
        
    if len(num_cols) == 2 and len(cat_cols) == 0:
        return 'scatter'
        
    if len(num_cols) == 1 and len(cat_cols) == 0:
        return 'histogram'

    if 'year' in map(str.lower, df.columns):
         return 'line'
        
    # Generic catch-all
    return 'bar'

def generate_figure(df: pd.DataFrame, query: str):
    """Takes a dataframe and user request, returns a Plotly figure."""
    if df is None or df.empty:
        return None, "Error: Empty dataframe cannot be charted."
        
    chart_type = select_chart_type(df, query)
    
    if chart_type == 'metric':
        return None, 'metric'
        
    columns = list(df.columns)
    
    try:
        # We attempt to auto-map axes. Usually: index/first col = x, second col = y
        x_col = columns[0]
        y_col = columns[1] if len(columns) > 1 else columns[0]
        
        if chart_type == 'line':
            fig = px.line(df, x=x_col, y=y_col, title=f"Trend of {y_col} by {x_col}", markers=True, text=y_col)
            fig.update_traces(textposition="top center", line=dict(width=5, color="#d11141"), marker=dict(size=14, line=dict(width=3, color="black")))
            
        elif chart_type == 'pie':
            fig = px.pie(df, names=x_col, values=y_col, title=f"Distribution of {y_col} by {x_col}")
            fig.update_traces(textinfo="label+percent+value", textfont_size=16, marker=dict(line=dict(color='#000000', width=4)))
            
        elif chart_type == 'scatter':
            # Scatter usually works best when both are numbers.
            num_cols = df.select_dtypes(include='number').columns.tolist()
            if len(num_cols) >= 2:
                fig = px.scatter(df, x=num_cols[0], y=num_cols[1], title=f"{num_cols[1]} vs {num_cols[0]}", text=num_cols[1])
            else:
                fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}", text=y_col)
            fig.update_traces(textposition="top center", marker=dict(size=16, color="#00aedb", line=dict(width=3, color="black")))
                
        elif chart_type == 'histogram':
            # Histogram prefers a single numeric column
            num_cols = df.select_dtypes(include='number').columns.tolist()
            if len(num_cols) > 0:
                fig = px.histogram(df, x=num_cols[0], title=f"Distribution of {num_cols[0]}", text_auto=True)
            else:
                fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}", text_auto=True)
            fig.update_traces(marker=dict(color="#00b159", line=dict(width=4, color="#000000")))
                
        elif chart_type == 'box':
            # Box plot works well with categorical x and numeric y
            num_cols = df.select_dtypes(include='number').columns.tolist()
            cat_cols = df.select_dtypes(exclude='number').columns.tolist()
            if len(cat_cols) > 0 and len(num_cols) > 0:
                fig = px.box(df, x=cat_cols[0], y=num_cols[0], title=f"Spread of {num_cols[0]} by {cat_cols[0]}")
            else:
                fig = px.box(df, y=y_col, title=f"Box Plot of {y_col}")
            fig.update_traces(marker=dict(color="#ffb100", line=dict(width=3, color="#000000")))
                
        else: # Bar graph is the safest general assumption
            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}", text=y_col)
            fig.update_traces(textposition='outside', marker=dict(color="#ffde59", line=dict(width=4, color="#000000")))
            
        # Global Comic Style Layout Parameters
        fig.update_layout(
            template="plotly_white", 
            margin=dict(l=20, r=20, t=60, b=20),
            font=dict(family="Comic Neue, Comic Sans MS, Courier New, monospace", size=16, color="#000000"),
            title_font=dict(family="Bangers, Comic Neue, cursive", size=26, color="#d11141"),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis=dict(showgrid=False, zeroline=True, zerolinewidth=4, zerolinecolor='black', tickfont=dict(color='black', size=14)),
            yaxis=dict(showgrid=True, gridwidth=2, gridcolor='rgba(0,0,0,0.1)', zeroline=True, zerolinewidth=4, zerolinecolor='black', tickfont=dict(color='black', size=14)),
        )
        return fig, chart_type
        
    except Exception as e:
        return None, f"Error rendering chart: {str(e)}"
