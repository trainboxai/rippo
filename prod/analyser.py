import os
import time
import random
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from colorama import Fore, Style
from google.api_core.exceptions import DeadlineExceeded

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])



def clean_json(json_string):
  
    generation_config = {
    "temperature": 0.2,
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
    system_instruction="You will be provided with a JSON string. The string may or may not contain structural issues which would make the JSON invalid and cannot be used in python scripts.\n\nYour task is to analyse the provided string and make corrections so that the end result is a valid JSON string. Return the clean corrected / updated string with no additional text. \n\nDo not say hello or goodbye. Do not return anything else other than the clean valid JSON string.",
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    print(Fore.GREEN + "Analysis done. Cleaning json list of dependancies . . . ." + Style.RESET_ALL)
    response = chat_session.send_message(json_string)

    #print(response.text)
    return response.text


def load_json(json_string):
    dependencies = json.loads(json_string)

    print(type(dependencies))
    return dependencies

def get_dependancy_list(markdown_file_content):
    generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
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
    system_instruction="You will be provided with a codebase in the form of JSON that contains important code from a git repository for a project. The code is separated by file path and name.\n\nYour task is to analyse this code meticulously and extract a list of all known dependancies. If any of these files exist, extract dependencies from them too:\n\nNode.js (npm, yarn): package.json is the central file.\nPython (pip): requirements.txt is common, but pyproject.toml (using Poetry or Pipenv) is gaining traction.\nJava (Maven, Gradle): pom.xml (Maven) or build.gradle (Gradle) define dependencies.\n.NET (NuGet): .csproj or .vbproj project files list dependencies.\nRuby (RubyGems, Bundler): Gemfile and Gemfile.lock manage dependencies.\nPHP (Composer): composer.json defines project dependencies.\nRust (Cargo): Cargo.toml manages dependencies.\nFlutter/Dart (pub): pubspec.yaml lists dependencies.\n\nAlso cross check import statements to ensure that we have a full list. Where possible extract the version number if it exists.\n\nYou must return a csv of the dependancies along with their known version numbers if known, else just the name and \"unknown\" version will suffice. The csv headers must always be \"dependancy\",\"version\". Here is an example of the CSV that must be returned:\n```\n\"dependancy\",\"version\"\n \"firebase\", \"10.12.0\"\n  \"nuxt\",\"3.11.2\",\n  \"vue\",\"3.4.27\",\n  \"vue-router\", \"unknown\"\n```\n\n\nDo not say hello or goodbye. Do not return anything else other than the csv content. If for whatever reason you do not find any dependancies at all, simply return this exact string: {\"result\": \"NO DEPS FOUND\"}\"",
)

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(markdown_file_content)

    print(response.text)
    #cleanJSON = load_json(response.text)
    #print(cleanJSON)
    return response.text 

   
def get_dependancy_list_with_backoff(markdown_file_content, max_retries=5):
    for attempt in range(max_retries):
        try:
            return get_dependancy_list(markdown_file_content) 
        except DeadlineExceeded:
            sleep_duration = 2**attempt + random.uniform(0, 1)
            print(f"Request timed out. Retrying in {sleep_duration} seconds...")
            time.sleep(sleep_duration)
    print(f"Failed to get Analysis response after {max_retries} retries.")
        # # TODO: write error to a log and use for rettries
    return None


## USE / TEST ##
"""
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
md_file_path = Path(os.path.join(output_dir, "final_TEST.json"))
md_content = md_file_path.read_text()
print(md_content)

#get deps
model_output = get_dependancy_list(md_content)
print(model_output)

#"""
