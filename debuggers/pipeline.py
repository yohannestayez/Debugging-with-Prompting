import autogen
from .agents import *

class AutoGenDebugPipeline:
    def __init__(self):
        self.user_proxy = autogen.UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )
        self.agents = {
            "instructor": InstructionRoleAgent(),
            "classifier": ErrorClassificationAgent(),
            "debugger": DebugReasoningAgent(),
            "fixer": CodeFixAgent(),
            "insighter": KnowledgeInsightAgent(),
            "refiner": ReActAgent()
        }
    
    def run_pipeline(self, code: str, error: str) -> dict:
        results = {}
        
        # Stage 1: Set context
        self.user_proxy.initiate_chat(
            self.agents["instructor"],
            message=f"Code:\n{code}\nError: {error}"
        )
        results["context"] = self._last_message()
        
        # Stage 2: Classify error
        self.user_proxy.initiate_chat(
            self.agents["classifier"],
            message=f"Error: {error}"
        )
        results["classification"] = self._last_message()
        
        # Stage 3: Debug reasoning
        self.user_proxy.initiate_chat(
            self.agents["debugger"],
            message=f"Code:\n{code}\nError: {error}"
        )
        results["reasoning"] = self._last_message()
        
        # Stage 4: Generate fix
        self.user_proxy.initiate_chat(
            self.agents["fixer"],
            message=f"Code:\n{code}\nReasoning: {results['reasoning']}"
        )
        results["fixed_code"] = self._parse_code(self._last_message())
        
        # Stage 5: Validate and refine
        if not self._simulate_test(results["fixed_code"]):
            self.user_proxy.initiate_chat(
                self.agents["refiner"],
                message=f"Failed Code:\n{results['fixed_code']}\nError: {error}"
            )
            results["fixed_code"] = self._parse_code(self._last_message())
        
        # Stage 6: Generate insights
        self.user_proxy.initiate_chat(
            self.agents["insighter"],
            message=f"Error: {error}\nReasoning: {results['reasoning']}"
        )
        results["insights"] = self._last_message()
        
        return results
    
    def _last_message(self) -> str:
        return self.user_proxy.chat_messages[self.agents["instructor"]][-1]["content"]
    
    def _parse_code(self, text: str) -> str:
        # Extract code blocks (simplified)
        return text.split("```python")[1].split("```")[0].strip()
    
    def _simulate_test(self, code: str) -> bool:
        # Placeholder for actual validation
        return True