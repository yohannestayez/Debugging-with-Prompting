import re

def extract_line_number(error_message: str) -> int:
    """
    Extract the line number from an error message.
    """
    match = re.search(r'line (\d+)', error_message)
    if match:
        return int(match.group(1))
    return -1

def simulated_test(original_code: str, fixed_code: str, error_message: str) -> bool:
    """
    Simulate testing the fixed code by checking if the problematic line or the entire code has changed.

    This function performs a simple static check to determine if the fixed code differs from the original,
    with a preference for checking the specific line indicated by the error message if available.
    """
    # Attempt to extract the line number from the error message
    line_number = extract_line_number(error_message)
    if line_number != -1:
        # Split the code into lines for comparison
        original_lines = original_code.splitlines()
        fixed_lines = fixed_code.splitlines()
        # Check if the line number is valid and compare the specific line
        if line_number <= len(original_lines) and line_number <= len(fixed_lines):
            return original_lines[line_number - 1] != fixed_lines[line_number - 1]
    
    # Fallback: check if the entire code has changed
    return original_code != fixed_code