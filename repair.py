from llm import query_gemini, extract_code_block

def repair_query(broken_code: str, error_traceback: str, columns: list) -> str:
    """
    Takes failing pandas code and its respective error trace, 
    bounces it off Gemini to self-heal the query.
    """
    
    repair_prompt = f"""
    You are an expert Data Engineer AI. The previous Pandas code generated threw an error.
    
    ### SCHEMA COLUMNS: {", ".join(columns)}
    
    ### BROKEN CODE:
    ```python
    {broken_code}
    ```
    
    ### ERROR MESSAGE:
    {error_traceback}
    
    ### RULES FOR REPAIR:
    1. Output ONLY the fixed valid Python code between ```python and ```.
    2. Do NOT hallucinate columns. If the error says KeyError or Hallucination Error, fix the spelling to match the exact schema columns provided above. NEVER guess columns.
    3. Make sure the output variable is named `result` and it returns a pandas DataFrame.
    4. If the query is impossible with the given schema, or completely irrelevant, return exactly: `result = "Error: Cannot repair."`
    """
    
    print("Initiating self-healing protocol...")
    response_text = query_gemini(repair_prompt)
    fixed_code = extract_code_block(response_text)
    return fixed_code
