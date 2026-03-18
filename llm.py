import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load local environment configuration
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def query_gemini(prompt: str, model_name="gemini-2.5-flash") -> str:
    """Core function to bounce a given raw prompt off the Gemini engine."""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: LLM Engine connectivity failed: {str(e)}"

def extract_code_block(llm_response: str) -> str:
    """Helper method to isolate the python code snippet from Gemini's markdown."""
    if "```python" in llm_response:
        return llm_response.split("```python")[1].split("```")[0].strip()
    elif "```" in llm_response:
        return llm_response.split("```")[1].split("```")[0].strip()
    return llm_response.strip()

def simulate_and_tune_code(code: str, question: str, columns: list) -> str:
    """Takes the generated code and explicitly asks the LLM to mentally simulate
    running it to find edge cases, logic flaws, or NaN issues, then return the tuned code."""
    prompt = f"""
You are an elite QA Data Engineer. Your job is to mentally execute the following Pandas code against a dataset with this schema: {columns}
The user originally asked: "{question}"

Initial Code:
```python
{code}
```

Please perform a tuning simulation by thinking step-by-step inside `<thought> ... </thought>` tags:
1. Ensure string filtering is case-insensitive (e.g., use `.str.contains(..., case=False, na=False)` if filtering strings).
2. Check if the aggregation accurately answers the user's question without hallucinating columns.
3. Ensure the final result is assigned to exactly one variable named `result`.
4. Ensure `.reset_index()` is used where appropriate so `result` is a flat dataframe.

Output your thoughts first, then ONLY the tuned and corrected python code block:
<thought>
your QA reasoning here
</thought>
```python
# your tuned code here
```
"""
    raw_response = query_gemini(prompt)
    if "```python" in raw_response or "```" in raw_response:
        return extract_code_block(raw_response)
    # If LLM didn't format correctly, return original code as fallback
    return code

def build_data_prompt(question, columns, prompt_template_path, previous_context="None"):
    """Reads the template text and injects real schema variables context."""
    with open(prompt_template_path, 'r') as file:
        template = file.read()
    
    return template.format(
        columns=", ".join(columns), 
        question=question,
        previous_context=previous_context
    )
