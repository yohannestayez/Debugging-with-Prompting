# Code Debugger

This project is a demonstration of different prompting techniques on an code debugging and generating assistant. It analyzes Python code snippets and errors, delivering corrected code, detailed debugging explanations, and insights on error patterns, using a variety of advanced prompting techniques orchestrated via AutoGen.

## Folder Structure

```
├── debuggers/
│   ├── __init__.py       # Package initialization
│   ├── agents.py         # AutoGen agent classes for debugging tasks done using different prompting techniques
│   ├── pipeline.py       # Orchestrates the multi-agent debugging pipeline
│   └── utils.py          # Helper functions (e.g., simulated testing)
├── main.py               # Flask-based backend entry point
├── requirements.txt    
└── README.md             
```

## Overview
The assistant employs a modular pipeline of specialized agents to process code and errors, showcasing a rich set of prompting techniques to enhance debugging accuracy, reasoning, and educational value.
## **Prompting Techniques Used**  

### **Core Techniques**  
- **Instruction Prompting**: Directly assigns tasks (e.g., *"Analyze this code for debugging"*).  
- **Role Prompting**: Assigns expert roles (e.g., *"You are a senior software engineer"*).  

### **Structured Output Techniques**  
- **Code Generation**: Produces corrected code (e.g., *"Provide the fix inside a Python block"*).  
- **Few-Shot Prompting**: Uses examples to guide structured outputs (e.g., error classification JSON).  

### **Reasoning Techniques**  
- **Chain-of-Thought (CoT)**: Breaks reasoning into steps (e.g., *"First, locate the error; second, check types..."*).  
- **Self-Consistency**: Generates multiple reasoning paths and synthesizes results.  
- **ReAct (Reasoning + Acting)**: Iterates between reasoning (*"Why did this fail?"*) and acting (*"Suggest an alternative fix"*).  

### **Knowledge Techniques**  
- **Generated Knowledge Prompting**: Extracts insights on error patterns (e.g., *"Explain common KeyError pitfalls"*).  
- **PAL (Program-Aided Language Model)**: Simulates execution to validate fixes.  

### **Multi-Turn Prompting**  
- **Multi-Turn Prompting**: One agent’s response informs another (e.g., Debugger → Fixer → Refiner).

---

<table>
  <tr>
    <td>
      <table>
        <tr><th>Agent</th><th>Prompting Techniques</th></tr>
        <tr><td><b>Instructor</b></td><td>Instruction Prompting, Role Prompting</td></tr>
        <tr><td><b>Classifier</b></td><td>Few-Shot Prompting</td></tr>
        <tr><td><b>Debugger</b></td><td>Chain-of-Thought (CoT), Self-Consistency</td></tr>
        <tr><td><b>Fixer</b></td><td>Code Generation, Program-Aided Language Model (PAL)</td></tr>
        <tr><td><b>Insighter</b></td><td>Generated Knowledge Prompting</td></tr>
        <tr><td><b>Refiner</b></td><td>ReAct (Reasoning + Acting)</td></tr>
      </table>
    </td>
    <td>
      <a href="https://www.youtube.com/watch?v=rFx68BZQpJw">
        <img src="https://img.youtube.com/vi/rFx68BZQpJw/0.jpg" width="500">
      </a>
      <p><b>Click the image to see the demo video!</b></p>
    </td>
  </tr>
</table>

## Tools Used

- **AutoGen (via `pyautogen`)**: Orchestrates the multi-agent pipeline, enabling seamless interaction between specialized agents.
- **Google Gemini 2.0 Flash (via `google-generativeai`)**: Provides fast, efficient language model capabilities for technical responses.
- **Flask**: Hosts a lightweight backend with a `/debug` endpoint for API access.
- **Python Standard Library**: Leverages `re` for regex-based parsing (e.g., extracting code blocks, line numbers).

## Setup and Running

Install dependencies from `requirements.txt`, set your Gemini API key in `main.py`, and run `python main.py` to start the server.

## Dependencies

- `google-generativeai`
- `pyautogen`
- `flask`

