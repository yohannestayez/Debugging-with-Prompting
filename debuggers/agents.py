import autogen

class InstructionRoleAgent(autogen.AssistantAgent):
    def __init__(self):
        system_message = """You are an expert software engineer. Analyze the provided code and error to set the debugging context."""
        super().__init__(name="Instructor", system_message=system_message)

class ErrorClassificationAgent(autogen.AssistantAgent):
    def __init__(self):
        system_message = """Classify the error type using examples. Respond with "Type: [ERROR_TYPE]\nExplanation: ...\""""
        super().__init__(name="Classifier", system_message=system_message)

class DebugReasoningAgent(autogen.AssistantAgent):
    def __init__(self):
        system_message = """Provide a step-by-step debugging explanation. Use detailed reasoning."""
        super().__init__(name="Debugger", system_message=system_message)

class CodeFixAgent(autogen.AssistantAgent):
    def __init__(self):
        system_message = """Generate corrected code in a Python block. Validate fixes with simulations."""
        super().__init__(name="Fixer", system_message=system_message)

class KnowledgeInsightAgent(autogen.AssistantAgent):
    def __init__(self):
        system_message = """Provide insights on common errors and best practices."""
        super().__init__(name="Insighter", system_message=system_message)

class ReActAgent(autogen.AssistantAgent):
    def __init__(self):
        system_message = """Refine fixes iteratively. If tests fail, suggest alternatives."""
        super().__init__(name="Refiner", system_message=system_message)