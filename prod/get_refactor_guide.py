import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import random
from groq import Groq
from openai import OpenAI
import anthropic
from google.api_core.exceptions import DeadlineExceeded

load_dotenv()

# # # CLIENTS

#GROQ
groq_client = Groq()
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


#CLAUDE
anthropic_client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
       api_key=os.environ["ANTHROPIC_API_KEY"]
    )

# GEMINI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 0.55,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

def get_refactor_html_withbackoff(guide_markdown_file_content, max_retries=3):
    providers = [
        get_refactor_html_from_claude,
        get_refactor_html,
        get_refactor_html_from_openai,
        
       
    ]
    
    for provider in providers:
        for attempt in range(max_retries):
            try:
                return provider(guide_markdown_file_content)
            except DeadlineExceeded:
                sleep_duration = 5**attempt + random.uniform(0, 1)
                print(f"Request to {provider.__name__} timed out. Retrying in {sleep_duration} seconds...")
                time.sleep(sleep_duration)
        print(f"Failed to get a response from {provider.__name__} after {max_retries} retries.")
    
    # If all providers fail
    print(f"Failed to get a response after trying all providers.")
    return '''
        <div class="mb-32 mt-12 border-t-2">
        <p class="mt-2">Refactor guide not available</p>
        </div>
        '''




def get_refactor_html(guide_markdown_file_content):
    try:
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
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




def get_refactor_html_from_claude(guide_markdown_file_content):
    try:
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            temperature=0.1,
            system="You will be provided with text from a markdown file and your task is to convert this text into a blog/guide in HTML. However, do not add any information that is not in the original file.\n\nSTYLING RULES:\n- You must use Tailwind CSS classes and the only colours allowed are white and any shade of gray.\n- The main or highest most DIV must have the following classes: <div class=\"bg-white p-4 rounded-md shadow-md\">\n- Only the top level header must be \"text-xl\" the rest of the text and sub-headers need no special font size\n- All headers and sub headers must be \"text-gray-900\"\n- All paragraphs must have class \"<p class=\"text-gray-700 mb-2\">\"\n- All sub-headers must have class \"<h3 class=\"font-bold text-gray-900 mb-2\">\"\n- All code must be wrapped around in a <code> element\n- Each topic or Finding must be separated with a top border line e.g.: <h3 class=\"border-t font-bold text-gray-900 mb-2\">Finding:</h3>\n\nHere is a very short example:\nPROVIDED MARKDOWN TEXT:\n## Refactoring Plan\n\n**Finding:** Code duplication: The header and navigation components are duplicated in 'pages/index.vue' and 'pages/about_me.vue'. This could be refactored into a shared layout component for better maintainability.\n**Issue:** Increased maintenance effort and potential for inconsistencies between pages.\n**Refactoring Approach:**\n1. Create a new layout component, e.g., `layouts/default.vue`.\n2. Move the duplicated header and navigation code from `pages/index.vue` and `pages/about_me.vue` into `layouts/default.vue`.\n3. Replace the duplicated code in both pages with `<NuxtLayout>` component.\n\n\n\nHTML GENERATED:\n            <div class=\"bg-white p-4 rounded-md shadow-md\">\n              <h2 class=\"text-2xl font-bold text-gray-900 mb-4\">\n                Refactoring Plan\n              </h2>\n              <h3 class=\"border-t font-bold text-gray-900 mb-2\">Finding:</h3>\n              <p class=\"text-gray-700 mb-8\">\n                Code duplication: The header and navigation components are\n                duplicated in 'pages/index.vue' and 'pages/about_me.vue'. This\n                could be refactored into a shared layout component for better\n                maintainability.\n              </p>\n              <h3 class=\"font-bold text-gray-900 mb-2\">Issue:</h3>\n              <p class=\"text-gray-700 mb-8\">\n                Increased maintenance effort and potential for inconsistencies\n                between pages.\n              </p>\n              <h3 class=\"font-bold text-gray-900 mb-2\">\n                Refactoring Approach:\n              </h3>\n              <ol class=\"list-decimal list-inside text-gray-700 mb-8\">\n                <li>\n                  Create a new layout component, e.g.,\n                  <code>layouts/default.vue</code>.\n                </li>\n                <li>\n                  Move the duplicated header and navigation code from\n                  <code>pages/index.vue</code> and\n                  <code>pages/about_me.vue</code> into\n                  <code>layouts/default.vue</code>.\n                </li>\n                <li>\n                  Replace the duplicated code in both pages with\n                  <code>&lt;NuxtLayout&gt;</code> component.\n                </li>\n              </ol>\n  </div>\n\n\nYou must return only the pure html with no explanation or commentary.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": guide_markdown_file_content
                        }
                    ]
                }
            ]
        )

        response = message.content[0].text
        print(response)

        return response
        
    except Exception as e:
            print(f"An error occurred: {e}")
            return None




