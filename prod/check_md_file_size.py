import os

def get_file_size(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / (1024 * 1024)  # Convert bytes to MB
    return size_in_mb

# Example usage
file_path = '/home/trainboxai/backend/rippo/outputs/final_xaDc_9.md'
size = get_file_size(file_path)
print(f"The size of the file is {size:.2f} MB.")