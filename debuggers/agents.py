import autogen
import json
import re

class Instructor(autogen.AssistantAgent):
    # Uses instruction and role prompting to set the debugging context based on the code and error message.

    def __init__(self, llm_config):
        system_message = """You are an expert software engineer. Analyze the provided code and error to set the debugging context."""
        super().__init__(name="Instructor", llm_config=llm_config, system_message=system_message)

    def set_context(self, code: str, error: str) -> str:
        """Sets the debugging context based on the provided code and error message."""

        prompt = f"Code:\n{code}\nError: {error}\nSet the context for debugging this issue."
        response = self.generate_reply([{"content": prompt, "role": "user"}])
        return response



class Classifier(autogen.AssistantAgent):
    # Employs few-shot prompting with examples embedded in the system message to classify the error type and provide an explanation.

    def __init__(self, llm_config):
        system_message = """
                Identify and classify the type of error and provide an explanation based on the given error message. Use the following examples as a reference:

                Error: "IndentationError: expected an indented block"
                Response: {"error_type": "SyntaxError", "explanation": "This is a syntax error due to incorrect indentation."}

                Error: "IndexError: list index out of range"
                Response: {"error_type": "RuntimeError", "explanation": "This is a runtime error from accessing an invalid list index."}

                Error: "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
                Response: {"error_type": "TypeError", "explanation": "This occurs when an operation is performed on incompatible data types."}

                Error: "KeyError: 'name'"
                Response: {"error_type": "RuntimeError", "explanation": "This occurs when trying to access a non-existent key in a dictionary."}

                Use these examples as guidance and return a JSON object containing error_type and explanation in the same format.
         """
        super().__init__(name="Classifier", llm_config=llm_config, system_message=system_message)

    def classify_error(self, error_message: str) -> dict:
        """Classifies the error message into a type and provides an explanation."""

        prompt = f"Classify this error: {error_message}"
        print(error_message)
        response = str(self.generate_reply([{"content": prompt, "role": "user"}])['content'])
        try:
            classification = json.loads(response)
        except json.JSONDecodeError:
            classification = {"error_type": "Unknown", "explanation": "Failed to classify the error."}
        return classification



class Debugger(autogen.AssistantAgent):
    # Uses chain-of-thought prompting to generate a step-by-step explanation, 
    # incorporating self-consistency by generating two reasoning paths and synthesizing them.

    def __init__(self, llm_config):
        system_message = """Provide a step-by-step debugging explanation. Use detailed step by step reasoning. Optionally, generate multiple reasoning paths for self-consistency."""
        super().__init__(name="Debugger", llm_config=llm_config, system_message=system_message)

    def generate_reasoning(self, code: str, error: str) -> str:
        """Generates a detailed debugging explanation using multiple reasoning paths."""
        prompt1 = f"Code:\n{code}\nError: {error}\nExplain the debugging process step-by-step."
        reasoning1 = self.generate_reply([{"content": prompt1, "role": "user"}])['content']
        
        prompt2 = f"Code:\n{code}\nError: {error}\nProvide another perspective on debugging this issue."
        reasoning2 = self.generate_reply([{"content": prompt2, "role": "user"}])['content']
        
        final_prompt = f"Follow on these two reasoning paths:\n1. {reasoning1}\n2. {reasoning2}\nProvide a comprehensive debugging explanation."
        final_reasoning = self.generate_reply([{"content": final_prompt, "role": "user"}])['content']
        return final_reasoning

class Fixer(autogen.AssistantAgent):
    def __init__(self, llm_config):
        # Code Generation Technique: In the system message, we instruct the assistant to generate a corrected code snippet.

        system_message = (
            "Generate corrected code in a Python code block and validate the corrections. "
            "Provide the corrected code inside a Python block and explain why it works."
        )
        super().__init__(name="Fixer", llm_config=llm_config, system_message=system_message)

    def generate_fix(self, code: str, reasoning: str) -> str:
        """
        Generates a corrected code snippet based on the provided reasoning using two prompting techniques:
        - Code Generation Technique (to produce corrected code)
        - Program-Aided Language Technique (to execute and validate the corrected code)
        """
        prompt = (
            f"Based on this reasoning: {reasoning}\n"
            f"Generate a corrected version of the following code:\n{code}\n"
            "Provide the corrected code inside a Python code block and explain why it should work."
        )
        response = self.generate_reply([{"content": prompt, "role": "user"}])['content']
        
        # Extract the Python code block from the assistant's response.
        code_match = re.search(r'```python(.*?)```', response, re.DOTALL)
        if not code_match:
            return "Failed to generate corrected code."
        
        fixed_code = code_match.group(1).strip()
        
        # Program-Aided Language Technique: Execute the corrected code to validate its correctness.
        try:
            exec_globals = {} # Capturing the execution context if needed

            # Execute the fixed code in a controlled environment
            print('Code execution result:')
            exec(fixed_code, exec_globals)
        except Exception as e:
            return f"Code execution failed: {e}"
        return fixed_code

class Insighter(autogen.AssistantAgent):
    def __init__(self, llm_config):
        # Generated knowledge prompting: Instruct the assistant to provide insights on error patterns and best practices.
        system_message = (
            "Provide insights on common errors and best practices. "
            "Explain error patterns and language-specific pitfalls clearly."
        )
        super().__init__(name="Insighter", llm_config=llm_config, system_message=system_message)

    def generate_insights(self, reasoning: str) -> str:
        """
        Provides additional insights based on the debugging reasoning.
        This function uses a knowledge extraction approach to elaborate on error patterns, pitfalls, and best practices.
        """
        # Generated knowledge prompting: Build a prompt that asks for further insights based on the given debugging reasoning.
        # Constrained prompting: used to constraint the output of the insighter
        prompt = (
            f"Given the following debugging reasoning: {reasoning}\n"
            "Provide additional insights on common error patterns, language-specific pitfalls, and best practices related to the issue."
            "Give a direct response within 250 words. Ignore unnecessary words like 'Let's'."
        )
        insights = self.generate_reply([{"content": prompt, "role": "user"}])['content']
        return insights

class Refiner(autogen.AssistantAgent):
    # Iterative Refinement(ReAct) Technique: Instruct the assistant to refine fixes iteratively.
    def __init__(self, llm_config):
        system_message = (
            "Refine fixes iteratively and suggest alternatives if tests fail. "
            "Provide the alternative code inside a Python code block."
        )
        super().__init__(name="Refiner", llm_config=llm_config, system_message=system_message)

    def refine_solution(self, code: str, current_fix: str, test_result: bool) -> str:
        """
        Refines the solution if the current fix fails a simulated test.
        Uses an iterative refinement approach to suggest alternative fixes.
        """
        if test_result:
            return current_fix
        else:
            # Iterative Refinement Technique: Build a prompt that asks for an alternative fix based on the current code and fix.
            prompt = (
                f"The current fix did not work for the following code:\n{code}\n"
                f"Current fix provided:\n{current_fix}\n"
                "Suggest an alternative fix and provide the alternative code inside a Python code block."
            )
            response = self.generate_reply([{"content": prompt, "role": "user"}])
            code_match = re.search(r'```python(.*?)```', response, re.DOTALL)
            if code_match:
                new_fix = code_match.group(1).strip()
            else:
                new_fix = "Failed to generate alternative fix."
            return new_fix