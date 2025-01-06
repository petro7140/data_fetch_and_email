import json

def print_service_account_email():
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
        print(f"Service Account Email: {creds['client_email']}")

if __name__ == "__main__":
    print_service_account_email()