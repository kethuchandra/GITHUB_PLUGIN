import requests
import json
import payload
import callLLMModel

GITHUB_API_URL = "https://api.github.com"
ACCESS_TOKEN = "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"
OWNER = "kethuchandra"
REPO = "GitHub-PlugIn"
PULL_NUMBER = 5  # Replace with the actual pull request number

# OWNER = payload.user_name
# REPO = payload.repo_name

def main():
    mergeable = check_pull_request_mergeability()
    if mergeable:
        review_pull_request()

def check_pull_request_mergeability():
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PULL_NUMBER}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers)
        # response.raise_for_status()
        pull_request = response.json()
        return pull_request["mergeable"]
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving pull request details: {e}")

    return False

# def llm_connection(filecode):
#     # file_code,filename,commit_id = review_pull_request()
#     return filecode

def review_pull_request():
    # Step 1: List pull request files with commit id
    files,commit_id = list_pull_request_files()
    print(files)
    #Review each file individually
    for file in files:
        filename = file["filename"]
        print(commit_id)
        print(filename)
        file_code = file["patch"]
        review_comment = adding_comments_to_git(file_code)
        print(review_comment)

        url_comments = f'{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PULL_NUMBER}/comments'
        headers = {
                'Authorization': f'token {ACCESS_TOKEN}',
                'Accept': 'application/vnd.github.v3+json'
                }
    
        data = { "body": review_comment, "path": filename, "commit_id": commit_id, "position": 3 }
        response = requests.post(url_comments, headers=headers, json=data)
        statusCode = response.status_code
        responseBody = response.text
        print("Response Status Code: " + str(statusCode))
        print("Response Body: " + responseBody)
        if response.ok:
            print("Comment added successfully")
        else:
            print("Failed to add comment")
        
        # Add logic to review the file, examine changes, lines, or sections
        # Step 3: Add review comments
        # add_review_comment(filename, additions, deletions)

def adding_comments_to_git(file_code):
    review_comment = callLLMModel.functional_method(file_code)
    return review_comment

def list_pull_request_files():
    commits = list_pull_request_commits()
    files = []
    COMMIT_ID = []
    for commit in commits:
        commit_id = commit["sha"]
        # print(commit_id)
        commit_files = list_commit_files(commit_id)
        files.extend(commit_files)
    return files,commit_id

def list_pull_request_commits():
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PULL_NUMBER}/commits"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers)
        # response.raise_for_status()
        print("I retrieved pull request commit")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving pull request commits: {e}")

    return []

def list_commit_files(commit_id):
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/commits/{commit_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        commit = response.json()
        return commit.get("files", [])
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving commit files: {e}")
    return []


def add_review_comment(filename, additions, deletions):
    # Implement logic to add review comments
    pass

if __name__ == "__main__":
    main()
