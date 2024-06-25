# This file needs to be located in prod folder for simplicity
# TODO - move to proper hierachy

from celery_app import generate_report


repo_url = "https://github.com/jerrydav1s/theswimcoach.ch.git"
repo_name = "jerrydav1s:theswimcoach.ch"
report_id = "Test_2"
user_id = "qKtISirBQbftY20mLxK0hWXsD053"
oauth_token = "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"


generate_report(repo_url,repo_name,report_id,user_id,oauth_token)