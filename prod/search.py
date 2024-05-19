from dotenv import load_dotenv
import os
import requests
import json
import time
import random
from scrapper import get_elements_containing_text
from colorama import Fore, Style



load_dotenv()

def search_vulnerabilities(dependencies,unique_id=0):
    # setup
    search_api_key = os.getenv('CUSTOM_SEARCH_API_KEY')
    search_engine_id = "f2954b6edb52b40c7"
    print(Fore.GREEN + "Starting searching for known Vulnerabilities . . . . ." + Style.RESET_ALL)

    results = []
    for dependency in dependencies["dependencies"]:
        name = dependency["name"]
        version = dependency.get("version", "")
        search_query = f"{name} {version}"
        url = f"https://www.googleapis.com/customsearch/v1?key={search_api_key}&cx={search_engine_id}&q={search_query}&num=10&start=1&fields=items(link,snippet,htmlFormattedUrl)" 
        
        retries = 0
        max_retries = 5
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
#dependencies = """{"dependencies": [{"name": "@leafac/rehype-shiki", "version": "^2.2.1"}, {"name": "@mdx-js/loader", "version": "^3.0.0"}, {"name": "@mdx-js/react", "version": "^3.0.0"}, {"name": "@next/mdx", "version": "^14.0.4"}, {"name": "@types/mdx", "version": "^2.0.7"}, {"name": "framer-motion", "version": "^10.15.2"}, {"name": "next", "version": "^14.0.4"}, {"name": "react", "version": "^18.2.0"}, {"name": "react-dom", "version": "^18.2.0"}, {"name": "recma-import-images", "version": "0.0.3"}, {"name": "remark-gfm", "version": "^4.0.0"}, {"name": "remark-rehype-wrap", "version": "0.0.3"}, {"name": "remark-unwrap-images", "version": "^4.0.0"}, {"name": "shiki", "version": "^0.11.1"}, {"name": "tailwindcss", "version": "^3.4.1"}, {"name": "typescript", "version": "^5.3.3"}]}
"""


dependencies = json.loads(dependencies)
vulnerability_results = search_vulnerabilities(dependencies)
print(vulnerability_results)

""" #/
