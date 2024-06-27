from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
import os
import json
from pathlib import Path
from manage_storage import upload_to_storage, upload_html
from flattener import extract_and_write_to_markdown
from analyser import get_dependancy_list
from search import search_vulnerabilities
from reporter import code_audit_report_with_backoff,vulnerability_report_with_backoff, quality_report_with_backoff
from recomender import generate_refactor_plan_with_backoff
from update_html_report import update_html_with_json
from clean_up_report_files import clean_up_files
from get_refactor_guide import get_refactor_html_withbackoff
from event_logger import write_event_log
from colorama import Fore, Style
import datetime


celery_app = Celery(
    "rippo_celery_app",  # Replace with a suitable name
    broker="redis://localhost:6379/0",  # Connect to your local Redis instance
)


# Initialize new log file for report
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')




@celery_app.task
def generate_report(repo_url, repo_name, report_id, user_id, oauth_token): 

    
    log_path = os.path.join(output_dir, "RUN_LOG.log")
    # - - - - STEPPING THROUGH WORK - - - - 
    # 1. Get flattened file and extract contents
    print(Fore.GREEN + "Get flattened file and extract contents . . ." + Style.RESET_ALL)
    # Validate repo url
    print(Fore.MAGENTA + "Gathering search results . . ." + Style.RESET_ALL)
    # get unique id from report_id
    uniqueId = report_id
    valid_repo_url = repo_url
    extract_and_write_to_markdown(valid_repo_url,oauth_token, uniqueId )


    # 2. Analyse and extract list of dependancies
        #codebase file
    markdown_file_path = Path(os.path.join(output_dir, f"final_{uniqueId}.md"))
    markdown_file = markdown_file_path.read_text()
    print(Fore.GREEN + "Analyse and extract list of dependancies . . . ." + Style.RESET_ALL)
    #get deps
    deps_list = get_dependancy_list(markdown_file)
    print(deps_list)
    write_event_log(event_id=104, source='analyser.py/get_dependancy_list', details='Analysed and extracted list of dependancies', level='INFO', log_path=log_path )
 

   
    # 3. Search for know Vulnerabilities
    #deps_list = json.loads(deps_list) 
    search_vulnerabilities(deps_list,uniqueId)
    write_event_log(event_id=105, source='search.py/search_vulnerabilities', details='Google searched dor known vulnerabilities', level='INFO', log_path=log_path )
    

    # 4. Create reports for Audit, Quality and Vulns
        # get code audit report
    print(Fore.MAGENTA + "Getting code audit report . . . . . ." + Style.RESET_ALL) 
    code_audit_report_with_backoff(markdown_file,uniqueId)
    write_event_log(event_id=106, source='reporter.py/code_audit_report_with_backoff', details='Code audit completed', level='INFO', log_path=log_path )

        # get vuln report
        # Vulnerability search results
    vuln_results_path = Path(os.path.join(output_dir, f"vuln_search_results_{uniqueId}.json"))
    vulnerability_search_results = vuln_results_path.read_text()    
    print(Fore.MAGENTA + "Getting vulnerability report . . . . . . ." + Style.RESET_ALL)     
    vulnerability_report_with_backoff(vulnerability_search_results,uniqueId)
    write_event_log(event_id=107, source='reporter.py/vulnerability_report_with_backoff', details='Vulnerability report completed', level='INFO', log_path=log_path )

        # get quality report
    code_audit_path = Path(os.path.join(reports_dir ,f'code_audit_{uniqueId}.json'))
    code_audit = code_audit_path.read_text()
    combined_input = f"""

    # # # Codebase below in markdown # # # 
    {markdown_file}

    ==========================================
    # # #  Code Audit report below # # # 
    {code_audit}

    """
    print(Fore.MAGENTA + "Getting quality report . . . . . . ." + Style.RESET_ALL)    
    quality_report_with_backoff(combined_input,uniqueId)
    write_event_log(event_id=108, source='reporter.py/quality_report_with_backoff', details='Code Quality report completed', level='INFO', log_path=log_path )



    # 5. Recommender - generate code refactoring recomendation
    generate_refactor_plan_with_backoff(combined_input,uniqueId) 
    write_event_log(event_id=108, source='reporter.py/generate_refactor_plan_with_backoff', details='Code Refactor Plan completed', level='INFO', log_path=log_path ) 

    # 6.1 Create the HTML report
    template_path = "template.html"
    code_audit_path = f"/home/trainboxai/backend/rippo/reports/code_audit_{uniqueId}.json"
    vuln_report_path = f"/home/trainboxai/backend/rippo/reports/vuln_report_{uniqueId}.json"
    quality_report_path = f"/home/trainboxai/backend/rippo/reports/quality_report_{uniqueId}.json"

    htmlReport = update_html_with_json(template_path, code_audit_path, vuln_report_path, quality_report_path)
    with open(os.path.join(reports_dir, f"report_{uniqueId}.html"), "w") as file:
        file.write(htmlReport)
    #print(htmlReport)

    # 6.2 Convert refactor guide from MD to HTML
    guide_md_file_path = f"/home/trainboxai/backend/rippo/reports/refactor_guide_{uniqueId}.md"
    with open(guide_md_file_path, 'r') as file:
        guide_markdown_file_content = file.read()
    refactor_guide_html = get_refactor_html_withbackoff(guide_markdown_file_content)
    with open(os.path.join(reports_dir, f"refactor_{uniqueId}.html"), "w") as file:
            file.write(refactor_guide_html)


    # 7. Upload files to Firestore Storage
    upload_html(user_id,report_id,repo_name) 


     

    # 8. Cleanup local files
    final_md_path = f"/home/trainboxai/backend/rippo/outputs/final_{uniqueId}.md"
    vuln_search_path = f"/home/trainboxai/backend/rippo/outputs/vuln_search_results_{uniqueId}.json"
    refactor_html_path = f"/home/trainboxai/backend/rippo/reports/refactor_{uniqueId}.html"
    report_html_path = f"/home/trainboxai/backend/rippo/reports/report_{uniqueId}.html"
    refactor_md_path = f"/home/trainboxai/backend/rippo/reports/refactor_guide_{uniqueId}.md"
    html_path = f"/home/trainboxai/backend/rippo/reports/{uniqueId}.html"

    clean_up_files(code_audit_path, vuln_report_path, quality_report_path, final_md_path,vuln_search_path,refactor_html_path, report_html_path, refactor_md_path, html_path)
  


@celery_app.task
def create_test_file():
    with open("test_file_from_celery.txt", "a") as f:  # 'a' for append mode
        f.write(f"Task executed at: {datetime.datetime.now()}\n")