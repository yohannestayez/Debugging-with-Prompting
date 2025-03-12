import os
import sys
sys.path.append('debuggers')
from pipeline import AutoGenDebugPipeline
from dotenv import load_dotenv


load_dotenv()

LLM_MODEL= os.getenv('LLM_MODEL')
API_KEY= os.getenv('API_KEY')

# LLM configuration
llm_config = {
    "model": LLM_MODEL,  
    "api_key": API_KEY, 
    "base_url": "https://generativelanguage.googleapis.com/v1beta",
    "api_type": "google"
}

# Instantiate the pipeline
pipeline = AutoGenDebugPipeline(llm_config)

# Run the pipeline
code = "def divide(a, b):\n    return a / b\nprint(divide(1, 0))"
error = "ZeroDivisionError: division by zero at line 2"
results = pipeline.run_pipeline(code, error)

# Access results
print("Fixed Code:\n", results["fixed_code"])
print("Insights:\n", results["insights"])