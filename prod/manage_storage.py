# manage_storage.py

import os
from shared_resources import db, bucket
# Initialize new log file for report
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')

def upload_to_storage(user_id, report_id, repo_name):
    # fetch project path
    user_doc = db.collection('users').document(user_id).collection('projects').document(repo_name).get()
    if user_doc.exists:
        project_paths = user_doc.to_dict().get('project_paths', [])
        for project in project_paths:
            if project.get('report_id') == report_id:
                project_path = project.get('path')
                print("Uploading files to:", project_path)

                # Upload files to Firebase Storage
                local_files = [f"code_audit_{report_id}.json", f"quality_report_{report_id}.json", f"vuln_report_{report_id}.json", f"refactor_guide_{report_id}.md"]
                for file_name in local_files:
                    blob = bucket.blob(f"{project_path}/{file_name}")
                    with open(os.path.join(reports_dir, file_name), 'rb') as file_data:
                        blob.upload_from_file(file_data, content_type='application/octet-stream')
                        print(f"Uploaded {file_name} to {project_path}/{file_name}")
                break
        

def upload_html(user_id, report_id, repo_name):
    # fetch project path
    user_doc = db.collection('users').document(user_id).collection('projects').document(repo_name).get()
    if user_doc.exists:
        project_paths = user_doc.to_dict().get('project_paths', [])
        for project in project_paths:
            if project.get('report_id') == report_id:
                project_path = project.get('path')
                print("Uploading HTML to:", project_path)

                # Combine HTML files
                report_file = os.path.join(reports_dir, f"report_{report_id}.html")
                refactor_file = os.path.join(reports_dir, f"refactor_guide_{report_id}.html")
                combined_html = os.path.join(reports_dir, f"{report_id}.html")

                with open(report_file, 'r') as report, open(refactor_file, 'r') as refactor, open(combined_html, 'w') as combined:
                    combined.write(report.read())
                    combined.write(refactor.read())

                # Upload combined HTML to Firebase Storage
                blob = bucket.blob(f"{project_path}/{report_id}.html")
                with open(combined_html, 'rb') as file_data:
                    blob.upload_from_file(file_data, content_type='text/html')
                    print(f"Uploaded {report_id}.html to {project_path}/{report_id}.html")