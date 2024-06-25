import json
from jinja2 import Template
import os


def update_html_with_json(template_path, code_audit_path, vuln_report_path, quality_report_path):
    with open(template_path) as f:
        template = Template(f.read())

    with open(code_audit_path) as f:
        code_audit = json.load(f)

    with open(vuln_report_path) as f:
        vuln_report = json.load(f)

    with open(quality_report_path) as f:
        quality_report = json.load(f)

    rendered_html = template.render(
        code_audit=code_audit, 
        vuln_report=vuln_report, 
        quality_report=quality_report
    )

    print(rendered_html)
    return rendered_html

"""
## Usage

# Initialize new log file for report
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')




template_path = "template.html"
code_audit_path = "/home/trainboxai/backend/rippo/reports/code_audit_Test_2.json"
vuln_report_path = "/home/trainboxai/backend/rippo/reports/vuln_report_Test_2.json"
quality_report_path = "/home/trainboxai/backend/rippo/reports/quality_report_Test_2.json"

htmlReport = update_html_with_json(template_path, code_audit_path, vuln_report_path, quality_report_path)
with open(os.path.join(reports_dir, f"report_1234.html"), "w") as file:
        file.write(htmlReport)
"""