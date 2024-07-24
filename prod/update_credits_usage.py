import json
import os
import requests
from shared_resources import db
from datetime import datetime


def calculate_credits_used(repo_size_kb):
    # Calculate credits based on 25000 KB increments
    return ((repo_size_kb - 1) // 25000 + 1) * 10

# Function to update the usage collection
def update_usage(user_id, repo_name, report_id):
    # Check if the user_id exists
    user_doc_ref = db.collection('users').document(user_id)
    user_doc = user_doc_ref.get()

    if user_doc.exists:
        # Calculate repo size
        oauth_token = user_doc.get("oauthAccessToken")
        repo_name = repo_name.replace(":", "/")
        repo_size = get_repository_size(oauth_token, repo_name).get("Size")
        print("REPO SIZE", repo_size)
        
        # Calculate credits used based on size
        credits_used = calculate_credits_used(repo_size)
        print("Credits used",  credits_used)

        user_data = user_doc.to_dict()
        current_credits = user_data.get('credits', 0)

        if current_credits >= credits_used:
            new_credits = current_credits - credits_used
            usage_data = {
                'projectName': repo_name,
                'reportID': report_id,
                'date': datetime.utcnow(),
                'repoSize': repo_size,
                'creditsUsed': credits_used
            }

            # Reference to the user's usage collection
            usage_ref = user_doc_ref.collection('usage')

            # Create or update the document in the usage collection
            usage_ref.add(usage_data)

            # Update the credits field in the user's document
            user_doc_ref.update({'credits': new_credits})

            print(f"Usage data added for user {user_id}: {usage_data}")
            print(f"User {user_id} credits updated to {new_credits}")
            return True
        else:
            print(f"ERROR: User {user_id} does not have enough credits!")
            return False
    else:
        print(f"ERROR: User {user_id} does not exist!")
        return False

def get_repository_size(oauth_token, repo_name):
    headers = {'Authorization': f'token {oauth_token}'}
    url = f'https://api.github.com/repos/{repo_name}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repo_data = response.json()
        return {"Name": repo_data['full_name'], "Size": repo_data['size']}
    else:
        return f"Failed to fetch repository: {response.status_code}"



"""
# Example usage
user_id = 'qKtISirBQbftY20mLxK0hWXsD053'
repo_name = "jerrydav1s:HoldingPage"
report_id = "D1L8Wt"
update_usage(user_id, repo_name, report_id )

#"""