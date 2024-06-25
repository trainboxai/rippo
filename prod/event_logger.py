import datetime
import os


def write_event_log(event_id, source, details, level, log_path):
    if level not in ["INFO", "ERROR"]:
        raise ValueError("Level must be 'INFO' or 'ERROR'")
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp}  ·  Event ID:{event_id}  ·  Source:{source}  ·  Details:{details}  ·  Level:{level}\n"
    
    with open(log_path, 'a') as log_file:
        log_file.write(log_entry)

# Example usage:
"""
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')

report_id = "syTCEF"
log_path = f"{output_dir}/{report_id}.log"

write_event_log(event_id=101, source='SELF', details='TEST: An error occurred.', level='ERROR', log_path=log_path )

 write_event_log(event_id=103, source='flattener.py/extract_and_write_to_markdown', details=f'File creared final_{unique_id}.md.', level='INFO', log_path=log_path )
#"""