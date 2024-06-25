import os

def clean_up_files(code_audit_path, vuln_report_path, quality_report_path, final_md_path,vuln_search_path,refactor_html_path, report_html_path, refactor_md_path):
    paths = [code_audit_path, vuln_report_path, quality_report_path, final_md_path,vuln_search_path,refactor_html_path, report_html_path, refactor_md_path]
    
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted: {path}")
        else:
            print(f"File not found: {path}")

"""
# Example usage
uniqueId = "Test_2"  # Replace with your unique ID
code_audit_path = f"/home/trainboxai/backend/rippo/reports/code_audit_{uniqueId}.json"
vuln_report_path = f"/home/trainboxai/backend/rippo/reports/vuln_report_{uniqueId}.json"
quality_report_path = f"/home/trainboxai/backend/rippo/reports/quality_report_{uniqueId}.json"

final_md_path = f"/home/trainboxai/backend/rippo/outputs/final_{uniqueId}.md"
vuln_search_path = f"/home/trainboxai/backend/rippo/outputs/vuln_search_results_{uniqueId}.json"
refactor_html_path = f"/home/trainboxai/backend/rippo/reports/refactor_{uniqueId}.html"
report_html_path = f"/home/trainboxai/backend/rippo/reports/report_{uniqueId}.html"
refactor_md_path = f"/home/trainboxai/backend/rippo/reports/refactor_guide_{uniqueId}.md"

clean_up_files(code_audit_path, vuln_report_path, quality_report_path, final_md_path,vuln_search_path,refactor_html_path, report_html_path, refactor_md_path)
#"""