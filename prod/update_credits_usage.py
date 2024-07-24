import json
import os
from shared_resources import db
from datetime import datetime

# Function to update the usage collection
def update_usage(user_id, repo_name, report_id, credits_used):
    # Check if the user_id exists
    user_doc_ref = db.collection('users').document(user_id)
    user_doc = user_doc_ref.get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        current_credits = user_data.get('credits', 0)

        if current_credits >= credits_used:
            new_credits = current_credits - credits_used
            usage_data = {
                'projectName': repo_name,
                'reportID': report_id,
                'date': datetime.utcnow(),
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

"""
# Example usage
user_id = 'qKtISirBQbftY20mLxK0hWXsD053'
credits_used = 10
repo_name = "blah"
report_id = "blah"
update_usage(user_id, repo_name, report_id, credits_used)
"""