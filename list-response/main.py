import requests
from colorama import Fore, Style

def check_emails(emails, api_token):
    disposable_emails = []
    non_disposable_emails = []
    
    url = 'https://api.api-aries.online/v1/checkers/proxy/email/'
    headers = {
        'Type': '1',  # learn more: https://support.api-aries.online/hc/articles/1/3/3/email-checker
        'APITOKEN': api_token  
    }
    
    checked_count = 0  # Initialize checked count
    
    for idx, email in enumerate(emails, start=1):
        params = {'email': email}
        response = requests.get(url, headers=headers, params=params)
        
        try:
            result_json = response.json()
            disposable = result_json.get('disposable')
            if disposable is not None:
                checked_count += 1 
                if disposable == 'yes':
                    disposable_emails.append(email)
                else:
                    non_disposable_emails.append(email)
            else:
                print(f"The disposable status of email '{email}' is unknown.")
        except Exception as e:
            print(f"Error processing email {email}: {e}.")
        
        print(f"Checked {idx}/{len(emails)} emails.", end='\r')
    
    print() 
    return checked_count, disposable_emails, non_disposable_emails

def write_emails_to_file(emails, filename):
    with open(filename, 'w') as file:
        for email in emails:
            file.write(email + '\n')

def read_emails_from_file(filename):
    with open(filename, 'r') as file:
        emails = file.read().splitlines()
    return emails

# Example filename containing emails
input_filename = 'emails.txt'

api_token = 'API-TOKEN'  # Replace this with your API token 

# learn more: https://support.api-aries.online/hc/articles/1/3/3/email-checker

email_list = read_emails_from_file(input_filename)

checked_count, disposable_emails, non_disposable_emails = check_emails(email_list, api_token)

disposable_filename = 'disposable_emails.txt'
write_emails_to_file(disposable_emails, disposable_filename)
print(f"{Fore.RED}Disposable{Style.RESET_ALL} emails written to '{disposable_filename}'.")

non_disposable_filename = 'non_disposable_emails.txt'
write_emails_to_file(non_disposable_emails, non_disposable_filename)
print(f"{Fore.GREEN}Non-disposable{Style.RESET_ALL} emails written to '{non_disposable_filename}'.")

print(f"Total emails checked: {checked_count}")
