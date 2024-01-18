import base64
import requests
import json
import payloadExample
import callLLMModel

GITHUB_API_URL = "https://api.github.com"
ACCESS_TOKEN = "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"
OWNER = "kethuchandra"
REPO = "Github_plugin_test"
PULL_NUMBER = 8 # Replace with the actual pull request number

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
        response.raise_for_status()
        pull_request = response.json()
        return pull_request["mergeable"]
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving pull request details: {e}")

    return False


def review_pull_request():
    # Step 1: List pull request files with commit id
    files,files_content,commit_id_list = list_pull_request_files()
    print(files_content)
    # testing_with_issue_comments()
    i = 0
    for file in files:
        filename = file["filename"]
        file_code = file["patch"]
        print(file_code)
        # review_comment = review_llm(str(file_code))
        review_comment = "Review Comments:1. Line 2: Import Statements No issues with import statements. 2. Lines 3-12: CodeDialog Class Lines 5-8:The comment // test the codeDialog box is unclear and doesn't provide meaningful information. Consider providing a more descriptive comment. Lines 9-11: The added for loop is missing braces {}. Consider adding braces for better code structure and readability. Overall Feedback:Consider providing clearer comments, especially for the purpose of the comment at Line 5. Add braces {} to the newly added for loop for better code structure. The feedback aims to improve code clarity and maintainability."
        # print(review_comment)
        lineCommentDict,fileFeedback = extract_comments(review_comment)
        adding_comments_to_github(lineCommentDict,filename,commit_id_list[i])
        i = i+1
    # addingReviewForEntirePullRequest("Adding Review For Entire PullRequest")

import re
def extract_comments(input_string):
    total_reponse = input_string.split("Review Comments:")
    fetching_review = total_reponse[1]
    print(fetching_review)
    overallFeedback = fetching_review.split("Overall Feedback:")
    fileFeedback = overallFeedback[-1]
    fetching_review_lines = overallFeedback[0]
    feedback_list = re.split(r'(\d+\.)',fetching_review_lines)
    p =[]
    for i in feedback_list:
        if("Line" in i):
            p.append(i)
    result_dict = {}
    for item in p:
        match = re.match(r'\s*(.*?):\s*(.*)', item)
        if match:
            key, value = match.groups()
            result_dict[key.strip()] = value.strip()
    return result_dict,fileFeedback

def adding_comments_to_github(review_comment,filename,commitId):
    print(review_comment)
    url_comments = f'{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PULL_NUMBER}/comments'
    headers = {
            'Authorization': f'token {ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
            }

    data = { "body": review_comment, "path": filename, "commit_id": commitId,"position": 2}
    response = requests.post(url_comments, headers=headers, json=data)
    statusCode = response.status_code
    responseBody = response.text
    print("Response Status Code: " + str(statusCode))
    print("Response Body: " + responseBody)
    if response.ok:
        print("Comment added successfully")
    else:
        print("Failed to add comment")

def testing_with_issue_comments():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{7}/comments" 
    # issues/{issue_number}/comments
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}
    data = {"body": "Your Message to Comment"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code)
    if response.ok:
        print("Comment added successfully")
    else:
        print("Failed to add comment")

def addingReviewForEntirePullRequest(review_comment):
    url_comments = f'{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PULL_NUMBER}/reviews'
    headers = {
            'Authorization': f'token {ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
            }

    data = { "body": review_comment}
    response = requests.post(url_comments, headers=headers, json=data)
    statusCode = response.status_code
    responseBody = response.text
    print("Response Status Code: " + str(statusCode))
    print("Response Body: " + responseBody)
    if response.ok:
        print("Review added successfully")
    else:
        print("Failed to add Revuew")
    
def review_llm(file_code):
    review_comment = callLLMModel.functional_method(file_code)
    return review_comment

def list_pull_request_files():
    commits = list_pull_request_commits()
    files = []
    files_content = []
    commit_id_list = []
    for commit in commits:
        commit_id = commit["sha"]
        # print(commit_id)
        commit_files,content_files = list_commit_files(commit_id)
        files.extend(commit_files)
        files_content.extend(content_files)
        commit_id_list.append(commit_id)
        # print(files_content)
    return files,files_content,commit_id_list
    
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
    content_files = []
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/commits/{commit_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        commit = response.json()
        # print(response)
        # print(commit)
        listed_files = commit.get("files", [])
        # print(listed_files)
        for listed in listed_files:
            # print(listed)
            a = listed["contents_url"]
            response = requests.get(a)
            data = response.json()
            content = data['content']
            decoded_content = base64.b64decode(content).decode('utf-8')
            content_files.append(decoded_content)
            # print(content_files)
        return commit.get("files", []),content_files
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving commit files: {e}")
    return []


def add_review_comment(filename, additions, deletions):
    # Implement logic to add review comments
    pass

# def fetchDiffPatchesFromPullRequest(commit_id,files):
#     x = []
#     for file in files:
#         filename = file["filename"]
#         url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls/{PULL_NUMBER}/commits/{commit_id}/files/{filename}" 
#         headers = {
#             "Authorization": "Bearer " + ACCESS_TOKEN,
#             "Accept": "application/vnd.github.v3+json"
#         }

#         try:
#             response = requests.get(url, headers=headers)
#             responseBody = response.text
#             print(responseBody)
#             print(response)
#             if response.ok:
#                 response_json = json.loads(responseBody)
#                 contents_url = response_json[0]['contents_url']
#                 response = response_json.get(contents_url)
#                 content = response.json()['content']
#                 decoded_content = base64.b64decode(content).decode('utf-8')
#                 x.append(decoded_content)
#                 print(decoded_content)
#                 return decoded_content
#             else:
#                 print("Failed to fetch pull request files")
            
#         except requests.exceptions.RequestException as e:
#             print(e)
#     return x

if __name__ == "__main__":
    main()