def get_refactor_html_from_openai(guide_markdown_file_content):
    try:
        response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "You will be provided with text from a markdown file and your task is to convert this text into a blog/guide in HTML. However, do not add any information that is not in the original file.\n\nSTYLING RULES:\n- You must use Tailwind CSS classes and the only colours allowed are white and any shade of gray.\n- The main or highest most DIV must have the following classes: <div class=\"bg-white p-4 rounded-md shadow-md\">\n- Only the top level header must be \"text-xl\" the rest of the text and sub-headers need no special font size\n- All headers and sub headers must be \"text-gray-900\"\n- All paragraphs must have class \"<p class=\"text-gray-700 mb-2\">\"\n- All sub-headers must have class \"<h3 class=\"font-bold text-gray-900 mb-2\">\"\n- All code must be wrapped around in a <code> element\n- Each topic or Finding must be separated with a top border line e.g.: <h3 class=\"border-t font-bold text-gray-900 mb-2\">Finding:</h3>\n\nHere is a very short example:\nPROVIDED MARKDOWN TEXT:\n## Refactoring Plan\n\n**Finding:** Code duplication: The header and navigation components are duplicated in 'pages/index.vue' and 'pages/about_me.vue'. This could be refactored into a shared layout component for better maintainability.\n**Issue:** Increased maintenance effort and potential for inconsistencies between pages.\n**Refactoring Approach:**\n1. Create a new layout component, e.g., `layouts/default.vue`.\n2. Move the duplicated header and navigation code from `pages/index.vue` and `pages/about_me.vue` into `layouts/default.vue`.\n3. Replace the duplicated code in both pages with `<NuxtLayout>` component.\n\n\n\nHTML GENERATED:\n            <div class=\"bg-white p-4 rounded-md shadow-md\">\n              <h2 class=\"text-2xl font-bold text-gray-900 mb-4\">\n                Refactoring Plan\n              </h2>\n              <h3 class=\"border-t font-bold text-gray-900 mb-2\">Finding:</h3>\n              <p class=\"text-gray-700 mb-8\">\n                Code duplication: The header and navigation components are\n                duplicated in 'pages/index.vue' and 'pages/about_me.vue'. This\n                could be refactored into a shared layout component for better\n                maintainability.\n              </p>\n              <h3 class=\"font-bold text-gray-900 mb-2\">Issue:</h3>\n              <p class=\"text-gray-700 mb-8\">\n                Increased maintenance effort and potential for inconsistencies\n                between pages.\n              </p>\n              <h3 class=\"font-bold text-gray-900 mb-2\">\n                Refactoring Approach:\n              </h3>\n              <ol class=\"list-decimal list-inside text-gray-700 mb-8\">\n                <li>\n                  Create a new layout component, e.g.,\n                  <code>layouts/default.vue</code>.\n                </li>\n                <li>\n                  Move the duplicated header and navigation code from\n                  <code>pages/index.vue</code> and\n                  <code>pages/about_me.vue</code> into\n                  <code>layouts/default.vue</code>.\n                </li>\n                <li>\n                  Replace the duplicated code in both pages with\n                  <code>&lt;NuxtLayout&gt;</code> component.\n                </li>\n              </ol>\n  </div>\n\n\nYou must return only the pure html with no explanation or commentary."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": guide_markdown_file_content
                }
            ]
            }
        ],
        temperature=0.3,
        max_tokens=12384,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        response = response.choices[0].message.content
        print(response)
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None




