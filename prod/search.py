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



""" #/
# Example usage
""" # /
#dependencies = """
"dependancy","version"
"autoprefixer","^10.4.17",
"@headlessui/vue","^1.7.19",
"@heroicons/vue","^2.1.3",
"@tailwindcss/forms","^0.5.7",
"axios","^1.6.8",
"nuxt","^3.9.3",
"postcss","^8.4.33",
"tailwindcss","^3.4.1",
"tailwindcss-text-fill-stroke","^1.1.2",
"vue","^3.4.14",
"vue-router","^4.2.5"

"""
vulnerability_results = search_vulnerabilities(dependencies)
print(vulnerability_results)

""" #/
