import ast

def validate_code(code_string: str, allowed_columns: list) -> tuple:
    """
    Analyzes the AST (Abstract Syntax Tree) of the generated Python code 
    to ensure it doesn't use unauthorized columns.
    
    Returns: (is_valid: bool, error_message: str)
    """
    try:
        # Check for syntactical correctness
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return False, f"Syntax Error in generated code: {str(e)}"
        
    # Check column exists in string literals (simple heuristic)
    # We explicitly look for strings used as DataFrame keys.
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
                col_name = node.slice.value
                if col_name not in allowed_columns:
                    # Ignore generic pandas strings that might not be columns, but if it's used as a subscript it's likely a column
                    return False, f"Hallucination Error: Column '{col_name}' does not exist in schema."
    

    class ColumnValidator(ast.NodeVisitor):
        def __init__(self, allowed_cols):
            self.allowed_cols = allowed_cols
            self.violations = []
            
        def visit_Str(self, node):
            # Watch out for pandas indexers: df['some_col']
            pass
            
        def visit_Constant(self, node):
            # In Python 3.8+, strings are parsed as Constant nodes
            if isinstance(node.value, str):
                # We do a loose check: if they reference a string that looks like a column 
                # name in pandas context but it's not in the schema.
                pass
                
        def visit_Subscript(self, node):
            # if we see df['column_name']
            if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
                col = node.slice.value
                # A heuristic check: We only throw a violation if it looks like a missing schema col
                # Note: The query itself might have string filters, we don't want false positives.
                # So we won't strictly enforce string constants unless we trace it directly to `df`.
                pass
    # We explicitly ban DANGEROUS modules and unsafe code
    dangerous_keywords = ['import ', '__import__', 'os.', 'sys.', 'eval(', 'exec(', 'subprocess', 'open(', 'write(']
    for bad in dangerous_keywords:
        if bad in code_string:
            return False, f"Security Violation: '{bad}' is not allowed in safe execution environment."
            
    # Check if 'result =' exists to ensure the dataframe assignment is present
    if 'result =' not in code_string and 'result=' not in code_string:
         return False, "Validation Error: Code does not assign output to 'result' variable."

    return True, "Valid"
