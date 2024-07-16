import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import random
from google.api_core.exceptions import DeadlineExceeded

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 0.55,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

def get_refactor_html_withbackoff(guide_markdown_file_content, max_retries=5):
    for attempt in range(max_retries):
        try:
            return get_refactor_html(guide_markdown_file_content)
        except DeadlineExceeded:
            sleep_duration = 2**attempt + random.uniform(0, 1)
            print(f"Request timed out. Retrying in {sleep_duration} seconds...")
            time.sleep(sleep_duration)
    print(f"Failed to get a response after {max_retries} retries.")
    # # TODO: write error to a log and use for rettries
    return None




def get_refactor_html(guide_markdown_file_content):
    model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
     system_instruction="You will be provided with text from a markdown file and your task is to convert this text into a blog/guide in HTML.  However, do not add any information that is not in the original file. \n\nSTYLING RULES:\n- You must use Tailwind CSS classes and the only colours allowed are white  and any shade of gray.\n- The main or highest most DIV must have the following classes:  <div class=\"bg-white p-4 rounded-md shadow-md\">\n- Only the top level header must be \"text-xl\" the rest of the text and sub-headers need no specialy font size\n- All headers and sub headers must be \"text-gray-900\"\n- All paragraphs must have class \"<p class=\"text-gray-700 mb-2\">\"\n- All sub-headers must have class \"<h3 class=\"font-bold text-gray-900 mb-2\">\"\n- All code must be wrapped around in a <code> element\n- Each topic or Finding must be separated with a top border line e.g.: <h3 class=\"border-t font-bold text-gray-900 mb-2\">Finding:</h3>\n\nHere is a very short example:\nPROVIDED MARKDOWN TEXT:\n## Refactoring Plan\n\n**Finding:** Code duplication: The header and navigation components are duplicated in 'pages/index.vue' and 'pages/about_me.vue'. This could be refactored into a shared layout component for better maintainability.\n**Issue:** Increased maintenance effort and potential for inconsistencies between pages.\n**Refactoring Approach:**\n1. Create a new layout component, e.g., `layouts/default.vue`.\n2. Move the duplicated header and navigation code from `pages/index.vue` and `pages/about_me.vue` into `layouts/default.vue`.\n3. Replace the duplicated code in both pages with `<NuxtLayout>` component.\n\n\n\nHTML GENERATED:\n            <div class=\"bg-white p-4 rounded-md shadow-md\">\n              <h2 class=\"text-2xl font-bold text-gray-900 mb-4\">\n                Refactoring Plan\n              </h2>\n              <h3 class=\"border-t font-bold text-gray-900 mb-2\">Finding:</h3>\n              <p class=\"text-gray-700 mb-8\">\n                Code duplication: The header and navigation components are\n                duplicated in 'pages/index.vue' and 'pages/about_me.vue'. This\n                could be refactored into a shared layout component for better\n                maintainability.\n              </p>\n              <h3 class=\"font-bold text-gray-900 mb-2\">Issue:</h3>\n              <p class=\"text-gray-700 mb-8\">\n                Increased maintenance effort and potential for inconsistencies\n                between pages.\n              </p>\n              <h3 class=\"font-bold text-gray-900 mb-2\">\n                Refactoring Approach:\n              </h3>\n              <ol class=\"list-decimal list-inside text-gray-700 mb-8\">\n                <li>\n                  Create a new layout component, e.g.,\n                  <code>layouts/default.vue</code>.\n                </li>\n                <li>\n                  Move the duplicated header and navigation code from\n                  <code>pages/index.vue</code> and\n                  <code>pages/about_me.vue</code> into\n                  <code>layouts/default.vue</code>.\n                </li>\n                <li>\n                  Replace the duplicated code in both pages with\n                  <code>&lt;NuxtLayout&gt;</code> component.\n                </li>\n              </ol>\n  </div>\n\n\nYou must return only the pure html with no explanation or commentary.",
)
    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "Convert this markdown content into HTML:",
            
        ],
        },
    ]
    )

    response = chat_session.send_message(guide_markdown_file_content)

    #print(response.text)
    return response.text


"""

# Initialize new log file for report
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')


guide_markdown_file_content = ""

refactor_guide_html = get_refactor_html_withbackoff(guide_markdown_file_content)
with open(os.path.join(reports_dir, f"refactor_guide_1234.html"), "w") as file:
        file.write(refactor_guide_html)



"""