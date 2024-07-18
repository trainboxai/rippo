
import os
from shared_resources import db

# Initialize new log file for report
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')

def update_report_status(user_id, report_id, repo_name):
    try:
        # Fetch project path
        user_doc_ref = db.collection('users').document(user_id).collection('projects').document(repo_name)
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            project_paths = user_doc.to_dict().get('project_paths', [])
            for index, project in enumerate(project_paths):
                if project.get('report_id') == report_id:
                    project_paths[index]['status'] = 'Completed'
                    break
            user_doc_ref.update({'project_paths': project_paths})
            print("Project status updated to Completed for:", report_id)
    except Exception as error:
        print(f"Failed to update {report_id} because of {error}")


"""
# Example usage
user_id = "TFUaoW4iBPUe297vr3vk36Mvp2p2"
report_id = "kTNKXQ"
repo_name = "trainboxai:trainbox-company-site"

update_report_status(user_id, report_id, repo_name)
#"""