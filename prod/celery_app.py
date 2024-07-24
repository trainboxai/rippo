from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
import os
import json
import time
from pathlib import Path
from manage_storage import upload_failed_report_html, upload_html
from flattener import extract_and_write_to_markdown
from analyser import get_dependancy_list_with_backoff
from search import search_vulnerabilities
from reporter import code_audit_report_with_backoff,vulnerability_report_with_backoff, quality_report_with_backoff
from recomender import generate_refactor_plan_with_backoff
from update_html_report import update_html_with_json
from clean_up_report_files import clean_up_files
from get_refactor_guide import get_refactor_html_withbackoff
from event_logger import write_event_log
from update_report_status import update_report_status, failed_report_status
from update_dash_stats import count_findings,count_vulnerabilities,update_dashboard_stats
from update_credits_usage import update_usage
from colorama import Fore, Style
import datetime



celery_app = Celery(
    "rippo_celery_app",  # Replace with a suitable name
    broker="redis://localhost:6379/0",  # Connect to your local Redis instance
)


# Initialize folder paths
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')




@celery_app.task
def generate_report(repo_url, repo_name, report_id, user_id, oauth_token): 
    log_path = os.path.join(output_dir, "RUN_LOG.log")
    
    try:
        # 1. Get flattened file and extract contents
        print(Fore.GREEN + "Get flattened file and extract contents . . ." + Style.RESET_ALL)
        print(Fore.MAGENTA + "Gathering search results . . ." + Style.RESET_ALL)
        uniqueId = report_id
        valid_repo_url = repo_url
        
        try:
            extract_and_write_to_markdown(valid_repo_url, oauth_token, uniqueId)
        except Exception as e:
            reason = "Failed to extract code. You will not be charged for this run. Please check that this repository exists and try again in a short while " 
            failed_report_status(user_id, report_id, repo_name, reason)
            raise

        markdown_file_path = Path(os.path.join(output_dir, f"final_{uniqueId}.md"))
        if not markdown_file_path.exists():
            reason = "Unable to access repository. You will not be charged for this run. Please check that this repository exists and try again in a short while."
            failed_report_status(user_id, report_id, repo_name, reason)
            raise

        # 2. Analyse and extract list of dependencies
        try:
            markdown_file = markdown_file_path.read_text()
            print(Fore.GREEN + "Analyse and extract list of dependencies . . ." + Style.RESET_ALL)
            deps_list = get_dependancy_list_with_backoff(markdown_file)
            print(deps_list)
            write_event_log(event_id=104, source='analyser.py/get_dependancy_list', details='Analysed and extracted list of dependencies', level='INFO', log_path=log_path)
        except Exception as e:
            reason = "Failed to analyze and extract dependencies. You will not be charged for this run. Please try again in a short while. " 
            failed_report_status(user_id, report_id, repo_name, reason)
            raise

        time.sleep(5)
        
        # 3. Search for known vulnerabilities
        try:
            search_vulnerabilities(deps_list, uniqueId)
            write_event_log(event_id=105, source='search.py/search_vulnerabilities', details='Google searched for known vulnerabilities', level='INFO', log_path=log_path)
        except Exception as e:
            reason = "Failed to search for known vulnerabilities. You will not be charged for this run. Please try again in a short while. " 
            failed_report_status(user_id, report_id, repo_name, reason)
            raise

        time.sleep(5)
        
        # 4. Create reports for Audit, Quality, and Vulnerabilities
        try:
            print(Fore.MAGENTA + "Getting code audit report . . ." + Style.RESET_ALL)
            code_audit_report_with_backoff(markdown_file, uniqueId)
            write_event_log(event_id=106, source='reporter.py/code_audit_report_with_backoff', details='Code audit completed', level='INFO', log_path=log_path)
        except Exception as e:
            reason = "Failed to get code audit report. You will not be charged for this run. Please try again in a short while. " 
            failed_report_status(user_id, report_id, repo_name, reason)
            raise

        time.sleep(5)

        try:
            vuln_results_path = Path(os.path.join(output_dir, f"vuln_search_results_{uniqueId}.json"))
            vulnerability_search_results = vuln_results_path.read_text()
            print(Fore.MAGENTA + "Getting vulnerability report . . ." + Style.RESET_ALL)
            vulnerability_report_with_backoff(vulnerability_search_results, uniqueId)
            write_event_log(event_id=107, source='reporter.py/vulnerability_report_with_backoff', details='Vulnerability report completed', level='INFO', log_path=log_path)
        except Exception as e:
            reason = "Failed to get vulnerability report. You will not be charged for this run. Please try again in a short while. " 
            failed_report_status(user_id, report_id, repo_name, reason)
            raise

        time.sleep(5)

        try:
            code_audit_path = Path(os.path.join(reports_dir, f'code_audit_{uniqueId}.json'))
            code_audit = code_audit_path.read_text()
            combined_input = f"""
            # # # Codebase below in markdown # # # 
            {markdown_file}
            ==========================================
            # # #  Code Audit report below # # # 
            {code_audit}
            """
            print(Fore.MAGENTA + "Getting quality report . . ." + Style.RESET_ALL)
            quality_report_with_backoff(combined_input, uniqueId)
            write_event_log(event_id=108, source='reporter.py/quality_report_with_backoff', details='Code Quality report completed', level='INFO', log_path=log_path)
        except Exception as e:
            reason = "Failed to get quality report. You will not be charged for this run. Please try again in a short while. " 
            failed_report_status(user_id, report_id, repo_name, reason)
            raise

        time.sleep(5)

        # 5. Recommender - generate code refactoring recommendation
        try:
            generate_refactor_plan_with_backoff(combined_input, reports_dir, uniqueId)
            write_event_log(event_id=109, source='reporter.py/generate_refactor_plan_with_backoff', details='Code Refactor Plan completed', level='INFO', log_path=log_path)
        except Exception as e:
            reason = "Failed to generate refactor plan. You will not be charged for this run. Please try again in a short while. " 
            failed_report_status(user_id, report_id, repo_name, reason)
            raise

        # 6.1 Create the HTML report
        try:
            template_path = "template.html"
            code_audit_path = f"/home/trainboxai/backend/rippo/reports/code_audit_{uniqueId}.json"
            vuln_report_path = f"/home/trainboxai/backend/rippo/reports/vuln_report_{uniqueId}.json"
            quality_report_path = f"/home/trainboxai/backend/rippo/reports/quality_report_{uniqueId}.json"
            htmlReport = update_html_with_json(template_path, code_audit_path, vuln_report_path, quality_report_path)
            with open(os.path.join(reports_dir, f"report_{uniqueId}.html"), "w") as file:
                file.write(htmlReport)
        except Exception as e:
            reason = "Failed to create HTML report. You will not be charged for this run. Please try again in a short while. " 
            failed_report_status(user_id, report_id, repo_name, reason)
            raise

        time.sleep(5)

        # 6.2 Convert refactor guide from MD to HTML
        try:
            default_refactor_guide_html = "<p> Refactor Report missing. Click below to fetch it. </p>"
            guide_md_file_path = f"/home/trainboxai/backend/rippo/reports/refactor_guide_{uniqueId}.md"
            with open(guide_md_file_path, 'r') as file:
                guide_markdown_file_content = file.read()
            refactor_guide_html = get_refactor_html_withbackoff(guide_markdown_file_content)
            if refactor_guide_html is None:
                refactor_guide_html = default_refactor_guide_html
            with open(os.path.join(reports_dir, f"refactor_{uniqueId}.html"), "w") as file:
                file.write(refactor_guide_html)
        except Exception as e:
            reason = "Failed to convert refactor guide from MD to HTML. You will not be charged for this run. Please try again in a short while. " 
            failed_report_status(user_id, report_id, repo_name, reason)
            raise
    
    except Exception as general_error:
        upload_failed_report_html(user_id, report_id, repo_name)
        print(f"An unexpected during steps 1 to 6 occurred: {general_error}")
        return

    
    # 7. Upload files to Firestore Storage
    upload_html(user_id,report_id,repo_name) 

    # 8. Update report status
    print("Updating report status")
    update_report_status(user_id, report_id, repo_name)
    print("Report status updated")


    # 9. Update Dashboard Stats
    # Count the findings and vulnerabilities
    findings_count = count_findings(code_audit_path)
    vulnerabilities_count = count_vulnerabilities(vuln_report_path)

    print("Updating dashboard status")
    update_dashboard_stats(user_id, repo_name, findings_count, vulnerabilities_count)
    print("Dashboard status updated")


    # 10. Update usage and credits
    print("Updating credits and usage")
    update_usage(user_id, repo_name, report_id )
    print("Credits and usage done")


    # 11. Cleanup local files
    final_md_path = os.path.join(output_dir, f"final_{uniqueId}.md")
    vuln_search_path = os.path.join(output_dir, f"vuln_search_results_{uniqueId}.json")
    refactor_html_path = os.path.join(reports_dir, f"refactor_{uniqueId}.html")
    report_html_path = os.path.join(reports_dir, f"report_{uniqueId}.html")
    refactor_md_path = os.path.join(reports_dir, f"refactor_guide_{uniqueId}.md")
    html_path = os.path.join(reports_dir, f"{uniqueId}.html")

    clean_up_files(code_audit_path, vuln_report_path, quality_report_path, final_md_path,vuln_search_path,refactor_html_path, report_html_path, refactor_md_path, html_path)


  
