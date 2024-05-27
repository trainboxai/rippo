from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse,JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
import uuid
import requests
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore
from dotenv import load_dotenv
from pathlib import Path
from flattener import extract_and_write_to_markdown
from analyser import get_dependancy_list
from search import search_vulnerabilities
from reporter import code_audit_report_with_backoff,vulnerability_report_with_backoff, quality_report_with_backoff
from recomender import generate_refactor_plan_with_backoff
from colorama import Fore, Style

app = FastAPI()
load_dotenv()

# Configure CORS
origins = [
    "http://localhost:3000",  # Your frontend URL
    "https://rippo.trainbox.ai"  # Your production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GitHub OAuth credentials
middleware_secret = os.getenv("MIDDLEWARE_SECRET")
app.add_middleware(SessionMiddleware, secret_key=middleware_secret)
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
FIREBASE_AUTH_HANDLER_URL = 'https://rippo-777.firebaseapp.com/__/auth/handler' 
# FIREBASE
cred = credentials.Certificate('rippo-777-firebase-adminsdk.json')  
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define a Pydantic model for the request body
class RepoUrl(BaseModel):
    repo_url: str

class RepoUrltest(BaseModel):
    repo_url_test: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Rippo API!"}


@app.post("/verify-token")
async def verify_token(request: Request):
    body = await request.json()
    token = body.get('token')
    email = body.get('email')
    displayName = body.get('displayName')
    photoUrl = body.get('photoUrl')
    
    if not token:
        raise HTTPException(status_code=400, detail="Token missing")
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()
        
        user_data = {
            "token": token,
            "email": email,
            "displayName": displayName,
            "photoUrl": photoUrl
        }
        
        
        if user_doc.exists:
            user_ref.update(user_data)
        else:
            user_ref.set(user_data)
        
        return JSONResponse(content={"uid": uid})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid token")


@app.post("/initialize")
# given a URL do stuff





@app.post("/master")
async def master(repo_url: RepoUrl):
    # # # MASTER PUPPETIER # # #
   
    #' Initialising directory paths'
    print(Fore.LIGHTYELLOW_EX + "Initialising directory paths . " + Style.RESET_ALL)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'outputs')
    reports_dir = os.path.join(script_dir, '..', 'reports')

    # generate unique id
    uniqueId = uuid.uuid4()


    # - - - - STEPPING THROUGH WORK - - - - TODO - backoff and jitter for all LLM calls
    # 1. Get flattened file and extract contents
    print(Fore.GREEN + "Get flattened file and extract contents . . ." + Style.RESET_ALL)
    # Validate repo url
    print(Fore.MAGENTA + "Gathering search results . . ." + Style.RESET_ALL)
    if "github.com" not in repo_url.repo_url:  #TODO: when we add support for other git repos, change this!!
        raise HTTPException(status_code=400, detail="URL provided is not a GitHub repository.")
    else:
        valid_repo_url = repo_url.repo_url

    extract_and_write_to_markdown(valid_repo_url, uniqueId)


    # 2. Analyse and extract list of dependancies
        #codebase file
    markdown_file_path = Path(os.path.join(output_dir, f"final_{uniqueId}.md"))
    markdown_file = markdown_file_path.read_text()
    print(Fore.GREEN + "Analyse and extract list of dependancies . . . ." + Style.RESET_ALL)
    #get deps
    deps_list = get_dependancy_list(markdown_file)
    print(deps_list)
 
   
    # 3. Search for know Vulnerabilities
    deps_list = json.loads(deps_list) 
    search_vulnerabilities(deps_list,uniqueId)
    

    # 4. Create reports for Audit, Quality and Vulns
        # get code audit report
    print(Fore.MAGENTA + "Getting code audit report . . . . . ." + Style.RESET_ALL) 
    code_audit_report_with_backoff(markdown_file,uniqueId)

        # get vuln report
        # Vulnerability search results
    vuln_results_path = Path(os.path.join(output_dir, f"vuln_search_results_{uniqueId}.json"))
    vulnerability_search_results = vuln_results_path.read_text()    
    print(Fore.MAGENTA + "Getting vulnerability report . . . . . . ." + Style.RESET_ALL)     
    vulnerability_report_with_backoff(vulnerability_search_results,uniqueId)

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



    # 5. Recommender - generate code refactoring recomendation
    generate_refactor_plan_with_backoff(combined_input,uniqueId)  




#TODO - create route to deal with file cleanup, could be initiated by the frontend


