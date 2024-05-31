from fastapi import FastAPI, HTTPException, Request, APIRouter, Depends, status
from fastapi.responses import RedirectResponse,JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
import uuid
import base64
import requests
import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import os
import json
from google.cloud import firestore, storage
import firebase_admin
from firebase_admin import credentials, auth, firestore
from dotenv import load_dotenv
from pathlib import Path
from flattener import extract_and_write_to_markdown
from analyser import get_dependancy_list
from search import search_vulnerabilities
from list_repos import list_repositories
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

# Storage client using the credentials object
storage_client = storage.Client.from_service_account_json('rippo-777-firebase-adminsdk.json')
bucket = storage_client.get_bucket("rippo-777.appspot.com")


# Define a Pydantic model for the request body
class RepoUrl(BaseModel):
    repo_url: str

class RepoName(BaseModel):
    repo_name: str

class ReportId(BaseModel):
    report_id: str

class ProjectName(BaseModel):
    project_name: str



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function to get the current user from the Firebase ID token.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) 


@app.get("/")
async def root():
    return {"message": "Welcome to the Rippo API!"}


@app.post("/verify-token")
async def verify_token(request: Request):
    body = await request.json()
    token = body.get('token')
    oauthToken = body.get('oauthToken')
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
            "photoUrl": photoUrl,
            "oauthAccessToken": oauthToken
        }
        
        
        if user_doc.exists:
            user_ref.update(user_data)
        else:
            user_ref.set(user_data)
        
        return JSONResponse(content={"uid": uid})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid token")


@app.post("/initialize")
async def initialize_project(user_id: str = Depends(get_current_user)):
    #print("User ID:", user_id) 
    #print(bucket)
    
    report_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('ascii')[:6]
  
    # Fetch OAuth token from Firestore
    user_doc = db.collection("users").document(user_id).get()
    oauth_token = user_doc.get("oauthAccessToken")
    if not oauth_token:
        raise HTTPException(status_code=400, detail="OAuth token not found for user")

    # Fetch list of repositories
    repositories = list_repositories(oauth_token)

    return {"ReportId": report_id, "Repositories": repositories}


@app.post("/fetch_projects")
async def fetch_projects(user_id: str = Depends(get_current_user)):
    """Fetches the list of projects (repo names) for the authenticated user."""

    print("Received USER ID:", user_id)

    # Query Firestore for projects
    project_docs = db.collection('users').document(user_id).collection('projects').stream()
    
    # Prepare a list of dictionaries with project name and last updated time
    projects = [{
        'name': doc.id,
        'last_updated': doc.to_dict().get('last_updated').isoformat() if doc.to_dict().get('last_updated') else None
    } for doc in project_docs]

    print("PROJECT DATA:", projects)

    return {"projects": projects}



@app.post("/fetch_reports")
async def fetch_reports(project_name: ProjectName, user_id: str = Depends(get_current_user)):
    """Fetches the list of reports for the authenticated user and given project name."""

    print("Received USER ID:", user_id)
    print("Received PROJECT_NAME:", project_name.project_name)

    # Query Firestore for the specified project
    project_ref = db.collection('users').document(user_id).collection('projects').document(project_name.project_name)
    project_doc = project_ref.get()

    if not project_doc.exists:
        return {"error": "Project not found"}, 404

    project_data = project_doc.to_dict()
    reports = project_data.get('project_paths', [])

    # Prepare the reports list
    reports_list = [{
        'created_at': report['created_at'].isoformat(),
        'path': report['path'],
        'report_id': report['report_id'],
        'created_by': report['created_by'],
        'status': report['status']
    } for report in reports] if reports else []

    print("REPORTS:", reports_list)

    return {"reports": reports_list}



@app.post("/master")
async def master(repo_url: RepoUrl, repo_name: RepoName,report_id: ReportId,  user_id: str = Depends(get_current_user)):
    print("Received Project ID:", report_id.report_id)
    print("Received Repo URL:", repo_url.repo_url)
    print("Received Repo NAME:", repo_name.repo_name)

    # # # MASTER PUPPETIER # # #

    # ' Initialising directory paths'
    report_id = report_id.report_id
    repo_name = repo_name.repo_name.replace('/', ':') if '/' in repo_name.repo_name else repo_name.repo_name

    print(Fore.LIGHTYELLOW_EX + "Initialising directory paths . " + Style.RESET_ALL)
    project_path = f"projects/{user_id}/{repo_name}/{report_id}"

    # Create Firebase Storage folder structure
    for folder in ["code_audit.json", "quality_report.json", "vulnerability_report.json", "refactor_guide.md"]:
        blob = bucket.blob(f"{project_path}/{folder}")
        blob.upload_from_string("")

        # Check if upload was successful
        if not blob.exists():
            raise HTTPException(status_code=500, detail=f"Failed to create folder: {folder}")
    

     # Get the display name of the user
    user_doc = db.collection('users').document(user_id).get()
    display_name = user_doc.to_dict().get('displayName', 'Unknown User')

    # Firestore document reference
    doc_ref = db.collection('users').document(user_id).collection('projects').document(repo_name)

    # Append project path to an array in the Firestore document
    doc_ref.set({
        'last_updated':datetime.datetime.utcnow(),
        'project_paths': firestore.ArrayUnion([{
            'report_id': report_id,
            'path': project_path,
            'created_at': datetime.datetime.utcnow(),
            'created_by': display_name,
            'status': 'In progress',
        }])
    }, merge=True)

    # get unique id from report_id
    uniqueId = report_id

    return uniqueId











@app.post("/master_continuesd")
async def master_continued(repo_url: RepoUrl):


 # get unique id from report_id
    uniqueId = 123
    output_dir = "dummy"
    reports_dir = "dummy"
    # - - - - STEPPING THROUGH WORK - - - - 
    # 1. Get flattened file and extract contents
    print(Fore.GREEN + "Get flattened file and extract contents . . ." + Style.RESET_ALL)
    # Validate repo url
    print(Fore.MAGENTA + "Gathering search results . . ." + Style.RESET_ALL)

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


