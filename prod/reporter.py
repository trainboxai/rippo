from dotenv import load_dotenv
import os
import json
import time
import random
import google.generativeai as genai
from google.api_core.exceptions import DeadlineExceeded
from pathlib import Path
from colorama import Fore, Style
import re

 # AUTH
load_dotenv
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


# FUNCTIONS

def code_audit_report(md_file, unique_id=0):
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
    ]

    model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="You will be provided with a codebase in the form of markdown text that contains all the important code from a git repository for a project. The code is separated by file path and name. \n\nYour task is to perform a code audit, checking for errors and areas for improvement.  Analyze the code for the following:\n\n*   **Syntax errors:** Errors that prevent the code from compiling or running.\n*   **Logical errors:** Errors in the code's logic that could lead to unexpected behavior.\n*   **Unused variables:** Variables that are declared but never used.\n*   **Violation of best practices:** Code that functions correctly but does not adhere to recommended coding standards. This includes:\n    *   **Code duplication:** Repetitive code blocks that could be consolidated into a single function or module.\n    *   **Hardcoded values:** Using literal values instead of variables or constants, hindering flexibility and maintainability.\n    *   **Inefficient resource management:** Failing to properly close files or release connections, potentially leading to resource leaks.\n\nClassify the report findings as follows:\n\n1.  **High:** Errors that will likely cause immediate issues or crashes, including syntax errors and logical errors that lead to incorrect results.\n2.  **Medium:** Issues that could impact the application's functionality or maintainability, including unused variables and violation of best practices like code duplication.\n3.  **Low:** Potential problems with minimal impact, such as hardcoded values that could be replaced with constants for better readability.\n\nWhen you have finished analyzing, write the report into a JSON dictionary in the following order: High, Medium, Low. \n\nSeparate each finding as its own item inside the classification it belongs to. For example:\n\n{\n  \"High\": [\n    {\n      \"finding\": \"Syntax error: Missing semicolon in line 42 of file project/scripts/main.py. This will prevent the code from compiling.\",\n      \"files\": [\n        \"project/scripts/main.py\"\n      ],\n      \"impact\": \"Compilation failure, preventing program execution.\"\n    },\n    {\n      \"finding\": \"Logical error: Incorrect comparison operator in function 'calculate_discount' in file project/utils/pricing.py.  This leads to incorrect discounts being applied.\",\n      \"files\": [\n        \"project/utils/pricing.py\"\n      ],\n      \"impact\": \"Inaccurate pricing calculations, potentially impacting revenue.\"\n    }\n  ],\n  \"Medium\": [\n    {\n      \"finding\": \"Unused variable: 'temp_data' declared in function 'process_order' but never used. This adds unnecessary complexity to the code.\",\n      \"files\": [\n        \"project/api/orders.py\"\n      ],\n      \"impact\": \"Reduced code readability and potential confusion for future developers.\"\n    },\n    {\n      \"finding\": \"Code duplication: The function 'validate_email' is duplicated in multiple files. This increases maintenance overhead.\",\n      \"files\": [\n        \"project/auth/signup.py\",\n        \"project/user/profile.py\"\n      ],\n      \"impact\": \"Increased maintenance effort and potential for inconsistencies if the function is modified.\"\n    }\n  ],\n  \"Low\": [\n    {\n      \"finding\": \"Hardcoded value: The API endpoint URL is hardcoded in the 'fetchData' function.  This limits flexibility for deploying to different environments.\",\n      \"files\": [\n        \"project/services/api.py\"\n      ],\n      \"impact\": \"Deployment challenges and difficulty adapting to environment changes.\"\n    }\n  ]\n}\n\nEach report finding should be concise yet informative with no more than 100 words per finding. The report should clearly describe:\nFinding: What is the specific issue identified?\nFiles: In which file(s) does this issue exist?\nImpact: What are the potential consequences of this issue? It's acceptable to hypothesize even if the exact impact is unknown.\nYou must return only the JSON content and nothing else. No explanations",
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(md_file)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(script_dir, '..', 'reports')
    # Remove both opening and closing delimiters
    cleaned_text = re.sub(r'```json', '', response.text)
    cleaned_text = re.sub(r'```', '', cleaned_text)

    with open(os.path.join(reports_dir,f'code_audit_{unique_id}.json'), 'w') as file:
        file.write(cleaned_text)
    #print(cleaned_text)
    return response.text


def vulnerability_report(input_file, unique_id=0):
    generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
    ]

    model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="You will be provided with a JSON file containing search results for vulnerabilities related to various software dependencies. Each dependency entry includes its name, version, a list of text results from vulnerability databases, and the source of the information.\n\nYour task is to analyze these search results and generate a vulnerability report in JSON format. For each dependency, determine if a vulnerability exists based on the provided text results.\n\nYou must be certain that the vulnerability mentioned in the results affects the specified version. If a vulnerability is identified, create a report entry with the following structure:\n\n{\n  \"vulnerability_report\": [\n    {\n      \"dependency\": \"dependency_name\",\n      \"version\": \"dependency_version\",\n      \"description\": \"Concise description of the vulnerability (under 100 words).\",\n      \"source\": \"URL of the source where the vulnerability information was found\"\n    },\n    {\n      \"dependency\": \"another_dependency\",\n      \"version\": \"another_dependency_version\",\n      \"description\": \"Concise description of this vulnerability (under 100 words).\",\n      \"source\": \"URL of the source for this vulnerability information\"\n    }\n    // ... more vulnerability entries as needed\n  ]\n}\n\nIf no vulnerabilities are found, return an empty \"vulnerability_report\" array:\n{\n  \"vulnerability_report\": []\n}\n\nDo not return anything else, only the JSON content as described above.\n**Key Considerations:**\n\n*   **Conciseness:** Keep the vulnerability descriptions brief and informative.\n*   **Source Attribution:** Always include the source URL for each reported vulnerability.\n*   **Clarity:**  Structure the JSON output clearly for easy parsing and use.\n\nYou must return only the JSON content and nothing else. No explanations",
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(input_file)

    print(response.text)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(script_dir, '..', 'reports')
    # Remove both opening and closing delimiters
    cleaned_text = re.sub(r'```json', '', response.text)
    cleaned_text = re.sub(r'```', '', cleaned_text)
    with open(os.path.join(reports_dir,f'vuln_report_{unique_id}.json'), 'w') as file:
        file.write(cleaned_text) 
    return response.text