# PAUSED FOR NOW
def get_refactor_html_from_groq(guide_markdown_file_content):
    try:
        completion = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with text from a markdown file and your task is to convert this text into a blog/guide in HTML. However, do not add any information that is not in the original file.\nSTYLING RULES:\n\nYou must use Tailwind CSS classes and the only colours allowed are white and any shade of gray.\nThe main or highest most DIV must have the following classes: <div class=\"bg-white p-4 rounded-md shadow-md\">\nOnly the top level header must be \"text-xl\" the rest of the text and sub-headers need no special font size\nAll headers and sub headers must be \"text-gray-900\"\nAll paragraphs must have class \"<p class=\"text-gray-700 mb-2\">\"\nAll sub-headers must have class \"<h3 class=\"font-bold text-gray-900 mb-2\">\"\nAll code must be wrapped around in a <code> element\nEach topic or Finding must be separated with a top border line e.g.: <h3 class=\"border-t font-bold text-gray-900 mb-2\">Finding:</h3>\n\nHere is a very short example:\nPROVIDED MARKDOWN TEXT:\nRefactoring Plan\nFinding: Code duplication: The header and navigation components are duplicated in 'pages/index.vue' and 'pages/about_me.vue'. This could be refactored into a shared layout component for better maintainability.\nIssue: Increased maintenance effort and potential for inconsistencies between pages.\nRefactoring Approach:\n\nCreate a new layout component, e.g., layouts/default.vue.\nMove the duplicated header and navigation code from pages/index.vue and pages/about_me.vue into layouts/default.vue.\nReplace the duplicated code in both pages with <NuxtLayout> component.\n\nHTML GENERATED:\n<div class=\"bg-white p-4 rounded-md shadow-md\">\n<h2 class=\"text-2xl font-bold text-gray-900 mb-4\">\nRefactoring Plan\n</h2>\n<h3 class=\"border-t font-bold text-gray-900 mb-2\">Finding:</h3>\n<p class=\"text-gray-700 mb-8\">\nCode duplication: The header and navigation components are\nduplicated in 'pages/index.vue' and 'pages/about_me.vue'. This\ncould be refactored into a shared layout component for better\nmaintainability.\n</p>\n<h3 class=\"font-bold text-gray-900 mb-2\">Issue:</h3>\n<p class=\"text-gray-700 mb-8\">\nIncreased maintenance effort and potential for inconsistencies\nbetween pages.\n</p>\n<h3 class=\"font-bold text-gray-900 mb-2\">\nRefactoring Approach:\n</h3>\n<ol class=\"list-decimal list-inside text-gray-700 mb-8\">\n<li>\nCreate a new layout component, e.g.,\n<code>layouts/default.vue</code>.\n</li>\n<li>\nMove the duplicated header and navigation code from\n<code>pages/index.vue</code> and\n<code>pages/about_me.vue</code> into\n<code>layouts/default.vue</code>.\n</li>\n<li>\nReplace the duplicated code in both pages with\n<code><NuxtLayout></code> component.\n</li>\n</ol>\n  </div>\nYou must return only the pure html with no explanation or commentary."
                },
                {
                    "role": "user",
                    "content": guide_markdown_file_content
                }
            ],
            temperature=0.3,
            max_tokens=32768,
            top_p=1,
            stream=False,
            stop=None,
        )

        response = completion.choices[0].message.content
        print(response)
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None




"""

# Initialize new log file for report
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')


guide_markdown_file_content = """

"""

#CLAUDE TEST
#get_refactor_html_from_claude(guide_markdown_file_content)

# GROQ TEST
#get_refactor_html_from_groq(guide_markdown_file_content)


#OPEN AI TEST
get_refactor_html_from_openai(guide_markdown_file_content)
#refactor_guide_html = get_refactor_html_withbackoff(guide_markdown_file_content)
#with open(os.path.join(reports_dir, f"refactor_guide_1234.html"), "w") as file:
 #       file.write(refactor_guide_html)



#"""