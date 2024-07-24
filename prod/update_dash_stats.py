import json
import os
from shared_resources import db

# Initialize new log file for report
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')

# Function to count findings in code_audit.json
def count_findings(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        high = len(data.get("High", []))
        medium = len(data.get("Medium", []))
        low = len(data.get("Low", []))
        total_findings = high + medium + low
        return total_findings

# Function to count vulnerabilities in vuln_report.json
def count_vulnerabilities(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        vulnerabilities = len(data.get("vulnerability_report", []))
        return vulnerabilities

def update_dashboard_stats(user_id, repo_name, findings_count, vulnerabilities_count):
    try:
        print("Checking Dashboard Stats")
        user_doc_ref = db.collection('users').document(user_id).collection('projects').document(repo_name)
        print(f"Document path: users/{user_id}/projects/{repo_name}")
        user_doc = user_doc_ref.get()
        
        if user_doc.exists:
            print(f"Project {repo_name} found")
            project_paths = user_doc.to_dict().get('project_paths', [])
            
            if len(project_paths) < 2:
                stats_ref = db.collection('users').document(user_id).collection('stats').document('statsDoc')
                stats_doc = stats_ref.get()
                
                if stats_doc.exists:
                    current_data = stats_doc.to_dict()
                    current_bugs = current_data.get('bugs', 0)
                    current_vulnerabilities = current_data.get('vulnerabilities', 0)
                    
                    stats_ref.update({
                        'bugs': current_bugs + findings_count,
                        'vulnerabilities': current_vulnerabilities + vulnerabilities_count
                    })
                else:
                    stats_ref.set({
                        'bugs': findings_count,
                        'vulnerabilities': vulnerabilities_count
                    })
        else:
            print(f"ERROR: Project {repo_name} NOT found!!")

        # Compute the total number of reports executed
        total_reports = 0
        projects_ref = db.collection('users').document(user_id).collection('projects')
        projects = projects_ref.get()

        for project in projects:
            project_paths = project.to_dict().get('project_paths', [])
            total_reports += len(project_paths)

        print(f"Total reports executed so far: {total_reports}")
        stats_ref = db.collection('users').document(user_id).collection('stats').document('statsDoc')
        stats_ref.update({
            'reviews': total_reports
        })
        return True
    except Exception as error:
        print(f"Failed to update dashboard stats because of {error}")
        return False






"""
 ## EXAMPLE USAGE       
# Paths to the JSON files
code_audit_file = '/home/trainboxai/backend/rippo/reports/code_audit_1PtimI.json'
vuln_report_file = '/home/trainboxai/backend/rippo/reports/vuln_report_1PtimI.json'

# Count the findings and vulnerabilities
findings_count = count_findings(code_audit_file)
vulnerabilities_count = count_vulnerabilities(vuln_report_file)


# Update the dashboard stats if the project is being run for the first time
user_id = "TFUaoW4iBPUe297vr3vk36Mvp2p2"  # Replace with the actual user ID
repo_name = "trainboxai:trainbox-company-site"  # Replace with the actual repository name
update_dashboard_stats(user_id, repo_name, findings_count, vulnerabilities_count)

# Print the counts
print(f"Number of Bugs & Issues: {findings_count}")
print(f"Number of vulnerabilities: {vulnerabilities_count}")

#"""