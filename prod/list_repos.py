import requests

def list_repositories(oauth_token):
    headers = {'Authorization': f'token {oauth_token}'}
    url = 'https://api.github.com/user/repos'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos_data = response.json()
        
        return [{"Name": repo['full_name'], "URL": repo['clone_url'], "Size": repo['size']} for repo in repos_data]
    else:
        return f"Failed to fetch repositories: {response.status_code}"


"""
# Example usage
oauth_token = "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"
repositories = list_repositories(oauth_token)
print(repositories)
#"""