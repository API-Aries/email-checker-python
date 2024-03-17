import requests

# ANSI escape codes for colors
GREEN = '\033[92m'  # Green
RED = '\033[91m'    # Red
RESET = '\033[0m'   # Reset to default color

def check_emails(emails, api_token):
    disposable_emails = []
    non_disposable_emails = []
    
    # API endpoint URL
    url = 'https://api.api-aries.online/v1/checkers/proxy/email/'
    
    # Headers required for the API request
    headers = {
        'Type': '1',  # learn more: https://support.api-aries.online/hc/articles/1/3/3/email-checker
        'APITOKEN': api_token 
    }
    
    for email in emails:
        params = {'email': email}

        response = requests.get(url, headers=headers, params=params)
        
        try:
            result_json = response.json()
            disposable = result_json.get('disposable')
            
            if disposable is not None:
                if disposable == 'yes':
                    disposable_emails.append(email)
                else:
                    non_disposable_emails.append(email)
            else:
                print(f"The disposable status of email '{email}' is unknown.")
        except Exception as e:
            print(f"Error processing email {email}: {e}.")
    
    return disposable_emails, non_disposable_emails

def read_emails_from_file(filename):
    with open(filename, 'r') as file:
        emails = file.read().splitlines()
    return emails

# Example filename containing emails
filename = 'emails.txt'

api_token = 'API-TOKEN' # Replace this with your API token  # learn more: https://support.api-aries.online/hc/articles/1/3/3/email-checker

email_list = read_emails_from_file(filename)

disposable_emails, non_disposable_emails = check_emails(email_list, api_token)

print("Disposable emails:")
for email in disposable_emails:
    print(f"{GREEN}{email}{RESET}")

print("\nNon-disposable emails:")
for email in non_disposable_emails:
    print(f"{RED}{email}{RESET}")
