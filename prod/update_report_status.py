
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
            return True
    except Exception as error:
        print(f"Failed to update {report_id} because of {error}")
        return False

def failed_report_status(user_id, report_id, repo_name, reason):
    try:
        # Fetch project path
        user_doc_ref = db.collection('users').document(user_id).collection('projects').document(repo_name)
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            project_paths = user_doc.to_dict().get('project_paths', [])
            updated = False
            for project in project_paths:
                if project.get('report_id') == report_id:
                    project['status'] = 'Failed'
                    project['reason'] = reason
                    updated = True
                    break
            if updated:
                user_doc_ref.update({'project_paths': project_paths})
                print("Project status updated to Failed for:", report_id)

                # Generate the HTML report
                template_path = 'failedReportTemplate.html'
                with open(template_path, 'r') as file:
                    template_content = file.read()

                report_content = template_content.replace('{% reason here %}', reason)
                report_path = os.path.join(reports_dir, f"{report_id}.html")
                with open(report_path, 'w') as file:
                    file.write(report_content)

                print(f"Failed report generated at: {report_path}")
                return True
        print(f"Project with report_id {report_id} not found.")
    except Exception as error:
        print(f"Failed to update {report_id} because of {error}")
    return False

#"""
# Example usage
user_id = "qKtISirBQbftY20mLxK0hWXsD053"
report_id = "SjbNd5"
repo_name = "jerrydav1s:ml-tinkering-blog"
reason = "An error occured. Unable to retrieve vulnerabilities at this time. You will not be charged for this run. Please try again in a short while."
failed_report_status(user_id, report_id, repo_name, reason)
#update_report_status(user_id, report_id, repo_name)
#"""