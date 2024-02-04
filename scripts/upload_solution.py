import os
from src.codeforces.api import get_accepted_submissions as cf_get_accepted_submissions, submit_solution as cf_submit_solution
# from leetcode.api import get_accepted_submissions as lc_get_accepted_submissions, submit_solution as lc_submit_solution
# from atcoder.api import get_accepted_submissions as ac_get_accepted_submissions, submit_solution as ac_submit_solution

def upload_codeforces_solutions(handle, password, github_token):
    submissions = cf_get_accepted_submissions(handle, password)

    for submission in submissions:
        problem_name = submission['problem']['name']

        # Print the entire submission for debugging
        print(f"Submission for problem {problem_name}: {submission}")

        # Try to get 'sourceCode' or 'source', if not found, print the submission for further inspection
        solution_code = submission.get('sourceCode') or submission.get('source')

        if not solution_code:
            print(f"Error: Could not find source code for problem {problem_name}")
            print(f"Full submission details: {submission}")
            continue  # Skip to the next submission if source code is not found

        upload_to_github(problem_name, solution_code, github_token)





# def upload_leetcode_solutions(username, password, github_token):
#     submissions = lc_get_accepted_submissions(username, password)

#     for submission in submissions:
#         problem_name = submission['problem']['title']
#         solution_code = submission['code']

#         # Modify this line to match the actual function in your GitHub API module
#         upload_to_github(problem_name, solution_code, github_token)

# def upload_atcoder_solutions(username, password, github_token):
#     submissions = ac_get_accepted_submissions(username, password)

#     for submission in submissions:
#         problem_name = submission['problem']['name']
#         solution_code = submission['source_code']

#         # Modify this line to match the actual function in your GitHub API module
#         upload_to_github(problem_name, solution_code, github_token)

def upload_to_github(problem_name, solution_code, github_token):
    # GitHub repository information
    owner = 'YashNuhash'
    repo = 'Codes-PlayGround-GitHub-Web-Development-Bootcamp'
    branch = 'main'  # or your desired branch

    # File details
    file_path = f'{problem_name}.cpp'  # adjust the file path and extension as needed

    # GitHub API endpoint for creating or updating a file
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'

    # Prepare the request headers
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Check if the file already exists in the repository
    existing_file_response = requests.get(api_url, headers=headers)
    existing_file_data = existing_file_response.json()

    if 'sha' in existing_file_data:
        # File exists, update the content
        content = solution_code.encode('base64').decode('utf-8')
        payload = {
            'message': f'Update {problem_name} solution',
            'content': content,
            'sha': existing_file_data['sha'],
            'branch': branch
        }
        response = requests.put(api_url, headers=headers, json=payload)
    else:
        # File doesn't exist, create a new one
        content = solution_code.encode('base64').decode('utf-8')
        payload = {
            'message': f'Added {problem_name} solution',
            'content': content,
            'branch': branch
        }
        response = requests.put(api_url, headers=headers, json=payload)

    # Check the response status
    if response.status_code == 200:
        print(f'Successfully uploaded {problem_name} solution to GitHub.')
    else:
        print(f'Failed to upload {problem_name} solution to GitHub. Status code: {response.status_code}, Message: {response.text}')



def main():
    cf_handle = os.environ.get('CF_HANDLE')
    cf_password = os.environ.get('CF_PASSWORD')
    # lc_username = os.environ.get('LC_USERNAME')
    # lc_password = os.environ.get('LC_PASSWORD')
    # ac_username = os.environ.get('AC_USERNAME')
    # ac_password = os.environ.get('AC_PASSWORD')
    gh_token = os.environ.get('GH_TOKEN')

    upload_codeforces_solutions(cf_handle, cf_password, gh_token)
    # upload_leetcode_solutions(lc_username, lc_password, gh_token)
    # upload_atcoder_solutions(ac_username, ac_password, gh_token)

if __name__ == "__main__":
    main()
