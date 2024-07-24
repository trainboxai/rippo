import json

def generate_folder_structure_html(flat_json_path, output_md_path):
    # Read the JSON data from the file
    with open(flat_json_path, 'r') as file:
        json_data = json.load(file)
    
    # Function to build folder structure from JSON data
    def build_folder_structure(data):
        root = {}
        for file in data:
            parts = file['filePath'].split('/')
            current = root
            for index, part in enumerate(parts):
                if part not in current:
                    current[part] = {} if index < len(parts) - 1 else None
                current = current[part]
        return root

    # Function to generate HTML from folder structure
    def generate_html(folder_structure):
        def generate_html_recursive(obj, indent=0):
            html = '<ul class="pl-4">'
            for key, value in obj.items():
                if value is None:
                    html += f'<li class="text-blue-500">{key}</li>'
                else:
                    html += f'<li class="font-bold">{key}</li>'
                    html += generate_html_recursive(value, indent + 1)
            html += '</ul>'
            return html
        return generate_html_recursive(folder_structure)

    # Build the folder structure
    folder_structure = build_folder_structure(json_data)

    # Generate the HTML
    html_output = generate_html(folder_structure)

    # Write the HTML output to the specified Markdown file
    with open(output_md_path, 'w') as file:
        file.write(html_output)

# Specify the paths
flat_json_path = "/home/trainboxai/backend/rippo/outputs/final_TEST.json"
output_md_path = "/home/trainboxai/backend/rippo/outputs/folder_structure.md"

# Generate the folder structure HTML
generate_folder_structure_html(flat_json_path, output_md_path)
