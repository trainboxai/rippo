import json
import math

import math
import json

def split_markdown_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    chunk_size = math.ceil(len(content) / 10)
    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    chunk_data = [{'chunk#': i + 1, 'data': chunk} for i, chunk in enumerate(chunks)]
    
    with open('/home/trainboxai/backend/rippo/outputs/test_chunks.json', 'w') as json_file:
        json.dump(chunk_data, json_file, indent=2)

# Replace 'your_markdown_file.md' with the path to your markdown file
md_file_path = "/home/trainboxai/backend/rippo/outputs/final_test.md"
split_markdown_file(md_file_path )