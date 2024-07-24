import os
import tempfile
import json
from git import Repo, Git
from event_logger import write_event_log


# # # # # F U N C T I O N S # # # # #
def extract_and_write_to_json(repo_url, oauth_token, unique_id=0):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        auth_repo_url = repo_url.replace('https://', f'https://{oauth_token}@')
        Repo.clone_from(auth_repo_url, temp_dir)
        json_data = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith("package-lock.json") or file_path.endswith("yarn.lock") or "README.md" in file_path or ".git" in file_path or "fonts" in file_path or os.path.basename(os.path.dirname(file_path)) == "fonts":
                    continue
                _, ext = os.path.splitext(file_path)
                if ext.lower() in ['.jpg', '.jpeg', '.ico', '.png', '.gif', '.svg', '.bmp', '.ttf', '.otf', '.woff', '.woff2']:
                    continue
                try:
                    with open(file_path, "r") as f:
                        file_content = f.read()
                    json_data.append({
                        "filePath": file_path[len(temp_dir)+1:],
                        "data": file_content
                    })
                except UnicodeDecodeError:
                    print(f"Skipping file: {file_path} (not a valid UTF-8 text file)")
        
        with open(os.path.join(output_dir, f"final_{unique_id}.json"), "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        
        log_path = os.path.join(output_dir, "RUN_LOG.log")
        write_event_log(event_id=103, source='flattener.py/extract_and_write_to_json', details=f'JSON file created final_{unique_id}.json.', level='INFO', log_path=log_path)




def extract_and_write_to_markdown(repo_url,oauth_token ,unique_id=0 ):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        auth_repo_url = repo_url.replace('https://', f'https://{oauth_token}@')
        Repo.clone_from(auth_repo_url, temp_dir)
        with open(os.path.join(output_dir, f"final_{unique_id}.md"), "w") as md_file:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.endswith("package-lock.json") or file_path.endswith("yarn.lock") or "README.md" in file_path or ".git" in file_path or "fonts" in file_path or os.path.basename(os.path.dirname(file_path)) == "fonts":
                        continue
                    _, ext = os.path.splitext(file_path)
                    if ext.lower() in ['.jpg', '.jpeg', '.ico', '.png', '.gif', '.svg', '.bmp', '.ttf', '.otf', '.woff', '.woff2']:
                        continue
                    try:
                        with open(file_path, "r") as f:
                            file_content = f.read()
                        md_file.write(f"# {file_path[len(temp_dir)+1:]}\n")
                        md_file.write("```\n")
                        md_file.write(file_content)
                        md_file.write("\n```\n\n")

                    except UnicodeDecodeError:
                        print(f"Skipping file: {file_path} (not a valid UTF-8 text file)")

        log_path = os.path.join(output_dir, "RUN_LOG.log")
        write_event_log(event_id=103, source='flattener.py/extract_and_write_to_markdown', details=f'Markdown file created final_{unique_id}.md.', level='INFO', log_path=log_path )



# # #  MAIN # # # 
"""
valid_repo_url = "https://github.com/Digimonger/upscalerlabs.git"
oauth_token = "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"
uniqueId = "TEST"
#usage
#extract_and_write_to_markdown(valid_repo_url,oauth_token, uniqueId )
extract_and_write_to_json(valid_repo_url,oauth_token, uniqueId )
#"""