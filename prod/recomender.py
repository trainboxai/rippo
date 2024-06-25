import os
import json
import time
import random
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
from google.api_core.exceptions import DeadlineExceeded

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')



def generate_refactor_plan_with_backoff(input_files, unique_id=0, max_retries=5):
    for attempt in range(max_retries):
        try:
            return generate_refactoring_plan(input_files, unique_id) 
        except DeadlineExceeded:
            sleep_duration = 2**attempt + random.uniform(0, 1)
            print(f"Request timed out. Retrying in {sleep_duration} seconds...")
            time.sleep(sleep_duration)
    raise Exception(f"Failed to get a response after {max_retries} retries.")


def generate_refactoring_plan(input_files,unique_id=0):
    generation_config = {
    "temperature": 0.4,
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
    system_instruction="\n## Task: Generate a Detailed Refactoring Plan with Code Examples\n\nYou are provided with a codebase (in markdown format, with code separated by file path and name) and an audit report highlighting issues within the code. Your task is to analyze the audit report and generate a detailed plan for mitigating each finding. For each finding:\n\n1.  **Identify the issue:** Clearly state the problem identified in the audit report.\n2.  **Refactoring Approach:** Provide a concise description of how to address the issue. Include **specific steps**, focusing on code-level changes. Whenever possible, provide **code examples** illustrating the proposed modifications.\n3.  **Indicate the relevant files:** List the files that need to be modified to address the issue.\n\n**Output Format:**\n\nReturn the refactoring plan as a markdown list, where each item corresponds to a finding from the audit report.\n\n**Example:**\n\nRefactoring Plan\nFinding: Unused variable: 'logoHovered' is passed as a prop to the 'Header' component but is never used.\nIssue: The 'logoHovered' prop is unnecessary and adds complexity.\nRefactoring Approach: Remove the 'logoHovered' prop from the 'Header' component definition.\nExample:\n// Before:\nfunction Header(props: { title: string; logoHovered: boolean }) { \n    // ...\n}\n\n// After:\nfunction Header(props: { title: string }) { \n    // ...\n}\n\nAlso, remove all instances where 'logoHovered' is passed as a prop to 'Header'.\nRelevant Files: src/components/RootLayout.tsx, src/components/Header.tsx\n\nFinding: Hardcoded shape values: The 'StylizedImage' component uses magic numbers (0, 1, 2) to represent different shapes. Using named constants would improve readability.\nIssue: Magic numbers reduce code readability.\nRefactoring Approach: Define named constants for each shape and replace the magic numbers with these constants.\nExample:\n// Before:\nconst shape = getShape(0); // 0 represents a circle\n\n// After:\nconst SHAPE_CIRCLE = 0;\nconst SHAPE_SQUARE = 1;\nconst SHAPE_TRIANGLE = 2;\nconst shape = getShape(SHAPE_CIRCLE);\nRelevant Files: src/components/StylizedImage.tsx\n\nFinding: Missing alt text: Several images lack descriptive alt text, impacting accessibility for users with screen readers.\nIssue: Missing alt text reduces accessibility and potentially harms SEO.\nRefactoring Approach: Add meaningful and descriptive alt text attributes to all img tags. The alt text should concisely describe the image content.\nExample:\n// Before:\n<img src=\"/images/product-photo.jpg\" />\n\n// After:\n<img src=\"/images/product-photo.jpg\" alt=\"A close-up photo of our latest product, showcasing its sleek design and vibrant colors.\" />\n\nRelevant Files: src/app/blog/a-short-guide-to-component-naming/page.mdx, src/app/blog/3-lessons-we-learned-going-back-to-the-office/page.mdx, [ ... list of all relevant files ... ]\n\nOnly return the refactoring plan. Do not respond with any other text or comments.\n",
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(input_files)

    print(response.text)
    # write the file to the report folder
    with open(os.path.join(reports_dir, f"refactor_guide_{unique_id}.md"), 'w' ) as file:
        file.write(response.text)
    return response.text 


"""
# 1. combine results and original md into 1 file for LLM input
markdown_codebase_path = Path(os.path.join(output_dir,"final.md")) 
markdown_codebase = markdown_codebase_path.read_text()

audit_file_path = Path(os.path.join(reports_dir, "code_audit_0.json")) #TODO: make dynamic with unique id fetching
audit = audit_file_path.read_text()

combined_input = f"""
#### CODE BASE ####
#{markdown_codebase}
##################

#### AUDIT REPORT ####
#{audit}
##################

"""

# 2. prompt for code gen
generate_refactor_plan_with_backoff(combined_input)

# clean up files?

"""