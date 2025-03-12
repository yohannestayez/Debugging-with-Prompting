import sys
sys.path.append('debuggers')

from utils import simulated_test
from agents import Instructor, Classifier, Debugger, Fixer, Insighter, Refiner

class AutoGenDebugPipeline:
    def __init__(self, llm_config):
        """
        Initialize the pipeline with all agents.
        
        """
        self.debuggers = {
            "instructor": Instructor(llm_config),
            "classifier": Classifier(llm_config),
            "debugger": Debugger(llm_config),
            "fixer": Fixer(llm_config),
            "insighter": Insighter(llm_config),
            "refiner": Refiner(llm_config)
        }

    def run_pipeline(self, code: str, error: str) -> dict:
        """
        Run the debugging pipeline through all stages.

        """
        results = {}

        # Stage 1: Set context
        results["context"] = self.debuggers["instructor"].set_context(code, error)

        # Stage 2: Classify error
        results["classification"] = self.debuggers["classifier"].classify_error(error)

        # Stage 3: Debug reasoning
        results["reasoning"] = self.debuggers["debugger"].generate_reasoning(code, error)

        # Stage 4: Generate fix
        results["fixed_code"] = self.debuggers["fixer"].generate_fix(code, results["reasoning"])

        # Stage 5: Validate and refine if necessary
        if not simulated_test(code, results["fixed_code"], error):
            results["fixed_code"] = self.debuggers["refiner"].refine_solution(
                code, results["fixed_code"], False
            )

        # Stage 6: Generate insights
        results["insights"] = self.debuggers["insighter"].generate_insights(results["reasoning"])

        return results