def quality_report(input_file,unique_id=0):
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
    ]

    model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="You will be provided with a codebase in the form of markdown text, with code separated by file path and name. You'll also receive the results of a previous code audit. \n\nYour task is to analyze the code and provide a quality review based on these criteria:\n\n*   **Readability:** How easy is it to understand the code's logic and flow? Consider indentation, comments, and naming conventions.\n*   **Efficiency:** Does the code perform its tasks optimally? Look for unnecessary complexity, redundant operations, or potential bottlenecks. Use the audit results to support your evaluation. \n*   **Documentation:**  How well-documented is the code? Assess the presence and quality of comments, docstrings, and any accompanying documentation files.\n\nFor each criterion, provide:\n\n*   **Score:** A numerical score out of 100, following this scale:\n    *   90+: Excellent\n    *   70-89: Good\n    *   40-69: Ok\n    *   Below 40: Bad\n*   **Summary:** A concise explanation (under 100 words) justifying the score.  Reference specific examples from the code to support your assessment.\n\nReturn your complete analysis as a JSON object in the following format e.g.:\n\n{\n  \"readability\": {\n    \"score\": 80,\n    \"summary\": \"The code is generally well-structured and uses clear naming conventions. However, some sections lack comments, making the logic difficult to follow.\"\n  },\n  \"efficiency\": {\n    \"score\": 60,\n    \"summary\": \"The code functions adequately but contains some areas of redundancy identified in the audit. For example, the 'validate_email' function is duplicated in multiple files.\"\n  },\n  \"documentation\": {\n    \"score\": 40,\n    \"summary\": \"While the code includes basic comments, there are no docstrings or separate documentation files. This makes it harder to understand the overall functionality.\"\n  }\n}\n\nYou must return only the JSON content and nothing else. No explanations ",
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(input_file)

    #print(response.text)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(script_dir, '..', 'reports')
    # Remove both opening and closing delimiters
    cleaned_text = re.sub(r'```json', '', response.text)
    cleaned_text = re.sub(r'```', '', cleaned_text)

    with open(os.path.join(reports_dir, f'quality_report_{unique_id}.json'), 'w') as file:
        file.write(cleaned_text)
        
    return response.text

# Bakcoff and Jitter implementaion
def code_audit_report_with_backoff(md_file, unique_id=0, max_retries=5):
    for attempt in range(max_retries):
        try:
            print(Fore.LIGHTRED_EX + f"Trying code audit, attempt {attempt + 1} " + Style.RESET_ALL)
            return code_audit_report(md_file, unique_id)
        except DeadlineExceeded:
            sleep_duration = 2**attempt + random.uniform(0, 1)
            print(f"Request timed out. Retrying in {sleep_duration} seconds...")
            time.sleep(sleep_duration)
    print(f"Code audit failed after {max_retries} retries.")
    return json.dumps({"error": f"Code audit failed after {max_retries} retries."})

def vulnerability_report_with_backoff(input_file, unique_id=0, max_retries=5):
    for attempt in range(max_retries):
        try:
            print(Fore.LIGHTRED_EX + f"Trying Vuln Report, attempt {attempt + 1} " + Style.RESET_ALL)
            return vulnerability_report(input_file, unique_id)
        except DeadlineExceeded:
            sleep_duration = 2**attempt + random.uniform(0, 1)
            print(f"Request timed out. Retrying in {sleep_duration} seconds...")
            time.sleep(sleep_duration)
    print(f"Vuln Report failed after {max_retries} retries.")
    return json.dumps({"error": f"Vuln Report failed after {max_retries} retries."})

def quality_report_with_backoff(input_files, unique_id=0, max_retries=5):
    for attempt in range(max_retries):
        try:
            print(Fore.LIGHTRED_EX + f"Trying Quality Report, attempt {attempt + 1} " + Style.RESET_ALL)
            return quality_report(input_files, unique_id)
        except DeadlineExceeded:
            sleep_duration = 2**attempt + random.uniform(0, 1)
            print(f"Request timed out. Retrying in {sleep_duration} seconds...")
            time.sleep(sleep_duration)
    print(f"Quality Report failed after {max_retries} retries.")
    return json.dumps({"error": f"Quality Report failed after {max_retries} retries."})






"""

# Testing TODO comment out when in prod
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')

#codebase
markdown_file_path = Path(os.path.join(output_dir, 'final.md'))
markdown_file = markdown_file_path.read_text()

# Vulnerability search results
vuln_results_path = Path(os.path.join(output_dir, 'vuln_results.json'))
vulnerability_search_results = vuln_results_path.read_text()

# code audit
code_audit_path = Path(os.path.join(reports_dir ,'code_audit.json'))
code_audit = code_audit_path.read_text()

quality_input = f"""
# # # Codebase below in markdown # # # 
#{markdown_file}

#==========================================
# # #  Code Audit report below # # # 
#{code_audit}

"""


# get code audit report
#code_audit_report(markdown_file)

# get vuln report
#vulnerability_report(vulnerability_search_results)

# get quality report
#quality_report(quality_input)

"""