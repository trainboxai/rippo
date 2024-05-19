import os
import tempfile
from git import Repo


# # # # # F U N C T I O N S # # # # #
def extract_and_write_to_markdown(repo_url,unique_id=0):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        Repo.clone_from(repo_url, temp_dir)
        with open(os.path.join(output_dir, f"final_{unique_id}.md"), "w") as md_file:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.endswith("package-lock.json") or file_path.endswith("yarn.lock") or "README.md" in file_path or  ".git" in file_path or "fonts" in file_path or os.path.basename(os.path.dirname(file_path)) == "fonts":
                        continue
                    _, ext = os.path.splitext(file_path)
                    if ext.lower() in ['.jpg', '.jpeg','.ico',  '.png', '.gif', '.svg', '.bmp', '.ttf', '.otf', '.woff', '.woff2']:
                        continue
                    #print("file found, processing . . :", file_path)
                    try:
                        with open(file_path, "r") as f:
                            file_content = f.read()
                        md_file.write(f"# {file_path[len(temp_dir)+1:]}\n")
                        md_file.write("```\n")
                        md_file.write(file_content)
                        md_file.write("\n```\n\n")
                    except UnicodeDecodeError:
                        print(f"Skipping file: {file_path} (not a valid UTF-8 text file)")






# # #  MAIN # # # 
#repo_url = "git@github.com-trainbox:trainboxai/trainbox-company-site.git"


#usage
#extract_and_write_to_markdown(repo_url)
