import requests
from src.config import CF_API_KEY, CF_API_SECRET

def get_accepted_submissions(handle, password):
    # Codeforces API endpoint for fetching user submissions
    api_url = f'https://codeforces.com/api/user.status?handle={handle}&from=1&count=10'

    # Use requests library to make the API request
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract and return accepted submissions
        submissions = [submission for submission in response.json()['result'] if submission['verdict'] == 'OK']
        return submissions
    else:
        # Handle API request failure
        print(f'Error fetching submissions. Status code: {response.status_code}')
        return []

def submit_solution(handle, password, problem_id, code):
    # Codeforces API endpoint for submitting a solution
    api_url = 'https://codeforces.com/api/problem.submit'
    
    # Set up the payload with necessary data
    payload = {
        'contestId': problem_id[0],
        'index': problem_id[1],
        'verdict': 'OK',  # Assuming successful submission for simplicity
        'programmingLanguage': 'cpp17',  # Replace with the actual programming language
        'source': code
    }

    # Set up the headers with authentication information
    headers = {
        'apiKey': CF_API_KEY,
        'secret': CF_API_SECRET
    }

    # Use requests library to make the API request
    response = requests.post(api_url, data=payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract and return submission result
        return response.json()['result']
    else:
        # Handle API request failure
        print(f'Error submitting solution. Status code: {response.status_code}')
        return {'verdict': 'FAILED'}  # Placeholder for failure

# Add other Codeforces-related functions as needed
