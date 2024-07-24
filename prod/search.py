from dotenv import load_dotenv
import os
import requests
import json
import time
import random
import csv
import os
import io
from scrapper import get_elements_containing_text
from colorama import Fore, Style



load_dotenv()

def preprocess_csv_data(data):
    return data.replace("{", "").replace("}", "").strip()

def search_vulnerabilities(csv_data, unique_id=0):
    # setup
    search_api_key = os.getenv('CUSTOM_SEARCH_API_KEY')
    search_engine_id = "f2954b6edb52b40c7"
    print(Fore.GREEN + "Starting searching for known Vulnerabilities . . . . ." + Style.RESET_ALL)

    results = []

    csv_data = preprocess_csv_data(csv_data)
    csv_reader = csv.DictReader(io.StringIO(csv_data))
    for row in csv_reader:
        name = row.get("dependancy", "")
        version = row.get("version", "")
        search_query = f"{name} {version}"
        url = f"https://www.googleapis.com/customsearch/v1?key={search_api_key}&cx={search_engine_id}&q={search_query}&num=10&start=1&fields=items(link,snippet,htmlFormattedUrl)" 

        retries = 0
        max_retries = 3
        while retries < max_retries:
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()
                
                scraped_data = []
                if 'items' in data:
                    for item in data['items']:
                        url = item['link']
                        keyword = "vulnerab"
                        relevant_elements = get_elements_containing_text(url, keyword)
                        scraped_data.extend(relevant_elements)

                results.append({
                    "name": name,
                    "version": version,
                    "results": scraped_data,
                    "source": url
                })
                break  # Exit the retry loop if successful

            except requests.exceptions.RequestException as e:
                retries += 1
                wait_time = 2**retries + random.uniform(0, 1)  # Exponential backoff with jitter
                print(f"Request failed, retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)

        if retries == max_retries:
            print(f"Failed to fetch results for {name} {version} after {max_retries} retries.")
            results.append({
                "name": name,
                "version": version,
                "results": "Searchapi, failed",
                "source": url
            })
    
    print(Fore.GREEN + "Completed searching for known Vulnerabilities . . . . ." + Style.RESET_ALL)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'outputs')
    with open(os.path.join(output_dir, f"vuln_search_results_{unique_id}.json"), "w") as f:
        json.dump(results, f, indent=4)        
    return results



""" /
# Example usage
""" # /
#dependencies = """
"dependancy","version"
"@headlessui/react","^1.7.17"
"@headlessui/tailwindcss","^0.2.0"
"@leafac/rehype-shiki","^2.2.1"
"@mdx-js/loader","^3.0.0"
"@next/mdx","^14.0.4"
"@tailwindcss/forms","^0.5.7"
"@vercel/analytics","^1.1.1"
"acorn","^8.11.2"
"acorn-jsx","^5.3.2"
"clsx","^2.0.0"
"escape-string-regexp","^5.0.0"
"framer-motion","^10.16.16"
"next","14.0.4"
"nodemailer","^6.9.13"
"path","^0.12.7"
"react","^18"
"react-dom","^18"
"recma-import-images","^0.0.3"
"remark-gfm","^4.0.0"
"remark-rehype-wrap","^0.0.3"
"remark-unwrap-images","^4.0.0"
"shiki","^0.14.6"
"unified-conditional","^0.0.2"
"@types/node","^20"
"@types/react","^18"
"@types/react-dom","^18"
"autoprefixer","^10.4.16"
"eslint","^8"
"eslint-config-next","14.0.4"
"postcss","^8.4.32"
"tailwindcss","^3.3.6"
"typescript","^5"
"tailwindcss","unknown"
"tailwindcss/defaultTheme","unknown"
"next","unknown"
"next/image","unknown"
"next/link","unknown"
"next/navigation","unknown"
"fast-glob","unknown"
"""
vulnerability_results = search_vulnerabilities(dependencies)
print(vulnerability_results)

#""" #/
