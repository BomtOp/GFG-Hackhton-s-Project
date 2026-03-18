import pandas as pd
from llm import query_gemini, extract_code_block, build_data_prompt, simulate_and_tune_code
from validator import validate_code
from repair import repair_query

def load_dataset(file_path="data/BMW Vehicle Inventory.csv"):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        return None

def execute_pandas_safe(df: pd.DataFrame, code: str) -> tuple:
    """Executes the pandas logic. Returns (Result, ErrorStr)"""
    local_vars = {'df': df, 'pd': pd}
    try:
        exec(code, {}, local_vars)
        if 'result' in local_vars:
            result = local_vars['result']
            if isinstance(result, str) and result.startswith("Error:"):
                return None, result
            if isinstance(result, pd.Series):
                result = result.to_frame()
            elif not isinstance(result, pd.DataFrame):
                result = pd.DataFrame({"Metric": [result]})
                
            if isinstance(result, pd.DataFrame) and result.empty:
                return None, "Error: The applied filters resulted in an empty dataframe."
                
            return result, None
        else:
            return None, "System Error: The LLM failed to assign a 'result' variable."
    except Exception as e:
        return None, str(e)


import streamlit as st

@st.cache_data(show_spinner=False)
def run_query_pipeline(df: pd.DataFrame, question: str, previous_context="None", max_retries=1):
    """
    Orchestrates the LLM -> Validator -> Execution -> Repair workflow.
    """
    columns = list(df.columns)
    
    # 1. Generate core logic (Now includes Simulation/Tuning in one pass)
    prompt = build_data_prompt(question, columns, "prompts/sql_prompt.txt", previous_context)
    raw_response = query_gemini(prompt)
    
    if "Error: Invalid Schema Requested" in raw_response:
        return None, "Error: You requested data that is not in the schema. Please check the dataset columns."
        
    code = extract_code_block(raw_response)
    
    # (Removed secondary simulation call to halve latency)
    
    # 2. Syntax/Security Validation
    is_valid, val_msg = validate_code(code, columns)
    if not is_valid:
        return None, val_msg
        
    # 3. Execution
    result, err = execute_pandas_safe(df, code)
    
    # 4. Self-Healing Loop
    retries = 0
    while err and retries < max_retries:
        print(f"Error caught: {err}. Attempting repair {retries + 1}/{max_retries}...")
        code = repair_query(code, err, columns)
        
        # Re-validate
        is_valid, val_msg = validate_code(code, columns)
        if not is_valid:
            return None, f"Repair triggered security validation failure: {val_msg}"
            
        # Re-execute
        result, err = execute_pandas_safe(df, code)
        retries += 1
        
    if err:
        return None, f"Query failed after {max_retries} automatic repair attempts.\nFinal Error: {err}"
        
    return result, code
