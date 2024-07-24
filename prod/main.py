from fastapi import FastAPI, HTTPException, Request, APIRouter, Depends, status
from fastapi.responses import RedirectResponse,JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
import uuid
import base64
import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import os
from shared_resources import db, bucket
import firebase_admin
from firebase_admin import credentials, auth, firestore
from dotenv import load_dotenv
from list_repos import list_repositories
from event_logger import write_event_log
from celery_app import celery_app, generate_report, create_test_file
from colorama import Fore, Style
from starlette.responses import HTMLResponse


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
# cred = credentials.Certificate('rippo-777-firebase-adminsdk.json')  
# firebase_admin.initialize_app(cred)

# Storage client using the credentials object
# storage_client = storage.Client.from_service_account_json('rippo-777-firebase-adminsdk.json')
# bucket = storage_client.get_bucket("rippo-777.appspot.com")


# Initialize new log file for report
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'outputs')
reports_dir = os.path.join(script_dir, '..', 'reports')


# Define a Pydantic model for the request body
class RepoUrl(BaseModel):
    repo_url: str

class RepoName(BaseModel):
    repo_name: str

class ReportId(BaseModel):
    report_id: str

class ProjectName(BaseModel):
    project_name: str

class ReportRequest(BaseModel):
    project_name: str
    report_id: str



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
            "oauthAccessToken": oauthToken,
            "credits": 0,
        }
        
        if user_doc.exists:
            existing_data = user_doc.to_dict()
            # Preserve existing credits if already present
            user_data["credits"] = existing_data.get("credits", 0)
            user_ref.update(user_data)
        else:
            user_ref.set(user_data)
        
        return JSONResponse(content={"uid": uid})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid token")


@app.post("/initialize")
async def initialize_project(user_id: str = Depends(get_current_user)):    
    report_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('ascii')[:6]

    log_path = f"{output_dir}/RUN_LOG.log"
    with open(log_path, 'w') as file: 
        file.write('')

  
    # Fetch OAuth token from Firestore
    user_doc = db.collection("users").document(user_id).get()
    oauth_token = user_doc.get("oauthAccessToken")
    if not oauth_token:
        raise HTTPException(status_code=400, detail="OAuth token not found for user")

    # Fetch list of repositories
    repositories = list_repositories(oauth_token)
    num_of_repos = len(repositories) 

    # LOG IT!
    write_event_log(event_id=101, source='/initialize', details=f'Initialization completed for new report {report_id}. Repos found = {num_of_repos}', level='INFO', log_path=log_path )
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


@app.post("/fetch_report_content")
async def fetch_report_content(request: ReportRequest, user_id: str = Depends(get_current_user)):
    """Fetches the HTML content of the report from Firebase storage."""
    
    project_name = request.project_name
    report_id = request.report_id
    
    # Construct the path to the report in the storage bucket
    blob = bucket.blob(f'projects/{user_id}/{project_name}/{report_id}/{report_id}.html')
    
    if not blob.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Download the report content
    report_content = blob.download_as_text()
    
    return HTMLResponse(content=report_content)


@app.post("/get_usage")
async def get_usage(user_id: str = Depends(get_current_user)):
    """Fetches the usage data for the authenticated user."""

    print("Received USER ID:", user_id)

    # Query Firestore for usage data
    usage_docs = db.collection('users').document(user_id).collection('usage').stream()
    
    # Prepare a list of dictionaries with usage data
    usage_data = [{
        'projectName': doc.to_dict().get('projectName'),
        'reportID': doc.to_dict().get('reportID'),
        'date': doc.to_dict().get('date').isoformat() if doc.to_dict().get('date') else None,
        'creditsUsed': doc.to_dict().get('creditsUsed')
    } for doc in usage_docs]

    print("USAGE DATA:", usage_data)

    return {"usage": usage_data}


@app.post("/update_user_credits")
def update_user_credits(user_id: str = Depends(get_current_user)):
    # Firestore query for payments with status "succeeded" and shipping "null"
    payments_ref = db.collection("users").document(user_id).collection("payments")
    query_ref = payments_ref.where("status", "==", "succeeded").where("shipping", "==", None)
    docs = query_ref.stream()

    new_credits = 0
    for doc in docs:
        payment_data = doc.to_dict()
        # Get the amount received from payment so we can add that to credits balance
        amount_received = payment_data.get("amount_received", 0)

        # Get the user doc so we can update credits
        user_doc_ref = db.collection("users").document(user_id)
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            current_credits = user_data.get("credits", 0)
            new_credits = current_credits + amount_received
            user_doc_ref.update({"credits": new_credits})

        # Update shipping status
        doc.reference.update({"shipping": "done"})

    return {"credits": new_credits}



@app.post("/accept_terms")
def accept_terms(user_id: str = Depends(get_current_user)):
    try:
        user_doc_ref = db.collection("users").document(user_id)
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            user_doc_ref.update({"termsAccepted": True})
            return {"message": "Terms accepted successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/master")
async def master(repo_url: RepoUrl, repo_name: RepoName,report_id: ReportId,  user_id: str = Depends(get_current_user)):
  
    # # # MASTER PUPPETIER # # #
    print("Received Project ID:", report_id.report_id)
    print("Received Repo URL:", repo_url.repo_url)
    print("Received Repo NAME:", repo_name.repo_name)

    # ' Initialising directory paths'
    log_path = os.path.join(output_dir, "RUN_LOG.log")
    report_id = report_id.report_id
    repo_name = repo_name.repo_name.replace('/', ':') if '/' in repo_name.repo_name else repo_name.repo_name

    print(Fore.LIGHTYELLOW_EX + "Initialising directory paths . " + Style.RESET_ALL)
    project_path = f"projects/{user_id}/{repo_name}/{report_id}"

    # Create Firebase Storage folder structure
    folder = f"{project_path}/"
    blob = bucket.blob(folder)
    blob.upload_from_string("")

    # Check if upload was successful
    if not blob.exists():
        write_event_log(event_id=202, source='/master', details=f"Failed to create folder: {folder}", level='ERROR', log_path=log_path)
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

       # Create "stats" collection at the same level as "projects"
    stats_ref = db.collection('users').document(user_id).collection('stats').document('statsDoc')
    stats_doc = stats_ref.get()
    if not stats_doc.exists:
        stats_ref.set({
            'reviews': 0,
            'bugs': 0,
            'vulnerabilities': 0
        })

    # get unique id from report_id
    uniqueId = report_id
    write_event_log(event_id=102, source='/master', details=f"New docs creted for user: {user_id} and project:{uniqueId} in master initialisation phase", level='INFO', log_path=log_path )
    
    # Fetch OAuth token from Firestore
    user_doc = db.collection("users").document(user_id).get()
    oauth_token = user_doc.get("oauthAccessToken")
    if not oauth_token:
        raise HTTPException(status_code=400, detail="OAuth token not found for user")


    # TRIGERR BACKEND JOB HERE
    repo_url = repo_url.repo_url
    #"""
        # Add the task to the Celery queue 
    generate_report.delay(
        repo_url, 
        repo_name,
       report_id, 
        user_id,
        oauth_token
    )  
    """
    print(repo_url)
    print(repo_name)
    print(report_id)
    print(user_id)
    print(oauth_token)
    """

    return {"message": "Report request received", "report_id": report_id}, 202



# # # TEST ROUTES HERE # # # 
@app.post("/master_test")
async def master_test():
    create_test_file.delay()  # Enqueue the Celery task
    return {"message": "Test task queued"}
