import json
from flask import Flask, request, jsonify, render_template
from debuggers.pipeline import AutoGenDebugPipeline
import os
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL= os.getenv('LLM_MODEL')
API_KEY= os.getenv('API_KEY')

# Initialize Flask application
app = Flask(__name__)

# LLM configuration
llm_config = {
    "model": LLM_MODEL,  # e.g., "gemini-2.0-flash"
    "api_key": API_KEY, 
    "temperature": 0.4,  # Lowered for more deterministic, accurate outputs
    "max_tokens": 500,
    "top_p": 0.8,  # Slightly tightened for better focus
    "frequency_penalty": 0.5,
    "presence_penalty": 0.5,
    "base_url": "https://generativelanguage.googleapis.com/v1beta",
    "api_type": "google"
}

# Initialize the debugging pipeline with the LLM configuration
pipeline = AutoGenDebugPipeline(llm_config)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/debug', methods=['POST'])
def debug_code():
    """
    Endpoint to debug code based on provided code snippet and error message.

    Expects a JSON body with 'code' and 'error' fields.
    Returns debugging results as JSON.
    """
    # Get JSON data from the request
    data = request.get_json()
    code = data.get('code')
    error = data.get('error')

    # Validate input
    if not code or not error:
        return jsonify({"error": "Both 'code' and 'error' are required."}), 400

    # Run the debugging pipeline and return results
    try:
        results = pipeline.run_pipeline(code, error)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":

    # Run the Flask app
    app.run(debug=True, port=5000)