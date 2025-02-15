import requests
import logging

# ANSI escape codes for colors
GREEN = '\033[92m'  # Green
RED = '\033[91m'    # Red
RESET = '\033[0m'   # Reset to default color

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_emails(emails, api_token):
    disposable_emails = []
    non_disposable_emails = []
    
    # API endpoint URL
    url = 'https://api.api-aries.com/v1/checkers/proxy/email/'
    
    # Headers required for the API request
    headers = {
        'APITOKEN': api_token 
    }
    
    for email in emails:
        params = {'email': email}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Check for HTTP errors
            
            result_json = response.json()
            disposable = result_json.get('disposable')
            
            if disposable is not None:
                if disposable == 'yes':
                    disposable_emails.append(email)
                else:
                    non_disposable_emails.append(email)
            else:
                logging.warning(f"The disposable status of email '{email}' is unknown.")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred for email {email}: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error occurred for email {email}: {req_err}")
        except Exception as e:
            logging.error(f"Error processing email {email}: {e}")
    
    return disposable_emails, non_disposable_emails

def read_emails_from_file(filename):
    try:
        with open(filename, 'r') as file:
            emails = file.read().splitlines()
        return emails
    except FileNotFoundError as fnf_error:
        logging.error(f"File not found: {fnf_error}")
    except Exception as e:
        logging.error(f"Error reading file: {e}")
    return []

# Example filename containing emails
filename = 'emails.txt'

api_token = 'API-TOKEN' # Replace this with your API token - https://panel.api-aries.com

email_list = read_emails_from_file(filename)

if email_list:
    disposable_emails, non_disposable_emails = check_emails(email_list, api_token)

    print("Disposable emails:")
    for email in disposable_emails:
        print(f"{GREEN}{email}{RESET}")

    print("\nNon-disposable emails:")
    for email in non_disposable_emails:
        print(f"{RED}{email}{RESET}")
else:
    print("No emails to process.")
